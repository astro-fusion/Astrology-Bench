"""Level 1 house tasks: graha drishti on a house, and where a house lord sits.

``aspect`` uses the engine's drishti table (``GRAHA_DRISHTI``) and whole-sign
counting (``house_from``), so it is generated for whole-sign cells only.
``lordship`` reads the sign on the cusp of house N and the house of its Parashari
lord from the engine chart, so it works for whole-sign and Placidus alike.
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from vedic_astrology_core.astrology.chart import BirthChart
from vedic_astrology_core.rules.predicates import house_from
from vedic_astrology_core.rules.predicates.placement import SIGN_LORDS
from vedic_astrology_core.rules.predicates.relations import GRAHA_DRISHTI
from vedic_astrology_core.rules.vocabulary import PLANET_NAMES, ordinal

from ..schema import Convention
from .common import planet_record
from .engine_task import EngineTask


def _sign(chart: BirthChart, planet: str) -> int:
    return int(float(planet_record(chart, planet)["longitude"]) % 360.0 // 30)


def _house_query(rng: random.Random, chart: BirthChart, moment: datetime) -> dict[str, Any]:
    return {"house": rng.randint(1, 12)}


# --------------------------------------------------------------------------- aspect


def _aspect_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> list[str]:
    target = (int(chart.ascendant["sign"]) + int(q["house"]) - 1) % 12
    return sorted(
        p for p in PLANET_NAMES if house_from(_sign(chart, p), target) in GRAHA_DRISHTI[p]
    )


def _aspect_prompt(conv: Convention, q: dict[str, Any]) -> str:
    return (
        f"Using the sidereal chart above ({conv.words()}), which planets cast a graha "
        f"drishti (Parashari sign aspect) on the {ordinal(int(q['house']))} house? Every "
        "planet aspects the 7th sign from itself; Mars also the 4th and 8th, Jupiter the "
        "5th and 9th, Saturn the 3rd and 10th; Rahu and Ketu the 7th only. A planet in the "
        'house itself is conjunct, not aspecting. Give "answer" as a list of planet names, '
        "[] if none."
    )


ASPECT = EngineTask(
    name="aspect", tier="MEDIUM", answer_type="set", grader="jaccard",
    query=_house_query, answer=_aspect_answer, prompt=_aspect_prompt,
    choices=list(PLANET_NAMES), whole_sign_only=True,
)

# --------------------------------------------------------------------------- lordship


def house_lord(chart: BirthChart, house: int) -> str:
    """Parashari lord of the sign on the cusp of ``house`` (no node lordship)."""
    return str(SIGN_LORDS[int(chart.houses[house - 1]["sign"])])


def _lord_answer(chart: BirthChart, q: dict[str, Any], moment: datetime) -> str:
    return str(chart.get_planet_in_house(house_lord(chart, int(q["house"]))))


def _lord_prompt(conv: Convention, q: dict[str, Any]) -> str:
    which = (
        "the sign of that house"
        if conv.house == "whole_sign"
        else "the sign on that house's cusp (cusps listed above)"
    )
    return (
        f"Using the sidereal chart above ({conv.words()}), in which house does the lord of "
        f"the {ordinal(int(q['house']))} house sit? The lord is the Parashari ruler of "
        f"{which}; Rahu and Ketu rule no sign. Give \"answer\" as the house number 1-12 as "
        "a string."
    )


LORDSHIP = EngineTask(
    name="lordship", tier="MEDIUM", answer_type="category", grader="exact",
    query=_house_query, answer=_lord_answer, prompt=_lord_prompt,
    choices=[str(h) for h in range(1, 13)], house_dependent=True,
)

TASKS = [ASPECT, LORDSHIP]
