# Changelog

## 2.0.0 (unreleased)

Rewrite. Astro-Bench is now a Python benchmark matrix (levels, tasks, sources,
conventions, tiers, splits). See `docs/adr/ADR-001-open-benchmark-matrix.md`.

- Gold for Levels 0 and 1 comes from the pinned `vedic-astrology-core` engine, validated
  against 24 golden charts (PyJHora) and a JPL Horizons cross-check.
- Items for Levels 0, 1 and 2 are generated with recorded seeds and balanced.
- Level 2 grades citations against `canon/`, with fabrication scored -1, no citation 0
  and a correct citation +1.
- Calibration scores (Brier, ECE) and Wilson 95% intervals are reported.
- Baselines in CI: oracle, random, constant, mock, nochart.
- `inspect_ai` tasks, one per level, to run any supported provider.
- Hidden test split with committed hash manifests.
- The 32 v1 items move to `items/judgment/seed/legacy_v1.jsonl` as `needs_review`. Four
  carry review notes.
- Level 3 is a seed set awaiting three raters. Level 4 is schema only.
- The v1 TypeScript runner is removed.

## 1.0.0

Retired. The first version was a TypeScript runner with 32 hand-written items scored on
a 1-to-5 scale and a mock agent as the only built-in solver. Its answers had no oracle,
its scale gave a constant guess a high floor, and its items had no citation grading. It
is replaced by 2.0.0.
