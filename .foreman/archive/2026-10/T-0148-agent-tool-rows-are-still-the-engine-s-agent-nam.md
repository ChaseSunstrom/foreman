---
id: T-0148
type: FEATURE
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/**, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T06:51:29Z
updated: 2026-10-03T07:18:11Z
base: f999a8042421f937f59614ad71e08716f03e1aca
base_tree: 669eb98437fe0269117b93d4df3ff3ba08233d6b
verified: ok
---
# Agent tool rows as Foreman rows; the resume prompt's compact row also matches its text
## Raw request
> Agent tool rows are still the engine's (agent name on a highlighted background block, 'Backgrounded agent (↓ to manage · ctrl+o to expand)'): draw them as Foreman rows (◆ type · description · in the background / done · N tools) — seen in a live snapshot
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finished subagent call reads ✓ ◆ type, description, tools · time · tokens and its report's first line (no highlighted block); a background launch reads 'in the background'; the engine's block under it is blanked; the resume prompt is one line whether or not its origin says plugin — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests, then rows; sync
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 56 tests across 1 file. [2.37s] [ran] [tree 131a7e0e06b5] (2026-10-03T07:17:41Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 56 tests across 1 file. [2.37s] [ran] [tree 131a7e0e06b5] (2026-10-03T07:17:41Z)
- (audit self) `self: the row draws only for a completed or background-launched result (errors keep the engine's row); the result block is blanked only in that case; report text goes through clean(); live check comes with the next subagent call after the reload` → no findings [tree 131a7e0e06b5] (2026-10-03T07:17:41Z)
## Log
- 2026-10-03T06:51:29Z created
- 2026-10-03T07:16:01Z planned from capture
- 2026-10-03T07:16:01Z focused
- 2026-10-03T07:17:41Z done
- 2026-10-03T07:18:11Z finding: Claude Code draws a plugin-submitted prompt outside the UserMessage render site (a probe fired for task-notification rows only), so its grey block can't be restyled by a mod
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0141 [FEATURE M, done, 3 steps] Clean tool rows: Edit/Write results as Foreman rows with a compact coloured diff; shell commands wrap under themselves — lesson: Snapsh…
- T-0143 [FEATURE M, done, 3 steps] Foreman-styled turn: replies, a Foreman working line instead of the engine's spinner and tip, shell rows that read like the running row…
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- T-0122 [FEATURE M, done, 4 steps] UI polish from the live render: narrow band, colored type words, quiet controls, human next, cleaner header and footer — lesson: Judge …
- likely tests for the scope: plugin/tests/test_shot.py
## Files touched
- CHANGELOG.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
