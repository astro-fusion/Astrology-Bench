"""Extract the model's JSON answer from a raw response.

The parser takes the first well-formed JSON object in the response, tolerating
code fences, prose before it and text after it. For ``likert`` items only, a
response without a JSON object falls back to the v1 tolerant 1-5 extractor
(ported from the retired ``src/core/parser.ts``).
"""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from .schema import ModelOutput


class ParseError(ValueError):
    """No usable JSON object (or, for likert items, no 1-5 score) in the response."""

    def __init__(self, raw: str, reason: str = "no JSON object found"):
        snippet = raw if len(raw) <= 120 else raw[:120] + "..."
        super().__init__(f"{reason}: {snippet!r}")
        self.raw = raw
        self.reason = reason


_FENCE = re.compile(r"```(?:json|JSON)?\s*\n?(.*?)```", re.DOTALL)
_DECODER = json.JSONDecoder()


def _objects(text: str) -> list[dict[str, Any]]:
    """Every top-level JSON object decodable from ``text``, in order."""
    found: list[dict[str, Any]] = []
    pos = 0
    while True:
        start = text.find("{", pos)
        if start < 0:
            return found
        try:
            obj, end = _DECODER.raw_decode(text, start)
        except json.JSONDecodeError:
            pos = start + 1
            continue
        if isinstance(obj, dict):
            found.append(obj)
        pos = end


def _candidates(raw: str) -> list[dict[str, Any]]:
    fenced = [obj for block in _FENCE.findall(raw) for obj in _objects(block)]
    return fenced + _objects(raw)


def first_json_object(raw: str) -> dict[str, Any] | None:
    """First JSON object with an ``answer`` key (fenced blocks first), else the first one."""
    objs = _candidates(raw)
    for obj in objs:
        if "answer" in obj:
            return obj
    return objs[0] if objs else None


# --------------------------------------------------------------------------- likert (v1 port)

_FRACTION = re.compile(r"([1-5])\s*/\s*5", re.IGNORECASE)
_LABELLED = re.compile(r"(?:score|rating|answer|result|response)[:\s]+([1-5])\b", re.IGNORECASE)
_OUT_OF = re.compile(r"([1-5])\s+out\s+of\s+5", re.IGNORECASE)
_ISOLATED = re.compile(r"(?<![0-9])[1-5](?![0-9])")
_WORDS = [
    (re.compile(r"\bone\b", re.I), 1),
    (re.compile(r"\btwo\b", re.I), 2),
    (re.compile(r"\bthree\b", re.I), 3),
    (re.compile(r"\bfour\b", re.I), 4),
    (re.compile(r"\bfive\b", re.I), 5),
]


def parse_likert(raw: str) -> int:
    """v1 layered 1-5 extraction: fraction, label, "out of 5", isolated digit, word."""
    cleaned = re.sub(r"\s+", " ", raw.strip())
    for pattern in (_FRACTION, _LABELLED, _OUT_OF):
        match = pattern.search(cleaned)
        if match:
            return int(match.group(1))
    match = _ISOLATED.search(cleaned)
    if match:
        return int(match.group(0))
    for pattern, value in _WORDS:
        if pattern.search(cleaned):
            return value
    raise ParseError(raw, "no 1-5 score found")


# --------------------------------------------------------------------------- public


def parse_response(raw: str | None, answer_type: str | None = None) -> ModelOutput:
    """Return the :class:`ModelOutput` in ``raw`` or raise :class:`ParseError`."""
    if raw is None or not raw.strip():
        raise ParseError(raw or "", "empty response")
    obj = first_json_object(raw)
    if obj is not None and "answer" in obj:
        try:
            return ModelOutput.model_validate(obj)
        except ValidationError as exc:
            raise ParseError(raw, f"invalid output object ({exc.error_count()} errors)") from exc
    if answer_type == "likert":
        return ModelOutput(answer=parse_likert(raw))
    if obj is not None:
        raise ParseError(raw, "JSON object has no 'answer' key")
    raise ParseError(raw)


__all__ = ["ParseError", "first_json_object", "parse_likert", "parse_response"]
