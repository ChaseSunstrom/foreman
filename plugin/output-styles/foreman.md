---
name: Foreman
description: Foreman progress format — task, stage and step first, one line per verification, changes summarized, then what's next and anything that needs the user.
keep-coding-instructions: true
---

# Foreman reply format

Use this format when the session has Foreman context (a "Foreman project …" note at session start, "Active: …" or "Next: …" notes). Without it, answer normally.

- First line, when a task is active: `▌T-0012 · FEATURE L · executing · step 3/5` (id, type and tier, stage, step), taken from Foreman's notes.
- For each step you work on: `▸ Step 3/5 — <step title>`, then one line per check you ran: `✓ <command> → <real result>` or `✗ <command> → <what failed>`.
- Summarize code changes as `Changed: <file> — <why>` instead of pasting code the user can already see in the tool output.
- New requests you captured: `⚑ Captured T-0021 — <title>`. Decisions you made without asking: `◆ Decided: <choice> (<why>)`.
- End with `Next: <the next action>`, and add `⚠ Needs you: <the one yes/no question or decision>` only when something does.
- Keep prose short: no headings or bullet lists for a one-paragraph answer, no restating the plan, no closing summary of what you just showed.
