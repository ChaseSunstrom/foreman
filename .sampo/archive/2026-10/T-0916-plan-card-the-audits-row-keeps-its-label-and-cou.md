---
id: T-0916
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:22:31Z
updated: 2026-10-15T19:23:28Z
base: b6e32590e051558beda54340d4255ad656827266
base_tree: b32232764986be465ca75f1e13e50c8693a41e77
verified: strong
---
# Plan card: the audits row keeps its label and count whole in a narrow pane (it wrapped to 'audit/s', '0//1')
## Raw request
> Plan card: the audits row keeps its label and count whole in a narrow pane (it wrapped to 'audit/s', '0//1')
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the audits label and count never shrink; the blocker text truncates instead — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] flexShrink 0 on the audits label, bar and count; a test on the props
## Resume here
## Docs impact
## Verification evidence
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 80 tests across 1 file. [6.30s] (start tree + this task's tests) [ran] [tree b50d5dcdc69a] (2026-10-15T19:23:20Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 80 tests across 1 file. [6.27s] [ran] [tree b50d5dcdc69a] (2026-10-15T19:23:20Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 80 tests across 1 file. [6.25s] [ran] [tree b50d5dcdc69a] (2026-10-15T19:23:27Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 80 tests across 1 file. [6.25s] [ran] [tree b50d5dcdc69a] (2026-10-15T19:23:27Z)
- (audit edge) `self: the label, bar and count sit in one Box that never shrinks; the blocker text is the one that truncates (seen wrapped in the re-recorded demo at 70 columns)` → the hero's progress row has no long text beside its count, so it can't squeeze it [tree b50d5dcdc69a] (2026-10-15T19:23:27Z)
- (audit self) `self: the label, bar and count sit in one Box that never shrinks; the blocker text is the one that truncates (seen wrapped in the re-recorded demo at 70 columns)` → no findings [tree b50d5dcdc69a] (2026-10-15T19:23:27Z)
## Log
- 2026-10-15T19:22:31Z created
- 2026-10-15T19:22:32Z focused
- 2026-10-15T19:23:28Z done
- 2026-10-15T19:23:28Z committed f1eee07 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0137 [FEATURE M, done, 3 steps] Everything in the chat: shell rows with their output formatted inline, folded command groups unfolded, the pane's Output card gone — le…
- T-0914 [FEATURE M, done, 1 steps] foreman-ui foldable cards: the quieter cards (pulse, files, fleet, gates, brainstorm, spend, bench, research, activity) fold to their h…
- T-0146 [FEATURE M, done, 3 steps] Dashboard: no duplicates between band and pane, nothing stale or cut without saying so, controls that read as actions — lesson: Record …
- decision 2026-10-15: Pane order: Needs you and waiting plans above the hero (T-0909)
- similar past tasks were M: consider --tier M
- similar finished tasks took 1–3 steps
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
