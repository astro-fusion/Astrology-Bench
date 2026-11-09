# Copy-paste prompts for running Astro-Bench in an AI coding agent

One run = one harness + one model + one effort setting. Replace the angle-bracket fields
before pasting. `<BENCH>` is the absolute path of this repository on your machine; it must
have `.venv/bin/astro-bench` installed (`python3 -m venv .venv && .venv/bin/pip install -e
".[dev]" && .venv/bin/python scripts/fetch_ephe.py`). Chunks live in
`runs/packs/pack-100-chart-v2/` (ten chunks of ten items). Reply files go to
`runs/<RUN>/replies-NN.txt`. Suggested run ids: `cursor-composer`, `cursor-grok-4-7`,
`antigravity-<model>`, `opencode-<model>`, `cline-<model>`, `grok-code-<model>`,
`claude-code-<model>`.

Fields: `<RUN>` run id; `<HARNESS>` e.g. "Cursor 1.x agent mode"; `<MODEL>` exactly as the
model picker shows it; `<MODEL_ID>` provider id if known, else "unknown"; `<EFFORT>` the
thinking or effort setting shown, else "not shown"; `<OPERATOR>` your handle; `<DATE>`.

## A. Terminal or IDE agent with tools allowed (reads, writes and runs the scorer itself)

One line, run all ten chunks in order, scoring after each, stopping cleanly at a token limit:

```
Work in <BENCH>. For N = 01 to 10 in order: read runs/packs/pack-100-chart-v2/pack-100-chunk-N.md and follow its "How to reply" and "System prompt" sections exactly (answer under each item's stated convention; cite only chapter and verse you are sure of, otherwise citations []); write runs/<RUN>/replies-N.txt containing first this disclosure header filled in exactly: "harness: <HARNESS>", "model (exactly as the UI shows): <MODEL>", "provider model id (if known): <MODEL_ID>", "effort or thinking setting (or \"not shown\"): <EFFORT>", "tools allowed (yes/no): yes", "operator: <OPERATOR>", "date: <DATE>", then for every item a line "### <item_id>" and one JSON object; then run: .venv/bin/astro-bench ingest --pack runs/packs/pack-100-chart-v2/pack-100.manifest.json $(ls runs/<RUN>/replies-*.txt | sed 's/^/--replies /') --run-id <RUN> --kind system_ui --description "<HARNESS>, <MODEL>, <EFFORT>, <DATE>" --out results/ && .venv/bin/astro-bench status --run-id <RUN> --out results/ and show me the summary. You may compute with any code or library you like, but you must not open items/, results/*.json, canon/, vendor/ or any file under runs/ other than the chunk you are answering and your own reply files. If you are near your context or token limit, finish the current chunk, ingest it, and tell me the last chunk number completed.
```

Resume later with:

```
Work in <BENCH>. Continue the Astro-Bench run <RUN> from chunk <N> to 10 exactly as before (same header, same files runs/<RUN>/replies-N.txt, ingest and status after each chunk); do not open items/, results/*.json, canon/, vendor/ or other runs/ files; report the last chunk completed and the status output.
```

## B. Agent measured as a bare model (no code, no tools; the operator scores)

```
Work in <BENCH>. Read only runs/packs/pack-100-chart-v2/pack-100-chunk-<N>.md and follow its "How to reply" and "System prompt" sections exactly, answering from your own knowledge and reasoning without running any code, command, calculator or search; cite only chapter and verse you are sure of, otherwise citations []. Write runs/<RUN>/replies-<N>.txt containing first the disclosure header filled in ("harness: <HARNESS>", "model (exactly as the UI shows): <MODEL>", "provider model id (if known): <MODEL_ID>", "effort or thinking setting (or \"not shown\"): <EFFORT>", "tools allowed (yes/no): no", "operator: <OPERATOR>", "date: <DATE>"), then for every item "### <item_id>" and one JSON object. Open no other file.
```

Then the operator scores:

```
cd <BENCH> && .venv/bin/astro-bench ingest --pack runs/packs/pack-100-chart-v2/pack-100.manifest.json $(ls runs/<RUN>/replies-*.txt | sed 's/^/--replies /') --run-id <RUN> --kind model --description "<HARNESS>, <MODEL>, <EFFORT>, <DATE>" --out results/ && .venv/bin/astro-bench status --run-id <RUN> --out results/
```

## C. Chat UI with no file access (paste the chunk)

Paste this line, then the whole content of the chunk file, as one message:

```
Answer the Astro-Bench chunk below exactly as its "How to reply" and "System prompt" sections say: for every item a line "### <item_id>" then one JSON object; answer under each item's stated convention; cite only chapter and verse you are sure of, otherwise use citations []. Do not use tools or search unless I say so. Reply with the answers only.
```

Save the reply as `runs/<RUN>/replies-<N>.txt` with the filled disclosure header pasted at the top of the first file, and score with the operator command in section B (use `--kind system_ui` if the UI ran code or searched, `--kind model` otherwise).

## D. Publish

```
cd <BENCH> && .venv/bin/astro-bench cards && .venv/bin/astro-bench leaderboard --results results/ --out LEADERBOARD.md && git add -- results/<RUN>.json results/<RUN>.replies.jsonl runs/<RUN> runs/README.md LEADERBOARD.md && git commit -m "results: <HARNESS>, <MODEL>, <EFFORT>, <DATE> (<RUN>)" -- results/<RUN>.json results/<RUN>.replies.jsonl runs/<RUN> runs/README.md LEADERBOARD.md
```

The maintainer re-ingests every published run from its reply files before accepting it.
