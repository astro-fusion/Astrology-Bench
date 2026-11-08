#!/usr/bin/env python3
"""Snapshot the research repo's ``rules/**`` (and a few golden charts) into ``vendor/``.

Usage:
    python scripts/sync_rules.py --src "/path/to/astro-research"

Writes ``vendor/rules/**`` (an exact copy of ``<src>/rules``), ``vendor/rules/UPSTREAM.yaml``
(upstream repo, commit, sync time, per-file sha256) and
``vendor/golden/golden_charts.subset.json`` (the Level 0 fixed charts, copied verbatim
from ``tests/fixtures/golden_charts.json`` with that file's sha256 recorded).
No network access is needed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_REPO = "https://github.com/astro-fusion/astro_research-white-paper"
GOLDEN_IDS = ["ktm_1990", "del_1947", "lon_1969", "syd_1973", "nyc_2001"]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_hashes(root: Path) -> dict[str, str]:
    """sha256 of every file under ``root`` except UPSTREAM.yaml, keyed by posix relpath."""
    out: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "UPSTREAM.yaml" and "__pycache__" not in path.parts:
            out[path.relative_to(root).as_posix()] = sha256_file(path)
    return out


def sync_rules(src: Path, dest: Path, commit: str) -> int:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src / "rules", dest, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    hashes = file_hashes(dest)
    meta = {
        "upstream_repo": UPSTREAM_REPO,
        "upstream_path": "rules/",
        "upstream_commit": commit,
        "synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": hashes,
    }
    (dest / "UPSTREAM.yaml").write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    return len(hashes)


def sync_golden(src: Path, dest: Path, commit: str, ids: list[str]) -> int:
    fixture = src / "tests" / "fixtures" / "golden_charts.json"
    data = json.loads(fixture.read_text(encoding="utf-8"))
    charts = [c for c in data["charts"] if c["id"] in ids]
    subset = {
        "upstream_repo": UPSTREAM_REPO,
        "upstream_path": "tests/fixtures/golden_charts.json",
        "upstream_commit": commit,
        "upstream_sha256": sha256_file(fixture),
        "provenance": data["provenance"],
        "charts": charts,
    }
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / "golden_charts.subset.json"
    out.write_text(json.dumps(subset, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return len(charts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--src", required=True, help="local checkout of the research repo")
    parser.add_argument("--dest", default=str(ROOT / "vendor"))
    args = parser.parse_args()
    src = Path(args.src).resolve()
    commit = subprocess.run(
        ["git", "-C", str(src), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    dest = Path(args.dest)
    n_rules = sync_rules(src, dest / "rules", commit)
    n_golden = sync_golden(src, dest / "golden", commit, GOLDEN_IDS)
    print(f"synced {n_rules} rule files and {n_golden} golden charts at {commit[:7]}")


if __name__ == "__main__":
    main()
