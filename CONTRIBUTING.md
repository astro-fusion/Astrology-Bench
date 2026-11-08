# Contributing to Astro-Bench

Thanks for helping. The rules below keep the benchmark checkable.

## Add a canon entry

Canon entries live in `canon/<text>.yaml`. The text must be listed in
`canon/REGISTRY.yaml` with its chapter count.

Each entry needs:

- the text, the edition, the chapter and the verse, taken from the pinned edition and
  never from memory;
- a URL where a reader can see the passage;
- a short verbatim quote, at most 40 words;
- a `verified` status:

| Status | Meaning |
|---|---|
| `quoted` | You read the passage at the URL and the quote is verbatim. Only these entries are Level 2 gold. |
| `paraphrased` | The passage exists but you only have a paraphrase. Not graded as gold. |
| `untraced` | A rule is attributed to the text but you could not find the locus. Not graded as gold. |

Do not promote an entry to `quoted` unless you checked the source. See
`docs/CANON_POLICY.md` for edition rules.

## Propose a task or generator

Open an issue first. A new generator must:

- call the pinned engine (`vedic-astrology-core`) for every gold answer;
- never add new astronomy or astrology math to this repo;
- take a seed and be deterministic, and record `generator.name`, `version`, `seed` and
  `engine_commit` on every item;
- balance yes/no tasks to within 45/55;
- ship tests, and pass `astro-bench validate items/`.

If the engine lacks the calculation, add it to the research repo first, then bump the
engine pin here.

Rules for Level 2 and above come from `vendor/rules/`. Do not edit that directory by
hand. Run `scripts/sync_rules.py` to update it.

## Submit a model result

1. Run the model on the dev split (or on a split you generated yourself).
2. Commit the output as `results/<run_id>.json`. It must include `items_sha256`,
   `model`, `provider`, `bench_version`, `engine_commit` and `convention_filter`.
3. Run `astro-bench score results/<run_id>.json` and `astro-bench leaderboard` and
   check that the row appears beside the baselines.
4. State the prompt, temperature and any tools the model could use.

Do not put hidden-split items in a pull request, in an issue or in a result file.
Hidden-split results carry an `items_sha256` that must match a committed manifest in
`manifests/`. The maintainer runs those.

## How Level 3 items get approved

Level 3 items are opinion until raters agree. An item becomes gradable only when:

- its `status` is `approved`;
- at least three named raters rated it independently;
- Krippendorff's alpha for the set is computed and published with the set.

Items flagged `needs_review` are never scored. Raters sign with a name or a stable
handle, not anonymously.

## Git rules

- Work on `main` or a branch you were told to use.
- Commit with explicit paths: `git add -- <paths>`, then `git commit -- <paths>`. Never
  `git add -A` or `git add .`.
- Never force-push. Never use `--no-verify`. Fix the failing hook instead.
- Do not rewrite history. To undo a change, add a new commit that reverts it.
- Run `ruff`, `mypy` and `pytest` before you push. CI also checks that generation is
  deterministic.
