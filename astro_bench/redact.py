"""The redacted solver view and the input modes (ADR-002)."""

from __future__ import annotations

from .schema import InputMode, Item, SolverItem

BIRTH_MODE_NOTE = (
    "No chart table is given: compute the sidereal chart yourself from the birth data "
    "above using {convention}. "
)


def effective_mode(item: Item, input_mode: InputMode) -> InputMode:
    """Level 0 is always birth mode; Level 2 items carry no chart either way."""
    return "birth" if item.level == 0 else input_mode


def to_solver_item(item: Item, input_mode: InputMode = "chart") -> SolverItem:
    """Redact ``item`` for a solver; ``birth`` mode drops the chart table.

    In birth mode an item that had a chart gets a sentence saying the chart must be
    computed under the item's convention, so the convention stays in the prompt.
    """
    inp = item.input.model_copy(deep=True)
    prompt = item.prompt
    if effective_mode(item, input_mode) == "birth" and inp.chart is not None:
        inp.chart = None
        prompt = BIRTH_MODE_NOTE.format(convention=item.convention.words()) + prompt
    return SolverItem(
        id=item.id, level=item.level, task=item.task, tier=item.tier,
        convention=item.convention.model_copy(), input=inp, prompt=prompt,
        answer_type=item.answer_type, choices=list(item.choices) if item.choices else None,
    )


__all__ = ["BIRTH_MODE_NOTE", "effective_mode", "to_solver_item"]
