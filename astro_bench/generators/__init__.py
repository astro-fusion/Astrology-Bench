"""Procedural item generators for Levels 0-2 (deterministic in the seed)."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

from ..canon import Canon
from ..ephemeris import configure
from ..schema import Item
from . import level0, level1_engine, level1_relations, level1_rules, level2
from .common import GenContext, load_places
from .engine_task import EngineTask

ENGINE_TASKS: dict[str, EngineTask] = {
    t.name: t for t in [*level1_engine.TASKS, *level1_relations.TASKS]
}


def generate_items(
    *,
    levels: Sequence[int],
    split: str,
    seed: int,
    canon: Canon,
    n_default: int = 40,
    n_other: int = 10,
    rules_dir: Path | None = None,
    places_path: Path | None = None,
    tasks: Sequence[str] | None = None,
    log: Callable[[str], None] = lambda msg: None,
) -> list[Item]:
    """Generate every requested level. Golden Level 0 and Level 2 items are built from
    public data (the PyJHora fixture, the canon), so they are dev-only."""
    model = configure()  # pinned Swiss Ephemeris files; raises rather than use Moshier
    ctx = GenContext(seed=seed, split=split, places=load_places(places_path), canon=canon,
                     rules_dir=rules_dir, log=log, ephemeris_model=model)

    def wanted(task: str) -> bool:
        return tasks is None or task in tasks

    items: list[Item] = []
    if 0 in levels and wanted("positions"):
        items += level0.generate(ctx, n_default, n_other)
        if split == "dev":
            items += level0.generate_golden(ctx)
    if 1 in levels:
        for name, task in ENGINE_TASKS.items():
            if wanted(name):
                items += task.generate(ctx, n_default, n_other)
        if wanted("yoga") or wanted("rule"):
            items += [i for i in level1_rules.generate(ctx, n_default, n_other)
                      if wanted(i.task)]
    if 2 in levels and split == "dev" and wanted("citation"):
        items += level2.generate(ctx)
    for (task_name, reason), count in sorted(ctx.rejections.items()):
        log(f"resampled {count:5d}  {task_name}: {reason}")
    ids = [i.id for i in items]
    if len(ids) != len(set(ids)):
        raise RuntimeError("generator produced duplicate item ids")
    return items


__all__ = ["ENGINE_TASKS", "generate_items"]
