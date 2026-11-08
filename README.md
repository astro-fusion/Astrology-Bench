# Astro-Bench

Astro-Bench measures whether a model, given a chart, can **compute** it, **recognise**
classical Vedic astrology patterns in it, **cite** the classical text that defines them,
and **apply** classical rules. It also measures whether the model says so when it cannot
cite. A fabricated citation scores below no citation.

It makes no claim about whether astrology predicts anything. For that question, see the
research repo: <https://github.com/astro-fusion/astro_research-white-paper>.

## The matrix

Rows are models or solvers. Columns are:

| Axis | Values |
|---|---|
| Level | 0 compute, 1 recognise, 2 cite, 3 judge, 4 conflict/abstain |
| Task | positions, lagna, nakshatra, varga, dasha, dignity, combustion, aspect, lordship, yoga, rule, citation, judgment, conflict |
| Source | BPHS, Brihat Jataka, Phaladeepika, Saravali, Jaimini Sutras, Brihat Samhita, modern (uncited, never citation-graded) |
| Convention | ayanamsa {lahiri, raman, krishnamurti}, node {mean, true}, house {whole_sign, placidus} |
| Tier | EASY, MEDIUM, HARD, VERY_HARD |
| Split | dev (public), test (hidden, hash-committed) |

The oracle is the `vedic-astrology-core` engine from the research repo. The benchmark
calls it and never re-implements astronomy or astrology math. See
[docs/METHODOLOGY.md](docs/METHODOLOGY.md) and
[docs/adr/ADR-001-open-benchmark-matrix.md](docs/adr/ADR-001-open-benchmark-matrix.md).

## Quick start

```sh
pip install -e ".[dev]"
```

The engine is pinned by commit in `pyproject.toml` and comes from the research repo.
`pyswisseph` falls back to the built-in Moshier ephemeris when no Swiss Ephemeris files
are installed. Results are then slightly less precise, so use the same setup when you
compare runs.

```sh
# generate the public dev split
astro-bench generate --level 0,1,2 --split dev --seed 20261108 --n-per-task 40

# check the items
astro-bench validate items/

# run baselines (no API key needed)
astro-bench run --solver oracle --items items/ --out results/
astro-bench run --solver random --items items/ --out results/
astro-bench run --solver constant --items items/ --out results/
astro-bench run --solver mock --items items/ --out results/
astro-bench run --solver nochart:random --items items/ --out results/

# render the leaderboard
astro-bench leaderboard --results results/ --out LEADERBOARD.md
```

To run a model, install the `[eval]` extra and use `inspect_ai`. There is one task per
level:

```sh
pip install -e ".[eval]"
inspect eval astro_bench/inspect_tasks.py@level1 --model anthropic/claude-sonnet-5-5
```

Any provider that `inspect_ai` supports works. `astro-bench run` also accepts any Python
callable `Solver` for offline work.

## Required output format

The system prompt (`astro_bench/prompts/system.md`) requires one JSON object:

```json
{"answer": "<per answer_type>",
 "citations": [{"text": "BPHS", "chapter": "36", "verse": "3", "edition": "santhanam1984"}],
 "confidence": 0.7,
 "note": "optional"}
```

- `answer` is graded against the engine's gold.
- `citations` is graded against the canon. Use `[]` when you cannot cite.
- `confidence` in [0, 1] feeds calibration scores (Brier, ECE).

The parser takes the first well-formed JSON object in the response and tolerates code
fences and surrounding prose. A response with no parsable object is a parse error. It
scores 0 for answer and citation and is counted separately.

One structured object lets the grader score answer, citation and confidence separately
without reading free text.

## Scoring

- **Answer score** in [0, 1]. Exact match for bool, category and citation. Jaccard for
  sets. For positions, the mean over planets of sign 0.5, nakshatra 0.25, degree within
  tolerance 0.25. The lagna sign counts as one more planet.
- **Citation score** in {-1, 0, +1}, graded only when the item has gold canon entries.
  +1 when a citation matches gold or an alternate. 0 when `citations` is empty. -1 when
  a citation names an unknown text, a chapter beyond the text's chapter count, or a real
  locus that does not support the claim.
- `fabricated_citation_rate` is the share of items with any -1 citation.
- Calibration is the Brier score and ECE (10 bins) of `confidence` against correctness.

Baselines run in CI without an API key:

| Solver | Purpose |
|---|---|
| `oracle` | The engine answers. Scores 1.0 on Levels 0 and 1. Defines the ceiling. |
| `random` | Uniform over the answer space. |
| `constant` | Majority class per task. |
| `mock` | The v1 seeded pseudo-random responder, kept to reproduce old numbers. |
| `nochart:<solver>` | Deletes `input.chart` and `input.birth` first. Detects prior-driven guessing. |

## Leaderboard

Numbers live in [LEADERBOARD.md](LEADERBOARD.md), rendered from `results/`. Baselines
always appear beside model rows. Every rate carries a Wilson 95% interval. A model that
does not clearly beat `constant` and `nochart` on a slice has shown nothing on it.

## Status

- v0.1 ships Levels 0, 1 and 2 as generated items.
- The canon holds 56 verified-quote entries across six texts (BPHS, Brihat Jataka,
  Phaladeepika, Saravali, Jaimini Sutras, Brihat Samhita); Kala Sarpa is recorded as
  untraced. See `docs/CANON_POLICY.md`.
- Level 3 is a seed set of human-authored items awaiting three raters. Until then the
  items are `needs_review` and not graded.
- Level 4 is schema only.
- v1 (TypeScript, 32 items, mock agent) is retired. See [CHANGELOG.md](CHANGELOG.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation and licence

- Code: MIT.
- Items: CC BY 4.0.
- Canon quotes are short fair-use excerpts, each with a URL where the source can be read.

If you use Astro-Bench, cite the repository and the version, and state the split and
convention filter you ran.
