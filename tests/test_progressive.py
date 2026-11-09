"""Chunked packs, multi-file resumable ingest, status and the in-progress table."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from astro_bench.canon import Canon
from astro_bench.cli import main
from astro_bench.io import load_items
from astro_bench.leaderboard import render
from astro_bench.progressive import HEADER_BLOCK, read_header
from astro_bench.runner import load_result
from astro_bench.solvers.oracle import OracleSolver

FIXTURE = str(Path(__file__).parent / "fixtures" / "canon")
HEADER = """harness: Cursor (free tier)
model (exactly as the UI shows): gpt-like-mini
provider model id (if known):
effort or thinking setting (or "not shown"): not shown
tools allowed (yes/no): no
operator: tests
date: 2026-11-09
"""


@pytest.fixture(scope="module")
def items_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("items")
    assert main(["generate", "--n-per-task", "3", "--n-per-cell", "1", "--out", str(out),
                 "--canon", FIXTURE]) == 0
    return out


def _chunk(items_dir: Path, out: Path) -> dict:
    assert main(["pack", "--items", str(items_dir), "--out", str(out), "--sample", "25",
                 "--sample-seed", "1", "--chunk", "10"]) == 0
    return json.loads((out / "pack-25.manifest.json").read_text())


def _replies(items_dir: Path, ids: list[str], canon: Canon, header: str = HEADER) -> str:
    by_id = {i.id: i for i in load_items(items_dir)}
    oracle = OracleSolver(canon)
    return header + "\n" + "\n\n".join(f"### {i}\n{oracle(by_id[i])}" for i in ids) + "\n"


def test_chunks_deterministic_and_redacted(items_dir: Path, tmp_path: Path) -> None:
    a = _chunk(items_dir, tmp_path / "a")
    b = _chunk(items_dir, tmp_path / "b")
    assert a == b and [c["file"] for c in a["chunks"]] == [
        "pack-25-chunk-01.md", "pack-25-chunk-02.md", "pack-25-chunk-03.md"]
    assert [len(c["ids"]) for c in a["chunks"]] == [10, 10, 5]
    assert sum((c["ids"] for c in a["chunks"]), []) == a["ids"]
    by_id = {i.id: i for i in load_items(items_dir)}
    for chunk in a["chunks"]:
        text = (tmp_path / "a" / chunk["file"]).read_text()
        assert text.count(HEADER_BLOCK) == 1 and "## System prompt" in text
        assert all(f"`{i}`" in text for i in chunk["ids"])
        for item_id in chunk["ids"]:
            item = by_id[item_id]
            for secret in [*item.canon_ids, item.rule_id or "\0", item.generator.name]:
                assert secret not in text
        assert '"gold"' not in text


def test_header_parsing() -> None:
    header = read_header(HEADER + "### X-1\n{}")
    assert header["harness"] == "Cursor (free tier)" and header["effort"] == "not shown"
    assert "model_id" not in header and header["tools_allowed"] == "no"
    assert read_header("### X-1\n{}") == {}


def test_multi_file_partial_then_complete(items_dir: Path, tmp_path: Path,
                                         canon: Canon, capsys: pytest.CaptureFixture[str]
                                         ) -> None:
    man = _chunk(items_dir, tmp_path / "pack")
    c1, c2, c3 = (c["ids"] for c in man["chunks"])
    files = {name: tmp_path / f"{name}.txt" for name in ("r1", "r2", "r3")}
    files["r2"].write_text(_replies(items_dir, c2, canon))  # no header needed after the first
    files["r1"].write_text(_replies(items_dir, c1 + c2[:3], canon))  # overlap, same answers
    base = ["ingest", "--pack", str(tmp_path / "pack" / "pack-25.manifest.json"),
            "--kind", "system_ui", "--description", "Cursor free tier gpt-like-mini",
            "--run-id", "cursor-mini", "--items", str(items_dir), "--canon", FIXTURE,
            "--out", str(tmp_path / "res")]
    assert main([*base, "--replies", str(files["r1"]), "--replies", str(files["r2"])]) == 0
    result = load_result(tmp_path / "res" / "cursor-mini.json")
    assert result.status == "partial" and result.answered_n == 20
    assert result.missing_ids == c3
    assert result.disclosure is not None and result.disclosure.model_name == "gpt-like-mini"
    assert result.disclosure.model_id == "unknown" and result.disclosure.tools_used == []
    capsys.readouterr()
    assert main(["status", "--run-id", "cursor-mini", "--out", str(tmp_path / "res"),
                 "--pack", str(tmp_path / "pack" / "pack-25.manifest.json")]) == 0
    out = capsys.readouterr().out
    assert "20/25 answered" in out and "pack-25-chunk-03.md: 5 missing" in out
    assert "chunk-01" not in out
    text = render([result])
    assert "## In progress (not ranked)" in text and "| 20/25 |" in text
    assert "## Systems" not in text
    # the third chunk arrives later, without a header: same run id, updated in place
    files["r3"].write_text(_replies(items_dir, c3, canon, header=""))
    assert main([*base, "--replies", str(files["r3"])]) == 0
    result = load_result(tmp_path / "res" / "cursor-mini.json")
    assert result.status == "complete" and result.missing_ids == [] and result.answered_n == 25
    assert result.summary.overall.answer_acc == 1.0
    assert result.disclosure is not None and result.disclosure.harness == "Cursor (free tier)"
    assert "## Systems" in render([result])


def test_conflicting_duplicates_are_refused(items_dir: Path, tmp_path: Path, canon: Canon,
                                           capsys: pytest.CaptureFixture[str]) -> None:
    man = _chunk(items_dir, tmp_path / "pack")
    ids = man["chunks"][0]["ids"]
    good = tmp_path / "good.txt"
    good.write_text(_replies(items_dir, ids, canon))
    bad = tmp_path / "bad.txt"
    bad.write_text(f"### {ids[0]}\n" + '{"answer": "definitely wrong", "citations": []}\n')
    args = ["ingest", "--pack", str(tmp_path / "pack" / "pack-25.manifest.json"),
            "--replies", str(good), "--replies", str(bad), "--kind", "model",
            "--description", "x", "--items", str(items_dir), "--canon", FIXTURE,
            "--out", str(tmp_path / "res")]
    assert main(args) == 2
    assert f"conflict: {ids[0]}" in capsys.readouterr().err
    assert not (tmp_path / "res").exists()


def test_incomplete_header_and_edited_chunk_are_refused(items_dir: Path, tmp_path: Path,
                                                       canon: Canon) -> None:
    man = _chunk(items_dir, tmp_path / "pack")
    ids = man["chunks"][0]["ids"]
    replies = tmp_path / "r.txt"
    replies.write_text(_replies(items_dir, ids, canon, header="harness: X\n"))
    args = ["ingest", "--pack", str(tmp_path / "pack" / "pack-25.manifest.json"),
            "--replies", str(replies), "--kind", "model", "--description", "x",
            "--items", str(items_dir), "--canon", FIXTURE, "--out", str(tmp_path / "res")]
    assert main(args) == 2  # header incomplete, no --disclosure, no previous run
    replies.write_text(_replies(items_dir, ids, canon))
    chunk = tmp_path / "pack" / "pack-25-chunk-02.md"
    chunk.write_text(chunk.read_text() + "edited\n")
    assert main(args) == 2
