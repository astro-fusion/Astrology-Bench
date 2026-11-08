"""Helpers importable as ``tests.helpers`` (used by the module:callable solver test)."""

from __future__ import annotations

import json

from astro_bench.schema import SolverItem


def always_true(item: SolverItem) -> str:
    return json.dumps({"answer": True, "citations": []})


def peek_at_gold(item: SolverItem) -> str:
    """A cheating solver: reads the gold if it can."""
    return json.dumps({"answer": item.gold.answer})  # type: ignore[attr-defined]
