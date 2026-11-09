"""``astro-bench`` commands for manual runs: pack, ingest (multi-file, resumable), status."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .canon import Canon
from .disclosure import complete, load_card, rel, resolve
from .io import load_items
from .manual import Manifest, PackError, ReplaySolver, slug, write_pack
from .progressive import (
    check_chunks,
    header_card,
    load_sidecar,
    merge,
    missing_by_chunk,
    read_header,
    sidecar_path,
    write_chunked_pack,
    write_sidecar,
)
from .runner import SampleInfo, load_result, run, write_result
from .sampling import ids_sha256, stratified_sample
from .schema import Item
from .score import format_summary

#: Placeholder brief for header-disclosed runs: the chunk files (via their manifest) are
#: the brief, so the manifest path is recorded.
HEADER_BRIEF = "<pack manifest>"


def _levels(text: str) -> list[int]:
    return sorted({int(x) for x in text.split(",") if x.strip()})


def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


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


def cmd_pack(args: argparse.Namespace) -> int:
    items = _filter(load_items(args.items), args)
    if not items:
        _log("no items selected")
        return 2
    keys = [k.strip() for k in args.stratify.split(",") if k.strip()]
    seed = None
    if args.sample:
        seed = args.sample_seed
        items = stratified_sample(items, args.sample, keys, seed)
    if args.chunk:
        manifest = write_chunked_pack(items, Path(args.out), chunk=args.chunk,
                                      input_mode=args.input_mode, sample_seed=seed,
                                      stratify=keys if args.sample else None)
    else:
        manifest = write_pack(items, Path(args.out), input_mode=args.input_mode,
                              fmt=args.format, sample_seed=seed,
                              stratify=keys if args.sample else None)
    print(f"wrote {args.out} ({len(items)} items, input mode {args.input_mode}) and {manifest}")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    if not (args.description or "").strip():
        _log("--description is required (harness, model, date)")
        return 2
    canon = Canon.load_or_empty(args.canon)
    manifest = Manifest.load(args.pack)
    run_id = args.run_id or f"manual-{slug(args.description)}"
    side = sidecar_path(args.out, run_id)
    previous = Path(args.out) / f"{run_id}.json"
    try:
        items = manifest.check(load_items(args.items))
        check_chunks(manifest)
        texts = [(Path(p).name, Path(p).read_text(encoding="utf-8")) for p in args.replies]
        merged = merge(load_sidecar(side), texts)
        card = _ingest_card(args, texts, manifest, previous)
    except PackError as exc:
        _log(f"refused: {exc}")
        return 2
    if merged.conflicts:
        for line in merged.conflicts:
            _log(f"conflict: {line}")
        _log(f"refused: {len(merged.conflicts)} ids have differing answers")
        return 2
    extra = sorted(set(merged.replies) - set(manifest.ids))
    if extra:
        _log(f"refused: {len(extra)} reply ids are not in the pack, e.g. {extra[0]}")
        return 2
    sample = SampleInfo(manifest.data.get("sample_seed"), len(items), ids_sha256(items))
    result = run(ReplaySolver(merged.replies), items, canon,
                 solver_name=f"manual:{slug(args.description)}", kind=args.kind,
                 description=args.description, input_mode=manifest.data["input_mode"],
                 run_id=run_id, model=args.model, provider="manual", sample=sample)
    result.missing_ids = [i for i in manifest.ids if i not in merged.replies]
    result.answered_n = len(manifest.ids) - len(result.missing_ids)
    result.status = "partial" if result.missing_ids else "complete"
    result.pack_manifest = rel(manifest.path)
    write_sidecar(side, merged, manifest.ids)
    pack = manifest.path.with_name(manifest.data["pack"]) if manifest.data.get("pack") \
        else manifest.path
    from_header = card.get("brief_path") == HEADER_BRIEF
    result.disclosure = complete(card, result, replies=side,
                                 pack=pack if pack.exists() else None,
                                 brief=manifest.path if from_header else None)
    if not result.disclosure.pack_sha256:
        result.disclosure.pack_sha256 = manifest.data["pack_sha256"]
    path = write_result(result, args.out)
    print(f"{path}: {result.status}, {result.answered_n}/{len(manifest.ids)} answered, "
          f"{len(result.missing_ids)} missing (scored as parse errors)")
    print(format_summary(result.summary))
    return 0


def _ingest_card(args: argparse.Namespace, texts: list[tuple[str, str]], manifest: Manifest,
                 previous: Path) -> dict[str, Any]:
    """--disclosure, else the filled header of the first reply file, else the previous run's."""
    if args.disclosure:
        return load_card(args.disclosure)
    header = read_header(texts[0][1]) if texts else {}
    if header:
        return header_card(header, HEADER_BRIEF)
    if previous.exists():
        old = load_result(previous).disclosure
        if old is not None:
            keep = {"sample", "replies_sha256", "pack_sha256", "input_mode", "engine_commit"}
            card = old.model_dump(exclude=keep)
            if card.get("brief_path") == rel(manifest.path):
                card["brief_path"] = HEADER_BRIEF  # the pack was the brief
            return card
    raise PackError("no disclosure: fill the header at the top of the first reply file, "
                    "or pass --disclosure card.yaml (ADR-002)")


def cmd_status(args: argparse.Namespace) -> int:
    path = Path(args.out) / f"{args.run_id}.json"
    if not path.exists():
        _log(f"no result {path}")
        return 2
    result = load_result(path)
    total = result.item_count
    answered = result.answered_n if result.answered_n is not None else total
    print(f"{result.run_id}: {result.status}, {answered}/{total} answered")
    if not result.missing_ids:
        return 0
    manifest: dict[str, Any] = {"ids": result.missing_ids, "pack": None}
    candidates = [Path(args.pack)] if args.pack else []
    if result.pack_manifest:
        candidates += [resolve(result.pack_manifest), Path(result.pack_manifest)]
    for candidate in candidates:
        if candidate.exists():
            manifest = json.loads(candidate.read_text(encoding="utf-8"))
            break
    for chunk, ids in missing_by_chunk(manifest, result.missing_ids):
        print(f"{chunk}: {len(ids)} missing: {', '.join(ids)}")
    return 0


