"""Checks on the committed dev split under ``items/`` (skipped until it exists)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from astro_bench.canon import Canon
from astro_bench.cli import validate_items
from astro_bench.io import item_files, load_items
from astro_bench.runner import run
from astro_bench.solvers.oracle import OracleSolver

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items"

pytestmark = pytest.mark.skipif(not item_files(ITEMS), reason="no committed items yet")


def test_no_committed_item_is_test_split() -> None:
    for path in sorted(ITEMS.rglob("*.jsonl")):  # judgment/ included: raw JSON check
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                assert json.loads(line).get("split") != "test", path


def test_committed_items_validate() -> None:
    canon = Canon.load_or_empty(ROOT / "canon")
    assert validate_items(load_items(ITEMS), canon, in_repo=True) == []


def test_oracle_scores_one_on_committed_levels_0_and_1() -> None:
    canon = Canon.load_or_empty(ROOT / "canon")
    items = [i for i in load_items(ITEMS) if i.level in (0, 1)]
    result = run(OracleSolver(canon), items, canon, solver_name="oracle")
    assert [r.id for r in result.per_item if r.answer_score != 1.0] == []
