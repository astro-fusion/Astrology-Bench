"""ADR-002: redacted view, solver kinds, input modes, sampling, leaderboard grouping."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from astro_bench.canon import Canon
from astro_bench.cli import main
from astro_bench.leaderboard import render
from astro_bench.redact import to_solver_item
from astro_bench.runner import call_solver, check_result, run
from astro_bench.sampling import ids_sha256, stratified_sample
from astro_bench.schema import Item, SolverItem
from astro_bench.solvers import default_kind, get_solver
from tests.helpers import peek_at_gold

FIXTURE = str(Path(__file__).parent / "fixtures" / "canon")
HIDDEN = {"gold", "canon_ids", "rule_id", "generator", "source", "split", "grader"}


def test_solver_item_has_no_gold_fields(small_items: list[Item]) -> None:
    assert not HIDDEN & set(SolverItem.model_fields)
    assert set(SolverItem.model_fields) == {"id", "level", "task", "tier", "convention",
                                            "input", "prompt", "answer_type", "choices"}
    view = to_solver_item(small_items[0])
    with pytest.raises(AttributeError):
        getattr(view, "gold")  # noqa: B009
    assert "gold" not in view.model_dump()


def test_runner_passes_redacted_view(small_items: list[Item], canon: Canon) -> None:
    seen: list[object] = []

    def probe(item: SolverItem) -> str:
        seen.append(item)
        return json.dumps({"answer": None})

    run(probe, small_items[:5], canon, solver_name="probe", kind="model")
    assert seen and all(type(x) is SolverItem for x in seen)
    cheat = run(peek_at_gold, small_items[:5], canon, solver_name="peek", kind="model")
    assert all(r.parse_error and "AttributeError" in (r.error or "") for r in cheat.per_item)


def test_only_the_runner_built_oracle_sees_full_items(small_items: list[Item],
                                                      canon: Canon) -> None:
    oracle = get_solver("oracle", small_items, canon)
    assert getattr(oracle, "full_item", False)
    item = next(i for i in small_items if i.level == 1)
    assert json.loads(call_solver(oracle, item, "chart"))["answer"] == item.gold.answer
    wrapped = get_solver("nochart:oracle", small_items, canon)
    assert not call_solver(wrapped, item, "chart").startswith("{")


def test_birth_mode(small_items: list[Item]) -> None:
    l1 = next(i for i in small_items if i.level == 1)
    view = to_solver_item(l1, "birth")
    assert view.input.chart is None and view.input.birth is not None
    assert view.input_mode == "birth" and l1.convention.words() in view.prompt
    assert to_solver_item(l1, "chart").input.chart is not None
    l0 = next(i for i in small_items if i.level == 0)
    assert to_solver_item(l0, "chart").input.chart is None  # Level 0 is always birth


def test_birth_mode_recorded_and_oracle_unaffected(small_items: list[Item],
                                                   canon: Canon) -> None:
    l1 = [i for i in small_items if i.level == 1][:20]
    result = run(get_solver("oracle", l1, canon), l1, canon, solver_name="oracle",
                 input_mode="birth")
    assert result.input_mode == "birth" and result.run_id == "baseline-oracle-birth"
    assert result.summary.overall.answer_acc == 1.0


def test_kinds_and_descriptions(small_items: list[Item], canon: Canon) -> None:
    assert default_kind("oracle") == "oracle"
    assert default_kind("mock") == default_kind("nochart:random") == "baseline"
    assert default_kind("http_json:x.yaml") is None
    with pytest.raises(ValueError):
        run(lambda i: "", small_items[:2], canon, solver_name="pkg:fn")
    res = run(lambda i: "", small_items[:2], canon, solver_name="pkg:fn", kind="system")
    assert check_result(res)  # no description
    res = res.model_copy(update={"solver_description": "model X + retrieval"})
    assert check_result(res) == []
    nochart = run(get_solver("nochart:constant", small_items, canon), small_items[:3], canon,
                  solver_name="nochart:constant")
    assert nochart.ablation == "nochart" and nochart.kind == "baseline"


def test_cli_kind_rules(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    items = tmp_path / "items"
    assert main(["generate", "--level", "1", "--task", "dignity", "--n-per-task", "4",
                 "--n-per-cell", "0", "--out", str(items), "--canon", FIXTURE]) == 0
    base = ["run", "--items", str(items), "--out", str(tmp_path / "res"), "--canon", FIXTURE]
    assert main([*base, "--solver", "tests.helpers:always_true"]) == 2  # kind required
    assert main([*base, "--solver", "tests.helpers:always_true", "--kind", "app_tools"]) == 2
    assert main([*base, "--solver", "tests.helpers:always_true", "--kind", "app_tools",
                 "--description", "app 1.2 with chart tool", "--run-id", "app"]) == 0
    assert main(["score", str(tmp_path / "res" / "app.json")]) == 0
    # a system result without a description is rejected by score
    path = tmp_path / "res" / "app.json"
    data = json.loads(path.read_text())
    data["solver_description"] = ""
    path.write_text(json.dumps(data))
    assert main(["score", str(path)]) == 1
    assert "REJECTED" in capsys.readouterr().out


def test_cli_sample(tmp_path: Path) -> None:
    items = tmp_path / "items"
    assert main(["generate", "--level", "1", "--task", "dignity,varga", "--n-per-task", "6",
                 "--n-per-cell", "1", "--out", str(items), "--canon", FIXTURE]) == 0
    args = ["run", "--solver", "mock", "--items", str(items), "--canon", FIXTURE,
            "--sample", "5", "--sample-seed", "3"]
    assert main([*args, "--out", str(tmp_path / "a")]) == 0
    assert main([*args, "--out", str(tmp_path / "b")]) == 0
    a = json.loads((tmp_path / "a" / "baseline-mock.json").read_text())
    b = json.loads((tmp_path / "b" / "baseline-mock.json").read_text())
    assert a["sample_n"] == 5 and a["sample_seed"] == 3
    assert a["sample_ids_sha256"] == b["sample_ids_sha256"]
    assert [r["id"] for r in a["per_item"]] == [r["id"] for r in b["per_item"]]


def test_stratified_sample(small_items: list[Item]) -> None:
    l1 = [i for i in small_items if i.level == 1]
    first = stratified_sample(l1, 18, ["task", "level"], seed=1)
    assert len(first) == 18 and first == stratified_sample(l1, 18, ["task", "level"], seed=1)
    assert len({i.task for i in first}) == len({i.task for i in l1})  # every stratum present
    assert ids_sha256(first) != ids_sha256(stratified_sample(l1, 18, ["task"], seed=2))
    assert stratified_sample(l1, 10_000, ["task"], seed=1) == sorted(l1, key=lambda i: i.id)
    with pytest.raises(ValueError):
        stratified_sample(l1, 3, ["colour"], seed=1)


def test_leaderboard_groups_and_ablations(small_items: list[Item], canon: Canon) -> None:
    items = small_items[:12]
    results = [
        run(get_solver("mock", items, canon), items, canon, solver_name="mock"),
        run(get_solver("nochart:mock", items, canon), items, canon, solver_name="nochart:mock"),
        run(lambda i: "{}", items, canon, solver_name="sys", kind="system",
            description="tool-using agent"),
        run(get_solver("random", items, canon), items, canon, solver_name="m", kind="model"),
        run(get_solver("oracle", items, canon), items, canon, solver_name="oracle"),
    ]
    text = render(results)
    order = [text.index(h) for h in ("## Baselines", "## Models", "## Systems",
                                     "## Ablations (not ranked)")]
    assert order == sorted(order)
    assert text.index("| oracle |") < text.index("| mock |")
    assert "| - | nochart:mock | ablation: nochart |" in text
    assert "| 1 | m | model |" in text and "| 1 | sys | system |" in text


def test_redacted_view_leaks_no_answer_keys(small_items: list[Item]) -> None:
    for item in small_items:
        view = to_solver_item(item)
        assert set(view.input.query) <= {"planet", "varga", "house", "level", "target_utc"}
        text = view.model_dump_json()
        for cid in item.canon_ids:
            assert cid not in text, item.id  # not in the id, the query or the prompt
        if item.rule_id:
            assert item.rule_id not in text
