"""Permanent guard: nothing a solver can see reveals the gold (CORRECTIONS 2026-11-09).

For every committed item, rendered through the redacted ``SolverItem`` view in both
input modes:

* no gold canon id appears anywhere a solver can see (id, query, prompt, input);
* for citation items, no gold ``chapter.verse`` locus (entry or ``also_in``) appears;
* the gold answer of a bool or category item does not appear, whole-word, in the item
  id, and the visible query holds only task parameters the prompt states anyway
  (planet, varga, house, level, target_utc). The prompt, choices, chart table and those
  parameters legitimately name options (the lord of the 9th can sit in the 9th), so
  they are not checked for the answer string.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

from astro_bench.canon import Canon
from astro_bench.io import dump_item, item_files, load_items
from astro_bench.redact import VISIBLE_QUERY_KEYS, to_solver_item

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items"

pytestmark = pytest.mark.skipif(not item_files(ITEMS), reason="no committed items")


def _whole(needle: str, hay: str) -> bool:
    return re.search(rf"(?<![\w.]){re.escape(needle)}(?!\w)", hay, re.IGNORECASE) is not None


def _answer_strings(answer: Any) -> list[str]:
    if isinstance(answer, bool):
        return [str(answer).lower()]
    if isinstance(answer, (str, int)):
        return [str(answer)]
    if isinstance(answer, dict):
        return [str(v) for v in answer.values() if isinstance(v, str)]
    return []


def test_whole_word_matcher() -> None:
    assert _whole("Venus", "id L1-x-Venus-000001")
    assert not _whole("7", "L1-lordship-lahiri-mean-ws-000007")
    assert _whole("36.3-4", "see 36.3-4 here") and not _whole("6.3", "36.3")


def find_leaks(items_dir: Path, canon: Canon) -> list[str]:
    """Every way the items under ``items_dir`` expose their gold to a solver."""
    leaks: list[str] = []
    for item in load_items(items_dir):
        for mode in ("chart", "birth"):
            view = to_solver_item(item, mode)  # type: ignore[arg-type]
            visible = view.model_dump_json()
            loci: list[tuple[str, str | None]] = []
            for cid in item.canon_ids:
                if cid in visible:
                    leaks.append(f"{item.id}: canon id {cid}")
                entry = canon.entry(cid)
                if entry is not None:
                    loci.append((entry.chapter, entry.verse))
                    loci += [(a.chapter, a.verse) for a in entry.also_in]
            if item.answer_type == "citation":
                gold = item.gold.answer or {}
                loci.append((str(gold.get("chapter")), gold.get("verse")))
                for chapter, verse in loci:
                    if verse and _whole(f"{chapter}.{verse}", visible):
                        leaks.append(f"{item.id}: locus {chapter}.{verse}")
            if set(view.input.query) - VISIBLE_QUERY_KEYS:
                leaks.append(f"{item.id}: hidden query keys {set(view.input.query)}")
            if item.answer_type in ("bool", "category"):
                # the node-model segment ("-true-") is the convention, not the answer
                id_text = view.id.replace(f"-{item.convention.node}-", "-")
                for text in _answer_strings(item.gold.answer):
                    if _whole(text, id_text):
                        leaks.append(f"{item.id}: gold answer {text!r} in the id")
    return sorted(set(leaks))


def test_no_committed_item_leaks_its_gold() -> None:
    assert find_leaks(ITEMS, Canon.load_or_empty(ROOT / "canon")) == []


def test_guard_catches_the_2026_11_09_leak(tmp_path: Path) -> None:
    """An item whose id embeds its canon id (the old Level 2 scheme) is caught."""
    canon = Canon.load_or_empty(ROOT / "canon")
    item = next((i for i in load_items(ITEMS) if i.level == 2), None)
    if item is None:
        pytest.skip("no Level 2 items")
    leaky = item.model_copy(update={"id": f"L2-citation-{item.canon_ids[0]}"})
    (tmp_path / "level2").mkdir()
    (tmp_path / "level2" / "citation.jsonl").write_text(dump_item(leaky) + "\n")
    assert any("canon id" in leak for leak in find_leaks(tmp_path, canon))


def test_committed_packs_leak_no_gold() -> None:
    """Every committed prompt pack and chunk under runs/ hides the gold of its items."""
    canon = Canon.load_or_empty(ROOT / "canon")
    by_id = {i.id: i for i in load_items(ITEMS)}
    packs = sorted((ROOT / "runs").rglob("pack-*.md"))
    leaks = []
    for pack in packs:
        text = pack.read_text(encoding="utf-8")
        if '"gold"' in text:
            leaks.append(f"{pack.name}: gold key")
        for item_id in re.findall(r"`(L\d-[A-Za-z0-9_.\-]+)`", text):
            item = by_id.get(item_id)
            if item is None:
                continue
            secrets = [*item.canon_ids, item.generator.name] + ([item.rule_id] if item.rule_id
                                                                 else [])
            leaks += [f"{pack.name}: {item_id} {s}" for s in secrets if s in text]
            for cid in item.canon_ids:
                entry = canon.entry(cid)
                if item.answer_type == "citation" and entry and entry.verse and \
                        _whole(f"{entry.chapter}.{entry.verse}", text):
                    leaks.append(f"{pack.name}: {item_id} locus")
    assert leaks == []
