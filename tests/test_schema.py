from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from astro_bench.io import dump_item
from astro_bench.runner import run
from astro_bench.schema import Item, ModelOutput, RunResult
from astro_bench.solvers import get_solver


def test_item_round_trip(small_items: list[Item]) -> None:
    for item in small_items:
        again = Item.model_validate_json(dump_item(item))
        assert again == item
        assert dump_item(again) == dump_item(item)


def test_item_rejects_unknown_fields(small_items: list[Item]) -> None:
    data = json.loads(dump_item(small_items[0]))
    data["surprise"] = 1
    with pytest.raises(ValidationError):
        Item.model_validate(data)


def test_item_schema_version_is_one(small_items: list[Item]) -> None:
    data = json.loads(dump_item(small_items[0]))
    data["schema_version"] = 2
    with pytest.raises(ValidationError):
        Item.model_validate(data)


def test_model_output_coerces_loose_fields() -> None:
    out = ModelOutput.model_validate(
        {"answer": "Mars", "citations": {"text": "BPHS", "chapter": 36, "verse": 3},
         "confidence": "1.7"}
    )
    assert out.citations[0].chapter == "36" and out.citations[0].verse == "3"
    assert out.confidence == 1.0
    assert ModelOutput.model_validate({"answer": 1, "citations": None}).citations == []


def test_run_result_round_trip(small_items: list[Item], canon) -> None:  # type: ignore[no-untyped-def]
    items = small_items[:20]
    result = run(get_solver("mock", items, canon), items, canon, solver_name="mock")
    again = RunResult.model_validate_json(result.model_dump_json(exclude_none=True))
    assert again.summary == result.summary
    assert again.item_count == 20
