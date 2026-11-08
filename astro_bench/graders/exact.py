"""Exact match for bool, category and dict-shaped category answers."""

from __future__ import annotations

from typing import Any

from .normalize import normalize


def grade_exact(answer: Any, gold: Any) -> float:
    """1.0 when the canonical forms are equal, else 0.0."""
    if isinstance(gold, bool):
        norm = normalize(answer)
        return 1.0 if isinstance(norm, bool) and norm == gold else 0.0
    return 1.0 if normalize(answer) == normalize(gold) else 0.0
