---
id: T-1437
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T21:21:06Z
updated: 2026-10-21T21:50:20Z
base: 48df981c4bf959552ed82236a38e489be597097e
base_tree: 44850c6e72aa2e72e4a04c323b5d689ec250d1cb
plan0_at: 2026-10-21T21:33:38Z
plan0_scope: []
verified: strong
---
# With the mascot off, a running subagent's time still updates: the poll repaints when its shown time changes
## Raw request
> foreman-ui: with mascot off, a running subagent's 'quiet Nm' row (and other time-based text) never advances — only the mascot's 2 s blink re-renders the pane between full refreshes; repaint on the poll while a subagent runs, at most once a minute for minute-resolution text (found in T-1427)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with mascot and motion off, a quiet subagent's row reads 'quiet 11m' after 11 minutes and offers Stop, and the subagent-row test runs well inside its 5 s budget (repaints only when the shown text changes) — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the subagent-row test gets { options: { motion: 'off', mascot: 'off' } } (red: the row never re-renders); in tick, with the mascot off, bump beat only when a running subagent's shown time or quiet/stop state changes
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 124 tests across 2 files. [30.13s] [ran] [tree 06197ba96f7d] (2026-10-21T21:34:25Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 125 tests across 2 files. [57.57s] [ran] [tree 223f76c04e9e] (2026-10-21T21:46:38Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 125 tests across 2 files. [51.81s] [ran] [tree a286c662fb8c] (2026-10-21T21:47:49Z)
- (audit intent) `self: tick reads the running subagents first; with the mascot on it blinks as before; with it off it bumps beat only when a running subagent's shown text (seconds under an hour, quiet and stop state) changes; the pane render now always reads beat so a bump redraws, while the mascot animation still uses 0 when off` → with the mascot off a quiet subagent row counts up between polls (new mod test); the subagent-row test passes 3 of 3 in about a second at load 40-60 [tree a286c662fb8c] (2026-10-21T21:47:49Z)
- (audit edge) `self: tick reads the running subagents first; with the mascot on it blinks as before; with it off it bumps beat only when a running subagent's shown text (seconds under an hour, quiet and stop state) changes; the pane render now always reads beat so a bump redraws, while the mascot animation still uses 0 when off` → with no subagent running and the mascot off, the poll never bumps beat (no idle repaints); with the mascot on, behaviour is unchanged [tree a286c662fb8c] (2026-10-21T21:47:49Z)
- (audit self) `self: tick reads the running subagents first; with the mascot on it blinks as before; with it off it bumps beat only when a running subagent's shown text (seconds under an hour, quiet and stop state) changes; the pane render now always reads beat so a bump redraws, while the mascot animation still uses 0 when off` → no findings [tree a286c662fb8c] (2026-10-21T21:47:49Z)
## Log
- 2026-10-21T21:21:06Z created
- 2026-10-21T21:33:36Z planned from capture
- 2026-10-21T21:33:37Z focused
- 2026-10-21T21:46:39Z scope: also T-1427's fix — the subagent-row test mounts its pane after the 11 fake minutes (0.3-1.2 s, was 5 s+); both in mods/foreman-ui/tests/foreman-ui.test.tsx
- 2026-10-21T21:50:17Z done
- 2026-10-21T21:50:20Z committed e60a679a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1026-review: MEDIUM** `mods/foreman-ui/hooks/register.tsx:1736-1742` — the Agents bars do not stay in one column when a stop button shows. [stale: mods/forema…
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- decision 2026-10-09: Added JARVIS (<user>@<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
## Regression test
foreman-ui.test.tsx 'with the mascot off a quiet subagent row still counts up (T-1437)': mounted at 2m01s, then +20 s must read 'quiet 2m 2Xs'; before the fix the pane never redrew with the mascot off (step 1 red run: the row test failed with mascot off)
## Why not caught
tests always ran with the mascot on, whose blink hid the missing repaint
## Lessons
- When a test times out on fake time, look at what renders during the advance: mounting after the advance tests the same state without hundreds of redraws
## Plan gaps
- failed first: step 1 the subagent-row test gets { options: { motion: 'off', mascot: 'off' } } (red: the row never re-ren…
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
