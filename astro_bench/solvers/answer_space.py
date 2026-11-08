"""Answer spaces per task, for the random, constant and mock baselines."""

from __future__ import annotations

import random
from typing import Any

from vedic_astrology_core.rules.vocabulary import (
    LAGNA,
    NAKSHATRA_NAMES,
    PLANET_NAMES,
    SIGN_NAMES,
)

from ..canon import Canon
from ..schema import Item


def random_point(rng: random.Random) -> dict[str, Any]:
    return {"sign": rng.choice(SIGN_NAMES), "deg_in_sign": round(rng.uniform(0, 30), 2),
            "nakshatra": rng.choice(NAKSHATRA_NAMES), "pada": rng.randint(1, 4)}


def random_answer(item: Item, rng: random.Random, canon: Canon) -> Any:
    """A uniform draw from the item's answer space."""
    kind = item.answer_type
    if kind == "bool":
        return rng.random() < 0.5
    if kind == "likert":
        return rng.randint(1, 5)
    if kind == "positions":
        answer = {name: random_point(rng) for name in PLANET_NAMES}
        answer[LAGNA] = {"sign": rng.choice(SIGN_NAMES)}
        return answer
    if kind == "citation":
        return random_citation(rng, canon)
    choices = item.choices or []
    if kind == "set":
        return sorted(c for c in choices if rng.random() < 0.5)
    if item.task == "nakshatra":
        return {"nakshatra": rng.choice(NAKSHATRA_NAMES), "pada": rng.randint(1, 4)}
    return rng.choice(choices) if choices else None


def random_citation(rng: random.Random, canon: Canon) -> dict[str, Any] | None:
    texts = list(canon.texts.values())
    if not texts:
        return None
    text = rng.choice(texts)
    return {"text": text.id, "chapter": str(rng.randint(1, text.chapters)),
            "verse": str(rng.randint(1, 40))}
