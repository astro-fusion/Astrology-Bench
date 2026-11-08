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
- The 32 v1 items move to `items/judgment/seed/legacy_v1.jsonl` as `needs_review`. Eighteen
  carry review notes: four flagged in the design review and fourteen more found by
  checking each item's stated logic against its chart.
- `canon/`: 56 verified-quote entries across six classical texts with edition pinning
  (BPHS = Santhanam 1984, Brihat Jataka = Iyer 1905); Kala Sarpa recorded as untraced.
- Level 3 is a seed set awaiting three raters. Level 4 is schema only.
- The v1 TypeScript runner is removed.
- Solver protocol (ADR-002): solvers receive a redacted `SolverItem` without gold; results
  carry `kind` (oracle, baseline, model, system, app_tools, system_ui),
  `solver_description`, `input_mode` and sample metadata; `run` gains `--kind`,
  `--description`, `--input-mode chart|birth`, `--sample`, `--stratify` and
  `--sample-seed`; a generic `http_json:<config.yaml>` solver; the leaderboard groups by
  kind and lists `nochart:` runs as unranked ablations.
- Chart tables carry a retrograde flag instead of speeds, and true-node longitudes to
  1 dp, so the dev split is byte-identical across Swiss Ephemeris builds.

## 1.0.0

Retired. The first version was a TypeScript runner with 32 hand-written items scored on
a 1-to-5 scale and a mock agent as the only built-in solver. Its answers had no oracle,
its scale gave a constant guess a high floor, and its items had no citation grading. It
is replaced by 2.0.0.
