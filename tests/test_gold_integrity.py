"""Gold integrity (CORRECTIONS 2026-11-09): Swiss files, edge margins, chart-mode gold."""

from __future__ import annotations

from pathlib import Path

import pytest

from astro_bench.ephemeris import EPHE_SET_SHA256, EphemerisError, configure, verify
from astro_bench.generators import ENGINE_TASKS
from astro_bench.generators.common import (
    BODY_MARGIN,
    NO_SPEED_SIGN,
    TRUE_NODE_MARGIN,
    chart_of,
    edge_distance,
    planet_record,
)
from astro_bench.generators.level1_rules import default_rules_dir, fires_on_table, load_registry
from astro_bench.io import item_files, load_items
from astro_bench.schema import Item

ITEMS = Path(__file__).resolve().parents[1] / "items"
committed = pytest.mark.skipif(not item_files(ITEMS), reason="no committed items")


def test_engine_uses_swiss_files() -> None:
    assert configure() == "swieph"


def test_missing_files_fail_loudly(tmp_path: Path) -> None:
    with pytest.raises(EphemerisError, match="fetch_ephe"):
        verify(tmp_path)
    (tmp_path / "sepl_18.se1").write_bytes(b"not the file")
    with pytest.raises(EphemerisError):
        verify(tmp_path)


def test_edge_distance() -> None:
    assert edge_distance(210.0023) == pytest.approx(0.0023)
    assert edge_distance(206.6708) == pytest.approx(0.0041, abs=1e-4)
    assert edge_distance(5.0) == pytest.approx(5.0 - 10 / 3)


def test_generated_items_record_the_ephemeris(small_items: list[Item]) -> None:
    for item in small_items:
        if item.generator.name != "positions_from_golden_charts":
            assert item.generator.ephemeris_model == "swieph"
            assert item.generator.ephe_sha256 == EPHE_SET_SHA256


@committed
def test_committed_items_are_swiss_and_away_from_edges() -> None:
    for item in load_items(ITEMS):
        if item.input.birth is None or item.generator.name == "positions_from_golden_charts":
            continue
        assert item.generator.ephemeris_model == "swieph", item.id
        chart = chart_of(item)
        for name in [n for n in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                                 "Saturn", "Rahu", "Ketu")]:
            margin = TRUE_NODE_MARGIN if name in NO_SPEED_SIGN and \
                item.convention.node == "true" else BODY_MARGIN
            lon = float(planet_record(chart, name)["longitude"])
            assert edge_distance(lon) >= margin, (item.id, name, lon)
        assert edge_distance(float(chart.ascendant["longitude"])) >= BODY_MARGIN, item.id


@committed
def test_chart_mode_gold_reproduces_from_the_printed_table() -> None:
    registry = load_registry(str(default_rules_dir()))
    for item in load_items(ITEMS):
        if item.level != 1 or item.input.chart is None:
            continue
        if item.task in ENGINE_TASKS:
            got = ENGINE_TASKS[item.task].solve_from_table(item)
        else:
            assert item.rule_id is not None
            got = fires_on_table(registry.get(item.rule_id), chart_of(item), item.input.chart,
                                 item.convention.node)
        assert got == item.gold.answer, item.id


def test_leaderboard_moves_older_split_rows(small_items: list[Item]) -> None:
    from astro_bench.canon import Canon
    from astro_bench.leaderboard import render
    from astro_bench.runner import run
    from astro_bench.solvers import get_solver

    canon = Canon.empty()
    items = small_items[:6]
    result = run(get_solver("mock", items, canon), items, canon, solver_name="m",
                 kind="model")
    current = {i.id: i for i in small_items}
    assert "## Older split" not in render([result], current)
    changed = dict(current)
    changed[items[0].id] = items[0].model_copy(update={"prompt": items[0].prompt + " "})
    text = render([result], changed)
    assert "## Older split (not ranked)" in text and "## Models" not in text
