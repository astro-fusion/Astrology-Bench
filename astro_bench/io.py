"""Reading and writing item JSONL, and the canonical items hash."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path

from .schema import Item

#: Directories under ``items/`` with their own (human-authored) schema, skipped here.
SKIP_DIRS = {"judgment"}


def dump_item(item: Item) -> str:
    """One canonical JSON line (sorted keys, no None fields, compact separators)."""
    data = item.model_dump(mode="json", exclude_none=True)
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def items_sha256(items: Iterable[Item]) -> str:
    """sha256 over the canonical lines of ``items`` sorted by id, each ending in newline."""
    h = hashlib.sha256()
    for item in sorted(items, key=lambda i: i.id):
        h.update((dump_item(item) + "\n").encode("utf-8"))
    return h.hexdigest()


def item_files(path: str | Path) -> list[Path]:
    root = Path(path)
    if root.is_file():
        return [root]
    return sorted(p for p in root.rglob("*.jsonl") if not SKIP_DIRS & set(p.parts))


def load_items(path: str | Path) -> list[Item]:
    """Every item in a JSONL file or under a directory (``judgment/`` skipped)."""
    items: list[Item] = []
    for file in item_files(path):
        for lineno, line in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                items.append(Item.model_validate_json(line))
            except ValueError as exc:
                raise ValueError(f"{file}:{lineno}: {exc}") from exc
    return items


def relpath_for(item: Item) -> str:
    return f"level{item.level}/{item.task}.jsonl"


def write_items(items: Sequence[Item], out_dir: str | Path) -> dict[str, int]:
    """Write ``items`` to ``<out_dir>/level<L>/<task>.jsonl`` sorted by id; return counts."""
    groups: dict[str, list[Item]] = defaultdict(list)
    for item in items:
        groups[relpath_for(item)].append(item)
    counts = {}
    for rel, group in sorted(groups.items()):
        target = Path(out_dir) / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        lines = [dump_item(i) for i in sorted(group, key=lambda i: i.id)]
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")
        counts[rel] = len(lines)
    return counts
