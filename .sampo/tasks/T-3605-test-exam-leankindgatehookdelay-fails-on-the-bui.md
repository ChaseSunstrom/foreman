---
id: T-3605
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T04:15:29Z
updated: 2026-11-07T04:53:24Z
lane: ~/.claude/foreman.lanes/T-3605
lane_branch: foreman/T-3605
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T04:15:38Z
plan0_scope: []
---
# test_exam.LeanKindGateHookDelay fails on the build branch and blocks merges
## Raw request
> test_exam.LeanKindGateHookDelay fails on the build branch and blocks merges
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] LeanKindGateHookDelay passes 10 runs in a row under load — verify with `nice -n 10 python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce and find the cause
2. [x] fix
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · Ran 37 tests in 45.1s (8 jobs, 16 at a time; slowest: GateEndToEnd 0s, AaFixtures 0s, WhichDiffsAreTimed 0s) / FAILED (1 classes: test_selfgate.LoadedWallCheck) [ran] [tree dfe7436c4a05] [world 2f1906870a] (2026-11-07T04:26:42Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 37 tests in 10.9s (8 jobs, 16 at a time; slowest: GateEndToEnd 0s, WhichDiffsAreTimed 0s, BaseCache 0s) / OK [ran] [tree dd7e6498d5f7] [world 2f1906870a] (2026-11-07T04:27:27Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_exam` → exit 0 · Ran 120 tests in 133.1s (106 jobs, 16 at a time; slowest: LeanKindGateHookDelay 108s, LeanKindGateGuardAllow 69s, LeanKindGateSessionLine 64s) / OK [ran] [tree 9358a40379a0] [world 2f1906870a] (2026-11-07T04:53:24Z)
## Log
- 2026-11-07T04:15:29Z created
- 2026-11-07T04:15:33Z lane: ~/.claude/foreman.lanes/T-3605 on foreman/T-3605
- 2026-11-07T04:15:38Z focused
- 2026-11-07T04:15:38Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:28:39Z cause: not a regression; a load flake. Loaded (>1 per CPU) the gate flags a waiting hook only on a wall-median doubling past 100 ms; the exam planted a fixed 250 ms, so once load slowed every one of the 16 fixtures' base wall past 250 ms (train at 44/16 CPUs) no row named 'hook '. Probe at 1.9-3.2 per CPU: base walls 46-1670 ms, noise up to 3x per fixture. Fix: plant c.load_scaled(0.25).
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2510 [FIX M, dropped, 0 steps] CI failed on this branch: run 41349606220
- T-2492 [FIX M, done, 3 steps] CI failed on this branch: run 41330915735 — lesson: a test that compares paths must compare real paths: macOS's temp folder is a symlink, s…
- T-2457 [FIX M, dropped, 0 steps] CI failed on this branch: run 41281493678
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
