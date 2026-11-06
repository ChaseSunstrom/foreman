---
id: T-0912
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:12:38Z
updated: 2026-10-15T19:16:46Z
base: 6e3d0b2af23fdd407a0aa9130bb49cd68931636f
base_tree: b56e65371192222cef6a88b9d75238f761621bc4
verified: strong
---
# foreman-ui motion setting: full (30 fps charts) · calm (8 fps, no blit) · off (still: no clocks, static glyphs)
## Raw request
> foreman-ui motion setting: full (30 fps charts) · calm (8 fps, no blit) · off (still: no clocks, static glyphs)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] motion off starts no clocks and draws the rail still; calm draws but never blits — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] userConfig motion + cfg; wake() honours it; a test per level
## Resume here
## Docs impact
CHANGELOG (Motion setting); the option's own description in plugin.json
## Verification evidence
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 2 fail / Ran 78 tests across 1 file. [6.55s] (start tree + this task's tests) [ran] [tree b45d93a284c3] (2026-10-15T19:16:38Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 78 tests across 1 file. [5.89s] [ran] [tree b45d93a284c3] (2026-10-15T19:16:38Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 78 tests across 1 file. [5.85s] [ran] [tree b45d93a284c3] (2026-10-15T19:16:45Z)
- (step 1) `claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.agents, foreman-ui.away, foreman-ui.beat, foreman-ui.ctx, foreman-ui.error, foreman-ui.files, foreman-ui.frame, foreman-ui.resumed, foreman-ui.shells, foreman- [ran] [tree b45d93a284c3] (2026-10-15T19:16:45Z)
- (audit edge) `self: tests count the blits (ui.blit hook): full > 5 over 320 ms, calm 0 with the rail still moving per frame, off 0 blits and one still frame with no spinner; off also skips the step glow, which needs a clock to fade` → motion off still redraws on the 2 s poll and on every atom change, so nothing goes stale; only animation stops [tree b45d93a284c3] (2026-10-15T19:16:45Z)
- (audit self) `self: tests count the blits (ui.blit hook): full > 5 over 320 ms, calm 0 with the rail still moving per frame, off 0 blits and one still frame with no spinner; off also skips the step glow, which needs a clock to fade` → no findings [tree b45d93a284c3] (2026-10-15T19:16:45Z)
## Log
- 2026-10-15T19:12:38Z created
- 2026-10-15T19:13:56Z focused
- 2026-10-15T19:16:46Z done
- 2026-10-15T19:16:46Z committed 600426a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- T-0681 [FEATURE M, done, 5 steps] Milestone: Features — UI and motion — lesson: Put new UI facts in the one view model first; the mod's change is then a pure render with…
- decision 2026-10-14: [costly] Turned compact output on for the user (fm compact-output on)
- similar past tasks were M: consider --tier M
- the similar finished task took 5 steps
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/.claude-plugin/plugin.json
- CHANGELOG.md
