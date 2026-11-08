from __future__ import annotations

import pytest

from astro_bench.parse import ParseError, parse_likert, parse_response


@pytest.mark.parametrize(
    "raw",
    [
        '{"answer": "Mars", "citations": [], "confidence": 0.8}',
        '```json\n{"answer": "Mars", "citations": []}\n```',
        'Sure! Here you go:\n{"answer": "Mars"}\nLet me know if you need more.',
        'Reasoning {not json} then {"answer": "Mars", "note": "x"} trailing } text',
        '{"thinking": "hmm"} and finally {"answer": "Mars"}',
        '```\n{"answer": "Mars"}\n```',
    ],
)
def test_extracts_answer(raw: str) -> None:
    assert parse_response(raw, "category").answer == "Mars"


def test_nested_objects_and_citations() -> None:
    raw = 'x {"answer": {"nakshatra": "Rohini", "pada": 2}, "citations": [{"text": "BPHS", ' \
          '"chapter": "3"}, "junk"]} y'
    out = parse_response(raw, "category")
    assert out.answer == {"nakshatra": "Rohini", "pada": 2}
    assert [c.text for c in out.citations] == ["BPHS"]


@pytest.mark.parametrize("raw", ["", "   ", "The answer is Mars.", '{"result": "Mars"}',
                                 "{broken json"])
def test_parse_errors(raw: str) -> None:
    with pytest.raises(ParseError):
        parse_response(raw, "category")


@pytest.mark.parametrize(
    ("raw", "score"),
    [("3", 3), ("4/5", 4), ("Score: 2", 2), ("I would rate this a 5 based on it", 5),
     ("1 out of 5", 1), ("**3**", 3), ("Answer:\n4", 4), ("three", 3)],
)
def test_likert_fallback_ports_v1(raw: str, score: int) -> None:
    assert parse_likert(raw) == score
    assert parse_response(raw, "likert").answer == score


def test_likert_fallback_only_for_likert() -> None:
    with pytest.raises(ParseError):
        parse_response("4/5", "category")
    with pytest.raises(ParseError):
        parse_likert("definitely maybe")
