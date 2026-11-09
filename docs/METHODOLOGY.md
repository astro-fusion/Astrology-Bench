# Methodology

This page is for readers who know model evaluation but not astrology.

## What is being tested

Vedic (sidereal) astrology has classical texts, such as the Brihat Parashara Hora Shastra
(BPHS), that define rules. A rule might say that Jupiter in a certain relation to the Moon
forms a named combination (a yoga). Astro-Bench asks whether a model can follow those
rules faithfully and point to the text. It does not ask whether the rules predict life
events.

## Why the levels are separate

Each level isolates one skill, so a score can be read as a diagnosis.

| Level | Skill | Failure it exposes |
|---|---|---|
| 0 compute | Planet positions from a birth time and place | The model cannot do ephemeris math |
| 1 recognise | Facts and patterns in a given chart | The model misapplies a rule on correct data |
| 2 cite | Name the text, chapter and verse for a rule | The model invents sources |
| 3 judge | Rate a reading against a classical claim | Opinion; needs raters |
| 4 conflict | Texts disagree; abstaining is acceptable | Overconfidence |

Levels 1 and 2 hand the model a computed chart. A model that fails Level 0 can still be
graded on rule-following.

## Why the engine is the oracle

Gold answers for Levels 0 to 2 come from `vedic-astrology-core`, from the research repo
`astro-fusion/astro_research-white-paper`. The benchmark pins its commit and never
re-implements the math.

The engine is validated two ways, both in the research repo:

- 24 golden charts computed with PyJHora, a widely used open implementation;
- a cross-check of planetary longitudes against JPL Horizons.

The `oracle` solver returns the engine's own answers and must score 1.0 on Levels 0 and
1. If it does not, the item or the grader is wrong.

## Item generation and balancing

- Charts are sampled uniformly over 1900-01-01 to 2030-12-31 UTC, and over a fixed list
  of 24 places with latitudes from -45 to +60.
- Every item records its generator name, version, seed and engine commit.
- For yes/no tasks the generator rejects samples until positives and negatives are
  within 45/55. Without this, "always say no" would look skilled on rare yogas.
- Tier (EASY to VERY_HARD) is assigned by the generator from task features such as
  number of conditions in the rule. It is not tuned from model results.
- `nochart:<solver>` deletes the chart and birth data. A model that scores well without
  data is using priors, not the chart.

## Conventions

The same birth gives different answers under different conventions. A model must be told
which one applies, and the grader uses it.

| Convention | Options | Effect |
|---|---|---|
| Ayanamsa | lahiri, raman, krishnamurti | Shifts all sidereal longitudes by tens of arc-minutes. Moves planets across sign and nakshatra edges. |
| Node | mean, true | Changes Rahu and Ketu by up to about 1.5 degrees. |
| House | whole_sign, placidus | Changes which planets sit in which house. |

Every item states its convention in the prompt and in `convention`. Results are
reported per convention, so a model that only knows one is visible.

## Scoring

### Answer score, in [0, 1]

| Answer type | Score |
|---|---|
| bool, category, citation | 1 if equal to gold, else 0 |
| set | Jaccard index: size of intersection over size of union |
| positions | mean over planets and lagna, see below |
| likert | v1 legacy scale; Level 3 only |

For positions, each planet scores `0.5 * sign_ok + 0.25 * nakshatra_ok + 0.25 * degree_ok`.
`degree_ok` is 1 when the degree in sign is within `tolerance_deg` of gold (1 degree for
Level 0). The lagna sign counts as one more planet. The item score is the mean.

### Citation score, in {-1, 0, +1}

Graded only when the item has gold canon entries (`canon_ids`). The gold set also
includes each entry's `also_in` alternates, since many rules appear in several texts.

| Score | Condition |
|---|---|
| +1 | Any citation matches a gold entry or alternate. Text and chapter must match. Verse must match when gold has one. |
| 0 | `citations` is empty. This is an honest "I cannot cite". |
| -1 | A citation names a text not in `canon/REGISTRY.yaml`, a chapter beyond that text's chapter count, or a real text and chapter that do not support the claim. |

The -1 is the fabrication penalty. Mixed outputs score -1 when any citation is
fabricated. `fabricated_citation_rate` is the share of items with a -1.

The design goal is that abstaining always beats inventing. A model that cites correctly
when it can and abstains otherwise is the best outcome short of citing everything.

### Calibration

`confidence` is compared with correctness (answer score of 1).

- Brier score: mean of (confidence - correct)^2. Lower is better.
- ECE: split items into 10 equal-width confidence bins; take the sum over bins of
  (bin size / n) * |mean confidence - accuracy|.

Parse errors are excluded from calibration and counted separately.

## What a floor teaches (v1 constant-3)

The v1 grader gave 1.0 for an exact match on the 1-to-5 scale and 0.5 for a miss by one.
With gold spread evenly over the five values, a solver that always answers 3 is exact
one time in five and off by one two times in five, so it scores 0.2 + 0.4 x 0.5 = 40
percent. Uniform random guessing scores 0.2 + 0.32 x 0.5 = 36 percent. Nothing was
learned about the solver, and a reported 60 percent would have looked strong.

The lessons built into v2:

- Always report a trivial baseline (`constant`, `random`) beside every model.
- Prefer exact and set-based scores over distance on a short scale.
- Report the score above the best baseline, not only the raw score.
- Use a `nochart` ablation to find prior-driven guessing.

## Intervals and item counts

Rates are reported with Wilson 95% intervals. For p = 0.5 the interval half-width is:

| n | Half-width |
|---|---|
| 32 | 0.164 (about 16 points) |
| 100 | 0.096 |
| 400 | 0.049 |
| 1000 | 0.031 |

The v1 set of 32 items could not separate models closer than about 30 points. Treat any
slice with fewer than 100 items as indicative only, and do not rank models whose
intervals overlap.

Slices (per task, source, convention, tier) are small. Intervals widen quickly there, so
the leaderboard shows `n` beside each rate.

## Solver kinds and input modes

ADR-002 fixes how a solver is run and labelled, so that a reported number means one
thing.

- **Redacted items.** A solver receives only `id, level, task, tier, convention, input,
  prompt, answer_type, choices`. `gold`, `canon_ids`, `rule_id` and `generator` are not
  present. The oracle is the one exception and is constructed inside the runner from
  the engine, not from the item's gold.
- **Kind.** Every result carries `kind` in {oracle, baseline, model, system, app_tools,
  system_ui} and a free-text `solver_description`. A tool-using system and a bare
  language model are not comparable, so the leaderboard groups rows by kind: baselines
  first, then `model`, then `system`. A system row without a description is rejected.
- **Input mode.** `chart` (default) gives the positions table; `birth` gives only the
  birth data plus the convention and lets the solver compute. Level 0 is always birth
  mode. The mode is recorded and shown.
- **Sampling.** `--sample N --stratify task,level --sample-seed S` draws a reproducible
  stratified subset; the result records the sample seed and the sampled ids' sha256, so
  two runs on the same sample are comparable.
- **Nochart is a kind of ablation, not a solver.** `nochart:<solver>` results are
  labelled `ablation: nochart` and are never ranked.

Every published model or system row is fully disclosed for research use (ADR-002,
decision 7): its card in `runs/<run_id>/CARD.md` names the harness, the model id, the
effort setting (recorded as unknown rather than omitted), the tools allowed and used, the
operator and date, the input mode and sample, and every deviation from the brief, and it
links the verbatim brief, the agent's own report and the raw replies with their sha256.
A reader can therefore re-score the published replies with `astro-bench ingest` and get
the published numbers, and can judge for themselves how the run was set up.

## Splits and contamination

- `dev` is public. It is generated with seed 20261108 and committed under `items/`.
- `test` is generated from a seed held in `ASTRO_BENCH_TEST_SEED`. It is not committed.
  Only `manifests/test-<version>.sha256` is committed, holding the hash of the generated
  JSONL and the item count. A later reveal is checkable against it.
- A test asserts that no committed item has `split: test`.
- Results on the hidden split carry `items_sha256`, which must match a manifest.
- Level 3 and 4 items are human-authored, split by the author, and the test half is held
  the same way.

Because generation is procedural, a new hidden split can be drawn at any time with a
new seed.

## Known limitations

- **Level 0 mostly measures tool use.** A language model cannot compute planetary
  longitudes to one degree without a tool. A model with a code tool or ephemeris
  access does well. A model without one scores near the floor. Report the tool setup.
- **Canon is edition-pinned.** Chapter and verse numbers differ between editions and
  translations. Gold uses the edition in the registry. A correct citation to another
  edition can score as wrong unless an `also_in` alternate covers it.
- **Coverage is partial.** Only rules whose source text is in the registry and whose
  entry is `quoted` are citation-graded. Everything else is `modern` and uncited.
- **Level 3 is opinion until raters agree.** The seed set is `needs_review`. It becomes
  gradable only with three named raters and a published Krippendorff's alpha.
- **Level 4 is schema only.** There is no data yet.
- **Rules are rules, not truth.** A model that applies BPHS faithfully scores well. That
  says nothing about whether the rule is valid.
- **Engine pin.** Gold is only as good as the pinned engine commit. A change of pin can
  change items. Each item records the commit.
- **Ephemeris precision.** Without Swiss Ephemeris files, Moshier is used. Differences
  are small, but they can flip an item that sits on a sign or nakshatra edge.
