from __future__ import annotations

from pathlib import Path

import pytest

from astro_bench.canon import Canon
from astro_bench.generators import generate_items
from astro_bench.schema import Item

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_CANON = ROOT / "tests" / "fixtures" / "canon"


@pytest.fixture(scope="session")
def canon() -> Canon:
    return Canon.load(FIXTURE_CANON)


@pytest.fixture(scope="session")
def small_items(canon: Canon) -> list[Item]:
    """A small dev set over every level, generated against the fixture canon."""
    return generate_items(levels=[0, 1, 2], split="dev", seed=7, canon=canon,
                          n_default=4, n_other=1)
