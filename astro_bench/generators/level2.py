"""Level 2 ``citation``: name the text, chapter and verse that defines a rule.

One item per ``verified: quoted`` canon entry. Gold is that entry's locus; any quoted
entry with the same ``rule_key`` (and every ``also_in`` alternate) is also accepted,
since a rule defined in two texts can be cited from either. Level 2 items carry no
birth data or chart: the question is about the text, not a chart.
"""

from __future__ import annotations

from ..schema import Item
from .common import DEFAULT_CONVENTION, GenContext, make_item

TASK = "citation"
TIER = "HARD"
GENERATOR = "citation_from_canon"


def prompt_for(statement: str, rule_key: str, topic: str) -> str:
    name = rule_key.replace("_", " ")
    return (
        f"Which classical text, chapter and verse defines the following {topic} rule "
        f"(\"{name}\")? Rule: {statement.strip()} Use the chapter and verse numbering of "
        "a standard edition and name it in \"edition\". Give \"answer\" as "
        '{"text": "<text>", "chapter": "<chapter>", "verse": "<verse>", "edition": '
        '"<edition>"} and repeat it in citations. If you do not know, set "answer" to null '
        f"and citations to []. (Convention, if it matters: {DEFAULT_CONVENTION.words()}.)"
    )


def generate(ctx: GenContext) -> list[Item]:
    entries = ctx.canon.quoted()
    if not entries:
        ctx.log("canon has no verified: quoted entries; skipping Level 2")
        return []
    items = []
    for index, entry in enumerate(entries):
        same_key = [e.id for e in ctx.canon.gold_for(entry.rule_key)]
        canon_ids = [entry.id] + [cid for cid in same_key if cid != entry.id]
        text_id = ctx.canon.resolve_text(entry.text) or entry.text
        answer = {"text": text_id, "chapter": entry.chapter, "verse": entry.verse}
        items.append(make_item(
            ctx=ctx, level=2, task=TASK, tier=TIER, conv=DEFAULT_CONVENTION, index=index,
            generator=GENERATOR, prompt=prompt_for(entry.statement, entry.rule_key, entry.topic),
            answer_type="citation", answer=answer, grader="citation", source=text_id,
            canon_ids=canon_ids, query={"rule_key": entry.rule_key, "canon_id": entry.id},
            item_id_override=f"L2-citation-{entry.id}",
        ))
    return items
