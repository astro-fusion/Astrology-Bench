"""Summaries: accuracy with Wilson intervals, citation score, fabrication, calibration."""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Callable, Sequence

import numpy as np

from .schema import PerItem, Stat, Summary

Z95 = 1.959963984540054


def wilson(successes: float, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval for a proportion (``successes`` may be fractional)."""
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))


def brier(confidence: Sequence[float], outcome: Sequence[float]) -> float | None:
    """Mean squared error of confidence against the answer score (0 = perfect)."""
    if not confidence:
        return None
    c, o = np.asarray(confidence, float), np.asarray(outcome, float)
    return float(np.mean((c - o) ** 2))


def ece(confidence: Sequence[float], outcome: Sequence[float], bins: int = 10) -> float | None:
    """Expected calibration error with ``bins`` equal-width confidence bins."""
    if not confidence:
        return None
    c, o = np.asarray(confidence, float), np.asarray(outcome, float)
    idx = np.minimum((c * bins).astype(int), bins - 1)
    total = 0.0
    for b in range(bins):
        mask = idx == b
        if mask.any():
            total += float(mask.sum()) / len(c) * abs(float(c[mask].mean() - o[mask].mean()))
    return total


def _r(x: float | None) -> float | None:
    return None if x is None else round(x, 4)


def stat(rows: Sequence[PerItem]) -> Stat:
    n = len(rows)
    acc = sum(r.answer_score for r in rows) / n if n else 0.0
    graded = [r for r in rows if r.citation_score is not None]
    cited = [r for r in rows if r.confidence is not None and not r.parse_error]
    conf = [float(r.confidence) for r in cited if r.confidence is not None]
    out = [r.answer_score for r in cited]
    return Stat(
        n=n,
        answer_acc=round(acc, 4),
        answer_ci=wilson(acc * n, n),
        citation_n=len(graded),
        citation_mean=_r(sum(r.citation_score or 0 for r in graded) / len(graded))
        if graded else None,
        fabricated_rate=_r(sum(r.fabricated for r in graded) / len(graded)) if graded else None,
        parse_error_rate=round(sum(r.parse_error for r in rows) / n, 4) if n else 0.0,
        brier=_r(brier(conf, out)),
        ece=_r(ece(conf, out)),
    )


def _group(rows: Sequence[PerItem], key: Callable[[PerItem], str]) -> dict[str, Stat]:
    groups: dict[str, list[PerItem]] = defaultdict(list)
    for r in rows:
        groups[key(r)].append(r)
    return {k: stat(v) for k, v in sorted(groups.items())}


def summarize(rows: Sequence[PerItem]) -> Summary:
    return Summary(
        overall=stat(rows),
        by_level=_group(rows, lambda r: str(r.level)),
        by_task=_group(rows, lambda r: r.task),
        by_source=_group(rows, lambda r: r.source),
        by_convention=_group(rows, lambda r: r.convention),
        by_tier=_group(rows, lambda r: r.tier),
    )


def format_summary(summary: Summary) -> str:
    """Plain-text table of a summary, one block per axis."""
    lines = []
    header = f"{'group':<34}{'n':>6}{'acc':>8}{'95% CI':>18}{'cite':>8}{'fab':>7}" \
             f"{'parse':>7}{'brier':>8}"
    for axis, groups in [("overall", {"all": summary.overall}), ("level", summary.by_level),
                         ("task", summary.by_task), ("source", summary.by_source),
                         ("convention", summary.by_convention), ("tier", summary.by_tier)]:
        lines += [f"== {axis}", header]
        for name, s in groups.items():
            ci = f"[{s.answer_ci[0]:.3f}, {s.answer_ci[1]:.3f}]"
            lines.append(
                f"{name:<34}{s.n:>6}{s.answer_acc:>8.3f}{ci:>18}{_f(s.citation_mean):>8}"
                f"{_f(s.fabricated_rate):>7}{s.parse_error_rate:>7.3f}{_f(s.brier):>8}"
            )
    return "\n".join(lines)


def _f(x: float | None) -> str:
    return "-" if x is None else f"{x:.3f}"
