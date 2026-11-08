"""The solver protocol and shared helpers."""

from __future__ import annotations

import json
from typing import Any, Protocol, runtime_checkable

from ..schema import SolverItem


@runtime_checkable
class Solver(Protocol):
    """Anything that maps a redacted item to a raw text response (parsed by the runner).

    Solvers receive a :class:`SolverItem` (ADR-002): no gold, canon ids, rule id or
    generator. Only a solver with ``full_item = True`` (the engine oracle, which the
    runner builds itself) is handed the full item.
    """

    def __call__(self, item: SolverItem) -> str: ...


def respond(answer: Any, citations: list[dict[str, Any]] | None = None,
            confidence: float | None = None, note: str | None = None) -> str:
    """A well-formed JSON response in the required output format."""
    payload: dict[str, Any] = {"answer": answer, "citations": citations or []}
    if confidence is not None:
        payload["confidence"] = round(float(confidence), 4)
    if note:
        payload["note"] = note
    return json.dumps(payload, ensure_ascii=False)
