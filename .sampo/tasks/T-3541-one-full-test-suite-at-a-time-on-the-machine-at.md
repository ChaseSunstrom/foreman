---
id: T-3541
type: PERFORMANCE
tier: S
status: active
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-11-06T22:04:57Z
updated: 2026-11-07T04:24:26Z
lane: ~/.claude/foreman.lanes/T-3541
lane_branch: foreman/T-3541
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-06T22:17:03Z
plan0_scope: []
group: hook, doctor and UI speed
lane_stop: merged 2026-11-07T04:14:53Z
lane_verified: b588290e3430b9939b83bd1bc14e515d85a56805
---
# One full test suite at a time on the machine: at 16:25 three ran at once (two builders'…
## Raw request
> PERFORMANCE!: one full test suite at a time on the machine: at 16:25 three ran at once (two builders' 16-job runs and the ship's 6-job run, 38 workers on 16 cores, load 30), so each took about three times as long; run.py's full run (no module args) takes a machine-wide slot (flock under the user's cache dir), a second full run waits for it and says so, targeted runs keep running niced; measure two concurrent full runs' wall time before and after
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a full run.py run (no module args) holds a machine-wide slot: a second full run waits for it and prints that it waits and for whom; targeted runs never wait; FOREMAN_NO_SUITE_SLOT=1 skips the slot — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] machine-wide full-suite slot in run.py, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run -k SuiteSlot` → ✗ exit 1 · Ran 1 tests in 123.3s (1 jobs, 16 at a time; slowest: SuiteSlot 121s) / FAILED (1 classes: test_run.SuiteSlot) [ran] [tree d1c74ab08426] [world 2f1906870a] (2026-11-06T22:19:18Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run test_check_paths test_doctor` → exit 0 · Ran 231 tests in 24.1s (119 jobs, 16 at a time; slowest: SuiteSlot.test_the_switch_skips_the_slot_and_a_wait_runs_out_beside_the_holder 9s, ViewsRepair 8s, PerTestJobs.test_a_killed_class_is_timed_and [ran] [tree 208afa631cb2] [world 2f1906870a] (2026-11-06T22:21:34Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run test_check_paths test_doctor` → exit 0 · Ran 231 tests in 17.9s (120 jobs, 16 at a time; slowest: ViewsRepair 11s, SuiteSlot.test_the_switch_skips_the_slot_and_a_wait_runs_out_beside_the_holder 9s, PerTestJobs.test_a_killed_class_is_timed_an [ran] [tree fdeaa4b3a4b8] [world 2f1906870a] (2026-11-06T22:25:56Z)
## Log
- 2026-11-06T22:04:57Z created
- 2026-11-06T22:05:19Z set tier=S
- 2026-11-06T22:05:20Z planned: it has criteria and steps
- 2026-11-06T22:16:58Z lane: ~/.claude/foreman.lanes/T-3541 on foreman/T-3541
- 2026-11-06T22:17:01Z focused
- 2026-11-06T22:17:03Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-07T04:14:53Z merged foreman/T-3541 in merge train
- 2026-11-07T04:24:26Z verified: the full suite is green on 020346f6d, which contains b588290e3
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3177 [PERFORMANCE M, deferred, 3 steps] Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load,…
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
