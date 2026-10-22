---
name: status
description: Use when asked where things stand (STATUS, "what's left"): Foreman's status in at most 25 lines.
---

# Foreman: status

Run `fm state` and `fm queue`, then report in ≤ 25 lines:
- Active task: id, type, tier, title, step n/m and the step text; last evidence line.
- Queue in canonical order (≤ 8 lines), marking urgent (!) and unapproved L/`?` items.
- Inbox count and the oldest items; blocked items with reasons.
- Pending approvals (`fm ask`) and autonomy (standard/full).
- Hygiene: last tidy, cycles or dangling dependencies, sensitive flag, drive on/off/paused.
No edits, no state changes.

Elsewhere: a shell prompt or status bar polls `fm glance` (one JSON line); `fm timeline ID > run.json` exports a task's
run for ui.perfetto.dev (`--otlp` for OpenTelemetry); an editor runs `fm lsp` (stdio) to see a brief's proof gaps.
