"""Gradual, resumable runs for free-tier harnesses: chunked packs, multi-file ingest, status.

One run is one harness + one model + one effort setting. A chunked pack splits the
sample into self-contained files of ``chunk`` items; the operator pastes them one at a
time, saves each reply, and re-ingests the same run id as files arrive. Merged replies
are kept beside the result (``<out>/<run_id>.replies.jsonl``) so re-ingesting with more
files updates the run in place.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import BENCH_VERSION, ENGINE_COMMIT
from .io import items_sha256
from .manual import REPLY_FORMAT, Manifest, PackError, _sha, parse_replies
from .parse import ParseError, parse_response
from .prompts import render_user_message, system_prompt
from .redact import to_solver_item
from .sampling import ids_sha256
from .schema import InputMode, Item

#: The fill-in disclosure header at the top of every chunk (and of every reply file).
HEADER_FIELDS = [
    ("harness", "harness"),
    ("model", "model (exactly as the UI shows)"),
    ("model_id", "provider model id (if known)"),
    ("effort", 'effort or thinking setting (or "not shown")'),
    ("tools_allowed", "tools allowed (yes/no)"),
    ("operator", "operator"),
    ("date", "date"),
]
HEADER_BLOCK = "\n".join(f"{label}:" for _, label in HEADER_FIELDS)


def chunk_name(n_items: int, k: int) -> str:
    return f"pack-{n_items}-chunk-{k:02d}.md"


def render_chunk(views: Sequence[Any], k: int, n_chunks: int, first: int, total: int,
                 input_mode: str) -> str:
    lines = [
        f"# Astro-Bench prompt pack, chunk {k:02d} of {n_chunks:02d} "
        f"(items {first}-{first + len(views) - 1} of {total}, input mode {input_mode})",
        "",
        "## Disclosure header",
        "",
        "Fill this in once per run and copy it, filled, to the top of every reply file. One "
        "run is one harness, one model and one effort setting.",
        "",
        "```",
        HEADER_BLOCK,
        "```",
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
    for n, view in enumerate(views, first):
        lines += ["", f"## Item {n} of {total}: `{view.id}`", "", render_user_message(view)]
    return "\n".join(lines) + "\n"


def write_chunked_pack(items: Sequence[Item], out_dir: Path, *, chunk: int,
                       input_mode: InputMode, sample_seed: int | None,
                       stratify: Sequence[str] | None) -> Path:
    """Write ``pack-<N>-chunk-XX.md`` files and ``pack-<N>.manifest.json``."""
    items = sorted(items, key=lambda i: i.id)
    total = len(items)
    groups = [items[i:i + chunk] for i in range(0, total, chunk)]
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[dict[str, Any]] = []
    for k, group in enumerate(groups, 1):
        views = [to_solver_item(i, input_mode) for i in group]
        name = chunk_name(total, k)
        text = render_chunk(views, k, len(groups), (k - 1) * chunk + 1, total, input_mode)
        (out_dir / name).write_text(text, encoding="utf-8")
        chunks.append({"file": name, "sha256": _sha(text.encode("utf-8")),
                       "ids": [i.id for i in group]})
    combined = _sha("".join(c["sha256"] + "\n" for c in chunks).encode())
    manifest = {
        "bench_version": BENCH_VERSION, "engine_commit": ENGINE_COMMIT, "pack": None,
        "pack_sha256": combined, "format": "md-chunks", "chunk_size": chunk,
        "input_mode": input_mode, "ids": [i.id for i in items],
        "ids_sha256": ids_sha256(items), "items_sha256": items_sha256(items),
        "sample_seed": sample_seed, "sample_n": total,
        "stratify": list(stratify) if stratify else None, "chunks": chunks,
    }
    path = out_dir / f"pack-{total}.manifest.json"
    path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return path


def check_chunks(manifest: Manifest) -> None:
    """Refuse when a chunk file next to the manifest was edited after it was written."""
    for chunk in manifest.data.get("chunks") or []:
        path = manifest.path.with_name(chunk["file"])
        if path.exists() and _sha(path.read_bytes()) != chunk["sha256"]:
            raise PackError(f"{chunk['file']} was altered after it was written")


# --------------------------------------------------------------------------- headers


def read_header(text: str) -> dict[str, str]:
    """The filled disclosure header before the first ``### <id>`` line (may be partial)."""
    head = re.split(r"^\s{0,3}###\s", text, maxsplit=1, flags=re.MULTILINE)[0]
    found: dict[str, str] = {}
    for key, label in HEADER_FIELDS:
        match = re.search(rf"^\s*{re.escape(label)}\s*:[ \t]*(.*?)\s*$", head,
                          re.MULTILINE | re.IGNORECASE)
        if match and match.group(1).strip():
            found[key] = match.group(1).strip()
    return found


def header_card(header: dict[str, str], brief_path: str) -> dict[str, Any]:
    """A disclosure card from a filled header; refuses when a field is missing."""
    missing = [label for key, label in HEADER_FIELDS
               if key not in header and key != "model_id"]
    if missing:
        raise PackError("the disclosure header is incomplete: " + ", ".join(missing))
    tools = header["tools_allowed"].strip().lower()
    if tools not in ("yes", "no"):
        raise PackError("'tools allowed' must be yes or no")
    return {
        "harness": header["harness"], "model_name": header["model"],
        "model_id": header.get("model_id") or "unknown", "effort": header["effort"],
        "tools_allowed": tools == "yes", "tools_used": "unknown" if tools == "yes" else [],
        "operator": header["operator"], "date": header["date"], "brief_path": brief_path,
        "deviations": [], "notes": "Disclosure taken from the filled header of the reply files.",
    }


# --------------------------------------------------------------------------- merging


def _key(raw: str) -> str:
    """Comparable form of a reply: the parsed answer and citations, else the stripped text."""
    try:
        out = parse_response(raw)
    except ParseError:
        return " ".join(raw.split())
    cites = [c.model_dump(exclude_none=True) for c in out.citations]
    return json.dumps({"answer": out.answer, "citations": cites}, sort_keys=True)


@dataclass
class Merged:
    replies: dict[str, str] = field(default_factory=dict)
    sources: dict[str, str] = field(default_factory=dict)
    conflicts: list[str] = field(default_factory=list)


def merge(existing: dict[str, tuple[str, str]], files: Sequence[tuple[str, str]]) -> Merged:
    """Merge replies from (source name, text) files into ``existing`` {id: (raw, source)}.

    The same id twice is fine when the answers agree; differing answers are conflicts.
    """
    merged = Merged()
    for item_id, (raw, src) in existing.items():
        merged.replies[item_id], merged.sources[item_id] = raw, src
    for source, text in files:
        for item_id, raw in parse_replies(text).items():
            if item_id in merged.replies:
                if _key(merged.replies[item_id]) != _key(raw):
                    merged.conflicts.append(
                        f"{item_id}: {merged.sources[item_id]} and {source} give different answers")
                continue
            merged.replies[item_id], merged.sources[item_id] = raw, source
    return merged


def sidecar_path(out_dir: str | Path, run_id: str) -> Path:
    return Path(out_dir) / f"{run_id}.replies.jsonl"


def load_sidecar(path: Path) -> dict[str, tuple[str, str]]:
    if not path.exists():
        return {}
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    return {r["id"]: (r["response"], r.get("source", "")) for r in rows}


def write_sidecar(path: Path, merged: Merged, order: Sequence[str]) -> None:
    rows = [{"id": i, "response": merged.replies[i], "source": merged.sources[i]}
            for i in order if i in merged.replies]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                    encoding="utf-8")


def missing_by_chunk(manifest: dict[str, Any], missing: Sequence[str]
                     ) -> list[tuple[str, list[str]]]:
    """(chunk file, missing ids in it) for every chunk with something missing."""
    gone = set(missing)
    out = []
    for chunk in manifest.get("chunks") or [{"file": manifest.get("pack") or "pack",
                                             "ids": manifest["ids"]}]:
        ids = [i for i in chunk["ids"] if i in gone]
        if ids:
            out.append((chunk["file"], ids))
    return out


def parse_ids(spec: str) -> list[str]:
    """Ids from a comma list or a file (one per line, or comma separated; # comments)."""
    path = Path(spec)
    text = path.read_text(encoding="utf-8") if path.is_file() else spec
    lines = [ln.split("#", 1)[0] for ln in text.splitlines()]
    return [x.strip() for ln in lines for x in ln.split(",") if x.strip()]


def write_ids_chunk(manifest: Manifest, items: Sequence[Item], ids: Sequence[str],
                    out: Path) -> Path:
    """One chunk with only ``ids`` from the manifest's item set and input mode.

    The chunk has the same redaction and fill-in header as the pack's own chunks; its
    replies are ingested under the original manifest. A small ``<stem>.manifest.json``
    records the parent manifest's sha256 and the chunk's own sha256.
    """
    chosen = {i.id: i for i in manifest.check(items)}
    unknown = [i for i in ids if i not in chosen]
    if unknown:
        raise PackError(f"{len(unknown)} ids are not in {manifest.path.name}, e.g. {unknown[0]}")
    wanted = set(ids)
    ordered = [i for i in manifest.ids if i in wanted]
    mode = manifest.data["input_mode"]
    views = [to_solver_item(chosen[i], mode) for i in ordered]
    text = render_chunk(views, 1, 1, 1, len(views), mode)
    text = text.replace("# Astro-Bench prompt pack, chunk 01 of 01",
                        f"# Astro-Bench prompt pack {manifest.path.name}, selected items", 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    meta = {"parent_manifest": manifest.path.name,
            "parent_manifest_sha256": _sha(manifest.path.read_bytes()),
            "input_mode": mode, "ids": ordered, "sha256": _sha(text.encode("utf-8"))}
    side = out.with_name(out.stem + ".manifest.json")
    side.write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    return side
