# Verbatim brief given to the agent

Operator: the Astro-Bench maintainer's Claude Code session (main model Claude Fable 5.1), which spawned a subagent with the Agent tool and `model: "sonnet"`, all tools available. Effort setting: the Claude Code default for subagents; recorded as "default, unknown". Paths are shortened to `<pack path>` and `<scratch>`.

```
You are being measured as a coding-agent harness ("Claude Code, Sonnet, tools allowed") on Astro-Bench, the way an IDE agent would be: you may use any tool you like (Bash, Python, files, the internet is NOT available) to compute answers, exactly as a developer's AI assistant would when asked these questions. You must NOT read anything inside `<the benchmark repo>` or `<the research repo>` (those hold the benchmark's own gold and oracle; reading them is cheating), and you must not open any file under `items/`, `results/`, `canon/` or `vendor/` anywhere. You may install or use general-purpose libraries available on this machine (for example `pip install pyswisseph` into a fresh venv in your scratch folder `<scratch>/claude-code-run/`), as any developer could. For citations, cite only what you actually know; an empty list scores better than a wrong verse.

1. Read `<pack path>/pack-100-chart.md` (100 items) and follow its "How to reply" and "System prompt" sections exactly, including the stated convention per item (ayanamsa, node model, house system).
2. Answer all 100 items; for each write `### <item_id>` then one JSON object. Do not skip or stop early.
3. Write the replies to `<pack path>/replies-claude-code-sonnet-tools.txt`.
4. Report in under 120 words: which tools and libraries you used, the time taken, and confirm you did not read the forbidden folders.
```
