from __future__ import annotations

import pytest

from astro_bench.canon import Canon, CanonError, chapter_number, verse_numbers
from astro_bench.graders.citation import grade_citation_answer, grade_citations
from astro_bench.schema import CanonEntry, CanonRegistry, Citation

GK = ["bphs.santhanam1984.ch36.v3"]


def cites(*rows: dict) -> list[Citation]:
    return [Citation.model_validate(r) for r in rows]


def test_canon_indexes(canon: Canon) -> None:
    assert canon.is_known_text("Brihat Parasara Hora Sastra")
    assert canon.resolve_text("phaladipika") == "Phaladeepika"
    assert not canon.is_known_text("Lal Kitab")
    assert canon.chapter_in_range("BPHS", "97") and not canon.chapter_in_range("BPHS", "98")
    assert [e.id for e in canon.gold_for("gaja_kesari")] == GK
    assert canon.gold_for("graha_drishti") == []  # paraphrased only
    assert ("BPHS", 36) in canon.by_text_chapter


def test_chapter_and_verse_parsing() -> None:
    assert chapter_number("Ch. 36") == 36 and chapter_number("intro") is None
    assert verse_numbers("3-4") == {3, 4} and verse_numbers("3, 7") == {3, 7}
    assert verse_numbers(None) == set()


@pytest.mark.parametrize(
    ("rows", "score", "fabricated"),
    [
        ([], 0, False),
        ([{"text": "BPHS", "chapter": "36", "verse": "3"}], 1, False),
        ([{"text": "Brihat Parashara Hora Shastra", "chapter": "Ch. 36", "verse": "4"}], 1, False),
        # the also_in alternate
        ([{"text": "Phaladeepika", "chapter": "6", "verse": "1"}], 1, False),
        # gold has a verse: wrong verse is unsupported
        ([{"text": "BPHS", "chapter": "36", "verse": "9"}], -1, True),
        # unknown text
        ([{"text": "Lal Kitab", "chapter": "2"}], -1, True),
        # chapter beyond the registry count
        ([{"text": "BPHS", "chapter": "120", "verse": "3"}], -1, True),
        # a real locus that does not support the claim
        ([{"text": "BPHS", "chapter": "12", "verse": "3"}], -1, True),
        # vague: known text, no chapter
        ([{"text": "BPHS"}], 0, False),
        # a match plus an unsupported real locus: +1 but flagged
        ([{"text": "BPHS", "chapter": "36", "verse": "3"}, {"text": "BPHS", "chapter": "12"}],
         1, True),
        # a match plus a fabricated text: the fabrication wins
        ([{"text": "BPHS", "chapter": "36", "verse": "3"}, {"text": "Lal Kitab", "chapter": "1"}],
         -1, True),
    ],
)
def test_citation_scores(canon: Canon, rows: list[dict], score: int, fabricated: bool) -> None:
    grade = grade_citations(canon, cites(*rows), GK)
    assert (grade.score, grade.fabricated) == (score, fabricated)


def test_not_graded_without_canon_ids(canon: Canon) -> None:
    grade = grade_citations(canon, cites({"text": "Lal Kitab", "chapter": "1"}), [])
    assert grade.score is None and not grade.fabricated


def test_citation_answer(canon: Canon) -> None:
    assert grade_citation_answer(canon, {"text": "BPHS", "chapter": 36, "verse": "3"}, GK) == 1.0
    assert grade_citation_answer(canon, [{"text": "BPHS", "chapter": "36"}], GK) == 0.0
    assert grade_citation_answer(canon, None, GK) == 0.0


def test_canon_rejects_unknown_text_and_bad_chapter() -> None:
    reg = CanonRegistry.model_validate({"texts": [{"id": "BPHS", "title": "B", "chapters": 2}]})
    base = {"text": "BPHS", "chapter": "1", "topic": "yoga", "rule_key": "x",
            "statement": "s", "verified": "quoted"}
    with pytest.raises(CanonError):
        Canon(reg, [CanonEntry.model_validate(dict(base, id="a", text="Nope"))])
    with pytest.raises(CanonError):
        Canon(reg, [CanonEntry.model_validate(dict(base, id="a", chapter="3"))])
    assert len(Canon(reg, [CanonEntry.model_validate(dict(base, id="a"))])) == 1
