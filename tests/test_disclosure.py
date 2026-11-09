"""ADR-002 decision 7: disclosure blocks, cards, the runs/ index and published hashes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from astro_bench.canon import Canon
from astro_bench.cli import main
from astro_bench.disclosure import (
    complete,
    load_card,
    render_card,
    render_index,
    sha256_file,
)
from astro_bench.leaderboard import load_results, render
from astro_bench.runner import check_result, run
from astro_bench.schema import DISCLOSED_KINDS, Disclosure, Item
from astro_bench.solvers import get_solver
from tests.helpers import write_card

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = str(Path(__file__).parent / "fixtures" / "canon")


def _base(**kw: object) -> dict:
    data = {"harness": "h", "model_id": "m", "model_name": "M", "effort": "default, unknown",
            "tools_allowed": False, "tools_used": "unknown", "operator": "o",
            "date": "2026-11-09", "input_mode": "chart", "brief_path": "runs/x/brief.md"}
    data.update(kw)
    return data


def test_schema() -> None:
    assert Disclosure.model_validate(_base()).tools_used == "unknown"
    for bad in ({"effort": ""}, {"effort": "   "}, {"model_id": ""}, {"surprise": 1},
                {"tools_used": "some"}):
        with pytest.raises(ValidationError):
            Disclosure.model_validate(_base(**bad))


def test_score_requires_disclosure(small_items: list[Item], canon: Canon,
                                   tmp_path: Path) -> None:
    items = small_items[:5]
    result = run(get_solver("mock", items, canon), items, canon, solver_name="mine",
                 kind="model")
    assert any("disclosure" in p for p in check_result(result))
    result.disclosure = complete(load_card(write_card(tmp_path)), result)
    assert check_result(result) == []
    baseline = run(get_solver("mock", items, canon), items, canon, solver_name="mock")
    assert check_result(baseline) == []  # baselines need none


def test_ingest_refuses_without_disclosure(tmp_path: Path) -> None:
    items = tmp_path / "items"
    assert main(["generate", "--level", "1", "--task", "dignity", "--n-per-task", "4",
                 "--n-per-cell", "0", "--out", str(items), "--canon", FIXTURE]) == 0
    assert main(["pack", "--items", str(items), "--out", str(tmp_path / "pack.md")]) == 0
    replies = tmp_path / "replies.txt"
    replies.write_text("")
    args = ["ingest", "--pack", str(tmp_path / "pack.manifest.json"), "--replies",
            str(replies), "--kind", "model", "--description", "d", "--items", str(items),
            "--canon", FIXTURE, "--out", str(tmp_path / "res")]
    assert main(args) == 2
    assert main([*args, "--disclosure", str(write_card(tmp_path))]) == 0
    data = json.loads(next((tmp_path / "res").glob("*.json")).read_text())
    d = data["disclosure"]
    assert d["replies_sha256"] == sha256_file(replies)
    assert d["pack_sha256"] == sha256_file(tmp_path / "pack.md")
    assert d["sample"] is None or d["sample"]["n"] == 4
    assert "/Users/" not in json.dumps(d) and "/private/" not in json.dumps(d)


def test_card_and_index_rendering(small_items: list[Item], canon: Canon,
                                  tmp_path: Path) -> None:
    items = small_items[:8]
    result = run(get_solver("mock", items, canon), items, canon, solver_name="mine",
                 kind="system_ui", description="IDE agent", run_id="demo")
    card = write_card(tmp_path, deviations=["read the pack twice"], tools_allowed=True,
                      tools_used=["Bash"])
    result.disclosure = complete(load_card(card), result)
    text = render_card(result)
    for needle in ("# demo", "| Model id | `test-model` |", "| Effort | default, unknown |",
                   "| Tools allowed | yes |", "- read the pack twice", "## Results by task",
                   "(../claude-haiku-notools-sample100/brief.md)"):
        assert needle in text
    index = render_index([result])
    assert "[CARD](demo/CARD.md)" in index and "allowed: Bash" in index
    assert "(runs/demo/CARD.md)" in render([result])
    with pytest.raises(ValueError):
        render_card(result.model_copy(update={"disclosure": None}))


def test_committed_results_are_fully_disclosed() -> None:
    results = [r for r in load_results(ROOT / "results") if r.kind in DISCLOSED_KINDS]
    assert results
    for r in results:
        d = r.disclosure
        assert d is not None, r.run_id
        assert check_result(r) == [], r.run_id
        card = ROOT / "runs" / r.run_id / "CARD.md"
        assert card.read_text() == render_card(r), f"{card} is stale: run astro-bench cards"
        assert (ROOT / d.brief_path).is_file(), r.run_id
        if d.agent_report_path:
            assert (ROOT / d.agent_report_path).is_file(), r.run_id
        for path, digest in ((d.replies_path, d.replies_sha256), (d.pack_path, d.pack_sha256)):
            if path:
                assert digest == sha256_file(ROOT / path), (r.run_id, path)
        if d.pack_path:
            pack = ROOT / d.pack_path
            chunked = pack.name.endswith(".manifest.json")  # chunked: the manifest is hashed
            manifest = json.loads((pack if chunked else pack.with_suffix(".manifest.json"))
                                  .read_text())
            if not chunked:
                assert manifest["pack_sha256"] == d.pack_sha256
            assert manifest["ids_sha256"] == r.sample_ids_sha256
        assert f"`{r.run_id}`" in (ROOT / "runs" / "README.md").read_text()
