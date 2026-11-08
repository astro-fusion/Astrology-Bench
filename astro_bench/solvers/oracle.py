"""The oracle: the engine answers every item; it defines the ceiling.

Answers are recomputed from ``input.birth`` and the convention by the same engine
calls the generators use, so Level 0/1 generated items score 1.0 by construction;
the golden Level 0 items (PyJHora gold) are a genuine cross-check. Citations are the
loci of the item's gold canon entries; confidence is 1.0. Without birth data (for
example under ``nochart:``) the oracle declines with a non-JSON reply.
"""

from __future__ import annotations

from typing import Any

from ..canon import Canon
from ..generators import ENGINE_TASKS, level0, level1_rules
from ..schema import Item
from .base import respond


def gold_citations(item: Item, canon: Canon) -> list[dict[str, Any]]:
    cites = []
    for cid in item.canon_ids:
        entry = canon.entry(cid)
        if entry is not None:
            cites.append({"text": canon.resolve_text(entry.text) or entry.text,
                          "chapter": entry.chapter, "verse": entry.verse,
                          "edition": entry.edition})
    return cites


class OracleSolver:
    name = "oracle"

    def __init__(self, canon: Canon):
        self.canon = canon

    def answer(self, item: Item) -> Any:
        if item.task == "citation":
            return item.gold.answer
        if item.input.birth is None:
            raise LookupError("no birth data")
        if item.task == "positions":
            return level0.solve(item)
        if item.task in ("yoga", "rule"):
            return level1_rules.solve(item)
        if item.task in ENGINE_TASKS:
            return ENGINE_TASKS[item.task].solve(item)
        raise LookupError(f"oracle has no solver for task {item.task!r}")

    def __call__(self, item: Item) -> str:
        try:
            answer = self.answer(item)
        except LookupError as exc:
            return f"I cannot answer this item: {exc}."
        return respond(answer, gold_citations(item, self.canon), 1.0)
