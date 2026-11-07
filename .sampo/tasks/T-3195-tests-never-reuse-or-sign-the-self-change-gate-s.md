---
id: T-3195
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T11:04:52Z
updated: 2026-11-05T11:10:36Z
base: abc778eaf3e21b3dd73d0f6d131f26df9116a0b7
base_tree: 92b27fab0a8620ca1ff040c4bbbf4e21f54f24b7
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T11:04:54Z
plan0_scope: []
verified: strong
---
# Tests never reuse or sign the self-change gate's base cache with the user's key: test_lanes.SelfChangeGate calls gate() twice per test and the second reused the first's cached base verdicts and bench (red on main since T-3176); in-process tests read the real ~/.config/sampo/selfgate.key
## Raw request
> Tests never reuse or sign the self-change gate's base cache with the user's key: test_lanes.SelfChangeGate calls gate() twice per test and the second reused the first's cached base verdicts and bench (red on main since T-3176); in-process tests read the real ~/.config/sampo/selfgate.key
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_lanes.SelfChangeGate passes on main, each gate() call judges afresh, and no in-process test reads or writes the real selfgate.key (ForemanTestCase points it at the test's temp dir) — verify with `python3 plugin/tests/run.py test_lanes.SelfChangeGate test_selfgate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] isolate the key in ForemanTestCase and clear the base cache between SelfChangeGate's gate calls
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.SelfChangeGate test_selfgate` → exit 0 · Ran 50 tests in 8.9s (8 classes, 16 at a time; slowest: SelfChangeGate 8s, GateEndToEnd 0s, AaFixtures 0s) / OK [ran] [tree e71adc4341c4] [world 2f1906870a] (2026-11-05T11:05:15Z)
- `python3 plugin/tests/run.py test_helpers_env test_lanes.SelfChangeGate` → exit 0 · Ran 19 tests in 13.1s (3 classes, 16 at a time; slowest: SelfChangeGate 10s, GitEnvIsolation 0s, GateKeyIsolation 0s) / OK (start tree + this task's tests) [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:05:56Z)
- `python3 plugin/tests/run.py test_helpers_env test_lanes.SelfChangeGate` → exit 0 · Ran 19 tests in 7.9s (3 classes, 16 at a time; slowest: SelfChangeGate 7s, GitEnvIsolation 0s, GateKeyIsolation 0s) / OK [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:05:56Z)
- (step 1) `cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/red-T-3195 && python3 plugin/tests/run.py test_lanes.SelfChangeGate` → ✗ exit 1 · Ran 16 tests in 17.2s (1 classes, 16 at a time; slowest: SelfChangeGate 13s) / FAILED (1 classes: test_lanes.SelfChangeGate) [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:06:43Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.SelfChangeGate test_selfgate test_helpers_env` → exit 0 · Ran 53 tests in 19.7s (10 classes, 16 at a time; slowest: SelfChangeGate 19s, GateEndToEnd 1s, GitEnvIsolation 0s) / OK [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:07:04Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.SelfChangeGate test_selfgate` → exit 0 · Ran 50 tests in 27.0s (8 classes, 16 at a time; slowest: SelfChangeGate 23s, GateEndToEnd 1s, BaseCache 1s) / OK [ran] [tree 1aa4dec9a3a5] [world 2f1906870a] (2026-11-05T11:08:10Z)
- (audit edge) `self: the gate's cache key is the base tree + settings, so two gate() calls in one test shared it; SelfChangeGate now clears the base cache per call, and every SampoTestCase points selfgate._keyfile at its temp dir (GateKeyIsolation asserts it); red on HEAD in a detached worktree (2 of 16), green after (53 tests)` → test_selfgate.BaseCache and KeyPath use plain TestCase with their own patches, unaffected; subprocess CLI tests don't reach the cache (scratch repos aren't Foreman, so the gate returns first) [tree 1aa4dec9a3a5] (2026-11-05T11:08:10Z)
- (audit self) `self: the gate's cache key is the base tree + settings, so two gate() calls in one test shared it; SelfChangeGate now clears the base cache per call, and every SampoTestCase points selfgate._keyfile at its temp dir (GateKeyIsolation asserts it); red on HEAD in a detached worktree (2 of 16), green after (53 tests)` → no findings [tree 1aa4dec9a3a5] (2026-11-05T11:08:10Z)
## Log
- 2026-11-05T11:04:52Z created
- 2026-11-05T11:04:53Z focused
- 2026-11-05T11:04:54Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T11:06:13Z red: on main abc778ea (before this fix) test_lanes.SelfChangeGate failed 2 of 16 (base verdicts and bench reused from the first gate call) - recorded in T-3143's step-1 evidence and rerun by hand; prove can't show it because the fix lives in test files (helpers.py, test_lanes.py), which prove carries onto the start tree
- 2026-11-05T11:10:26Z done
- 2026-11-05T11:10:36Z committed 29c887af (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3176 [PERFORMANCE S, done, 2 steps] A gated merge benches the base tree once per base commit: the self-change gate caches the base side's bench and guard replay by the…
- T-3192 [SECURITY S, active, 2 steps] Selfgate's MAC key path follows SAMPO_SECRETS/FOREMAN_SECRETS (via models.secrets_path),…
- T-3139 [PERFORMANCE M, done, 2 steps] Fast merges part 1: the bench records which modules each hook really imports, and the self-change gate times hooks only when a diff…
- decision 2026-11-05: merge speed order: T-3118 (bench only the hook path) first, the biggest cut; then T-3109 (closes yield to a waiting merge), T-3120 (closes reuse a g…
- similar finished tasks took 2–2 steps
## Regression test
test_lanes.SelfChangeGate itself plus test_helpers_env.GateKeyIsolation. The fix lives in test files, which prove carries onto the start tree, so the red was recorded in a detached worktree of HEAD (evidence: ✗ exit 1, SelfChangeGate 2 of 16 failing) and the green on the fixed tree (53 tests OK)
## Lessons
- a merge that adds a cache to a function must run every test module that calls the function more than once per test; T-3176's affected set skipped test_lanes
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_lanes.py
- plugin/tests/test_helpers_env.py
