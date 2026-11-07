---
id: T-3614
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T04:38:05Z
updated: 2026-11-07T04:55:06Z
lane: ~/.claude/foreman.lanes/T-3614
lane_branch: foreman/T-3614
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T04:43:56Z
plan0_scope: []
---
# PERFORMANCE (merge latency, user 2026-11-06: why is merging so slow): the merge train's…
## Raw request
> PERFORMANCE (merge latency, user 2026-11-06: why is merging so slow): the merge train's gate test run takes CPU slots from the same machine-wide pool as every builder lane's test run (run.py cpu_slot ~81, 16 slots, each waiter polls every 50 ms), so with ~10 builders testing at load 40 the train, the one critical path, gets about 1/N of the slots and its gate takes 20+ min; nice doesn't help a slot wait. Give the train's (and ship's) runs priority: while a priority run waits for a slot, lane runs don't take a freed one (e.g. a prio-<pid> marker in the slot folder that low-priority waiters check), and builder runs default to low priority; measure the gate's wall with 8 builders testing, before and after
## Interpretation
Reading 1 (chosen): priority runs (the train's gate and probes, sampo ship's suite, sampo check in the main checkout) get first claim on slots freed in run.py's machine-wide pool while they wait; every other run (lanes by default) leaves freed slots to them. Reading 2 (ruled out): renice or cap the builders' runs: nice doesn't help a slot wait, and a cap idles CPU while no train runs.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A priority waiter gets a freed slot ahead of a low waiter on a full pool, and a dead priority waiter's marker blocks nobody — verify with `nice -n 10 python3 plugin/tests/run.py test_slots`
- [ ] The train's gate and the main checkout's sampo check run with SAMPO_SLOT_PRIORITY=1, a lane's sampo check without it — verify with `nice -n 10 python3 plugin/tests/run.py test_lane_train.SlotPriority`
## Non-goals
## Approach (options → choice → why)
1) prio markers: a flock'd prio-<pid>-<n> file in the slot folder while a priority waiter waits; low waiters skip a pass while one is live. Likely outcome: the train takes each freed slot; fails if old-code lanes (not rebased) ignore the marker until they rebase. 2) reserve k slots for priority runs: fails because it idles k CPUs while no train runs and still splits the rest 1/N. 3) a FIFO ticket queue under a lock: fair, not prioritized, more state and stale tickets; likely outcome: no gain for the train. 4) use what exists: suite_slot (T-3541) serializes full suites only, not per-class slots; the train probe already runs niced; fails if: nice and the suite slot don't touch a per-class slot wait, so no gain. 5) do less: SAMPO_SLOTS per lane; fails if: it caps lanes even while nothing waits, idling CPU. Choice 1 (80%): one folder scan per poll, the kernel drops a dead waiter's lock, nothing reserved while no priority run waits. Priority = SAMPO_SLOT_PRIORITY=1 (unset or 0: low), set unless already set by run_command(priority=True) in the train, ship's env, sampo check when not in a lane.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: priority waiter wins a freed slot; dead marker blocks nobody; train/check wiring  <- CURRENT
2. [x] run.py: prio markers in cpu_slot; low waiters skip a pass while one is live
3. [x] Wire SAMPO_SLOT_PRIORITY into train gate/probes, ship's env, sampo check outside lanes
4. [x] Measure one class's wall under 4 low runs filling the pool, before and after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_slots test_lane_train.SlotPriority` → ✗ exit 1 · Ran 12 tests in 45.2s (2 jobs, 16 at a time; slowest: Slots 36s, SlotPriority 5s) / FAILED (2 classes: test_slots.Slots, test_lane_train.SlotPriority) [ran] [tree 2a05d75a0f2a] [world 2f1906870a] (2026-11-07T04:45:34Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_slots` → exit 0 · Ran 11 tests in 78.0s (1 jobs, 16 at a time; slowest: Slots 3s) / OK [ran] [tree 6cda2d9afd53] [world 2f1906870a] (2026-11-07T04:52:34Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_check_paths test_ship test_slots` → exit 0 · Ran 105 tests in 62.8s (9 jobs, 16 at a time; slowest: Ship 52s, Train 29s, CheckSkip 10s) / OK [ran] [tree 369640cc4793] [world 2f1906870a] (2026-11-07T04:53:45Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_slots test_lane_train.SlotPriority` → exit 0 · Ran 13 tests in 19.8s (2 jobs, 16 at a time; slowest: Slots 3s, SlotPriority 1s) / OK [ran] [tree 369640cc4793] [world 2f1906870a] (2026-11-07T04:54:50Z)
- (step 4) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3614-bench/bench.sh new` → exit 0 · new full pool, run 2: 1166 ms / new full pool, run 3: 1098 ms [ran] [tree 369640cc4793] [world 2f1906870a] (2026-11-07T04:55:01Z)
## Log
- 2026-11-07T04:38:05Z created
- 2026-11-07T04:43:14Z set type=PERFORMANCE
- 2026-11-07T04:43:15Z planned: it has criteria and steps
- 2026-11-07T04:43:22Z lane: ~/.claude/foreman.lanes/T-3614 on foreman/T-3614
- 2026-11-07T04:43:56Z focused
- 2026-11-07T04:43:56Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:55:06Z measured: one priority class (0.5 s sleep) beside 4 low run.py -j 4 filling a private 4-slot pool (2 s classes): old run.py 60.0+ (timeout), 40.4, 16.3, 60.0+, 15.7, 45.4 s; new 0.87, 1.18, 1.13, 0.83, 1.22, 1.08, 0.87, 1.17, 1.10 s; idle pool 0.62-0.66 s either way (bench: scratchpad t3614-bench/bench.sh old|new)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- T-3177 [PERFORMANCE M, deferred, 3 steps] Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load,…
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
