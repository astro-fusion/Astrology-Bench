"""Level 1 ``yoga`` and ``rule`` items from the vendored research rules.

Selection: rules with machine conditions, ``status: active``, no ``window`` and no
natal input (``EvalContext.at(moment, place)`` is enough). ``general/*`` rules become
``yoga`` items; other rules are kept, as ``rule`` items, only when their
``source.text`` resolves to a canon registry text.

The rule engine computes with the Lahiri ayanamsa and whole-sign houses only, so
these items exist for the cells lahiri/{mean,true}/whole_sign.

``rule_key`` mapping: take the rule id's segments after the domain, last first
(``general.gaja_kesari.classical`` -> ``classical``, ``gaja_kesari``); the first
segment that is a canon ``rule_key`` wins, else the last segment. ``canon_ids`` are
``canon.gold_for(rule_key)`` when the rule's source resolves to a canon text, else [].

Balance: per rule and cell, positives and negatives are sampled by rejection until
each class has half of the quota (so the split is 50/50, inside the ADR's 45/55).
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any

from vedic_astrology_core.rules.context import EvalContext, Location
from vedic_astrology_core.rules.engine import evaluate_context, rule_inputs
from vedic_astrology_core.rules.loader import RuleRegistry, discover
from vedic_astrology_core.rules.schema import Rule

from ..canon import Canon
from ..schema import Convention, Item
from .common import (
    CITE_HINT,
    DEFAULT_CONVENTION,
    GenContext,
    birth_model,
    build_chart,
    chart_table,
    make_item,
    parse_utc,
    repo_root,
    rng_for,
    sample_birth,
)

TIER = "MEDIUM"
GENERATOR = "yoga_from_rule"
CELLS = [Convention(node="mean"), Convention(node="true")]
TRIES_PER_ITEM = 400


def default_rules_dir() -> Path:
    return repo_root() / "vendor" / "rules"


@lru_cache(maxsize=4)
def load_registry(rules_dir: str) -> RuleRegistry:
    """The vendored rules (``ASTRO_RULES_DIR`` is set for the engine's own lookups)."""
    os.environ["ASTRO_RULES_DIR"] = rules_dir
    files = [p for p in discover([rules_dir]) if p.name != "UPSTREAM.yaml"]
    return RuleRegistry.load(files)


def rule_key(rule_id: str, canon: Canon) -> str:
    segments = rule_id.split(".")[1:] or rule_id.split(".")
    for seg in reversed(segments):
        if seg in canon.rule_keys():
            return seg
    return segments[-1]


def rule_tag(rule_id: str) -> str:
    """Id fragment for a rule: the id after the domain, dots as underscores."""
    return (rule_id.split(".", 1)[-1]).replace(".", "_")


def task_of(rule: Rule) -> str:
    return "yoga" if rule.domain == "general" else "rule"


def select_rules(registry: Iterable[Rule], canon: Canon) -> list[Rule]:
    """Rules evaluable from a moment and place, as described in the module docstring."""
    chosen = []
    for rule in registry:
        if rule.conditions is None or rule.status != "active" or rule.window is not None:
            continue
        if rule.natal is not None or rule_inputs(rule) - {"place"}:
            continue
        if rule.domain == "general" or canon.resolve_text(rule.source.text):
            chosen.append(rule)
    return sorted(chosen, key=lambda r: r.id)


def fires(rule: Rule, moment: Any, lat: float, lon: float, tz: str, node: str) -> bool:
    ctx = EvalContext.at(moment, Location(lat, lon, tz), None, node_model=node)
    return bool(evaluate_context(rule, ctx).fired)


def prompt_for(rule: Rule, conv: Convention) -> str:
    claim = " ".join(rule.claim.split())
    return (
        f"Using the sidereal chart above ({conv.words()}), does \"{rule.name}\" hold in this "
        f"chart? The rule as stated: {claim} Answer true or false. {CITE_HINT}"
    )


def _citation_for(rule: Rule, canon: Canon) -> tuple[str, list[str], str]:
    key = rule_key(rule.id, canon)
    text_id = canon.resolve_text(rule.source.text)
    if text_id is None:
        return "modern", [], key
    return text_id, [e.id for e in canon.gold_for(key)], key


def _rule_items(ctx: GenContext, rule: Rule, conv: Convention, n: int) -> list[Item]:
    want = {True: n // 2 + n % 2, False: n // 2}
    got: dict[bool, list[tuple[Any, Any]]] = {True: [], False: []}
    task = task_of(rule)
    attempt = 0
    while (len(got[True]) < want[True] or len(got[False]) < want[False]) and \
            attempt < TRIES_PER_ITEM * n:
        rng = rng_for(ctx.seed, f"{task}:{rule.id}", conv, attempt)
        attempt += 1
        moment, place = sample_birth(rng, ctx.places)
        verdict = fires(rule, moment, place.lat, place.lon, place.tz, conv.node)
        if len(got[verdict]) < want[verdict]:
            got[verdict].append((moment, place))
    if len(got[True]) < want[True] or len(got[False]) < want[False]:
        ctx.log(f"{rule.id} {conv.key}: could not balance "
                f"({len(got[True])}+/{len(got[False])}-); skipped")
        return []
    source, canon_ids, key = _citation_for(rule, ctx.canon)
    samples = sorted(((m, p, v) for v in (True, False) for m, p in got[v]),
                     key=lambda s: (s[0], s[1].name))
    items = []
    for index, (moment, place, verdict) in enumerate(samples):
        chart = build_chart(moment, place.lat, place.lon, conv)
        items.append(make_item(
            ctx=ctx, level=1, task=task, tier=TIER, conv=conv, index=index,
            generator=GENERATOR, prompt=prompt_for(rule, conv), answer_type="bool",
            answer=verdict, grader="exact", birth=birth_model(moment, place),
            chart=chart_table(chart, conv), query={"rule_id": rule.id, "rule_key": key},
            source=source, canon_ids=canon_ids, rule_id=rule.id, tag=rule_tag(rule.id),
        ))
    return items


def generate(ctx: GenContext, n_default: int, n_other: int) -> list[Item]:
    """``n_default`` items per task in the default cell (split over its rules), ``n_other``
    in the true-node cell; each rule gets at least 2 items per cell."""
    rules_dir = ctx.rules_dir or default_rules_dir()
    if not Path(rules_dir).exists():
        ctx.log(f"rules not found at {rules_dir}; skipping yoga/rule items")
        return []
    rules = select_rules(load_registry(str(rules_dir)), ctx.canon)
    items: list[Item] = []
    for task in ("yoga", "rule"):
        group = [r for r in rules if task_of(r) == task]
        if not group:
            continue
        for conv in CELLS:
            total = n_default if conv == DEFAULT_CONVENTION else n_other
            per_rule = max(2, total // len(group))
            for rule in group:
                items.extend(_rule_items(ctx, rule, conv, per_rule))
    return items


def solve(item: Item, rules_dir: Path | None = None) -> bool:
    """Evaluate the item's rule with the engine at the item's birth moment and place."""
    birth = item.input.birth
    assert birth is not None and item.rule_id is not None
    registry = load_registry(str(rules_dir or default_rules_dir()))
    rule = registry.get(item.rule_id)
    return fires(rule, parse_utc(birth.utc), birth.lat, birth.lon, birth.tz or "UTC",
                 item.convention.node)
