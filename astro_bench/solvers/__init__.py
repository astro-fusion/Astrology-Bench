"""Solvers: built-in baselines, the ``nochart:`` wrapper and ``module:callable`` loading."""

from __future__ import annotations

import importlib
from collections.abc import Sequence
from typing import Any, cast

from ..canon import Canon
from ..schema import Item
from .base import Solver, respond
from .baselines import ConstantSolver, MockSolver, RandomSolver
from .oracle import OracleSolver

BASELINES = ("oracle", "random", "constant", "mock")


class NoChartSolver:
    """Delete ``input.chart`` and ``input.birth`` before calling the inner solver."""

    def __init__(self, inner: Solver, inner_name: str):
        self.inner = inner
        self.name = f"nochart:{inner_name}"

    def __call__(self, item: Item) -> str:
        stripped = item.model_copy(deep=True)
        stripped.input.chart = None
        stripped.input.birth = None
        return self.inner(stripped)


def get_solver(name: str, items: Sequence[Item], canon: Canon) -> Solver:
    """Build a solver by name: a baseline, ``nochart:<name>`` or ``package.module:callable``.

    A ``module:callable`` target is called with no arguments when it is a class or a
    factory marked ``astro_bench_factory = True``; otherwise it is used as the solver.
    """
    if name.startswith("nochart:"):
        inner_name = name.split(":", 1)[1]
        return NoChartSolver(get_solver(inner_name, items, canon), inner_name)
    if name == "oracle":
        return OracleSolver(canon)
    if name == "random":
        return RandomSolver(canon)
    if name == "constant":
        return ConstantSolver(items)
    if name == "mock":
        return MockSolver()
    if ":" in name:
        module_name, attr = name.split(":", 1)
        target: Any = getattr(importlib.import_module(module_name), attr)
        if isinstance(target, type) or getattr(target, "astro_bench_factory", False):
            return cast(Solver, target())
        return cast(Solver, target)
    raise ValueError(f"unknown solver {name!r}; use {', '.join(BASELINES)}, nochart:<s> "
                     "or package.module:callable")


__all__ = ["BASELINES", "NoChartSolver", "Solver", "get_solver", "respond"]
