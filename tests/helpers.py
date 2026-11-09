"""Helpers importable as ``tests.helpers`` (used by the module:callable solver test)."""

from __future__ import annotations

import json
from pathlib import Path

from astro_bench.schema import SolverItem


def always_true(item: SolverItem) -> str:
    return json.dumps({"answer": True, "citations": []})


def peek_at_gold(item: SolverItem) -> str:
    """A cheating solver: reads the gold if it can."""
    return json.dumps({"answer": item.gold.answer})  # type: ignore[attr-defined]


def write_card(directory: Path, **overrides: object) -> Path:
    """A minimal disclosure card for tests (brief: a committed runs/ file)."""
    import yaml

    card = {"harness": "test harness", "model_id": "test-model", "model_name": "Test Model",
            "effort": "default, unknown", "tools_allowed": False, "tools_used": ["Read"],
            "operator": "tests", "date": "2026-11-09",
            "brief_path": "runs/claude-haiku-notools-sample100/brief.md",
            "deviations": [], "notes": "", **overrides}
    path = directory / "card.yaml"
    path.write_text(yaml.safe_dump(card))
    return path
