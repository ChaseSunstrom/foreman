---
id: T-1427
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T20:28:16Z
updated: 2026-10-21T21:59:37Z
base: a55b263cc3c8f57805a8c6da21006b835c21077c
base_tree: 2d587d36d46561e6d538ce7118314f380118ef3e
plan0_at: 2026-10-21T21:12:16Z
plan0_scope: []
verified: strong
---
# The UI mod's subagent-row test runs without the redraw timer, so it can't time out under load
## Raw request
> mods/foreman-ui test 'a subagent the engine no longer lists leaves; a quiet one shows how long and can be stopped' times out at 5000 ms under load (~50); make it wait on its condition, not a fixed budget (seen during T-1388's close)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the subagent-row test finishes well under its 5 s budget (motion off: no 120 ms redraw timer firing ~5,500 times across 11 fake minutes) and still checks quiet 11m, Stop, and the row leaving — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] give the test { options: { motion: 'off' } } like the motion-off test; run the mod suite and time that test
## Resume here
## Docs impact
CHANGELOG line (with T-1437)
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 124 tests across 2 files. [41.87s] [ran] [tree 4eb7e168e295] (2026-10-21T21:13:51Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 125 tests across 2 files. [23.46s] [ran] [tree a286c662fb8c] (2026-10-21T21:50:58Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 125 tests across 2 files. [34.82s] [ran] [tree a286c662fb8c] (2026-10-21T21:51:34Z)
- (audit intent) `self: the test now mounts its pane after advancing 11 fake minutes, so the 2 s poll and frame timers fire without a pane to render; it checks the same state (quiet 11m, Stop, the row leaving); the mascot-off repaint it exposed is fixed and tested in T-1437` → the subagent-row test passes 3 of 3 at load 40-60 in 0.3-1.2 s (was 5 s timeouts) [tree a286c662fb8c] (2026-10-21T21:51:34Z)
- (audit edge) `self: the test now mounts its pane after advancing 11 fake minutes, so the 2 s poll and frame timers fire without a pane to render; it checks the same state (quiet 11m, Stop, the row leaving); the mascot-off repaint it exposed is fixed and tested in T-1437` → the row's live updating while mounted is covered by T-1437's test [tree a286c662fb8c] (2026-10-21T21:51:34Z)
- (audit self) `self: the test now mounts its pane after advancing 11 fake minutes, so the 2 s poll and frame timers fire without a pane to render; it checks the same state (quiet 11m, Stop, the row leaving); the mascot-off repaint it exposed is fixed and tested in T-1437` → no findings [tree a286c662fb8c] (2026-10-21T21:51:34Z)
## Log
- 2026-10-21T20:28:16Z created
- 2026-10-21T21:12:14Z planned from capture
- 2026-10-21T21:12:16Z focused
- 2026-10-21T21:21:07Z blocked: 3 attempts: motion off (removes ~5,500 frame timers; still 2.8-5 s at load 40-50), a per-test timeout option (ignored by claude plugin test; the 5 s budget is fixed), mascot off (0.7 s but the row never re-renders — product gap captured). Cause: 330 pane re-renders from the 2 s poll's mascot beat across the test's 11 fake minutes (STOP_MS is 10 min). Fix options: repaint time-based text once a minute instead of every poll (then the test is cheap), or test quiet/stop with shorter thresholds injected through cfg
- 2026-10-21T21:50:31Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-21T21:50:31Z focused
- 2026-10-21T21:59:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1132 [FIX S, done, 1 steps] Mod test 'the tap is cheap on a long one-line step… (T-1090)' times out at 5 s under load — lesson: A test that times out under load usuall…
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- T-0121 [FIX M, done, 3 steps] A subagent that ended without its finish event stays 'running' for hours in the dashboard — lesson: Never derive 'still running' from the a…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Why not caught
the suite ran mostly on an idle machine until today
## Lessons
- When a test times out on fake time, look at what renders during the advance
## Plan gaps
- failed first: step 1 give the test { options: { motion: 'off' } } like the motion-off test; run the mod suite and time t…
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- mods/foreman-ui/hooks/register.tsx
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmmodels.py
- plugin/skills/improve/SKILL.md
- plugin/tests/test_bench.py
- plugin/tests/test_code_hardening.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_runner_lint.py
