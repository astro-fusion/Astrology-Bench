"""Checks on the real ``canon/`` (skipped until it exists)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest
import yaml

from astro_bench.canon import Canon
from astro_bench.graders.citation import grade_citations
from astro_bench.schema import Citation

CANON = Path(__file__).resolve().parents[1] / "canon"

pytestmark = pytest.mark.skipif(not (CANON / "REGISTRY.yaml").exists(), reason="no canon/")


@pytest.fixture(scope="module")
def real() -> Canon:
    return Canon.load(CANON)


def test_ids_unique_and_texts_registered(real: Canon) -> None:
    raw_ids = []
    for path in sorted(CANON.glob("*.yaml")):
        if path.name != "REGISTRY.yaml":
            raw_ids += [e["id"] for e in yaml.safe_load(path.read_text())["entries"]]
    assert [k for k, n in Counter(raw_ids).items() if n > 1] == []
    assert len(real) == len(raw_ids)
    for entry in real.entries.values():
        assert entry.text in real.texts, entry.id
        assert real.chapter_in_range(entry.text, entry.chapter), entry.id
        for alt in entry.also_in:
            assert alt.text in real.texts and real.chapter_in_range(alt.text, alt.chapter), entry.id


def test_quoted_entries_have_quote_and_url(real: Canon) -> None:
    quoted = real.quoted()
    assert quoted
    for entry in quoted:
        assert entry.quote and entry.quote.strip(), entry.id
        assert entry.url and entry.url.startswith("http"), entry.id


@pytest.mark.parametrize("key", ["gaja_kesari", "combustion_orbs", "graha_drishti",
                                 "vimshottari_dasha_years", "exaltation_degrees"])
def test_gold_for_core_rules(real: Canon, key: str) -> None:
    assert real.gold_for(key)


def test_secondary_rule_keys_and_untraced(real: Canon) -> None:
    assert real.gold_for("debilitation_degrees")  # only ever a second rule key
    assert any(u.get("rule_key") == "kala_sarpa" for u in real.untraced)
    assert real.gold_for("kala_sarpa") == []


def test_every_quoted_entry_cites_itself(real: Canon) -> None:
    for entry in real.quoted():
        cite = Citation(text=entry.text, chapter=entry.chapter, verse=entry.verse)
        assert grade_citations(real, [cite], [entry.id]).score == 1, entry.id
        for alt in entry.also_in:
            alt_cite = Citation(text=alt.text, chapter=alt.chapter, verse=alt.verse)
            assert grade_citations(real, [alt_cite], [entry.id]).score == 1, (entry.id, alt)
