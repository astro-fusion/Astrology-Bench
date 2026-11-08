"""Answer and citation graders."""

from __future__ import annotations

from typing import Any

from ..canon import Canon
from ..schema import Item
from .citation import CitationGrade, grade_citation_answer, grade_citations
from .exact import grade_exact
from .jaccard import grade_jaccard
from .positions import grade_positions


def grade_answer(item: Item, answer: Any, canon: Canon) -> float:
    """Answer score in [0, 1] for ``item`` using its declared grader."""
    name = item.grader.name
    gold = item.gold.answer
    if name == "positions":
        return grade_positions(answer, gold, item.grader.tolerance_deg)
    if name == "jaccard":
        return grade_jaccard(answer, gold)
    if name == "citation":
        return grade_citation_answer(canon, answer, item.canon_ids)
    return grade_exact(answer, gold)


__all__ = [
    "CitationGrade",
    "grade_answer",
    "grade_citation_answer",
    "grade_citations",
    "grade_exact",
    "grade_jaccard",
    "grade_positions",
]
