---
id: T-2797
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T06:01:10Z
updated: 2026-11-03T18:43:32Z
builder_model: sonnet
base: e323766da5afe030fc83af865d1ef319fd97c052
base_tree: fa52ee13b58bc49aef7949ac94433bfaccb8a0be
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-03T15:02:32Z
plan0_scope: []
lane_stop: merged 2026-11-03T15:18:17Z
verified: strong
---
# Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm lane merge and fm check wait for load to fall (bounded) and scale their run timeouts by load per core
## Raw request
> FIX: on 2026-11-03 five builder lanes, a design agent and a close run together drove load to 55 (3.5 per core): every fm check full gate hit the 600 s evidence cap, bench_hooks failed as flaky, and 4 closes and 2 lane merges failed for timing alone. fm lane brief should refuse or queue a new lane when the box's load per core is over ~1.5, and fm task finish / lane merge should wait for load to fall (as the scratchpad merges.sh does) instead of running gates that can only time out
## Interpretation
1. Make gates survive load (chosen): when the box is busy, new lanes are held and gate runs wait a bounded time, then run with timeouts scaled by load per CPU, so a slow-but-correct gate passes instead of failing for timing.
2. Only stop over-subscription: refuse new lanes past a load bar; gates keep their fixed 600 s cap. Partial: load from a design agent or browser still times gates out, as on 2026-11-03.
3. Treat timeouts under load as non-failures (record and skip): ruled out; a gate that didn't run must never read green.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief refuses a new lane while the 1-minute load is over 1.5 per CPU, naming the load and the running lanes; FOREMAN_HOST fakes the load in tests — verify with `python3 plugin/tests/run.py test_lanes`
- [x] fm task finish --run, fm lane merge's criteria and fm check wait (bounded, printing why) while load is over 1.5 per CPU, then run with the timeout scaled by max(1, load per CPU), so a gate under load gets the time it needs instead of a 600 s cap — verify with `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check`
## Non-goals
## Approach (options → choice → why)
1. One c.wait_for_load helper plus load-scaled timeouts (chosen): lower host_strain's lane bar to 1.5 per CPU; finish, lane merge and check call c.wait_for_load(limit) (polls host_load, prints why, gives up after a bound and runs anyway) and multiply their run timeouts by max(1, load per CPU). Likely outcome: gates under load take longer but pass; new lanes stop piling on. Fails if: load stays high for the whole bound; then the scaled timeout still gives the run room.
2. Scale timeouts only, no waiting. Likely outcome: fewest lines; every gate still competes with the load that slows it. Fails if: load keeps rising as more lanes start, since nothing holds them.
3. A machine-wide semaphore for gate runs (one full gate at a time). Likely outcome: gates never overlap. Fails if: a crashed holder leaves the lock; more state and recovery code than the problem needs.
4) use what exists: c.host_load and c.host_strain (T-0465, T-1518) and FOREMAN_HOST for tests; lanes.py and hooks.py already call host_strain. Likely outcome: the helper is a few lines over host_load. Fails if: host_load is unreadable (returns None); then nothing waits, as today.
5) do less: only lower the lane threshold. Likely outcome: fewer lanes start under load, but a close run under a design agent's load still times out. Fails if: load comes from outside lanes (a browser, a build), as on 2026-11-03.
Choice: 1 with 4's helpers (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: tests for the lane threshold and the scaled timeout under FOREMAN_HOST load
2. [x] lower host_strain's lane threshold to 1.5 per CPU; one c.wait_for_load helper used by finish, merge and check
3. [x] run the tests
## Resume here
## Docs impact
none: the wait message says what it waits for
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -25` → exit 0 · Ran 148 tests in 45.7s (13 classes, 16 at a time; slowest: Lanes 44s, LaneRecovery 31s, RaceEvidence 20s) / OK [ran] [tree 07ceee1d67f4] [world 2f1906870a] (2026-11-03T15:05:00Z)
- (step 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -25` → exit 0 · Ran 148 tests in 45.7s (13 classes, 16 at a time; slowest: Lanes 44s, LaneRecovery 31s, RaceEvidence 20s) / OK [ran] [tree 07ceee1d67f4] [world 2f1906870a] (2026-11-03T15:05:00Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_close_gates test_verify_check test_orchestration 2>&1 | tail -25` → exit 0 · Ran 173 tests in 48.0s (51 classes, 16 at a time; slowest: TaskLifecycle 47s, CloseGates 39s, CaptureAndIntake 25s) / OK [ran] [tree 07ceee1d67f4] [world 2f1906870a] (2026-11-03T15:05:51Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 148 tests in 41.8s (13 classes, 16 at a time; slowest: Lanes 41s, LaneRecovery 35s, RaceEvidence 25s) / OK [ran] [tree 07ceee1d67f4] [world 2f1906870a] (2026-11-03T15:06:38Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_close_gates test_verify_check` → exit 0 · Ran 166 tests in 22.1s (46 classes, 16 at a time; slowest: TaskLifecycle 22s, CloseGates 17s, CaptureAndIntake 11s) / OK [ran] [tree 07ceee1d67f4] [world 2f1906870a] (2026-11-03T15:07:02Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_lanes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.70s] [ran] [tree 07ceee1d67f4] [world 2f1906870a] (2026-11-03T15:07:47Z)
- `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check` → ✗ exit 1 · Ran 314 tests in 30.0s (59 classes, 16 at a time; slowest: Lanes 29s, LaneRecovery 25s, TaskLifecycle 24s) / FAILED (1 classes: test_lanes.LoadGates) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:49:17Z)
- `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check` → exit 0 · Ran 314 tests in 35.2s (59 classes, 16 at a time; slowest: Lanes 35s, LaneRecovery 28s, TaskLifecycle 27s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:49:17Z)
- `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check` → ✗ exit 1 · Ran 314 tests in 58.9s (59 classes, 16 at a time; slowest: Lanes 57s, TaskLifecycle 45s, LaneRecovery 40s) / FAILED (1 classes: test_lanes.LoadGates) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:51:12Z)
- `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check` → exit 0 · Ran 314 tests in 53.5s (59 classes, 16 at a time; slowest: Lanes 53s, TaskLifecycle 43s, LaneRecovery 40s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:51:12Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 148 tests in 23.2s (13 classes, 16 at a time; slowest: Lanes 23s, LaneRecovery 21s, RaceEvidence 10s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:42:08Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:51:12Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:42:08Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:51:12Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:42:08Z)
- (audit intent) `self: read the diff; wait_for_load is bounded (FOREMAN_LOAD_WAIT, 300 s), polls at most every 5 s, and an unreadable load never waits; load_scaled multiplies only finite timeouts` → gates under machine load wait or stretch instead of failing for timing, and no new lane piles on past 1.5 load per CPU [tree 07445d19b39c] (2026-11-03T18:42:08Z)
- (audit edge) `self: read the diff; wait_for_load is bounded (FOREMAN_LOAD_WAIT, 300 s), polls at most every 5 s, and an unreadable load never waits; load_scaled multiplies only finite timeouts` → unreadable load: no wait, no scaling; FOREMAN_HOST fakes low load in every test so the suite never waits; a memory-strained host also holds a brief (shared host_strain) [tree 07445d19b39c] (2026-11-03T18:42:08Z)
- (audit adversary) `self: read the diff; wait_for_load is bounded (FOREMAN_LOAD_WAIT, 300 s), polls at most every 5 s, and an unreadable load never waits; load_scaled multiplies only finite timeouts` → the wait only delays and the scale only lengthens a timeout; no gate is skipped or read green, and a run that times out still fails [tree 07445d19b39c] (2026-11-03T18:42:08Z)
## Log
- 2026-11-03T06:01:10Z created
- 2026-11-03T15:02:02Z planned from capture
- 2026-11-03T15:02:05Z criterion 2 verify: `python3 plugin/tests/run.py test_lanes test_cli test_check` → `python3 plugin/tests/run.py test_lanes test_cli test_gates`
- 2026-11-03T15:02:16Z criterion 2 verify: `python3 plugin/tests/run.py test_lanes test_cli test_gates` → `python3 plugin/tests/run.py test_lanes test_cli test_close_gates test_verify_check`
- 2026-11-03T15:02:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2797.builder.md
- 2026-11-03T15:02:30Z focused
- 2026-11-03T15:02:32Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-03T15:18:17Z merged worktree-agent-a43acec7c4608c710 (4 file(s))
- 2026-11-03T15:18:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a43acec7c4608c710
- 2026-11-03T17:05:19Z focused
- 2026-11-03T17:07:11Z paused: focus moved to T-2742
- 2026-11-03T17:48:10Z focused
- 2026-11-03T17:51:13Z paused: focus moved to T-2810
- 2026-11-03T18:41:43Z focused
- 2026-11-03T18:43:32Z done
## Follow-ups captured
## Build vs reuse
reuse: c.host_load and c.host_strain (T-0465, T-1518), FOREMAN_HOST test stand-in, check_run's recorded load (T-2763); new: one c.wait_for_load helper and a timeout multiplier
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-10-31: [reverses: a later Mission's lane waits only for earlier-Mission lanes launched before it] Mission-order merging, revised: lanes that are ready merg…
## Why not caught
none: no gate knew the machine load; bench_hooks and the lane gates had only run on a quiet machine before parallel lanes (2026-11-02)
## Lessons
- Under load, give a correct-but-slow gate time instead of a red
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/cli.py
