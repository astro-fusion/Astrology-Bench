"""Jaccard similarity for set answers."""

from __future__ import annotations

from typing import Any

from .normalize import as_set


def grade_jaccard(answer: Any, gold: Any) -> float:
    """|A & G| / |A | G|; two empty sets score 1.0; a non-list answer scores 0.0."""
    got = as_set(answer)
    want = as_set(gold)
    if got is None or want is None:
        return 0.0
    if not got and not want:
        return 1.0
    return len(got & want) / len(got | want)
