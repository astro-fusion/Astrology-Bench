"""Run a solver over items: call, parse, grade, summarise."""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import BENCH_VERSION, ENGINE_COMMIT
from .canon import Canon
from .graders import grade_answer, grade_citations
from .io import items_sha256
from .parse import ParseError, parse_response
from .schema import Item, PerItem, RunResult
from .score import summarize
from .solvers import BASELINES, Solver


def grade_response(item: Item, raw: str | None, canon: Canon, error: str | None = None
                   ) -> PerItem:
    """Grade one raw response (a parse error scores 0 on answer and citation)."""
    base: dict[str, Any] = {
        "id": item.id, "level": item.level, "task": item.task, "tier": item.tier,
        "source": item.source, "convention": item.convention.key,
    }
    graded_cites = bool(item.canon_ids)
    try:
        if error is not None:
            raise ParseError(raw or "", error)
        out = parse_response(raw, item.answer_type)
    except ParseError as exc:
        return PerItem(**base, parse_error=True, answer_score=0.0,
                       citation_score=0 if graded_cites else None, error=exc.reason)
    cite = grade_citations(canon, out.citations, item.canon_ids)
    return PerItem(
        **base, parse_error=False, answer_score=round(grade_answer(item, out.answer, canon), 6),
        citation_score=cite.score, fabricated=cite.fabricated, confidence=out.confidence,
        answer=None if item.answer_type == "positions" else out.answer,
    )


def run(solver: Solver, items: Sequence[Item], canon: Canon, *, solver_name: str,
        run_id: str | None = None, model: str | None = None, provider: str | None = None,
        split: str | None = None, convention_filter: str | None = None) -> RunResult:
    rows = []
    for item in sorted(items, key=lambda i: i.id):
        raw: str | None = None
        error = None
        try:
            raw = solver(item)
        except Exception as exc:  # noqa: BLE001 - a crashing solver is a parse error
            error = f"solver raised {type(exc).__name__}: {exc}"
        rows.append(grade_response(item, raw, canon, error))
    splits = sorted({i.split for i in items})
    is_baseline = solver_name.split(":")[-1] in BASELINES
    return RunResult(
        run_id=run_id or default_run_id(solver_name),
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        model=model or solver_name,
        provider=provider or ("baseline" if is_baseline else "local"),
        solver=solver_name,
        bench_version=BENCH_VERSION,
        items_sha256=items_sha256(items),
        split=split or ",".join(splits),
        item_count=len(items),
        convention_filter=convention_filter,
        engine_commit=ENGINE_COMMIT,
        per_item=rows,
        summary=summarize(rows),
    )


def default_run_id(solver_name: str) -> str:
    safe = solver_name.replace(":", "-").replace(".", "_").replace("/", "_")
    if solver_name.split(":")[-1] in BASELINES:
        return f"baseline-{safe}"
    return f"{safe}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def write_result(result: RunResult, out_dir: str | Path) -> Path:
    path = Path(out_dir) / f"{result.run_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = result.model_dump(mode="json", exclude_none=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_result(path: str | Path) -> RunResult:
    return RunResult.model_validate_json(Path(path).read_text(encoding="utf-8"))
