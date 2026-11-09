"""Level 1 engine-direct tasks: nakshatra, varga, dasha, dignity, combustion.

Every gold value is one call into ``vedic_astrology_core``; nothing here computes
astrology itself. Dignity uses the engine's own classifiers: ``get_dignity_type``
for moolatrikona / exalted / debilitated / own sign (its precedence), and the rule
vocabulary's ``dignities_of`` for the natural friend / enemy / neutral relation to
the sign lord when none of those applies.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any

from vedic_astrology_core.astrology.chart import BirthChart, get_nakshatra
from vedic_astrology_core.astrology.divisional import varga_sign
from vedic_astrology_core.dasha.vimshottari import (
    compute_vimshottari_nested_periods,
    get_vimshottari_chain_at,
    get_vimshottari_lord_at,
)
from vedic_astrology_core.dignity.exaltation_matrix import get_dignity_type
from vedic_astrology_core.rules.predicates.placement import dignities_of
from vedic_astrology_core.rules.vocabulary import (
    NAKSHATRA_NAMES,
    PLANET_NAMES,
    SIGN_NAMES,
    to_planet_enum,
)

from ..schema import Convention
from .common import fmt_utc, parse_utc, planet_record
from .engine_task import EngineTask

SEVEN = PLANET_NAMES[:7]


def _lon(chart: BirthChart, planet: str) -> float:
    return float(planet_record(chart, planet)["longitude"])


# --------------------------------------------------------------------------- nakshatra


def _nak_query(rng: random.Random, chart: BirthChart, moment: datetime) -> dict[str, Any]:
    return {"planet": "Moon"}


def _nak_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> dict[str, Any]:
    nak = get_nakshatra(_lon(chart, q["planet"]))
    return {"nakshatra": nak["name"], "pada": int(nak["pada"])}


def _nak_prompt(conv: Convention, q: dict[str, Any]) -> str:
    return (
        f"Using the sidereal chart above ({conv.words()}), in which nakshatra and pada is "
        f'the {q["planet"]}? Give "answer" as {{"nakshatra": "<name>", "pada": <1-4>}}.'
    )


NAKSHATRA = EngineTask(
    name="nakshatra", tier="EASY", answer_type="category", grader="exact",
    query=_nak_query, answer=_nak_answer, prompt=_nak_prompt, choices=list(NAKSHATRA_NAMES),
)

# --------------------------------------------------------------------------- varga

VARGAS = {9: "D9 Navamsa", 10: "D10 Dasamsa", 7: "D7 Saptamsa"}


def _varga_query(rng: random.Random, chart: BirthChart, moment: datetime) -> dict[str, Any]:
    return {"planet": rng.choice(PLANET_NAMES), "varga": rng.choice(sorted(VARGAS))}


def _varga_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> str:
    return SIGN_NAMES[varga_sign(_lon(chart, q["planet"]), int(q["varga"]))]


def _varga_prompt(conv: Convention, q: dict[str, Any]) -> str:
    return (
        f"Using the sidereal chart above ({conv.words()}) and the Parashari (BPHS) varga "
        f"rules, which sign does {q['planet']} occupy in the {VARGAS[int(q['varga'])]} chart? "
        'Give "answer" as the sign name.'
    )


VARGA = EngineTask(
    name="varga", tier="MEDIUM", answer_type="category", grader="exact",
    query=_varga_query, answer=_varga_answer, prompt=_varga_prompt, choices=list(SIGN_NAMES),
)

# --------------------------------------------------------------------------- dasha

DASHA_YEAR_DAYS = 365.25
BOUNDARY_MARGIN = timedelta(days=4)


def _dasha_query(rng: random.Random, chart: BirthChart, moment: datetime) -> dict[str, Any] | None:
    level = "antardasha" if rng.random() < 0.5 else "mahadasha"
    target = moment + timedelta(days=rng.uniform(0, 80 * DASHA_YEAR_DAYS))
    target = target.replace(second=0, microsecond=0)
    periods = compute_vimshottari_nested_periods(moment, _lon(chart, "Moon"), depth=2)
    edges = [p["start"] for p in periods] + [p["end"] for p in periods]
    if min(abs(target - edge) for edge in edges) < BOUNDARY_MARGIN:
        return None  # too close to a period boundary to be fair at 2 dp of the Moon
    return {"level": level, "target_utc": fmt_utc(target)}


def _dasha_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> str:
    target = parse_utc(q["target_utc"])
    moon = _lon(chart, "Moon")
    if q["level"] == "mahadasha":
        return str(get_vimshottari_lord_at(target, moment, moon))
    periods = compute_vimshottari_nested_periods(moment, moon, depth=2)
    return str(get_vimshottari_chain_at(target, periods)[1])


def _dasha_prompt(conv: Convention, q: dict[str, Any]) -> str:
    return (
        f"Using the sidereal chart above ({conv.words()}) and Vimshottari dasha from the "
        f"Moon's nakshatra at birth (dasha year = 365.25 days), which planet's "
        f"{q['level']} is running at {q['target_utc']}? Give \"answer\" as the planet name."
    )


DASHA = EngineTask(
    name="dasha", tier="MEDIUM", answer_type="category", grader="exact",
    query=_dasha_query, answer=_dasha_answer, prompt=_dasha_prompt, choices=list(PLANET_NAMES),
)

# --------------------------------------------------------------------------- dignity

DIGNITY_LABELS = ["moolatrikona", "exalted", "debilitated", "own", "friend", "enemy", "neutral"]
_ENGINE_TYPE = {"Moolatrikona": "moolatrikona", "Exalted": "exalted",
                "Debilitated": "debilitated", "Own Sign": "own"}


def dignity_label(planet: str, longitude: float) -> str:
    """One label: the engine's get_dignity_type, else its natural relation to the sign lord."""
    enum = to_planet_enum(planet)
    kind = get_dignity_type(longitude, enum)
    if kind in _ENGINE_TYPE:
        return _ENGINE_TYPE[kind]
    relation = dignities_of(enum, longitude, "taurus") & {"friend", "enemy", "neutral"}
    return sorted(relation)[0] if relation else "neutral"


def _dignity_query(rng: random.Random, chart: BirthChart, moment: datetime) -> dict[str, Any]:
    return {"planet": rng.choice(SEVEN)}


def _dignity_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> str:
    return dignity_label(q["planet"], _lon(chart, q["planet"]))


def _dignity_prompt(conv: Convention, q: dict[str, Any]) -> str:
    return (
        f"Using the sidereal chart above ({conv.words()}), what is the dignity of "
        f"{q['planet']}? Choose one of: moolatrikona, exalted, debilitated, own, friend, "
        "enemy, neutral. Exaltation and debilitation are by whole sign and moolatrikona by "
        "the BPHS degree ranges; when several apply, report the first in the order "
        "moolatrikona, exalted, debilitated, own. Otherwise report the natural (naisargika) "
        "relation of the planet to the lord of the sign it occupies."
    )


DIGNITY = EngineTask(
    name="dignity", tier="EASY", answer_type="category", grader="exact",
    query=_dignity_query, answer=_dignity_answer, prompt=_dignity_prompt,
    choices=list(DIGNITY_LABELS),
)

# --------------------------------------------------------------------------- combustion

COMBUSTIBLE = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def _comb_query(rng: random.Random, chart: BirthChart, moment: datetime) -> dict[str, Any]:
    return {}


def _comb_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> list[str]:
    return sorted(p for p in COMBUSTIBLE if planet_record(chart, p)["combust"])


def _comb_prompt(conv: Convention, q: dict[str, Any]) -> str:
    return (
        f"Using the sidereal chart above ({conv.words()}), which planets are combust? Use "
        "the Surya Siddhanta orbs in longitude from the Sun: Moon 12, Mars 17, Mercury 14 "
        "(12 when retrograde), Jupiter 11, Venus 10 (8 when retrograde), Saturn 15 degrees; "
        "Rahu and Ketu are never combust. Give \"answer\" as a list of planet names, [] if "
        "none."
    )


COMBUSTION = EngineTask(
    name="combustion", tier="EASY", answer_type="set", grader="jaccard",
    query=_comb_query, answer=_comb_answer, prompt=_comb_prompt, choices=list(COMBUSTIBLE),
)

TASKS = [NAKSHATRA, VARGA, DASHA, DIGNITY, COMBUSTION]
