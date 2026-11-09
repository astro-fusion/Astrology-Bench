from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from astro_bench.cli import main

FIXTURE = str(Path(__file__).parent / "fixtures" / "canon")


def _tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*.jsonl")):
        h.update(p.relative_to(root).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def test_generate_dev_twice_is_identical(tmp_path: Path) -> None:
    args = ["generate", "--level", "0,1", "--task", "positions,lordship,yoga",
            "--n-per-task", "2", "--n-per-cell", "1", "--canon", FIXTURE]
    assert main([*args, "--out", str(tmp_path / "a")]) == 0
    assert main([*args, "--out", str(tmp_path / "b")]) == 0
    assert _tree_hash(tmp_path / "a") == _tree_hash(tmp_path / "b")
    assert main(["validate", str(tmp_path / "a"), "--canon", FIXTURE]) == 0


def test_test_split_needs_env_and_outside_out(tmp_path: Path,
                                             monkeypatch: pytest.MonkeyPatch) -> None:
    args = ["generate", "--split", "test", "--level", "0", "--n-per-task", "1",
            "--n-per-cell", "0", "--canon", FIXTURE, "--manifests", str(tmp_path / "m")]
    monkeypatch.delenv("ASTRO_BENCH_TEST_SEED", raising=False)
    assert main([*args, "--out", str(tmp_path / "t")]) == 2
    monkeypatch.setenv("ASTRO_BENCH_TEST_SEED", "4242")
    inside = Path(__file__).resolve().parents[1] / "items-test-should-not-exist"
    assert main([*args, "--out", str(inside)]) == 2
    assert not inside.exists()
    assert main([*args, "--out", str(tmp_path / "t")]) == 0
    manifest = (tmp_path / "m" / "test-0.1.0.sha256").read_text()
    assert "ALL" in manifest and "level0/positions.jsonl" in manifest


def test_run_score_leaderboard(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    items = tmp_path / "items"
    assert main(["generate", "--level", "1", "--task", "dignity", "--n-per-task", "3",
                 "--n-per-cell", "0", "--out", str(items), "--canon", FIXTURE]) == 0
    for solver in ("oracle", "constant"):
        assert main(["run", "--solver", solver, "--items", str(items), "--out",
                     str(tmp_path / "res"), "--canon", FIXTURE]) == 0
    assert main(["score", str(tmp_path / "res" / "baseline-oracle.json")]) == 0
    assert "1.000" in capsys.readouterr().out
    out = tmp_path / "LB.md"
    assert main(["leaderboard", "--results", str(tmp_path / "res"), "--out", str(out),
                 "--items", str(items)]) == 0
    text = out.read_text()
    assert text.index("| oracle |") < text.index("| constant |")
