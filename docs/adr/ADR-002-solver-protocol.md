# ADR-002: Solver protocol. Redacted items, solver kinds, input modes and sampling

Status: accepted 2026-11-08. Extends ADR-001.

## Problem

ADR-001 lets any Python callable act as a solver. Three things make a reported number untrustworthy:
the solver can see `gold`; a tool-using system and a bare language model sit in the same column;
and apps that take birth data cannot consume the positions table that models are given.

## Decisions

1. **Redacted view.** Solvers receive a `SolverItem` with only `id, level, task, tier, convention,
   input, prompt, answer_type, choices`. `gold`, `canon_ids`, `rule_id` and `generator` are not
   present. The oracle is the one exception and is constructed inside the runner from the engine,
   not from the item's gold. A test asserts the redacted model has no gold field and that the
   runner passes it to external solvers.
2. **Solver kind.** Every result file carries `kind` in `{oracle, baseline, model, system, app_tools,
   system_ui}` and a free-text `solver_description` (what the system is: model, tools, retrieval,
   app version). The leaderboard shows `kind` and `date` columns and groups rows by kind, baselines
   first, then `model`, then `system`. A `system` row without a description is rejected by
   `astro-bench score`.
3. **Input mode.** `--input-mode chart` (default) gives the positions table; `--input-mode birth`
   gives only `input.birth` plus the convention and lets the solver compute. Level 0 is always
   birth mode. Results record the mode; the leaderboard shows it.
4. **Generic HTTP solver.** `http_json:<config.yaml>` posts `{system, prompt, convention,
   input_mode, item_id}` to a URL with headers from environment variables named in the config,
   and reads the reply text from a JSON path. No credentials in the repo.
5. **Sampling.** `--sample N --stratify task,level --sample-seed S` draws a reproducible stratified
   subset; the result records the sample seed and the sampled ids' sha256 so two runs on the same
   sample are comparable.
6. **Nochart is a kind of ablation, not a solver.** `nochart:<solver>` results are labelled
   `ablation: nochart` and are never ranked.

## Non-goals

No app internals, hostnames or schemas are described in this repository. The private adapter that
measures the AstroFusion chat lives in that product's repository; only its description and its
rows appear here.
