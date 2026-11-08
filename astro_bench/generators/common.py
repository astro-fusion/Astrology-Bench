"""Shared generator plumbing: places, seeded sampling, conventions, charts, item ids.

Everything is deterministic in ``(seed, task, convention, index)``: each item gets its
own ``random.Random`` seeded with a string, which Python hashes with SHA-512, so the
stream does not depend on ``PYTHONHASHSEED`` or on the order items are generated in.
"""

from __future__ import annotations

import random
import warnings
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml
from vedic_astrology_core.astrology.ayanamsa import AyanamsaSystem
from vedic_astrology_core.astrology.chart import BirthChart
from vedic_astrology_core.rules.vocabulary import PLANET_NAMES, to_planet_enum

from .. import BENCH_VERSION, ENGINE_COMMIT
from ..canon import Canon
from ..schema import (
    Birth,
    Body,
    ChartTable,
    Convention,
    GeneratorInfo,
    Gold,
    GraderSpec,
    Item,
    ItemInput,
)

START = datetime(1900, 1, 1, tzinfo=timezone.utc)
END = datetime(2030, 12, 31, 23, 59, tzinfo=timezone.utc)
HOUSE_ABBR = {"whole_sign": "ws", "placidus": "pl"}
AYANAMSAS = ("lahiri", "raman", "krishnamurti")
NODES = ("mean", "true")
HOUSES = ("whole_sign", "placidus")
DEFAULT_CONVENTION = Convention()


def repo_root() -> Path:
    """The checkout root (parent of the ``astro_bench`` package)."""
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Place:
    name: str
    lat: float
    lon: float
    tz: str


def load_places(path: str | Path | None = None) -> list[Place]:
    """The 24 sampling places from ``scripts/places.yaml``."""
    src = Path(path) if path else repo_root() / "scripts" / "places.yaml"
    data = yaml.safe_load(src.read_text(encoding="utf-8"))
    return [Place(p["name"], float(p["lat"]), float(p["lon"]), p["tz"]) for p in data["places"]]


@dataclass
class GenContext:
    """What every task generator needs."""

    seed: int
    split: str
    places: list[Place]
    canon: Canon
    rules_dir: Path | None = None
    log: Callable[[str], None] = field(default=lambda msg: None)


def conventions(house_dependent: bool = False, whole_sign_only: bool = False) -> list[Convention]:
    """Convention cells, default cell first.

    House-independent tasks use whole-sign cells only (the house system cannot
    change their answer); house-dependent tasks add the Placidus cells.
    """
    houses = HOUSES if house_dependent and not whole_sign_only else ("whole_sign",)
    cells = [
        Convention(ayanamsa=a, node=n, house=h)  # type: ignore[arg-type]
        for h in houses
        for a in AYANAMSAS
        for n in NODES
    ]
    return sorted(cells, key=lambda c: c != DEFAULT_CONVENTION)


def rng_for(seed: int, task: str, conv: Convention, index: int, salt: str = "") -> random.Random:
    return random.Random(f"astro-bench|{seed}|{task}|{conv.key}|{index}|{salt}")


def sample_moment(rng: random.Random) -> datetime:
    """Uniform UTC minute in 1900-01-01 .. 2030-12-31."""
    minutes = int((END - START).total_seconds() // 60)
    return START + timedelta(minutes=rng.randrange(minutes + 1))


def sample_birth(rng: random.Random, places: Sequence[Place]) -> tuple[datetime, Place]:
    return sample_moment(rng), places[rng.randrange(len(places))]


def fmt_utc(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)


def birth_model(moment: datetime, place: Place) -> Birth:
    return Birth(utc=fmt_utc(moment), lat=place.lat, lon=place.lon, place=place.name, tz=place.tz)


def build_chart(moment: datetime, lat: float, lon: float, conv: Convention) -> BirthChart:
    """The engine's chart for one convention (warnings about Placidus silenced)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        chart = BirthChart(
            moment,
            lat,
            lon,
            ayanamsa_system=AyanamsaSystem(conv.ayanamsa),
            house_system=conv.house,
            node_type=conv.node,
        )
        _ = chart.planets, chart.houses
    return chart


def chart_of(item: Item) -> BirthChart:
    """Rebuild the engine chart from an item's birth data and convention."""
    birth = item.input.birth
    if birth is None:
        raise ValueError(f"{item.id}: no birth data")
    return build_chart(parse_utc(birth.utc), birth.lat, birth.lon, item.convention)


def planet_record(chart: BirthChart, name: str) -> dict[str, Any]:
    rec: dict[str, Any] = chart.planets[to_planet_enum(name)]
    return rec


def chart_table(chart: BirthChart, conv: Convention) -> ChartTable:
    """Sidereal longitudes (2 dp), speeds (3 dp) and Lagna; cusps for non-whole-sign."""
    bodies = {
        name: Body(
            lon=round(float(planet_record(chart, name)["longitude"]), 2),
            speed=round(float(planet_record(chart, name)["longitude_speed"]), 3),
        )
        for name in PLANET_NAMES
    }
    cusps = None
    if conv.house != "whole_sign":
        cusps = [round(float(h["longitude"]), 2) for h in chart.houses]
    return ChartTable(lagna=round(float(chart.ascendant["longitude"]), 2), bodies=bodies,
                      cusps=cusps)


def item_id(level: int, task: str, conv: Convention, index: int, tag: str | None = None) -> str:
    parts = [f"L{level}", task] + ([tag] if tag else [])
    parts += [conv.ayanamsa, conv.node, HOUSE_ABBR[conv.house], f"{index:06d}"]
    return "-".join(parts)


#: Canon rule keys looked up for the engine-direct tasks (first quoted match wins).
TASK_RULE_KEYS: dict[str, list[str]] = {
    "positions": [],
    "nakshatra": ["nakshatra", "nakshatra_pada"],
    "varga": ["navamsa", "varga", "divisional_charts", "dasamsa", "saptamsa"],
    "dasha": ["vimshottari", "vimshottari_dasha", "dasha"],
    "dignity": ["dignity", "exaltation", "moolatrikona", "own_sign"],
    "combustion": ["combustion", "astangata"],
    "aspect": ["graha_drishti", "aspect", "aspects"],
    "lordship": ["house_lordship", "lordship", "bhavesha_phala", "sign_lords"],
}


def task_canon(canon: Canon, task: str) -> tuple[str, list[str]]:
    """(source, canon_ids) for an engine-direct task; ``modern`` when nothing is quoted."""
    for key in TASK_RULE_KEYS.get(task, []):
        gold = canon.gold_for(key)
        if gold:
            return gold[0].text, [e.id for e in gold]
    return "modern", []


def make_item(
    *,
    ctx: GenContext,
    level: int,
    task: str,
    tier: str,
    conv: Convention,
    index: int,
    generator: str,
    prompt: str,
    answer_type: str,
    answer: Any,
    grader: str,
    birth: Birth | None = None,
    chart: ChartTable | None = None,
    query: dict[str, Any] | None = None,
    choices: list[str] | None = None,
    source: str = "modern",
    canon_ids: list[str] | None = None,
    rule_id: str | None = None,
    tag: str | None = None,
    tolerance_deg: float | None = None,
    item_id_override: str | None = None,
) -> Item:
    return Item.model_validate(
        {
            "id": item_id_override or item_id(level, task, conv, index, tag),
            "level": level,
            "task": task,
            "tier": tier,
            "source": source,
            "canon_ids": canon_ids or [],
            "rule_id": rule_id,
            "convention": conv,
            "split": ctx.split,
            "input": ItemInput(birth=birth, chart=chart, query=query or {}),
            "prompt": prompt,
            "answer_type": answer_type,
            "choices": choices,
            "gold": Gold(answer=answer),
            "grader": GraderSpec(name=grader, tolerance_deg=tolerance_deg),  # type: ignore[arg-type]
            "generator": GeneratorInfo(
                name=generator, version=BENCH_VERSION, seed=ctx.seed,
                engine_commit=ENGINE_COMMIT, index=index,
            ),
        }
    )


CITE_HINT = (
    "Answer in the JSON format given in the system prompt and cite the classical text, "
    "chapter and verse that supports your answer. If you cannot cite one, set citations "
    "to [] and say so."
)
