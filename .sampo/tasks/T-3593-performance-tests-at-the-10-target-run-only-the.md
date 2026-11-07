---
id: T-3593
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: [T-3502]
source: user
created: 2026-11-07T03:30:40Z
updated: 2026-11-07T05:38:47Z
lane: ~/.claude/foreman.lanes/T-3593
base_note: 
lane_branch: foreman/T-3593
base: d28c6d50d409fc07ff493d0334263484a1475726
base_tree: b3a03c6f5b8a68e1b7bf8c30c28c8e9818a2dadb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T03:36:04Z
plan0_scope: []
---
# PERFORMANCE tests at the 10% target: run only the tests a change can affect — select by…
## Raw request
> PERFORMANCE tests at the 10% target: run only the tests a change can affect — select by recorded per-test coverage (extend T-3502's run-cache coverage keys) for train gates, closes and builders' runs, falling back to the module map when coverage is missing; full suite only on a schedule when the machine is idle; measure CPU-s per merged lane before and after
## Interpretation
Reading 1 (taken): phase 1 of the request: run.py records, per test class, which repo files its whole process tree read (audit hooks in the class process and every Python child through a sitecustomize on PYTHONPATH: opens, imports, listings, subprocess script paths), and a named-module run skips a class green in the cache whose covered files' blobs are all unchanged; a class with no record, a changed covered file, an untracked Python child, or a change to run.py or a helper beside it runs; the 1-in-10 resample stays; trains, closes and builders benefit without changing callers. Reading 2 (ruled out for now): the whole request at once, also moving the full suite to an idle-time schedule and per-lane CPU accounting in the train; that is phase 2, since phase 1 must ship alone. Builds on T-3502's cache (unmerged: merged into this lane).
## Assumptions (confidence)
## Acceptance criteria
- [ ] A class whose covered file changed runs, one the change doesn't touch is skipped, a new or renamed class runs, a change to run.py or a helper beside it runs every class, and an fm call's child process files count as covered — verify with `nice -n 10 python3 plugin/tests/run.py test_run_cache`
- [ ] run.py's other tests still pass — verify with `nice -n 10 python3 plugin/tests/run.py test_run`
## Non-goals
Phase 2 (captured): the full suite only on a schedule when the machine is idle, CPU-s per merged lane recorded by the train, line-level coverage. Phase 1 measures CPU-s before and after on three recent lanes' diffs by hand (the NUMBERS line).
## Approach (options → choice → why)
1) Audit-hook file coverage per class (open/pyc/listdir/subprocess events, children via sitecustomize), records {file: blob}, skip when none changed. Likely outcome: lanes that leave core.py/cli.py alone skip most classes; fails if a test reads repo files from a non-Python child (the 1-in-10 resample catches it).
2) sys.monitoring line coverage plus diff hunks: finer (a cli.py edit reruns only tests that ran the edited functions). Fails on cost: line records for every child and hunk mapping, a much bigger cache; phase 2.
3) Use what exists: T-3502's static key (import closure plus the map's links plus the whole plugin/ tree). Likely outcome: any plugin/ edit reruns every class, today's near-zero hit rate across lanes.
4) strace or fanotify over the process tree: catches non-Python reads. Fails here: strace isn't installed and fanotify needs root.
Choice 1 (80%): the smallest step that is safe and measured; 2 captured as phase 2.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: coverage-keyed skip (changed covered file runs, untouched skips, new class runs, run.py/helper change runs all, child coverage)
2. [x] Coverage recorder in run.py: sitecustomize in each class's temp, audit hooks, per-class {file: blob} records in T-3502's cache
3. [x] Measure 3 recent lanes' diffs: classes run and CPU-s before and after, niced
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run_cache` → ✗ exit 1 · Ran 31 tests in 83.7s (5 jobs, 16 at a time; slowest: Store 0s, Coverage 0s, Recorder 0s) / FAILED (5 classes: test_run_cache.Main, test_run_cache.Coverage, test_run_cache.Store, test_run_cache.Record [ran] [tree 013b1d0a6e85] [world 2f1906870a] (2026-11-07T03:59:26Z)
- (step 1) `FOREMAN_NO_TEST_CACHE=1 nice -n 10 python3 plugin/tests/run.py test_run_cache` → exit 0 · Ran 36 tests in 1.9s (5 jobs, 16 at a time; slowest: EndToEnd 1s, Recorder 1s, Coverage 0s) / OK [ran] [tree 57778b82db72] [world 2f1906870a] (2026-11-07T04:07:55Z)
- (step 2) `FOREMAN_NO_TEST_CACHE=1 nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_map` → exit 0 · Ran 147 tests in 13.3s (82 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 6s, Ship 5s, Hang 5s) / OK [ran] [tree 57778b82db72] [world 2f1906870a] (2026-11-07T04:08:09Z)
- (step 2) `FOREMAN_NO_TEST_CACHE=1 nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_map test_sandbox` → exit 0 · Ran 183 tests in 65.5s (82 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 8s, Map 7s, UnknownNames.test_a_name_whose_tests_a_k_filters_out_names_the_k 5s) / O [ran] [tree 51e1e0ce193c] [world 2f1906870a] (2026-11-07T04:26:50Z)
- (step 2) `FOREMAN_NO_TEST_CACHE=1 nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_map test_sandbox` → ✗ exit 1 · Ran 184 tests in 196.6s (102 jobs, 16 at a time; slowest: Recorder 42s, Ship 27s, PerTestJobs.test_a_class_with_setup_runs_whole 10s) / FAILED (1 classes: test_ship.Ship) [ran] [tree 91bfb4539548] [world 2f1906870a] (2026-11-07T05:35:39Z)
- (step 3) `bench: 109 test modules (every 4th + the lanes' linked ones) in a clone, niced -j4, CPU-s by a subreaper wrapper; warm at 6adf05663, then the merges of T-3539/T-3533/T-3331 in turn (scratchpad bench2.sh, report.py)` → whole modules 2312 tests, 867 CPU-s (no cache; 733 CPU-s on the warm coverage run, same set). Selected: T-3539 1436 tests (+876 cached) 708 CPU-s; T-3533 (cli.py) 2171 (+144) 736 CPU-s; T-3331 1593 (+725) 563 CPU-s. Measured before 59636b5f1, which follows the costliest whole-tree classes; not re-measured [tree 91bfb4539548] (2026-11-07T05:35:43Z)
- (step 2) `FOREMAN_NO_TEST_CACHE=1 nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_map test_sandbox` → exit 0 · Ran 184 tests in 38.6s (118 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 6s, Hang 5s, Ship.test_the_test_run_is_marked_while_it_runs_and_waits_for_a_live_ch [ran] [tree 91bfb4539548] [world 2f1906870a] (2026-11-07T05:38:47Z)
## Log
- 2026-11-07T03:30:40Z created
- 2026-11-07T03:35:35Z planned: it has criteria and steps
- 2026-11-07T03:35:36Z set depends_on=['T-3502']
- 2026-11-07T03:35:38Z lane: ~/.claude/foreman.lanes/T-3593 on foreman/T-3593
- 2026-11-07T03:36:03Z focused
- 2026-11-07T03:36:04Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3572 [PERFORMANCE M, active, 4 steps] A new test engine (user 2026-11-06): the suite has ~7,000 call sites that spawn the…
- T-3531 [PERFORMANCE M, done, 1 steps] The train's pre-filter probes (T-3474) run one lane at a time, about 2-4 min each when a… — lesson: Run per-item checks in parallel…
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
- similar finished tasks took 1–4 steps
