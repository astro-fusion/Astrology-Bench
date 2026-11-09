# Corrections

## 2026-11-09: Level 2 gold leaked to solvers through item ids and item queries

**What was wrong.** Two things a solver can see gave away answers. First, Level 2
citation items were named `L2-citation-<canon id>`, and a canon id names the gold
locus (for example `bphs.santhanam1984.ch36.v3-4`: text, chapter and verse), so any
solver could read the answer to all 56 Level 2 items from `item.id`. Second, the
redacted `SolverItem` view passed `input.query` through unchanged, exposing `rule_id`
and `rule_key` on yoga and rule items, `canon_id` and `rule_key` on Level 2 items and
`golden_id` on the golden Level 0 items. ADR-002 says solvers see no gold, canon ids or
rule ids.

**Since when.** Level 2 ids since the first canon-backed dev split (2026-11-08); the
query pass-through since the redacted view was added (ADR-002, commit `d41fd8e`).

**What changed.** Commit `e402d09`: Level 2 ids are now
`L2-citation-<first 12 hex of sha256("astro-bench-l2|" + canon id)>`, which is stable
but reveals nothing, and the redacted view keeps only the query keys a prompt states
anyway (`planet`, `varga`, `house`, `level`, `target_utc`). Only the 56 Level 2 ids
changed; no gold, input or prompt changed. The baselines were rerun; only mock moved,
because its replies are seeded from the item id. `tests/test_no_gold_leak.py` now checks
every committed item in both input modes and fails if any gold canon id, any gold
`chapter.verse` locus of a citation item, any hidden query key, or (whole-word) the gold
answer of a bool or category item appears in what a solver sees.

**Results affected.** No model rows had been published. The one published `app_tools`
row (`results/app-tools-astrofusion-dev.json`) was scored on the old ids and is being
rerun on the new split, so that every published result matches the current items.

## 2026-11-09: dignity gold, moolatrikona degree ranges corrected to BPHS 3.51-54

**What was wrong.** The oracle engine (`vedic-astrology-core`, pinned at `24d048b`) had
wrong moolatrikona degree ranges for five planets in
`dignity/exaltation_matrix.py`: Mars Aries 0-18 (BPHS: 0-12), Jupiter Sagittarius
0-13 (BPHS: 0-10), Venus Libra 0-10 (BPHS: 0-15), the Moon Taurus 4-30 (BPHS: 3-30) and
Mercury Virgo 16-20 (BPHS: 15-20), and it counted the end degree as inside the range.
The source is BPHS ch. 3 v. 51-54 (Santhanam 1984); the upstream record is the
2026-11-09 entry of the research repository's `CORRECTIONS.md`.

**Since when.** Every dev split generated before this entry: the first committed split
(2026-11-08) through commit `1f9dfc4`. The Level 1 `dignity` task, which reads the
engine's `get_dignity_type` and `dignities_of`, is the only task that uses the table.

**What changed.** The engine pin moved to `7018b2aa3652460c03e819135c35d8b81190fbc1`
(`ENGINE_COMMIT = "7018b2a"`, recorded in every item's `generator.engine_commit`).
`vendor/rules` and `vendor/golden` were re-synced at that commit; their contents did not
change. The dev split was regenerated with the same seed (20261108) and diffed against
the previous one: no item was added or removed, no input or prompt changed, and exactly
one item's gold changed.

| Item | Chart | Old gold | New gold |
|---|---|---|---|
| `L1-dignity-lahiri-mean-ws-000019` | Jupiter at Sagittarius 10.04 | moolatrikona | own |

A test now checks that the pyproject pin, the vendored snapshot stamps and every
committed item's `engine_commit` agree.

**Results affected.** No results had been published. The committed baseline runs in
`results/` were rerun: the oracle still scores 1.0, and the random, constant, mock and
nochart:constant numbers are unchanged at the reported precision. Any private run scored
against the earlier split differs on at most this one item: re-score it with
`astro-bench run` against the current `items/`.
