# Level 3 judgment items

`seed/legacy_v1.jsonl` holds the 32 hand-written cases from Astro-Bench v1, migrated
to the v2 item schema. They are seeds, not gold.

- Every item has `status: needs_review`. The `gold.answer` is the v1 author's 1-to-5
  score and has not been checked by anyone else.
- An item becomes gradable only when three named raters approve it and a Krippendorff's
  alpha for the set is published (ADR-001, Level 3 and 4 policy). Until then the
  runner and the leaderboard must not count these items as gold.
- `canon_ids` is empty on purpose. The v1 `reference` values (book, chapter, verse)
  are kept under `legacy.reference` and are unverified against `canon/`. Several do
  not match the pinned editions (see the Phaladeepika notes).
- `review_notes` lists problems found while migrating: 18 of 32 items carry notes.
  The four flagged in ADR-001 are BPHS-01, BPHS-05, BPHS-08 and SYN-01. A check of each
  remaining case's `logic` against its chart description added more (for example an
  aspect that cannot occur from the stated sign, or a dignity the logic ignores).
- Polarity of the 1-to-5 scale is not fixed across items (BPHS-08, SAR-06, SAR-08).
  Settle one convention before approving any "risk" or "reversal" prompt.
- `input.chart_description` is the v1 `chartState` object as written, not a computed
  chart. The `convention` block is a placeholder (Lahiri, mean node, whole sign) because
  v1 never stated one.
