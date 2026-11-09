"""Run a solver over items: call, parse, grade, summarise."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePath
from typing import Any

from . import BENCH_VERSION, ENGINE_COMMIT
from .canon import Canon
from .ephemeris import EPHE_SET_SHA256, configure
from .graders import grade_answer, grade_citations
from .io import items_sha256
from .parse import ParseError, parse_response
from .redact import to_solver_item
from .schema import DESCRIBED_KINDS, DISCLOSED_KINDS, InputMode, Item, PerItem, RunResult
from .score import summarize
from .solvers import BASELINES, NoChartSolver, Solver, default_kind


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


def call_solver(solver: Solver, item: Item, input_mode: InputMode) -> str:
    """Hand the solver the redacted view; only a runner-built ``full_item`` solver
    (the engine oracle) gets the full item (ADR-002)."""
    if getattr(solver, "full_item", False) and not isinstance(solver, NoChartSolver):
        return solver(item)  # type: ignore[arg-type]
    return solver(to_solver_item(item, input_mode))


@dataclass(frozen=True)
class SampleInfo:
    seed: int | None
    n: int
    ids_sha256: str


def run(solver: Solver, items: Sequence[Item], canon: Canon, *, solver_name: str,
        kind: str | None = None, description: str = "", input_mode: InputMode = "chart",
        run_id: str | None = None, model: str | None = None, provider: str | None = None,
        split: str | None = None, convention_filter: str | None = None,
        sample: SampleInfo | None = None) -> RunResult:
    solver_name = public_solver_name(solver_name)
    kind = kind or default_kind(solver_name)
    if kind is None:
        raise ValueError(f"solver {solver_name!r} needs an explicit kind")
    rows = []
    for item in sorted(items, key=lambda i: i.id):
        raw: str | None = None
        error = None
        try:
            raw = call_solver(solver, item, input_mode)
        except Exception as exc:  # noqa: BLE001 - a crashing solver is a parse error
            error = f"solver raised {type(exc).__name__}: {exc}"
        rows.append(grade_response(item, raw, canon, error))
    splits = sorted({i.split for i in items})
    is_baseline = kind in ("oracle", "baseline")
    return RunResult(
        run_id=run_id or default_run_id(solver_name, input_mode),
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        model=model or solver_name,
        provider=provider or ("baseline" if is_baseline else "local"),
        solver=solver_name,
        kind=kind,  # type: ignore[arg-type]
        solver_description=description,
        ablation="nochart" if solver_name.startswith("nochart:") else None,
        input_mode=input_mode,
        sample_seed=sample.seed if sample else None,
        sample_n=sample.n if sample else None,
        sample_ids_sha256=sample.ids_sha256 if sample else None,
        ephemeris_model=configure(),
        ephe_sha256=EPHE_SET_SHA256,
        bench_version=BENCH_VERSION,
        items_sha256=items_sha256(items),
        split=split or ",".join(splits),
        item_count=len(items),
        convention_filter=convention_filter,
        engine_commit=ENGINE_COMMIT,
        per_item=rows,
        summary=summarize(rows),
    )


def public_solver_name(name: str) -> str:
    """The solver name as recorded in results: ``http_json:<config path>`` becomes
    ``http_json:<config basename without extension>`` (also inside ``nochart:``), so no
    local filesystem path is ever written to a result file."""
    if name.startswith("nochart:"):
        return "nochart:" + public_solver_name(name.split(":", 1)[1])
    if name.startswith("http_json:"):
        return "http_json:" + PurePath(name.split(":", 1)[1].replace("\\", "/")).stem
    return name


def default_run_id(solver_name: str, input_mode: str = "chart") -> str:
    safe = solver_name.replace(":", "-").replace(".", "_").replace("/", "_")
    if input_mode != "chart":
        safe = f"{safe}-{input_mode}"
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


def check_result(result: RunResult) -> list[str]:
    """Problems that make a result unreportable (ADR-002)."""
    problems = []
    if result.kind in DESCRIBED_KINDS and not result.solver_description.strip():
        problems.append(f"kind {result.kind} needs a non-empty solver_description")
    if result.kind in DISCLOSED_KINDS:
        d = result.disclosure
        if d is None:
            problems.append(f"kind {result.kind} needs a disclosure block (ADR-002)")
        elif d.input_mode != result.input_mode:
            problems.append("disclosure input_mode differs from the run's input_mode")
        elif result.sample_ids_sha256 and (d.sample is None
                                           or d.sample.ids_sha256 != result.sample_ids_sha256):
            problems.append("disclosure sample differs from the run's sample")
    return problems
