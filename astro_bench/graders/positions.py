"""Positions grader (ADR-001 weights).

Per planet: sign exact 0.5, nakshatra exact 0.25, longitude within ``tolerance_deg``
0.25 (the longitude is sign * 30 + deg_in_sign, compared on the circle). The Lagna
is one more "planet" scored on its sign alone (1.0 or 0.0). The score is the mean
over every planet in the gold.
"""

from __future__ import annotations

from typing import Any

from vedic_astrology_core.rules.vocabulary import (
    LAGNA,
    SIGN_NAMES,
    VocabularyError,
    point_name,
    sign_name,
)

from .normalize import normalize

DEFAULT_TOLERANCE_DEG = 1.0


def _sign_index(value: Any) -> int | None:
    try:
        return SIGN_NAMES.index(sign_name(str(value)))
    except (VocabularyError, ValueError):
        return None


def _lon(rec: dict[str, Any]) -> float | None:
    idx = _sign_index(rec.get("sign"))
    try:
        deg = float(rec.get("deg_in_sign"))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    if idx is None:
        return None
    return idx * 30.0 + deg


def _by_point(answer: Any) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not isinstance(answer, dict):
        return out
    for key, rec in answer.items():
        try:
            name = point_name(str(key))
        except VocabularyError:
            continue
        if isinstance(rec, dict):
            out[name] = rec
        elif isinstance(rec, str):
            out[name] = {"sign": rec}
    return out


def grade_planet(got: dict[str, Any] | None, want: dict[str, Any], tol: float) -> float:
    if not got:
        return 0.0
    score = 0.0
    if _sign_index(got.get("sign")) == _sign_index(want.get("sign")):
        score += 0.5
    if normalize(got.get("nakshatra")) == normalize(want.get("nakshatra")):
        score += 0.25
    lon_got, lon_want = _lon(got), _lon(want)
    if lon_got is not None and lon_want is not None:
        diff = abs(lon_got - lon_want) % 360.0
        if min(diff, 360.0 - diff) <= tol:
            score += 0.25
    return score


def grade_positions(answer: Any, gold: Any, tolerance_deg: float | None = None) -> float:
    tol = DEFAULT_TOLERANCE_DEG if tolerance_deg is None else tolerance_deg
    got = _by_point(answer)
    want = _by_point(gold)
    if not want:
        return 0.0
    total = 0.0
    for name, rec in want.items():
        if name == LAGNA:
            same = _sign_index(got.get(name, {}).get("sign")) == _sign_index(rec.get("sign"))
            total += 1.0 if same else 0.0
        else:
            total += grade_planet(got.get(name), rec, tol)
    return total / len(want)
