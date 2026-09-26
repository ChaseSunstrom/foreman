---
name: status
description: Use when the user asks where things stand (STATUS, "what's going on", "what's left", /foreman:status). Shows Foreman status for this project in at most 25 lines — active task and step, queue, inbox, blocked items, pending approvals, autonomy, hygiene.
---

# Foreman: status

Run `fm state` and `fm queue`, then report in ≤ 25 lines:
- Active task: id, type, tier, title, step n/m and the step text; last evidence line.
- Queue in canonical order (≤ 8 lines), marking urgent (!) and unapproved L/`?` items.
- Inbox count and the oldest items; blocked items with reasons.
- Pending approvals (`fm ask`) and autonomy (standard/full).
- Hygiene: last tidy, cycles or dangling dependencies, sensitive flag, drive on/off/paused.
No edits, no state changes.
