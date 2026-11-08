from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

from astro_bench import ENGINE_COMMIT

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "vendor" / "rules"


def test_vendored_rules_match_upstream_manifest() -> None:
    meta = yaml.safe_load((RULES / "UPSTREAM.yaml").read_text(encoding="utf-8"))
    assert meta["upstream_commit"].startswith(ENGINE_COMMIT)
    files = meta["files"]
    on_disk = sorted(p.relative_to(RULES).as_posix() for p in RULES.rglob("*")
                     if p.is_file() and p.name != "UPSTREAM.yaml")
    assert on_disk == sorted(files)
    for rel, digest in files.items():
        assert hashlib.sha256((RULES / rel).read_bytes()).hexdigest() == digest, rel


def test_golden_subset_provenance() -> None:
    data = json.loads((ROOT / "vendor" / "golden" / "golden_charts.subset.json").read_text())
    assert data["upstream_commit"].startswith(ENGINE_COMMIT)
    assert len(data["upstream_sha256"]) == 64
    assert {c["id"] for c in data["charts"]} == {"ktm_1990", "del_1947", "lon_1969",
                                                  "syd_1973", "nyc_2001"}
