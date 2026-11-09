"""``astro-bench`` command line (ADR-001 §CLI)."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from . import BENCH_VERSION, DEV_SEED, ENGINE_COMMIT
from .canon import Canon
from .cli_manual import _filter, _levels, _log, cmd_ingest, cmd_pack, cmd_status
from .disclosure import complete, load_card, write_cards
from .generators import generate_items
from .generators.common import repo_root
from .io import item_files, items_sha256, load_items, write_items
from .leaderboard import load_results, write_leaderboard
from .runner import SampleInfo, check_result, load_result, run, write_result
from .sampling import ids_sha256, stratified_sample
from .schema import DESCRIBED_KINDS, Item
from .score import format_summary, summarize
from .solvers import default_kind, get_solver

SOLVER_KINDS = ["oracle", "baseline", "model", "system", "app_tools", "system_ui"]

TEST_SEED_ENV = "ASTRO_BENCH_TEST_SEED"


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------- generate


def cmd_generate(args: argparse.Namespace) -> int:
    canon = Canon.load_or_empty(args.canon)
    root = repo_root()
    if args.split == "test":
        raw_seed = os.environ.get(TEST_SEED_ENV)
        if not raw_seed:
            _log(f"--split test needs the seed in ${TEST_SEED_ENV} (never committed)")
            return 2
        if not args.out or _inside(Path(args.out), root):
            _log("--split test needs --out pointing OUTSIDE the repository")
            return 2
        seed = int(raw_seed)
    else:
        seed = args.seed
    out = Path(args.out or "items")
    items = generate_items(
        levels=_levels(args.level), split=args.split, seed=seed, canon=canon,
        n_default=args.n_per_task, n_other=args.n_per_cell,
        rules_dir=Path(args.rules) if args.rules else None,
        places_path=Path(args.places) if args.places else None,
        tasks=args.task.split(",") if args.task else None, log=_log,
    )
    for level in _levels(args.level):
        for stale in sorted((out / f"level{level}").glob("*.jsonl")):
            stale.unlink()
    counts = write_items(items, out)
    for rel, n in counts.items():
        print(f"{n:6d}  {out / rel}")
    print(f"{len(items):6d}  total (split {args.split}, canon entries {len(canon)})")
    if args.split == "test":
        manifest = write_manifest(items, out, counts, Path(args.manifests))
        print(f"manifest: {manifest}")
    return 0


def write_manifest(items: Sequence[Item], out: Path, counts: dict[str, int],
                   manifests_dir: Path) -> Path:
    lines = [f"# Astro-Bench hidden test split; bench {BENCH_VERSION}; engine {ENGINE_COMMIT}",
             "# <sha256>  <count>  <file>; ALL = items_sha256 over every item (sorted by id)",
             f"{items_sha256(items)}  {len(items)}  ALL"]
    for rel, n in counts.items():
        digest = hashlib.sha256((out / rel).read_bytes()).hexdigest()
        lines.append(f"{digest}  {n}  {rel}")
    manifests_dir.mkdir(parents=True, exist_ok=True)
    path = manifests_dir / f"test-{BENCH_VERSION}.sha256"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------- validate


def validate_items(items: Sequence[Item], canon: Canon, in_repo: bool) -> list[str]:
    problems = []
    dupes = [k for k, n in Counter(i.id for i in items).items() if n > 1]
    problems += [f"duplicate id {d}" for d in dupes]
    for item in items:
        if in_repo and item.split == "test":
            problems.append(f"{item.id}: split test must never be committed")
        if len(canon) and any(canon.entry(c) is None for c in item.canon_ids):
            problems.append(f"{item.id}: canon_ids not in canon: {item.canon_ids}")
        if item.level == 1 and item.input.chart is None:
            problems.append(f"{item.id}: Level 1 item without chart")
        if item.level == 0 and item.input.chart is not None:
            problems.append(f"{item.id}: Level 0 item must not carry a chart")
        gold = item.gold.answer
        if item.answer_type == "category" and isinstance(gold, str) and item.choices \
                and gold not in item.choices:
            problems.append(f"{item.id}: gold {gold!r} not among choices")
    return problems


def cmd_validate(args: argparse.Namespace) -> int:
    canon = Canon.load_or_empty(args.canon)
    files = item_files(args.path)
    items = load_items(args.path)
    problems = validate_items(items, canon, _inside(Path(args.path), repo_root()))
    for p in problems:
        print(f"ERROR {p}")
    by = Counter((i.level, i.task) for i in items)
    for (level, task), n in sorted(by.items()):
        print(f"L{level} {task:<12}{n:6d}")
    print(f"{len(items)} items in {len(files)} files; {len(problems)} problems")
    return 1 if problems else 0


# --------------------------------------------------------------------------- run / score


def cmd_run(args: argparse.Namespace) -> int:
    canon = Canon.load_or_empty(args.canon)
    items = _filter(load_items(args.items), args)
    if not items:
        _log("no items selected")
        return 2
    kind = args.kind or default_kind(args.solver)
    if kind is None:
        _log(f"--kind is required for solver {args.solver!r} "
             f"(one of {', '.join(SOLVER_KINDS)})")
        return 2
    if kind in DESCRIBED_KINDS and not (args.description or "").strip():
        _log(f"--kind {kind} needs a non-empty --description (model, tools, retrieval, version)")
        return 2
    sample = None
    if args.sample:
        keys = [k.strip() for k in args.stratify.split(",") if k.strip()]
        items = stratified_sample(items, args.sample, keys, args.sample_seed)
        sample = SampleInfo(args.sample_seed, len(items), ids_sha256(items))
    solver = get_solver(args.solver, items, canon)
    result = run(solver, items, canon, solver_name=args.solver, kind=kind,
                 description=args.description or "", input_mode=args.input_mode,
                 run_id=args.run_id, model=args.model, provider=args.provider,
                 convention_filter=args.convention, sample=sample)
    if args.disclosure:
        result.disclosure = complete(load_card(args.disclosure), result)
    path = write_result(result, args.out)
    s = result.summary.overall
    print(f"{path}: n={s.n} acc={s.answer_acc:.3f} cite={s.citation_mean} "
          f"fab={s.fabricated_rate} parse_err={s.parse_error_rate:.3f}")
    return 0


def cmd_disclose(args: argparse.Namespace) -> int:
    """Attach a disclosure block to an existing result; scores are not touched."""
    result = load_result(args.result)
    result.disclosure = complete(load_card(args.disclosure), result, replies=args.replies,
                                 pack=args.pack)
    path = Path(args.result)
    path.write_text(json.dumps(result.model_dump(mode="json", exclude_none=True), indent=1,
                               ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"disclosure added to {path}")
    return 0


def cmd_cards(args: argparse.Namespace) -> int:
    written = write_cards(load_results(args.results), args.runs)
    for path in written:
        print(f"wrote {path}")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    result = load_result(args.result)
    problems = check_result(result)
    for problem in problems:
        print(f"REJECTED {result.run_id}: {problem}")
    if problems:
        return 1
    summary = summarize(result.per_item)
    print(f"{result.run_id}: solver {result.solver} ({result.kind}"
          f"{', ablation ' + result.ablation if result.ablation else ''}), input mode "
          f"{result.input_mode}, split {result.split}, {result.item_count} items, "
          f"items sha256 {result.items_sha256}")
    if result.solver_description:
        print(f"description: {result.solver_description}")
    if result.sample_n is not None:
        print(f"sample: n={result.sample_n} seed={result.sample_seed} "
              f"ids sha256 {result.sample_ids_sha256}")
    if result.split == "test":
        known = any(result.items_sha256 in p.read_text(encoding="utf-8")
                    for p in Path(args.manifests).glob("test-*.sha256"))
        print("hidden split manifest: " + ("MATCH" if known else "NO MATCH"))
    print(format_summary(summary))
    return 0


def cmd_leaderboard(args: argparse.Namespace) -> int:
    path = write_leaderboard(args.results, args.out, args.items)
    print(f"wrote {path}")
    return 0


# --------------------------------------------------------------------------- parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="astro-bench", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("generate", help="generate Level 0-2 items")
    g.add_argument("--level", default="0,1,2", help="comma list of levels (default 0,1,2)")
    g.add_argument("--split", choices=["dev", "test"], default="dev")
    g.add_argument("--seed", type=int, default=DEV_SEED, help=f"dev seed (default {DEV_SEED})")
    g.add_argument("--n-per-task", type=int, default=40,
                   help="items per task in the default convention cell (default 40)")
    g.add_argument("--n-per-cell", type=int, default=10,
                   help="items per task in every other convention cell (default 10)")
    g.add_argument("--task", help="comma list of tasks to generate (default all)")
    g.add_argument("--out", help="output dir (default items/; test split: outside the repo)")
    g.add_argument("--canon", default="canon", help="canon directory (default canon/)")
    g.add_argument("--rules", help="rules directory (default vendor/rules)")
    g.add_argument("--places", help="places YAML (default scripts/places.yaml)")
    g.add_argument("--manifests", default="manifests", help="manifest dir for --split test")
    g.set_defaults(func=cmd_generate)

    v = sub.add_parser("validate", help="validate item files")
    v.add_argument("path", nargs="?", default="items")
    v.add_argument("--canon", default="canon")
    v.set_defaults(func=cmd_validate)

    r = sub.add_parser("run", help="run a solver over items and write results/<run_id>.json")
    r.add_argument("--solver", required=True,
                   help="oracle|random|constant|mock|nochart:<solver>|http_json:<config.yaml>|"
                        "package.module:callable")
    r.add_argument("--kind", choices=SOLVER_KINDS,
                   help="required except for oracle (oracle) and random/constant/mock (baseline)")
    r.add_argument("--description", help="what the solver is (model, tools, retrieval, app "
                   "version); required for system, app_tools and system_ui")
    r.add_argument("--input-mode", choices=["chart", "birth"], default="chart",
                   help="chart (default): positions table; birth: birth data only "
                        "(Level 0 is always birth)")
    r.add_argument("--sample", type=int, help="run a reproducible stratified subset of N items")
    r.add_argument("--stratify", default="task,level",
                   help="comma list of task, level, tier, source, convention (default task,level)")
    r.add_argument("--sample-seed", type=int, default=0, help="sampling seed (default 0)")
    r.add_argument("--items", default="items")
    r.add_argument("--out", default="results")
    r.add_argument("--canon", default="canon")
    r.add_argument("--level")
    r.add_argument("--task")
    r.add_argument("--convention", help="e.g. lahiri/mean/whole_sign")
    r.add_argument("--disclosure", help="disclosure card YAML (required by score for model, "
                   "system, app_tools and system_ui)")
    r.add_argument("--run-id")
    r.add_argument("--model")
    r.add_argument("--provider")
    r.set_defaults(func=cmd_run)

    p = sub.add_parser("pack", help="write a prompt pack for a manual or IDE-agent run")
    p.add_argument("--items", default="items")
    p.add_argument("--out", required=True, help="pack file, e.g. pack.md")
    p.add_argument("--format", choices=["md", "jsonl"], default="md")
    p.add_argument("--input-mode", choices=["chart", "birth"], default="chart")
    p.add_argument("--sample", type=int, help="reproducible stratified subset of N items")
    p.add_argument("--stratify", default="task,level")
    p.add_argument("--sample-seed", type=int, default=0)
    p.add_argument("--chunk", type=int, help="split into self-contained files of this many "
                   "items (--out is then a directory)")
    p.add_argument("--ids", help="only these ids (comma list or file); needs --manifest")
    p.add_argument("--manifest", help="existing pack manifest the --ids come from")
    p.add_argument("--level")
    p.add_argument("--task")
    p.add_argument("--convention")
    p.set_defaults(func=cmd_pack)

    ing = sub.add_parser("ingest", help="score the replies to a prompt pack")
    ing.add_argument("--pack", required=True, help="the pack's .manifest.json")
    ing.add_argument("--replies", required=True, action="append",
                     help="'### <id>' blocks each followed by a JSON object, "
                          "or JSONL {id, response}")
    ing.add_argument("--kind", choices=["model", "system", "system_ui"], required=True)
    ing.add_argument("--description", required=True, help="harness, model and date")
    ing.add_argument("--items", default="items")
    ing.add_argument("--canon", default="canon")
    ing.add_argument("--out", default="results")
    ing.add_argument("--disclosure", help="disclosure card YAML; default: the filled header "
                     "of the first reply file, then the previous ingest of this run id")
    ing.add_argument("--run-id")
    ing.add_argument("--model")
    ing.set_defaults(func=cmd_ingest)

    st = sub.add_parser("status", help="answered and missing ids of a manual run, by chunk")
    st.add_argument("--run-id", required=True)
    st.add_argument("--out", default="results")
    st.add_argument("--pack", help="the pack manifest (default: the one recorded at ingest)")
    st.set_defaults(func=cmd_status)

    dc = sub.add_parser("disclose", help="attach a disclosure card to a result file")
    dc.add_argument("result")
    dc.add_argument("--disclosure", required=True)
    dc.add_argument("--replies", help="raw replies file (hashed)")
    dc.add_argument("--pack", help="prompt pack file (hashed)")
    dc.set_defaults(func=cmd_disclose)

    cd = sub.add_parser("cards", help="render runs/<run_id>/CARD.md and runs/README.md")
    cd.add_argument("--results", default="results")
    cd.add_argument("--runs", default="runs")
    cd.set_defaults(func=cmd_cards)

    s = sub.add_parser("score", help="print the summary of a results file")
    s.add_argument("result")
    s.add_argument("--manifests", default="manifests")
    s.set_defaults(func=cmd_score)

    lb = sub.add_parser("leaderboard", help="render LEADERBOARD.md from results/")
    lb.add_argument("--results", default="results")
    lb.add_argument("--out", default="LEADERBOARD.md")
    lb.add_argument("--items", default="items",
                    help="current split; rows scored on other items are listed as older split")
    lb.set_defaults(func=cmd_leaderboard)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
