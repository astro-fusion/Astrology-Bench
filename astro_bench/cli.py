"""``astro-bench`` command line (ADR-001 §CLI)."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from . import BENCH_VERSION, DEV_SEED, ENGINE_COMMIT
from .canon import Canon
from .generators import generate_items
from .generators.common import repo_root
from .io import item_files, items_sha256, load_items, write_items
from .leaderboard import write_leaderboard
from .runner import load_result, run, write_result
from .schema import Item
from .score import format_summary, summarize
from .solvers import get_solver

TEST_SEED_ENV = "ASTRO_BENCH_TEST_SEED"


def _levels(text: str) -> list[int]:
    return sorted({int(x) for x in text.split(",") if x.strip()})


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


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


def _filter(items: list[Item], args: argparse.Namespace) -> list[Item]:
    if args.level:
        levels = set(_levels(args.level))
        items = [i for i in items if i.level in levels]
    if args.task:
        tasks = set(args.task.split(","))
        items = [i for i in items if i.task in tasks]
    if args.convention:
        items = [i for i in items if i.convention.key == args.convention]
    return items


def cmd_run(args: argparse.Namespace) -> int:
    canon = Canon.load_or_empty(args.canon)
    items = _filter(load_items(args.items), args)
    if not items:
        _log("no items selected")
        return 2
    solver = get_solver(args.solver, items, canon)
    result = run(solver, items, canon, solver_name=args.solver, run_id=args.run_id,
                 model=args.model, provider=args.provider, convention_filter=args.convention)
    path = write_result(result, args.out)
    s = result.summary.overall
    print(f"{path}: n={s.n} acc={s.answer_acc:.3f} cite={s.citation_mean} "
          f"fab={s.fabricated_rate} parse_err={s.parse_error_rate:.3f}")
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    result = load_result(args.result)
    summary = summarize(result.per_item)
    print(f"{result.run_id}: solver {result.solver}, split {result.split}, "
          f"{result.item_count} items, items sha256 {result.items_sha256}")
    if result.split == "test":
        known = any(result.items_sha256 in p.read_text(encoding="utf-8")
                    for p in Path(args.manifests).glob("test-*.sha256"))
        print("hidden split manifest: " + ("MATCH" if known else "NO MATCH"))
    print(format_summary(summary))
    return 0


def cmd_leaderboard(args: argparse.Namespace) -> int:
    path = write_leaderboard(args.results, args.out)
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
                   help="oracle|random|constant|mock|nochart:<solver>|package.module:callable")
    r.add_argument("--items", default="items")
    r.add_argument("--out", default="results")
    r.add_argument("--canon", default="canon")
    r.add_argument("--level")
    r.add_argument("--task")
    r.add_argument("--convention", help="e.g. lahiri/mean/whole_sign")
    r.add_argument("--run-id")
    r.add_argument("--model")
    r.add_argument("--provider")
    r.set_defaults(func=cmd_run)

    s = sub.add_parser("score", help="print the summary of a results file")
    s.add_argument("result")
    s.add_argument("--manifests", default="manifests")
    s.set_defaults(func=cmd_score)

    lb = sub.add_parser("leaderboard", help="render LEADERBOARD.md from results/")
    lb.add_argument("--results", default="results")
    lb.add_argument("--out", default="LEADERBOARD.md")
    lb.set_defaults(func=cmd_leaderboard)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
