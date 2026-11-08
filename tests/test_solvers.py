from __future__ import annotations

import json

from astro_bench.canon import Canon
from astro_bench.parse import parse_response
from astro_bench.runner import run
from astro_bench.schema import Item
from astro_bench.solvers import NoChartSolver, get_solver
from astro_bench.solvers.oracle import OracleSolver


def _acc(name: str, items: list[Item], canon: Canon) -> float:
    return run(get_solver(name, items, canon), items, canon, solver_name=name)\
        .summary.overall.answer_acc


def test_oracle_is_perfect_on_levels_0_1_2(small_items: list[Item], canon: Canon) -> None:
    result = run(OracleSolver(canon), small_items, canon, solver_name="oracle")
    bad = [r.id for r in result.per_item if r.answer_score != 1.0]
    assert bad == []
    assert result.summary.overall.citation_mean == 1.0
    assert result.summary.overall.parse_error_rate == 0.0


def test_baselines_below_oracle(small_items: list[Item], canon: Canon) -> None:
    for name in ("random", "constant", "mock"):
        assert _acc(name, small_items, canon) < 0.75


def test_baselines_are_deterministic(small_items: list[Item], canon: Canon) -> None:
    for name in ("random", "mock"):
        solver = get_solver(name, small_items, canon)
        assert [solver(i) for i in small_items[:30]] == [solver(i) for i in small_items[:30]]


def test_mock_reproduces_v1_likert_formats(small_items: list[Item]) -> None:
    item = small_items[0].model_copy(update={"answer_type": "likert", "id": "BPHS-01"})
    seed = sum(map(ord, "BPHS-01"))
    reply = get_solver("mock", [item], Canon.empty())(item)
    score = seed % 5 + 1
    formats = [f"{score}", f"{score}/5", f"Score: {score}",
               f"I would rate this a {score} based on the planetary configuration provided.",
               f"{score} out of 5"]  # v1 harness.ts mockAgentCall
    assert reply == formats[seed % 5]
    assert parse_response(reply, "likert").answer == score


def test_nochart_strips_inputs(small_items: list[Item], canon: Canon) -> None:
    seen: list[Item] = []

    def spy(item: Item) -> str:
        seen.append(item)
        return json.dumps({"answer": None})

    item = next(i for i in small_items if i.level == 1)
    NoChartSolver(spy, "spy")(item)
    assert seen[0].input.chart is None and seen[0].input.birth is None
    assert item.input.chart is not None  # original untouched
    l1 = [i for i in small_items if i.level == 1]
    result = run(get_solver("nochart:oracle", l1, canon), l1, canon, solver_name="nochart:oracle")
    assert result.summary.overall.parse_error_rate == 1.0


def test_module_callable_solver(small_items: list[Item], canon: Canon) -> None:
    solver = get_solver("tests.helpers:always_true", small_items, canon)
    assert json.loads(solver(small_items[0]))["answer"] is True
