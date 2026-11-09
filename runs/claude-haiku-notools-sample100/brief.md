# Verbatim brief given to the agent

Operator: the Astro-Bench maintainer's Claude Code session (main model Claude Fable 5.1), which spawned a subagent with the Agent tool and `model: "haiku"`. Effort setting: the Claude Code default for subagents; the brief did not set one and the operator cannot read it back, so it is recorded as "default, unknown". Paths are shortened to `<pack path>`.

```
You are being measured as a bare language model on Astro-Bench. Rules, strictly: you may call exactly two tools, `Read` once to load the pack file, and `Write` once at the end to save your replies. No Bash, no Python, no web, no other files, no calculators of any kind. Every answer must come from your own knowledge and reasoning; if you cannot compute something (for example exact planetary positions from a birth date), give your best estimate and set a low `confidence`, or follow the pack's instruction for abstaining on citations. Never invent a chapter or verse you are not sure of; an empty `citations` list scores better than a wrong one.

1. Read `<pack path>/pack-100-chart.md` (100 items). Follow its "How to reply" and "System prompt" sections exactly.
2. Answer all 100 items. For each, write a line `### <item_id>` (the id exactly as shown in backticks in the item header) followed by one JSON object on the next line(s) in the required shape. Keep going until item 100; do not skip any, do not stop early, do not summarise.
3. Write the full reply text to `<pack path>/replies-claude-<model>-notools.txt` with one Write call. Then report in two sentences: how many items you answered and that you used no tools beyond Read and Write.
```
