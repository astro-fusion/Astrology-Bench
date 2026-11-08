"""Baseline solvers: random, constant (majority class) and the v1 mock responder."""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from collections.abc import Sequence
from typing import Any

from vedic_astrology_core.rules.vocabulary import LAGNA, NAKSHATRA_NAMES, PLANET_NAMES, SIGN_NAMES

from ..canon import Canon
from ..schema import Item
from .answer_space import random_answer
from .base import respond


class RandomSolver:
    """Uniform over the answer space; never cites; confidence 0.5."""

    name = "random"

    def __init__(self, canon: Canon, seed: int = 0):
        self.canon = canon
        self.seed = seed

    def __call__(self, item: Item) -> str:
        rng = random.Random(f"random|{self.seed}|{item.id}")
        answer = random_answer(item, rng, self.canon)
        cites = [answer] if item.answer_type == "citation" and answer else []
        return respond(answer, cites, 0.5)


def _key(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def _majority(values: Sequence[Any]) -> tuple[Any, float]:
    counts = Counter(_key(v) for v in values)
    key, count = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    return json.loads(key), count / len(values)


class ConstantSolver:
    """The majority gold answer per task over the item set (positions: per field)."""

    name = "constant"

    def __init__(self, items: Sequence[Item]):
        by_task: dict[str, list[Item]] = defaultdict(list)
        for item in items:
            by_task[item.task].append(item)
        self.answers: dict[str, tuple[Any, float]] = {}
        for task, group in by_task.items():
            if group[0].answer_type == "positions":
                self.answers[task] = (self._positions(group), 0.0)
            else:
                self.answers[task] = _majority([i.gold.answer for i in group])

    @staticmethod
    def _positions(group: Sequence[Item]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for name in [*PLANET_NAMES, LAGNA]:
            recs = [i.gold.answer.get(name, {}) for i in group]
            rec: dict[str, Any] = {"sign": _majority([r.get("sign") for r in recs])[0]}
            if name != LAGNA:
                rec["nakshatra"] = _majority([r.get("nakshatra") for r in recs])[0]
                rec["pada"] = _majority([r.get("pada") for r in recs])[0]
                rec["deg_in_sign"] = 15.0
            out[name] = rec
        return out

    def __call__(self, item: Item) -> str:
        answer, share = self.answers.get(item.task, (None, 0.0))
        cites = [answer] if item.answer_type == "citation" and isinstance(answer, dict) else []
        return respond(answer, cites, share)


class MockSolver:
    """Port of the v1 seeded responder: seed = sum of the item id's character codes.

    For ``likert`` items it reproduces the five v1 reply formats exactly. For every
    other item it derives an answer from the seed, wraps the JSON in one of three
    formats (bare, fenced, prose) and cites BPHS chapter ``seed % 120 + 1`` on every
    third item, so it exercises the parser and the fabrication penalty.
    """

    name = "mock"

    def __call__(self, item: Item) -> str:
        seed = sum(ord(c) for c in item.id)
        if item.answer_type == "likert":
            score = seed % 5 + 1
            return [f"{score}", f"{score}/5", f"Score: {score}",
                    f"I would rate this a {score} based on the planetary configuration provided.",
                    f"{score} out of 5"][seed % 5]
        cites = [{"text": "BPHS", "chapter": str(seed % 120 + 1)}] if seed % 3 == 0 else []
        body = respond(self._answer(item, seed), cites, (seed % 10) / 10)
        return [body, f"```json\n{body}\n```", f"Here is my answer: {body} Hope this helps."][
            seed % 3]

    @staticmethod
    def _answer(item: Item, seed: int) -> Any:
        kind = item.answer_type
        choices = item.choices or []
        if kind == "bool":
            return seed % 2 == 0
        if kind == "positions":
            answer: dict[str, Any] = {
                name: {"sign": SIGN_NAMES[(seed + i) % 12], "deg_in_sign": float(seed % 30),
                       "nakshatra": NAKSHATRA_NAMES[(seed + i) % 27], "pada": seed % 4 + 1}
                for i, name in enumerate(PLANET_NAMES)
            }
            answer[LAGNA] = {"sign": SIGN_NAMES[seed % 12]}
            return answer
        if kind == "citation":
            return {"text": "BPHS", "chapter": str(seed % 120 + 1), "verse": str(seed % 30 + 1)}
        if kind == "set":
            return [c for i, c in enumerate(choices) if (seed >> i) & 1]
        if item.task == "nakshatra":
            return {"nakshatra": NAKSHATRA_NAMES[seed % 27], "pada": seed % 4 + 1}
        return choices[seed % len(choices)] if choices else None
