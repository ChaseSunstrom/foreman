---
id: T-1041
type: FEATURE
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T03:37:24Z
updated: 2026-10-16T08:02:15Z
base: b679927353303c7a5c53ec00825544aebd8e44e7
base_tree: 068738d1e7d32aa5e90985195929d199c5bda6e9
plan0_at: 2026-10-16T07:56:42Z
plan0_scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: strong
---
# Register.tsx:68` resets `treeTall` only in turn.start. `feed.length = 0` at line 537 (new
## Raw request
> register.tsx:68` resets `treeTall` only in turn.start. `feed.length = 0` at line 537 (new session) does not reset it, which is harmless but inconsistent
> (noticed by an agent; research T-1039-review)
## Interpretation
treeTall (the band tree's height, which never shrinks mid-turn) is reset only on the first turn.start; session.start empties the feed but keeps the old height, so a new session's first turn may start with blank padding rows.
## Assumptions (confidence)
## Acceptance criteria
- [x] after a new session starts, the band tree has no pad rows left over from the old session's tall tree — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Reset treeTall with the feed in session.start: one assignment. A test: a tall tree, then session.start, then a short turn has no pad rows.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then reset treeTall in session.start
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 118 tests across 1 file. [12.62s] [ran] [tree fcfb8f5cf0be] (2026-10-16T08:00:25Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 118 tests across 1 file. [11.34s] (start tree + this task's tests) [ran] [tree fcfb8f5cf0be] (2026-10-16T08:00:49Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 118 tests across 1 file. [11.35s] [ran] [tree fcfb8f5cf0be] (2026-10-16T08:00:49Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 118 tests across 1 file. [15.94s] [ran] [tree cf7ed46ced1e] (2026-10-16T08:01:14Z)
- (audit self) `self: one assignment beside the feed reset in session.start; the test counts pad rows (red without it, 118/118 with it); a just-finished subagent can still add a row, which is intended` → no findings [tree cf7ed46ced1e] (2026-10-16T08:01:14Z)
## Log
- 2026-10-16T03:37:24Z created
- 2026-10-16T07:56:38Z set tier=S
- 2026-10-16T07:56:39Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md']
- 2026-10-16T07:56:42Z focused
- 2026-10-16T08:00:12Z hypothesis: the extra row after the reset was a just-finished subagent still shown, not treeTall; counting tree-pad rows isolates the reset (passes with the fix; prove checks it fails without)
- 2026-10-16T08:02:13Z done
- 2026-10-16T08:02:15Z committed 0f83aae (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1039-review: HIGH** `mods/foreman-ui/hooks/rows.tsx:578-579, 594-595, 619-621`. The time bars are not in one aligned column. [stale: mods/foreman-ui/hooks/reg…
- research T-1033-review: Verdict: changes needed.** Acceptance criterion 2 ("idle it shrinks to one summary line") is not implemented, and nothing tests it. I only read t…
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Preflight
Changed in scope since this was planned (2026-10-16): CHANGELOG.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx; re-ground the plan against them before editing
## Lessons
- Per-session module state resets in session.start together, or not at all
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
