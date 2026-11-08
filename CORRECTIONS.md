# Corrections

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
