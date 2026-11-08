"""Canonical forms for answer values, using the engine's own vocabulary.

Planet, sign and nakshatra names go through ``vedic_astrology_core.rules.vocabulary``
so "Guru", "Mesha" and "Aswini" equal "Jupiter", "Aries" and "Ashwini". Other strings
are compared casefolded with spaces, hyphens and underscores removed.
"""

from __future__ import annotations

import re
from typing import Any

from vedic_astrology_core.rules.vocabulary import (
    VocabularyError,
    nakshatra_name,
    planet_name,
    sign_name,
)

_INT = re.compile(r"^[+-]?\d+$")
_BOOL = {"true": True, "yes": True, "false": False, "no": False}


def norm_str(value: str) -> Any:
    text = value.strip()
    low = text.lower()
    if low in _BOOL:
        return _BOOL[low]
    if _INT.match(text):
        return int(text)
    for resolve in (planet_name, sign_name, nakshatra_name):
        try:
            return resolve(text)
        except VocabularyError:
            continue
    return re.sub(r"[\s_\-]+", "", low)


def normalize(value: Any) -> Any:
    """Recursively canonicalise an answer value for comparison."""
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else round(value, 6)
    if isinstance(value, str):
        return norm_str(value)
    if isinstance(value, dict):
        return {str(k).strip().lower(): normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        items = [normalize(v) for v in value]
        try:
            return sorted(set(items), key=repr)
        except TypeError:
            return sorted(items, key=repr)
    return value


def as_set(value: Any) -> set[Any] | None:
    """A set of hashable canonical members, or None when ``value`` is not a list."""
    if isinstance(value, str):
        value = [v for v in re.split(r"[,;]", value) if v.strip()]
    if not isinstance(value, (list, tuple, set)):
        return None
    out: set[Any] = set()
    for member in value:
        norm = normalize(member)
        try:
            out.add(norm)
        except TypeError:
            out.add(repr(norm))
    return out
