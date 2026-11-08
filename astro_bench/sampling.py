"""Reproducible stratified subsets of an item set (ADR-002 decision 5)."""

from __future__ import annotations

import hashlib
import random
from collections import defaultdict
from collections.abc import Sequence

from .schema import Item

STRATA_KEYS = ("task", "level", "tier", "source", "convention")


def _stratum(item: Item, keys: Sequence[str]) -> tuple[str, ...]:
    out = []
    for key in keys:
        if key == "convention":
            out.append(item.convention.key)
        elif key in STRATA_KEYS:
            out.append(str(getattr(item, key)))
        else:
            raise ValueError(f"unknown stratify key {key!r}; use {', '.join(STRATA_KEYS)}")
    return tuple(out)


def stratified_sample(items: Sequence[Item], n: int, keys: Sequence[str], seed: int
                      ) -> list[Item]:
    """``n`` items, allocated to strata in proportion to their size (largest remainder,
    ties by stratum name), drawn within each stratum by a seeded RNG over ids sorted.

    The result depends only on (item ids and strata, n, keys, seed), sorted by id.
    """
    if n >= len(items):
        return sorted(items, key=lambda i: i.id)
    groups: dict[tuple[str, ...], list[Item]] = defaultdict(list)
    for item in items:
        groups[_stratum(item, keys)].append(item)
    total = len(items)
    quotas = {g: n * len(members) / total for g, members in groups.items()}
    alloc = {g: int(q) for g, q in quotas.items()}
    left = n - sum(alloc.values())
    for g in sorted(groups, key=lambda g: (-(quotas[g] - alloc[g]), g))[:left]:
        alloc[g] += 1
    chosen: list[Item] = []
    for g in sorted(groups):
        members = sorted(groups[g], key=lambda i: i.id)
        rng = random.Random(f"astro-bench-sample|{seed}|{'|'.join(g)}")
        chosen.extend(rng.sample(members, alloc[g]))
    return sorted(chosen, key=lambda i: i.id)


def ids_sha256(items: Sequence[Item]) -> str:
    """sha256 of the sorted item ids, one per line."""
    return hashlib.sha256("".join(f"{i}\n" for i in sorted(x.id for x in items)).encode()
                          ).hexdigest()
