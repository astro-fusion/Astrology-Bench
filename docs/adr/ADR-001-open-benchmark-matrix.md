# ADR-001: Astro-Bench v2, an open benchmark matrix for classical-rule fidelity

Status: accepted 2026-11-08. Supersedes the v1 TypeScript runner (32 hand-written
1-to-5 items, mock agent only), which is retired by this decision.

## What the benchmark measures

Not "does the AI predict well". It measures whether a model, given a chart, can
**compute, recognise, cite and apply** classical Vedic astrology faithfully, and
whether it **says so when it cannot cite**. Every claim a model makes must come with
a source (text, chapter, verse) that exists and that supports the claim. Fabricated
citations are scored below no citation. That is the property the owner asked for:
answers with a credible source and an accurate reference to the classical text.

## The matrix

Rows are models (or solvers). Columns are:

| Axis | Values |
|---|---|
| Level | 0 compute, 1 recognise, 2 cite, 3 judge, 4 conflict/abstain |
| Task | positions, lagna, nakshatra, varga, dasha, dignity, combustion, aspect, lordship, yoga, rule, citation, judgment, conflict |
| Source | BPHS, Brihat Jataka, Phaladeepika, Saravali, Jaimini Sutras, Brihat Samhita, modern (uncited, never citation-graded) |
| Convention | ayanamsa {lahiri, raman, krishnamurti}, node {mean, true}, house {whole_sign, placidus} |
| Tier | EASY, MEDIUM, HARD, VERY_HARD |
| Split | dev (public), test (hidden, hash-committed) |

v0.1 ships Levels 0, 1 and 2 generated procedurally, Level 3 as a seed set awaiting
rater approval, Level 4 as schema only.

## Oracle and generator

- Engine: `vedic-astrology-core` from `astro-fusion/astro_research-white-paper`, pinned
  by commit in `pyproject.toml`. Its 24 golden charts (PyJHora) and the JPL Horizons
  cross-check are what make the Level 0 and 1 gold trustworthy. The benchmark never
  re-implements astronomy or astrology math; it calls the engine.
- Rules: a pinned snapshot of the research repo's `rules/**` under `vendor/rules/`
  with `vendor/rules/UPSTREAM.yaml` (upstream commit, per-file sha256), synced by
  `scripts/sync_rules.py`. Only rules whose `source.text` resolves to a text in
  `canon/REGISTRY.yaml` are citation-graded; the rest are `source: modern`.
- Canon: `canon/<text>.yaml` entries, each with edition, chapter, verse, a short
  verbatim quote (fair use, at most 40 words), a URL where it can be read, and a
  `verified` status. Only `verified: quoted` entries are Level 2 gold. Chapter numbers
  come from the pinned edition, never from memory.
- Charts are sampled uniformly over 1900-01-01 to 2030-12-31 UTC and a fixed list of
  24 places spanning latitudes -45 to +60, with the seed recorded on every item.
  Items are balanced: for yes/no tasks the generator rejects samples until positives
  and negatives are within 45/55.
- Reproducibility across CPython builds: pyswisseph gives results that differ by about 1e-5
  degrees between builds, so the chart table prints no speed magnitudes (a `retrograde` flag
  instead, none for the nodes) and true-node longitudes to 1 decimal; `tests/test_reproducibility.py`
  guards the rounding margin.

## Item schema (`items/**/*.jsonl`, one JSON object per line)

```json
{
  "id": "L1-yoga-gaja_kesari-lahiri-mean-ws-000123",
  "schema_version": 1,
  "level": 1,
  "task": "yoga",
  "tier": "MEDIUM",
  "source": "BPHS",
  "canon_ids": ["bphs.santhanam.ch36.v3"],
  "rule_id": "general.gaja_kesari.classical",
  "convention": {"ayanamsa": "lahiri", "node": "mean", "house": "whole_sign"},
  "split": "dev",
  "input": {
    "birth": {"utc": "1990-05-15T04:45:00Z", "lat": 27.7172, "lon": 85.324},
    "chart": {"lagna": 103.25, "bodies": {"Sun": {"lon": 30.38, "retrograde": false}, "...": {}}}
  },
  "prompt": "Using the sidereal chart above (Lahiri ayanamsa, mean node, whole-sign houses), is Gaja Kesari yoga present? Answer in the JSON format given in the system prompt and cite the classical text, chapter and verse that defines the yoga. If you cannot cite one, set citations to [] and say so.",
  "answer_type": "bool | category | set | positions | citation | likert",
  "gold": {"answer": true},
  "grader": {"name": "exact", "tolerance_deg": null},
  "generator": {"name": "yoga_from_rule", "version": "0.1.0", "seed": 20261108, "engine_commit": "24d048b"}
}
```

Level 0 items carry `input.birth` only (no `chart`). Level 1 and 2 items carry both;
Level 2 prompts ask only for the citation of a named rule or yoga, graded against
`canon_ids` and their `also_in` alternates. `gold.answer` shapes: bool; string
category; sorted list for sets; `{planet: {sign, deg_in_sign, nakshatra, pada}}` for
positions; `{text, chapter, verse}` for citation.

## Required model output

System prompt (shipped in `astro_bench/prompts/system.md`) requires one JSON object:

```json
{"answer": <per answer_type>, "citations": [{"text": "BPHS", "chapter": "36", "verse": "3", "edition": "santhanam1984"}], "confidence": 0.0-1.0, "note": "optional"}
```

The parser takes the first well-formed JSON object in the response, tolerating code
fences and prose. A response with no parsable object is a parse error: answer score 0,
citation score 0, and it is counted separately.

## Scoring

- `answer_score` in [0, 1]: exact match for bool/category/citation; Jaccard for sets;
  for positions the mean over planets of (sign exact 0.5, nakshatra exact 0.25,
  degree within `tolerance_deg` 0.25), lagna sign counted as one more planet.
- `citation_score` in [-1, 1] per item, graded only when `canon_ids` is non-empty:
  +1 when any citation matches a gold canon entry or an `also_in` alternate (text and
  chapter required, verse when gold has one); 0 when `citations` is empty; -1 when a
  citation names a text not in `canon/REGISTRY.yaml`, a chapter beyond that text's
  chapter count, or a real locus that does not support the claim (text+chapter in the
  registry but not in gold or alternates). This is the fabrication penalty.
- `fabricated_citation_rate`: share of items with any -1 citation.
- `calibration`: Brier score on `confidence` against answer correctness, and ECE with
  10 bins.
- Summary is reported per level, task, source, convention and tier with Wilson 95%
  intervals, always beside the baselines.

## Baselines (run in CI, no API key)

| Solver | Purpose |
|---|---|
| `oracle` | the engine answers; must score 1.0 on Levels 0 and 1, defines the ceiling |
| `random` | uniform over the answer space |
| `constant` | majority class per task |
| `mock` | the v1 seeded pseudo-random responder, kept so old numbers can be reproduced |
| `nochart:<solver>` | wrapper that deletes `input.chart` and `input.birth` before calling any solver; detects prior-driven guessing |

Model solvers run through `inspect_ai` tasks (`astro_bench/inspect_tasks.py`, one
`@task` per level, extra `[eval]`) so any provider inspect supports can be evaluated
with one command. The built-in runner (`astro-bench run`) also accepts any Python
callable `Solver` for offline work.

## Splits and contamination

- `dev`: generated with seed 20261108, committed under `items/`.
- `test`: generated with the seed in `ASTRO_BENCH_TEST_SEED` (not committed). Only
  `manifests/test-<version>.sha256` (sha256 of the generated JSONL and the item
  count) is committed, so a later reveal is verifiable. A test asserts no committed
  item has `split: test`.
- Level 3 and 4 items are human-authored; they get a dev/test split by the item
  author and the test half is held the same way.

## Results

`results/<run_id>.json`: `run_id, created_at, model, provider, solver, bench_version,
items_sha256, split, item_count, convention_filter, engine_commit, per_item[],
summary{}`. `astro-bench leaderboard` renders `LEADERBOARD.md` from `results/` with
baselines first. Results for hidden-split runs carry `items_sha256` that must match a
committed manifest.

## Level 3 and 4 policy

The 32 v1 items are migrated to `items/judgment/seed/legacy_v1.jsonl` with
`status: needs_review`. Four are flagged with `review_notes` (BPHS-01 exaltation claim
vs own sign; BPHS-05 Jupiter in Capricorn debilitated; BPHS-08 polarity of the scale;
SYN-01 conflict resolved to 3 by fiat). An item becomes gradable only when
`status: approved` with at least three named raters and a published Krippendorff's
alpha for the set. Level 4 gold is a set of acceptable readings plus `abstain_ok`.

## CLI

```
astro-bench generate --level 0,1,2 --split dev --seed 20261108 --n-per-task 60
astro-bench validate items/
astro-bench run --solver oracle|random|constant|mock|nochart:<s> --items items/ --out results/
astro-bench score results/<run>.json
astro-bench leaderboard --results results/ --out LEADERBOARD.md
inspect eval astro_bench/inspect_tasks.py@level1 --model anthropic/claude-sonnet-5-5
```

## Repo layout

```
astro_bench/            package: schema.py, parse.py, graders/, generators/, solvers/, runner.py, score.py, leaderboard.py, inspect_tasks.py, prompts/
canon/                  REGISTRY.yaml + <text>.yaml entries
vendor/rules/           pinned snapshot of the research repo rules + UPSTREAM.yaml
items/                  dev split JSONL by level/task; judgment/seed/
manifests/              hidden-split hashes
results/                committed baseline runs
scripts/                sync_rules.py, places.yaml
tests/                  pytest
docs/adr/, docs/METHODOLOGY.md, docs/CANON_POLICY.md, CONTRIBUTING.md, README.md, LEADERBOARD.md
.github/workflows/ci.yml   lint (ruff), mypy, pytest, generate-determinism check, baselines
```

## Work packages

| WP | Scope | Model | Files |
|---|---|---|---|
| B-1 core | package, schema, parser, graders, generators L0-L2, solvers, runner, score, leaderboard, inspect adapters, vendor sync, tests, CI, pyproject | Opus | `astro_bench/`, `vendor/`, `items/` (generated), `manifests/`, `results/`, `scripts/`, `tests/`, `.github/`, `pyproject.toml`, `LEADERBOARD.md` |
| B-2 canon | `canon/REGISTRY.yaml`, canon entries with quotes and URLs, `docs/CANON_POLICY.md`, legacy item migration to `items/judgment/seed/` | Sonnet | `canon/`, `items/judgment/`, `docs/CANON_POLICY.md` |
| B-3 docs | `README.md`, `CONTRIBUTING.md`, `docs/METHODOLOGY.md`, `CHANGELOG.md` | Sonnet | those files only |

Integration (main session): remove the v1 TypeScript files, reconcile README with the
real CLI, run the gates, commit, push.
