---
id: T-3366
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py]
depends_on: []
source: followup
created: 2026-11-06T05:55:37Z
updated: 2026-11-06T06:08:18Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a03cf6a68eef026f5
lane_branch: worktree-agent-a03cf6a68eef026f5
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:10Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py]
---
# Hook time limits scale in tests: one FOREMAN_HOOK_SLACK factor (default 1) multiplies hooks.py's fixed limits (fm task new 3 s ~790, queueing 3.2 s ~853, fm focus 3 s ~901, Stop close 25/20 s ~1152/1160), and the test helper's hook() passes busy_factor()
## Raw request
> Hook time limits scale in tests: one FOREMAN_HOOK_SLACK factor (default 1) multiplies hooks.py's fixed limits (fm task new 3 s ~790, queueing 3.2 s ~853, fm focus 3 s ~901, Stop close 25/20 s ~1152/1160), and the test helper's hook() passes busy_factor()
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] NoTaskGate classes pass under simulated load and production limits are unchanged at slack 1 — verify with `python3 plugin/tests/run.py --load 48 test_hooks -k NoTaskGate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] slack constant and helper env
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py --load 48 test_hooks -k NoTaskGate` → exit 0 · Ran 31 tests in 199.3s (6 jobs, 16 at a time; slowest: NoTaskGateClose 25s, NoTaskGateMulti 23s, NoTaskGateKinds 19s) / OK (ran] (tree afec363fa052] (world 2f1906870a] (2026-11-06T06:08:18Z)
## Log
- 2026-11-06T05:55:37Z created
- 2026-11-06T05:56:07Z focused
- 2026-11-06T05:56:10Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
