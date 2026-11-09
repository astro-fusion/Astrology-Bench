"""Disclosure blocks, per-run cards and the ``runs/`` index (ADR-002 decision 7).

Every published row of kind model, system, app_tools or system_ui carries a disclosure
block: the harness, the exact model id, the effort setting (recorded even when unknown),
whether tools were allowed and which were used, the operator and date, the input mode,
the sample, the sha256 of the pack and of the raw replies, and paths to the verbatim
brief and the agent's own report. The block's source is ``runs/<run_id>/disclosure.yaml``;
the computed fields (hashes, sample, input mode, engine commit) are filled in here.
"""

from __future__ import annotations

import hashlib
import posixpath
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import yaml

from .generators.common import repo_root
from .schema import Disclosure, DisclosureSample, RunResult, Stat

DISCLOSURE_FILE = "disclosure.yaml"
CARD_FILE = "CARD.md"


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rel(path: str | Path, root: Path | None = None) -> str:
    """A repository-relative posix path; never an absolute local path."""
    base = (root or repo_root()).resolve()
    p = Path(path)
    resolved = (p if p.is_absolute() else Path.cwd() / p).resolve()
    try:
        return resolved.relative_to(base).as_posix()
    except ValueError:
        return p.name


def resolve(path: str, root: Path | None = None) -> Path:
    return (root or repo_root()) / path


def complete(card: dict[str, Any], result: RunResult, *, root: Path | None = None,
             replies: str | Path | None = None, pack: str | Path | None = None,
             brief: str | Path | None = None) -> Disclosure:
    """Fill the computed fields of a disclosure card from the run and the files."""
    data = dict(card)
    data["input_mode"] = result.input_mode
    data["engine_commit"] = result.engine_commit
    if result.sample_n is not None and result.sample_ids_sha256:
        data["sample"] = DisclosureSample(n=result.sample_n, seed=result.sample_seed,
                                          ids_sha256=result.sample_ids_sha256)
    given = {"replies": replies, "pack": pack}
    for key in ("replies", "pack"):
        source = given[key]
        if source is not None:  # hash the file given, record a repo-relative path
            data[f"{key}_path"] = rel(source, root)
            data[f"{key}_sha256"] = sha256_file(source)
        elif data.get(f"{key}_path"):
            data[f"{key}_sha256"] = sha256_file(resolve(data[f"{key}_path"], root))
    if brief is not None:  # an existing file given directly (e.g. the chunk manifest)
        data["brief_path"] = rel(brief, root)
    for key in ("brief_path", "agent_report_path"):
        if key == "brief_path" and brief is not None:
            continue
        if data.get(key) and not resolve(data[key], root).exists():
            raise FileNotFoundError(f"{key} {data[key]} does not exist")
    return Disclosure.model_validate(data)


def load_card(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: a disclosure card is a YAML mapping")
    return data


# --------------------------------------------------------------------------- cards


def _pct(x: float | None) -> str:
    return "-" if x is None else f"{100 * x:.1f}%"


def _num(x: float | None, signed: bool = False) -> str:
    if x is None:
        return "-"
    return f"{x:+.3f}" if signed else f"{x:.3f}"


def _table(title: str, groups: dict[str, Stat]) -> list[str]:
    lines = [f"| {title} | n | answer acc [95% CI] | citation score | fabricated | "
             "parse errors | Brier |", "|---|---|---|---|---|---|---|"]
    for name, s in groups.items():
        acc = f"{100 * s.answer_acc:.1f}% [{100 * s.answer_ci[0]:.1f}, {100 * s.answer_ci[1]:.1f}]"
        lines.append(f"| {name} | {s.n} | {acc} | {_num(s.citation_mean, True)} | "
                     f"{_pct(s.fabricated_rate)} | {_pct(s.parse_error_rate)} | {_num(s.brier)} |")
    return lines


def _link(path: str | None, run_dir: str) -> str:
    if not path:
        return "-"
    return f"[`{path}`]({posixpath.relpath(path, run_dir)})"


def render_card(result: RunResult) -> str:
    d = result.disclosure
    if d is None:
        raise ValueError(f"{result.run_id} has no disclosure block")
    run_dir = f"runs/{result.run_id}"
    tools = "unknown" if d.tools_used == "unknown" else (", ".join(d.tools_used) or "none")
    sample = (f"{d.sample.n} items, seed {d.sample.seed}, ids sha256 `{d.sample.ids_sha256}`"
              if d.sample else f"full split ({result.item_count} items)")
    rows = [
        ("Run id", f"`{result.run_id}`"), ("Kind", result.kind),
        ("Status", result.status if result.status == "complete" else
         f"partial: {result.answered_n}/{result.item_count} answered, not ranked"),
        ("Harness", d.harness),
        ("Model id", f"`{d.model_id}`"), ("Model name", d.model_name), ("Effort", d.effort),
        ("Tools allowed", "yes" if d.tools_allowed else "no"), ("Tools used", tools),
        ("Operator", d.operator), ("Date", d.date), ("Input mode", d.input_mode),
        ("Sample", sample), ("Split", result.split),
        ("Bench version", result.bench_version),
        ("Engine commit", f"`{d.engine_commit or result.engine_commit}`"),
        ("Items sha256", f"`{result.items_sha256}`"),
        ("Pack", _link(d.pack_path, run_dir)),
        ("Pack sha256", f"`{d.pack_sha256}`" if d.pack_sha256 else "-"),
        ("Raw replies", _link(d.replies_path, run_dir)),
        ("Replies sha256", f"`{d.replies_sha256}`" if d.replies_sha256 else "-"),
        ("Brief (verbatim)", _link(d.brief_path, run_dir)),
        ("Agent report (verbatim)", _link(d.agent_report_path, run_dir)),
        ("Result file", f"[`results/{result.run_id}.json`](../../results/{result.run_id}.json)"),
    ]
    s = result.summary.overall
    lines = [
        f"# {result.run_id}",
        "",
        "Generated by `astro-bench cards` from the result's disclosure block; do not edit "
        f"by hand (edit `{run_dir}/{DISCLOSURE_FILE}` and re-run).",
        "",
        f"**Overall:** answer accuracy {100 * s.answer_acc:.1f}% "
        f"[{100 * s.answer_ci[0]:.1f}, {100 * s.answer_ci[1]:.1f}] on {s.n} items; citation "
        f"score {_num(s.citation_mean, True)} on {s.citation_n} graded items; fabricated "
        f"{_pct(s.fabricated_rate)}; parse errors {_pct(s.parse_error_rate)}.",
        "",
        "## Disclosure",
        "",
        "| Field | Value |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in rows],
        "",
        "## Deviations from the brief",
        "",
        *([f"- {x}" for x in d.deviations] or ["None recorded."]),
        "",
    ]
    if d.notes:
        lines += ["## Notes", "", d.notes.strip(), ""]
    lines += ["## Results by level", "", *_table("level", result.summary.by_level), "",
              "## Results by task", "", *_table("task", result.summary.by_task), ""]
    return "\n".join(lines)


def render_index(results: Sequence[RunResult]) -> str:
    lines = [
        "# Disclosed runs",
        "",
        "Every published row of kind model, system, app_tools or system_ui, with its card "
        "(ADR-002 decision 7). Each card links the verbatim brief, the agent's own report and "
        "the raw replies, with their sha256. Generated by `astro-bench cards`.",
        "",
        "| run id | kind | harness | model | effort | tools | date | answer acc | "
        "citation score | fabricated | card |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in sorted(results, key=lambda r: r.run_id):
        d = r.disclosure
        if d is None:
            continue
        s = r.summary.overall
        used = "unknown" if d.tools_used == "unknown" else (", ".join(d.tools_used) or "none")
        tools = ("allowed: " if d.tools_allowed else "not allowed: ") + used
        lines.append(
            f"| `{r.run_id}` | {r.kind} | {d.harness} | `{d.model_id}` | {d.effort} | {tools} "
            f"| {d.date} | {_pct(s.answer_acc)} | {_num(s.citation_mean, True)} | "
            f"{_pct(s.fabricated_rate)} | [CARD]({r.run_id}/{CARD_FILE}) |")
    return "\n".join(lines) + "\n"


def write_cards(results: Sequence[RunResult], runs_dir: str | Path) -> list[Path]:
    out = Path(runs_dir)
    written = []
    disclosed = [r for r in results if r.disclosure is not None]
    for result in disclosed:
        path = out / result.run_id / CARD_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_card(result), encoding="utf-8")
        written.append(path)
    index = out / "README.md"
    index.write_text(render_index(disclosed), encoding="utf-8")
    written.append(index)
    return written
