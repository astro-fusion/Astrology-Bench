"""A Level 1 task whose gold is one engine call on a chart (no rules involved)."""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from vedic_astrology_core.astrology.chart import BirthChart

from ..schema import Convention, Item
from .common import (
    CITE_HINT,
    DEFAULT_CONVENTION,
    GenContext,
    birth_model,
    build_chart,
    chart_of,
    chart_table,
    conventions,
    make_item,
    near_edge,
    parse_utc,
    rng_for,
    sample_birth,
    table_chart,
    task_canon,
)

QueryFn = Callable[[random.Random, BirthChart, datetime], "dict[str, Any] | None"]
AnswerFn = Callable[[BirthChart, "dict[str, Any]", datetime], Any]
PromptFn = Callable[[Convention, "dict[str, Any]"], str]


@dataclass(frozen=True)
class EngineTask:
    name: str
    tier: str
    answer_type: str
    grader: str
    query: QueryFn
    answer: AnswerFn
    prompt: PromptFn
    choices: list[str] | None = None
    house_dependent: bool = False
    whole_sign_only: bool = False
    generator: str = "engine_direct"
    max_tries: int = 200

    def cells(self) -> list[Convention]:
        return conventions(self.house_dependent, self.whole_sign_only)

    def solve(self, item: Item) -> Any:
        """Recompute the answer from the item's birth data with the engine."""
        assert item.input.birth is not None
        moment = parse_utc(item.input.birth.utc)
        return self.answer(chart_of(item), item.input.query, moment)

    def solve_from_table(self, item: Item) -> Any:
        """Recompute the answer from the item's printed chart table (chart mode)."""
        assert item.input.birth is not None and item.input.chart is not None
        moment = parse_utc(item.input.birth.utc)
        return self.answer(table_chart(chart_of(item), item.input.chart), item.input.query,
                           moment)

    def make(self, ctx: GenContext, conv: Convention, index: int) -> Item:
        for attempt in range(self.max_tries):
            rng = rng_for(ctx.seed, self.name, conv, index, salt=str(attempt))
            moment, place = sample_birth(rng, ctx.places)
            chart = build_chart(moment, place.lat, place.lon, conv)
            if near_edge(chart, conv):
                ctx.reject(self.name, "near an edge")
                continue
            query = self.query(rng, chart, moment)
            if query is None:
                ctx.reject(self.name, "near a dasha boundary")
                continue
            table = chart_table(chart, conv)
            answer = self.answer(table_chart(chart, table), query, moment)
            if answer != self.answer(chart, query, moment):
                ctx.reject(self.name, "table and engine disagree")
                continue
            source, canon_ids = task_canon(ctx.canon, self.name, query)
            prompt = f"{self.prompt(conv, query)} {CITE_HINT}"
            return make_item(
                ctx=ctx, level=1, task=self.name, tier=self.tier, conv=conv, index=index,
                generator=self.generator, prompt=prompt, answer_type=self.answer_type,
                answer=answer, grader=self.grader,
                birth=birth_model(moment, place), chart=table, query=query,
                choices=self.choices, source=source, canon_ids=canon_ids,
            )
        raise RuntimeError(f"{self.name}: no valid sample after {self.max_tries} tries")

    def generate(self, ctx: GenContext, n_default: int, n_other: int) -> list[Item]:
        items: list[Item] = []
        for conv in self.cells():
            n = n_default if conv == DEFAULT_CONVENTION else n_other
            items.extend(self.make(ctx, conv, index) for index in range(n))
        return items
