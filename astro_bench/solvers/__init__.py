"""Solvers: built-in baselines, the ``nochart:`` wrapper and ``module:callable`` loading."""

from __future__ import annotations

import importlib
from collections.abc import Sequence
from typing import Any, cast

from ..canon import Canon
from ..schema import Item, SolverItem
from .base import Solver, respond
from .baselines import ConstantSolver, MockSolver, RandomSolver
from .http_json import HttpJsonSolver
from .oracle import OracleSolver

BASELINES = ("oracle", "random", "constant", "mock")


def default_kind(name: str) -> str | None:
    """oracle -> oracle; random/constant/mock -> baseline; anything else needs --kind."""
    inner = name.split(":", 1)[1] if name.startswith("nochart:") else name
    if inner == "oracle":
        return "oracle"
    if inner in BASELINES:
        return "baseline"
    return None


class NoChartSolver:
    """Ablation: delete ``input.chart`` and ``input.birth`` from the redacted view."""

    def __init__(self, inner: Solver, inner_name: str):
        self.inner = inner
        self.name = f"nochart:{inner_name}"

    def __call__(self, item: SolverItem) -> str:
        if not isinstance(item, SolverItem):
            raise TypeError("nochart: expects the redacted SolverItem view")
        empty = item.input.model_copy(update={"chart": None, "birth": None})
        return self.inner(item.model_copy(update={"input": empty}))


def get_solver(name: str, items: Sequence[Item], canon: Canon) -> Solver:
    """Build a solver: a baseline, ``nochart:<name>``, ``http_json:<config.yaml>`` or
    ``package.module:callable``.

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
    if name.startswith("http_json:"):
        return HttpJsonSolver.from_file(name.split(":", 1)[1])
    if ":" in name:
        module_name, attr = name.split(":", 1)
        target: Any = getattr(importlib.import_module(module_name), attr)
        if isinstance(target, type) or getattr(target, "astro_bench_factory", False):
            return cast(Solver, target())
        return cast(Solver, target)
    raise ValueError(f"unknown solver {name!r}; use {', '.join(BASELINES)}, nochart:<s>, "
                     "http_json:<config.yaml> or package.module:callable")


__all__ = ["BASELINES", "HttpJsonSolver", "NoChartSolver", "Solver", "default_kind", "get_solver",
           "respond"]
