"""Citation grading against the canon (ADR-001 Scoring).

Per citation:

* ``+1`` it matches a gold canon entry or one of its ``also_in`` alternates: same
  text (resolved through the registry), same chapter number, and an overlapping verse
  when the gold locus has a verse;
* ``0`` it names a registry text but no chapter (vague, not fabricated);
* ``-1`` it names a text not in the registry, a chapter beyond that text's chapter
  count, or a real locus that is not among the gold loci (unsupported claim).

Per item (only when ``canon_ids`` is non-empty): no citations scores 0; any
fabricated text or out-of-range chapter scores -1; otherwise any match scores +1;
otherwise -1 if any citation scored -1, else 0. ``fabricated`` is True when any
citation scored -1.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..canon import Canon, chapter_number, verse_numbers
from ..schema import Citation


@dataclass(frozen=True)
class Locus:
    text: str
    chapter: int
    verses: frozenset[str]


@dataclass(frozen=True)
class CitationGrade:
    score: int | None
    fabricated: bool
    per_citation: tuple[int, ...] = ()


def gold_loci(canon: Canon, canon_ids: Sequence[str]) -> list[Locus]:
    """The gold loci of ``canon_ids`` and their ``also_in`` alternates."""
    loci: list[Locus] = []
    for cid in canon_ids:
        entry = canon.entry(cid)
        if entry is None:
            continue
        pairs = [(entry.text, entry.chapter, entry.verse)]
        pairs += [(alt.text, alt.chapter, alt.verse) for alt in entry.also_in]
        for text, chapter, verse in pairs:
            text_id = canon.resolve_text(text) or text
            num = chapter_number(chapter)
            if num is not None:
                loci.append(Locus(text_id, num, frozenset(verse_numbers(verse))))
    return loci


def matches(canon: Canon, cite: Citation, locus: Locus) -> bool:
    """True when ``cite`` names ``locus`` (text, chapter, verse when gold has one)."""
    if canon.resolve_text(cite.text) != locus.text:
        return False
    if chapter_number(cite.chapter) != locus.chapter:
        return False
    if not locus.verses:
        return True
    return bool(verse_numbers(cite.verse) & locus.verses)


def score_one(canon: Canon, cite: Citation, loci: Sequence[Locus]) -> int:
    """+1, 0 or -1 for one citation (see module docstring)."""
    text_id = canon.resolve_text(cite.text)
    if text_id is None:
        return -1
    if cite.chapter is None or not str(cite.chapter).strip():
        return 0
    if not canon.chapter_in_range(text_id, cite.chapter):
        return -1
    return 1 if any(matches(canon, cite, locus) for locus in loci) else -1


def _hard_fabrication(canon: Canon, cite: Citation) -> bool:
    if canon.resolve_text(cite.text) is None:
        return True
    has_chapter = cite.chapter is not None and str(cite.chapter).strip() != ""
    return has_chapter and not canon.chapter_in_range(cite.text, cite.chapter)


def grade_citations(
    canon: Canon, citations: Sequence[Citation], canon_ids: Sequence[str]
) -> CitationGrade:
    """Item-level citation score in {-1, 0, 1}, or None when not graded."""
    if not canon_ids:
        return CitationGrade(None, False)
    if not citations:
        return CitationGrade(0, False)
    loci = gold_loci(canon, canon_ids)
    per = tuple(score_one(canon, c, loci) for c in citations)
    fabricated = -1 in per
    if any(_hard_fabrication(canon, c) for c in citations):
        return CitationGrade(-1, True, per)
    if 1 in per:
        return CitationGrade(1, fabricated, per)
    return CitationGrade(-1 if fabricated else 0, fabricated, per)


def grade_citation_answer(canon: Canon, answer: object, canon_ids: Sequence[str]) -> float:
    """Answer score for ``answer_type: citation``: 1.0 when the answer names a gold locus."""
    if isinstance(answer, list) and answer:
        answer = answer[0]
    if not isinstance(answer, dict):
        return 0.0
    try:
        cite = Citation.model_validate(answer)
    except ValueError:
        return 0.0
    loci = gold_loci(canon, canon_ids)
    return 1.0 if any(matches(canon, cite, locus) for locus in loci) else 0.0
