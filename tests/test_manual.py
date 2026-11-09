"""pack / ingest: manual and IDE-agent runs without an API key."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from astro_bench.canon import Canon
from astro_bench.cli import main
from astro_bench.io import load_items
from astro_bench.manual import parse_replies, slug
from astro_bench.solvers.oracle import OracleSolver
from tests.helpers import write_card

FIXTURE = str(Path(__file__).parent / "fixtures" / "canon")


@pytest.fixture(scope="module")
def items_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("items")
    assert main(["generate", "--n-per-task", "3", "--n-per-cell", "1", "--out", str(out),
                 "--canon", FIXTURE]) == 0
    return out


def _pack(items_dir: Path, out: Path, *extra: str) -> dict:
    assert main(["pack", "--items", str(items_dir), "--out", str(out), "--sample", "25",
                 "--sample-seed", "1", *extra]) == 0
    return json.loads(out.with_name(out.stem + ".manifest.json").read_text())


def _oracle_replies(items_dir: Path, ids: list[str], canon: Canon) -> str:
    by_id = {i.id: i for i in load_items(items_dir)}
    oracle = OracleSolver(canon)
    return "\n\n".join(f"### {i}\n{oracle(by_id[i])}" for i in ids) + "\n"


def test_pack_is_deterministic_and_redacted(items_dir: Path, tmp_path: Path) -> None:
    a = _pack(items_dir, tmp_path / "a" / "pack.md", "--input-mode", "birth")
    b = _pack(items_dir, tmp_path / "b" / "pack.md", "--input-mode", "birth")
    assert a["pack_sha256"] == b["pack_sha256"] and a["ids"] == b["ids"]
    assert a["sample_n"] == 25 and a["input_mode"] == "birth" and a["sample_seed"] == 1
    text = (tmp_path / "a" / "pack.md").read_text()
    assert "### <item_id>" in text and "## System prompt" in text
    assert all(f"`{i}`" in text for i in a["ids"])
    assert "Sidereal chart" not in text  # birth mode: no chart tables
    for item in load_items(items_dir):
        if item.id in a["ids"]:
            assert item.generator.name not in text
            for cid in item.canon_ids:
                assert cid not in text
    assert '"gold"' not in text and "rule_id" not in text


def test_pack_jsonl_format(items_dir: Path, tmp_path: Path) -> None:
    man = _pack(items_dir, tmp_path / "pack.jsonl", "--format", "jsonl")
    rows = [json.loads(x) for x in (tmp_path / "pack.jsonl").read_text().splitlines()]
    assert rows[0]["type"] == "header" and [r["id"] for r in rows[1:]] == man["ids"]
    assert all(set(r) == {"type", "n", "id", "prompt"} for r in rows[1:])


def test_ingest_oracle_round_trip(items_dir: Path, tmp_path: Path, canon: Canon) -> None:
    man = _pack(items_dir, tmp_path / "pack.md")
    replies = tmp_path / "replies.txt"
    replies.write_text("Here are my answers.\n\n" + _oracle_replies(items_dir, man["ids"], canon))
    args = ["ingest", "--pack", str(tmp_path / "pack.manifest.json"), "--replies",
            str(replies), "--kind", "system_ui", "--description",
            "Cursor agent, model X, 2026-11-09", "--items", str(items_dir), "--canon", FIXTURE,
            "--out", str(tmp_path / "res"), "--disclosure", str(write_card(tmp_path))]
    assert main(args) == 0
    [path] = list((tmp_path / "res").glob("*.json"))
    result = json.loads(path.read_text())
    assert result["summary"]["overall"]["answer_acc"] == 1.0
    assert result["solver"] == "manual:cursor-agent-model-x-2026-11-09"
    assert result["kind"] == "system_ui" and result["input_mode"] == "chart"
    assert result["sample_n"] == 25 and result["sample_seed"] == 1
    assert main(["score", str(path)]) == 0


def test_ingest_missing_and_extra_ids(items_dir: Path, tmp_path: Path, canon: Canon) -> None:
    man = _pack(items_dir, tmp_path / "pack.md")
    base = ["ingest", "--pack", str(tmp_path / "pack.manifest.json"), "--kind", "model",
            "--description", "chat UI 2026-11-09", "--items", str(items_dir),
            "--canon", FIXTURE, "--out", str(tmp_path / "res"),
            "--disclosure", str(write_card(tmp_path))]
    partial = tmp_path / "partial.txt"
    partial.write_text(_oracle_replies(items_dir, man["ids"][:20], canon))
    assert main([*base, "--replies", str(partial)]) == 0
    result = json.loads(next((tmp_path / "res").glob("*.json")).read_text())
    assert result["summary"]["overall"]["parse_error_rate"] == pytest.approx(5 / 25)
    extra = tmp_path / "extra.txt"
    extra.write_text(_oracle_replies(items_dir, man["ids"], canon)
                     + '### L9-made-up-000001\n{"answer": 1}\n')
    assert main([*base, "--replies", str(extra)]) == 2


def test_ingest_jsonl_and_tamper(items_dir: Path, tmp_path: Path, canon: Canon) -> None:
    man = _pack(items_dir, tmp_path / "pack.md", "--input-mode", "birth")
    by_id = {i.id: i for i in load_items(items_dir)}
    oracle = OracleSolver(canon)
    rows = [{"id": i, "response": json.loads(oracle(by_id[i]))} for i in man["ids"]]
    replies = tmp_path / "replies.jsonl"
    replies.write_text("".join(json.dumps(r) + "\n" for r in rows))
    base = ["ingest", "--pack", str(tmp_path / "pack.manifest.json"), "--replies",
            str(replies), "--kind", "model", "--description", "batch 2026-11-09",
            "--items", str(items_dir), "--canon", FIXTURE, "--out", str(tmp_path / "res"),
            "--disclosure", str(write_card(tmp_path))]
    assert main(base) == 0
    result = json.loads(next((tmp_path / "res").glob("*.json")).read_text())
    assert result["summary"]["overall"]["answer_acc"] == 1.0
    assert result["input_mode"] == "birth"
    pack = tmp_path / "pack.md"
    pack.write_text(pack.read_text() + "\nedited\n")
    assert main(base) == 2  # pack altered


def test_parse_replies_tolerance() -> None:
    text = ("intro\n### `A-1`\nsome prose {\"answer\": true}\n\n###  B-2 \n```json\n"
            '{"answer": "Mars"}\n```\n')
    assert parse_replies(text) == {"A-1": 'some prose {"answer": true}',
                                   "B-2": '```json\n{"answer": "Mars"}\n```'}
    assert slug("Claude Code + Opus, 2026-11-09!") == "claude-code-opus-2026-11-09"
