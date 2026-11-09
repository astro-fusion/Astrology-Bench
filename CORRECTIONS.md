# Corrections

## 2026-11-09: gold computed with the Moshier ephemeris; edge items; chart-table gold

**What was wrong.** A parity check of four disagreements between the oracle and an
independent implementation found three problems.

1. *Moshier gold.* The oracle ran without Swiss Ephemeris files (`SE_EPHE_PATH` unset),
   and the engine fell back silently to the Moshier analytic ephemeris
   (`ephemeris_model == "moshier"`). Moshier's true lunar node differs from the
   Swiss-file value by 1e-3 to 5e-3 deg, enough to put three true-node items on the wrong
   side of a pada or sign edge (for example Rahu 209.9996 by Moshier and 210.0023 from the
   files, against the Libra/Scorpio edge at 210.0; one such item printed Rahu 210.0 in
   Scorpio in its chart table while its gold said Libra).
2. *Edge items.* Nothing kept sampled moments away from edges, so a value that rounds or
   differs between ephemeris sources by a few thousandths of a degree could change the
   answer. A dasha item's target was 2.07 days from an antardasha boundary, just outside
   the 2-day margin, where civil-date dasha conventions differ by up to 2.5 days.
3. *Chart-mode gold.* Gold was computed from unrounded engine longitudes while a
   chart-mode solver sees the rounded table, so the two could disagree at an edge.

**Since when.** Every dev split before this entry.

**What changed.** Commit `778cf94`:

- `scripts/fetch_ephe.py` fetches `sepl_18.se1`, `semo_18.se1` and `seas_18.se1` from the
  official Swiss Ephemeris repository (aloistr/swisseph, pinned commit, pinned sha256;
  AGPL or Swiss Ephemeris Professional licence, not committed). The generator, the oracle
  and the runner refuse to run unless the engine reports `swieph`; every item and result
  records `ephemeris_model` and the file-set sha256. CI fetches the files first.
- The generator redraws a moment when a true node is within 0.02 deg, or any other body
  or the Lagna within 0.002 deg, of a multiple of 3 deg 20' (pada edges, which include
  nakshatra and sign edges), and the dasha boundary margin is 4 days.
- Level 1 gold is computed from the printed, rounded chart table, and a sample is redrawn
  when that differs from the engine's unrounded answer, so chart and birth modes share
  one gold. A test recomputes every committed chart-mode gold from its printed table.

The dev split was regenerated with the same seed. All 955 ids are kept. 21 items were
redrawn (positions 2, dasha 2, nakshatra 1, aspect 1, dignity 4, rule 4, lordship 2,
varga 3, combustion 1, yoga 1; the four rule items move because one rejected sample
reorders that rule's items). 2 more Level 0 items changed gold on the same birth data
(Swiss positions), and 28 further items changed only printed chart-table digits.

**Results affected.** No model rows had been ranked on a corrected split before this
entry. The baselines were rerun (oracle 1.0). The four Claude rows on the 100-item sample
stay published as scored, listed under "Older split" on the leaderboard; their replies
were re-scored on the new split without any new model call: 92 of 100 replies carry over
for each run (8 sampled items changed their prompt), published as partial `-v2` rows.
The app-tools row is listed under "Older split" until it is rerun. The 100-item chunk pack
was regenerated as `runs/packs/pack-100-chart-v2/`; `pack-100-chart/` is kept for the
record.

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
