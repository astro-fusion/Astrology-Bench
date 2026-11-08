from __future__ import annotations

from collections import Counter, defaultdict

from astro_bench.canon import Canon
from astro_bench.generators import generate_items
from astro_bench.generators.common import load_places
from astro_bench.generators.level1_rules import rule_key
from astro_bench.io import items_sha256
from astro_bench.schema import Item


def test_places_span() -> None:
    places = load_places()
    assert len(places) == 24
    lats = [p.lat for p in places]
    assert min(lats) < -44 and max(lats) > 59 and all(-46 <= x <= 61 for x in lats)


def test_every_level_and_task_present(small_items: list[Item]) -> None:
    tasks = {(i.level, i.task) for i in small_items}
    for task in ["nakshatra", "varga", "dasha", "dignity", "combustion", "aspect", "lordship",
                 "yoga", "rule"]:
        assert (1, task) in tasks
    assert (0, "positions") in tasks and (2, "citation") in tasks


def test_tiers(small_items: list[Item]) -> None:
    expected = {"positions": "HARD", "nakshatra": "EASY", "dignity": "EASY",
                "combustion": "EASY", "varga": "MEDIUM", "aspect": "MEDIUM",
                "lordship": "MEDIUM", "dasha": "MEDIUM", "yoga": "MEDIUM", "rule": "MEDIUM",
                "citation": "HARD"}
    for item in small_items:
        assert item.tier == expected[item.task]


def test_level_inputs(small_items: list[Item]) -> None:
    for item in small_items:
        if item.level == 0:
            assert item.input.birth is not None and item.input.chart is None
        if item.level == 1:
            assert item.input.birth is not None and item.input.chart is not None
            assert item.convention.words() in item.prompt
        if item.convention.house == "placidus":
            assert item.input.chart is not None and item.input.chart.cusps is not None


def test_convention_cells(small_items: list[Item]) -> None:
    cells = defaultdict(set)
    for item in small_items:
        cells[item.task].add(item.convention.key)
    assert len(cells["dasha"]) == 6  # 3 ayanamsas x 2 nodes, whole sign
    assert len(cells["lordship"]) == 12  # plus Placidus
    assert cells["aspect"] == cells["dasha"]
    assert cells["yoga"] == {"lahiri/mean/whole_sign", "lahiri/true/whole_sign"}
    default = Counter(i.task for i in small_items if i.convention.key == "lahiri/mean/whole_sign")
    assert default["dasha"] == 4


def test_golden_level0_items(small_items: list[Item]) -> None:
    golden = [i for i in small_items if "golden" in i.id]
    assert len(golden) == 5
    first = next(i for i in golden if i.id.endswith("ktm_1990"))
    assert first.gold.answer["Lagna"] == {"sign": "Cancer"}
    assert first.gold.answer["Sun"]["sign"] == "Taurus"


def test_yoga_items_balanced(small_items: list[Item]) -> None:
    by_rule: dict[tuple[str, str], list[bool]] = defaultdict(list)
    for item in small_items:
        if item.task in ("yoga", "rule"):
            by_rule[(item.rule_id or "", item.convention.key)].append(item.gold.answer)
    assert by_rule
    for answers in by_rule.values():
        assert abs(sum(answers) - len(answers) / 2) <= 0.5


def test_yoga_canon_ids_from_rule_key(small_items: list[Item], canon: Canon) -> None:
    assert rule_key("general.gaja_kesari.classical", canon) == "gaja_kesari"
    assert rule_key("general.budha_aditya", canon) == "budha_aditya"
    gk = [i for i in small_items if i.rule_id == "general.gaja_kesari.classical"]
    assert gk and all(i.canon_ids == ["bphs.santhanam1984.ch36.v3"] for i in gk)
    assert all(i.source == "BPHS" for i in gk)
    ba = [i for i in small_items if i.rule_id == "general.budha_aditya"]
    assert ba and all(i.canon_ids == [] and i.source == "modern" for i in ba)


def test_level2_from_fixture_canon(small_items: list[Item], canon: Canon) -> None:
    l2 = sorted((i for i in small_items if i.level == 2), key=lambda i: i.id)
    assert [i.input.query["canon_id"] for i in l2] == [e.id for e in canon.quoted()]
    gk = next(i for i in l2 if i.input.query["rule_key"] == "gaja_kesari")
    assert gk.gold.answer == {"text": "BPHS", "chapter": "36", "verse": "3-4"}
    assert gk.input.birth is None and gk.answer_type == "citation"


def test_level2_skipped_without_canon() -> None:
    items = generate_items(levels=[2], split="dev", seed=1, canon=Canon.empty())
    assert items == []


def test_engine_tasks_cite_canon_when_quoted(small_items: list[Item]) -> None:
    comb = [i for i in small_items if i.task == "combustion"]
    assert all(i.canon_ids == ["bphs.santhanam1984.ch3.v49"] for i in comb)
    assert all(i.canon_ids == [] for i in small_items if i.task == "nakshatra")


def test_generation_is_deterministic(canon: Canon) -> None:
    kwargs = dict(levels=[0, 1], split="dev", seed=11, canon=canon, n_default=2, n_other=1,
                  tasks=["positions", "dasha", "yoga"])
    first = generate_items(**kwargs)  # type: ignore[arg-type]
    second = generate_items(**kwargs)  # type: ignore[arg-type]
    assert items_sha256(first) == items_sha256(second)
    other = generate_items(**dict(kwargs, seed=12))  # type: ignore[arg-type]
    assert items_sha256(other) != items_sha256(first)


def test_test_split_has_no_public_items(canon: Canon) -> None:
    items = generate_items(levels=[0, 2], split="test", seed=99, canon=canon, n_default=1,
                           n_other=0)
    assert items and all(i.split == "test" for i in items)
    assert not any("golden" in i.id or i.level == 2 for i in items)
