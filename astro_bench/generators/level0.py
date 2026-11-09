"""Level 0 ``positions``: compute sidereal positions from birth data alone.

Gold per planet: sign, degree in sign (2 dp), nakshatra and pada; plus the Lagna sign.
Generated items take their gold from the engine; the fixed ``golden`` items take it
from the vendored PyJHora golden charts (``vendor/golden``), so the ceiling is
traceable to an independent implementation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vedic_astrology_core.astrology.ayanamsa import get_zodiac_sign
from vedic_astrology_core.astrology.chart import BirthChart, get_nakshatra
from vedic_astrology_core.rules.vocabulary import LAGNA, NAKSHATRA_NAMES, PLANET_NAMES

from ..schema import Birth, Convention, Item
from .common import (
    DEFAULT_CONVENTION,
    GenContext,
    birth_model,
    build_chart,
    chart_of,
    conventions,
    lon_digits,
    make_item,
    near_edge,
    parse_utc,
    planet_record,
    repo_root,
    rng_for,
    sample_birth,
)

TASK = "positions"
TIER = "HARD"
GENERATOR = "positions_from_engine"
TOLERANCE_DEG = 1.0

FORMAT = (
    'Give "answer" as an object keyed by Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, '
    'Rahu, Ketu and Lagna. Each planet maps to {"sign": "<sign>", "deg_in_sign": <0-30, '
    '2 decimals>, "nakshatra": "<nakshatra>", "pada": <1-4>}; Lagna maps to {"sign": '
    '"<sign>"}. Ketu is exactly opposite Rahu.'
)


def _point(longitude: float, digits: int = 2) -> dict[str, Any]:
    _idx, sign, deg = get_zodiac_sign(longitude)
    nak = get_nakshatra(longitude)
    return {"sign": sign, "deg_in_sign": round(deg, digits), "nakshatra": nak["name"],
            "pada": int(nak["pada"])}


def positions_answer(chart: BirthChart) -> dict[str, Any]:
    """Engine gold: every graha's sign, degree, nakshatra, pada; the Lagna sign."""
    answer = {
        name: _point(float(planet_record(chart, name)["longitude"]),
                     lon_digits(name, chart.node_type))
        for name in PLANET_NAMES
    }
    answer[LAGNA] = {"sign": chart.ascendant["sign_name"]}
    return answer


def prompt_for(conv: Convention) -> str:
    return (
        "From the birth data above alone, compute the sidereal position of each graha and "
        f"the Lagna using {conv.words()}. {FORMAT} No citation is required for this task; "
        "set citations to [] unless you want to name the source of your method."
    )


def solve(item: Item) -> dict[str, Any]:
    return positions_answer(chart_of(item))


def generate(ctx: GenContext, n_default: int, n_other: int) -> list[Item]:
    items: list[Item] = []
    for conv in conventions():
        n = n_default if conv == DEFAULT_CONVENTION else n_other
        for index in range(n):
            for attempt in range(200):
                rng = rng_for(ctx.seed, TASK, conv, index, salt=str(attempt) if attempt else "")
                moment, place = sample_birth(rng, ctx.places)
                chart = build_chart(moment, place.lat, place.lon, conv)
                if not near_edge(chart, conv):
                    break
                ctx.reject(TASK, "near an edge")
            else:
                raise RuntimeError(f"{TASK}: no sample away from edges")
            items.append(make_item(
                ctx=ctx, level=0, task=TASK, tier=TIER, conv=conv, index=index,
                generator=GENERATOR, prompt=prompt_for(conv), answer_type="positions",
                answer=positions_answer(chart), grader="positions",
                birth=birth_model(moment, place), tolerance_deg=TOLERANCE_DEG,
            ))
    return items


# --------------------------------------------------------------------------- golden


def golden_path() -> Path:
    return repo_root() / "vendor" / "golden" / "golden_charts.subset.json"


def golden_answer(chart: dict[str, Any]) -> dict[str, Any]:
    """Gold copied from the PyJHora fixture (mean node, Lahiri)."""
    answer: dict[str, Any] = {}
    for name in PLANET_NAMES:
        key = name.upper()
        body_key = f"{key}_MEAN" if key in ("RAHU", "KETU") else key
        lon = float(chart["bodies"][body_key]["longitude"])
        _idx, sign, deg = get_zodiac_sign(lon)
        nak = chart["nakshatra_pada"][key]
        answer[name] = {"sign": sign, "deg_in_sign": round(deg, 2),
                        "nakshatra": NAKSHATRA_NAMES[int(nak["nakshatra"])],
                        "pada": int(nak["pada"])}
    answer[LAGNA] = {"sign": get_zodiac_sign(float(chart["ascendant"]))[1]}
    return answer


def generate_golden(ctx: GenContext, path: Path | None = None) -> list[Item]:
    src = path or golden_path()
    if not src.exists():
        ctx.log(f"golden charts not found at {src}; skipping golden Level 0 items")
        return []
    data = json.loads(src.read_text(encoding="utf-8"))
    conv = DEFAULT_CONVENTION
    items = []
    for index, chart in enumerate(data["charts"]):
        moment = parse_utc(chart["utc"])
        birth = Birth(utc=moment.strftime("%Y-%m-%dT%H:%M:%S") + "Z", lat=chart["latitude"],
                      lon=chart["longitude"], place=chart.get("place"), tz=chart.get("timezone"))
        items.append(make_item(
            ctx=ctx, level=0, task=TASK, tier=TIER, conv=conv, index=index,
            generator="positions_from_golden_charts", prompt=prompt_for(conv),
            answer_type="positions", answer=golden_answer(chart), grader="positions",
            birth=birth, tolerance_deg=TOLERANCE_DEG, query={"golden_id": chart["id"]},
            item_id_override=f"L0-positions-golden-{chart['id']}",
        ))
    return items
