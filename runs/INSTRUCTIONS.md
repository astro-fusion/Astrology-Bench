# Running Astro-Bench by hand in a free-tier harness

For chat UIs and IDE or terminal agents (Antigravity, Cursor, OpenCode, Cline, ...) with
token limits: the 100-item sample is split into ten self-contained chunks of ten items
in `runs/packs/pack-100-chart/` (seed 1, stratified by task and level, chart mode). Paste
or point the agent at one chunk at a time, save each reply file, and ingest as you go.

**One run = one harness + one model + one effort setting.** Several models in the same
harness are separate runs with separate run ids. Never mix models or settings inside a
run; if you change either mid-way, start a new run id.

## 1. Fill the disclosure header once

Every chunk starts with this block. Fill it in once and put it, filled, at the top of
your first reply file (later files may repeat it or leave it out):

```
harness: Cursor 1.x, free tier
model (exactly as the UI shows): <as shown in the model picker>
provider model id (if known): <or leave empty>
effort or thinking setting (or "not shown"): not shown
tools allowed (yes/no): no
operator: <your name or handle>
date: 2026-11-09
```

## 2a. Chat UI (paste)

1. Open a new chat with the chosen model. Paste the whole of `pack-100-chunk-01.md`.
2. Copy the reply into `runs/<run_id>/replies-01.txt` (put the filled header on top of
   this first file). The reply must contain `### <item_id>` lines, each followed by one
   JSON object.
3. Repeat for chunks 02 to 10, one file each, in the same chat or a new one with the same
   model and setting.

## 2b. Terminal or IDE agent (reads and writes files itself)

Give the agent this instruction, once per chunk:

```
Read runs/packs/pack-100-chart/pack-100-chunk-01.md and follow its "How to reply" and
"System prompt" sections exactly. Write your replies to runs/<run_id>/replies-01.txt:
first the disclosure header below, filled in, then for each item a line `### <item_id>`
and one JSON object. Do not read any other file in this repository.
<paste the filled disclosure header>
```

Record whether tools were allowed (`yes`/`no`) honestly; an agent that ran code is a
`system_ui` row, not a bare model.

## 3. Ingest as you go (resumable)

```sh
astro-bench ingest --pack runs/packs/pack-100-chart/pack-100.manifest.json \
  --replies runs/<run_id>/replies-01.txt --replies runs/<run_id>/replies-02.txt \
  --run-id <run_id> --kind system_ui --description "<harness>, <model>, <effort>, <date>" \
  --out results/
astro-bench status --run-id <run_id> --out results/   # which chunk to paste next
```

Re-run `ingest` with the same `--run-id` whenever more reply files arrive; files can be
given in any order and may overlap. A repeated id with a different answer is refused and
reported. Until every id is answered the row is `partial`: listed under "In progress" on
the leaderboard and never ranked. Use `--kind model` only for a bare model with no tools,
`system_ui` for an IDE agent or chat UI.

## 4. Publish

```sh
astro-bench cards && astro-bench leaderboard
```

Commit `runs/<run_id>/` (your reply files), `results/<run_id>.json`,
`results/<run_id>.replies.jsonl` and the regenerated cards and leaderboard.
