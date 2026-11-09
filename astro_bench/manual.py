"""Manual and IDE-agent runs with no API key: ``pack`` a prompt file, ``ingest`` replies.

A pack holds the system prompt once and, per item, only the redacted ``SolverItem`` view
(ADR-002) rendered as the user message: never gold, canon ids or rule ids. Its manifest
records the sampled ids, the sample seed, the items sha256, the input mode and the pack's
own sha256, so ``ingest`` can check that neither the items nor the pack changed.

Reply format: for each item, a line ``### <item_id>`` followed by one JSON object.
A JSONL file of ``{"id": ..., "response": ...}`` objects is accepted too.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import BENCH_VERSION, ENGINE_COMMIT
from .io import items_sha256
from .prompts import render_user_message, system_prompt
from .redact import to_solver_item
from .sampling import ids_sha256
from .schema import InputMode, Item, SolverItem

REPLY_FORMAT = (
    "Reply to every item below. For each item write a line `### <item_id>` (the id exactly "
    "as given) and, on the next lines, one JSON object in the format of the system prompt: "
    '{"answer": ..., "citations": [...], "confidence": 0.0-1.0, "note": "optional"}. '
    "Nothing else is graded. Example:\n\n### L1-dasha-lahiri-mean-ws-000000\n"
    '{"answer": "Venus", "citations": [], "confidence": 0.6}\n'
)


class PackError(ValueError):
    """The pack, manifest or replies are inconsistent."""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def render_md(views: Sequence[SolverItem], header: dict[str, Any]) -> str:
    lines = [
        "# Astro-Bench prompt pack",
        "",
        f"{len(views)} items; input mode {header['input_mode']}; bench {BENCH_VERSION}; "
        f"items sha256 `{header['items_sha256'][:12]}`.",
        "",
        "## How to reply",
        "",
        REPLY_FORMAT,
        "## System prompt",
        "",
        system_prompt().strip(),
        "",
        "## Items",
    ]
    for n, view in enumerate(views, 1):
        lines += ["", f"## Item {n} of {len(views)}: `{view.id}`", "",
                  render_user_message(view)]
    return "\n".join(lines) + "\n"


def render_jsonl(views: Sequence[SolverItem], header: dict[str, Any]) -> str:
    rows = [{"type": "header", "system": system_prompt(), "reply_format": REPLY_FORMAT,
             "input_mode": header["input_mode"], "items_sha256": header["items_sha256"]}]
    rows += [{"type": "item", "n": n, "id": v.id, "prompt": render_user_message(v)}
             for n, v in enumerate(views, 1)]
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


def manifest_path(pack: Path) -> Path:
    return pack.with_name(pack.stem + ".manifest.json")


def write_pack(items: Sequence[Item], out: Path, *, input_mode: InputMode, fmt: str,
               sample_seed: int | None, stratify: Sequence[str] | None) -> Path:
    """Write the pack and ``<pack stem>.manifest.json``; return the manifest path."""
    items = sorted(items, key=lambda i: i.id)
    header = {"input_mode": input_mode, "items_sha256": items_sha256(items)}
    views = [to_solver_item(i, input_mode) for i in items]
    text = render_md(views, header) if fmt == "md" else render_jsonl(views, header)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    manifest = {
        "bench_version": BENCH_VERSION,
        "engine_commit": ENGINE_COMMIT,
        "pack": out.name,
        "pack_sha256": _sha(out.read_bytes()),
        "format": fmt,
        "input_mode": input_mode,
        "ids": [i.id for i in items],
        "ids_sha256": ids_sha256(items),
        "items_sha256": header["items_sha256"],
        "sample_seed": sample_seed,
        "sample_n": len(items),
        "stratify": list(stratify) if stratify else None,
    }
    path = manifest_path(out)
    path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------- ingest

_HEADER = re.compile(r"^\s{0,3}###\s+`?([A-Za-z0-9_.:\-]+)`?\s*$", re.MULTILINE)


def parse_replies(text: str) -> dict[str, str]:
    """Map item id -> raw reply text, from ``### <id>`` blocks or JSONL ``{id, response}``."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    jsonl = _jsonl(lines)
    if jsonl is not None:
        return jsonl
    out: dict[str, str] = {}
    matches = list(_HEADER.finditer(text))
    for k, match in enumerate(matches):
        end = matches[k + 1].start() if k + 1 < len(matches) else len(text)
        item_id = match.group(1)
        if item_id in out:
            raise PackError(f"reply for {item_id} given twice")
        out[item_id] = text[match.end():end].strip()
    return out


def _jsonl(lines: list[str]) -> dict[str, str] | None:
    if not lines:
        return None
    out: dict[str, str] = {}
    for line in lines:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return None
        if not isinstance(row, dict) or "id" not in row or "response" not in row:
            return None
        resp = row["response"]
        out[str(row["id"])] = resp if isinstance(resp, str) else json.dumps(resp)
    return out


@dataclass(frozen=True)
class Manifest:
    data: dict[str, Any]
    path: Path

    @classmethod
    def load(cls, path: str | Path) -> Manifest:
        p = Path(path)
        return cls(json.loads(p.read_text(encoding="utf-8")), p)

    @property
    def ids(self) -> list[str]:
        return list(self.data["ids"])

    def check(self, items: Sequence[Item]) -> list[Item]:
        """The manifest's items, after checking ids, items sha256 and the pack file."""
        by_id = {i.id: i for i in items}
        missing = [i for i in self.ids if i not in by_id]
        if missing:
            raise PackError(f"{len(missing)} manifest ids are not in the items, e.g. {missing[0]}")
        chosen = [by_id[i] for i in self.ids]
        if items_sha256(chosen) != self.data["items_sha256"]:
            raise PackError("items changed since the pack was written (items sha256 differs)")
        pack = self.path.with_name(self.data["pack"])
        if pack.exists() and _sha(pack.read_bytes()) != self.data["pack_sha256"]:
            raise PackError(f"{pack.name} was altered after it was written")
        return chosen


class ReplaySolver:
    """Returns the ingested reply for each id; a missing id raises (a parse error)."""

    def __init__(self, replies: dict[str, str]):
        self.replies = replies

    def __call__(self, item: SolverItem) -> str:
        if item.id not in self.replies:
            raise LookupError(f"no reply for {item.id}")
        return self.replies[item.id]


def slug(text: str, limit: int = 48) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return out[:limit].strip("-") or "manual"
