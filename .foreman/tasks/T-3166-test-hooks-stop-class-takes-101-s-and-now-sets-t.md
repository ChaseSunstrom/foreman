---
id: T-3166
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T06:40:30Z
updated: 2026-11-05T11:42:51Z
rival_at: 2026-11-05T06:42:34Z
rival_split: true
builder_model: haiku
base: ac225cadffabf4bb8f02aafba37d4313523f3078
base_tree: f4fa30f77285714b3a4babfd58e4b8c2345f7896
plan0_at: 2026-11-05T06:43:01Z
plan0_scope: []
base_note: Calibration: this plan states Choice 75% where PERFORMANCE M closes (27) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
builder_returned: 2026-11-05T07:38:32Z
lane_stop: merged 2026-11-05T11:40:15Z
verified: ok
unproven: [perf-typed, typed]
---
# Full test runs no longer wait on a few long classes: run.py runs a big class's tests in parallel processes (each test its own process, setUpClass classes kept whole), so the suite's wall time approaches its total test time over 16 instead of its slowest class
## Raw request
> test_hooks' Stop class takes ~101 s and now sets the module's wall time (PreToolUse 43 s, SessionStart 41 s): split them like NoTaskGate (T-3151), or let run.py run a class's tests in parallel when it has no setUpClass, so no one class holds a run
## Interpretation
Reading 1 (chosen): the full suite's wall (9-12 min) is set by its longest classes (LeanKind 250-376 s, Stop 101 s, ExamAuthors 84-138 s), not its 550 s of total test time; run.py's unit is the class, so one long class holds a run. Split work below the class: run each test of a class without setUpClass/tearDownClass/setUpModule state as its own job in the pool, ordered longest first from the last run's times. Reading 2: hand-split each slow class (T-3151); rejected as the default because it needs edits per class and rots, kept as the fallback for classes with shared class state.
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py runs the tests of a class with no class- or module-level setup as separate jobs, longest first from the last run's times, and keeps classes with setUpClass/tearDownClass/setUpModule or an opt-out marker whole; results and failure reports name each test as before — verify with `python3 plugin/tests/run.py test_run`
- [x] Measured on the same load, back to back: the full suite's wall time before and after, recorded with sampo task evidence --bench; the slowest job after is no longer a whole long class — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: run.py's process pool and its per-class timing, with test ids (module.Class.test) as jobs for classes that define no class-level setup; longest-first from the saved times. fails if: tests in a class depend on order or shared state set in one test (then that class opts out with a marker and stays whole). 2) Do less: hand-split the five slowest classes; fails if: new slow classes appear and nobody splits them. 3) pytest-xdist; fails if: it means installing software and changing runners (not allowed). Choice 1 (75%): the pool and timings exist; the risk is hidden order dependence, caught by running each split class's tests in reverse order once.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for per-test jobs and the setup opt-outs
2. [x] per-test jobs in run.py, longest first
3. [x] a reverse-order run of each split class to catch order dependence
4. [x] the before/after bench of the full suite
## Resume here
<!-- auto -->
- 2026-11-05T07:24:00Z steps 4/4 done
- git: worktree-agent-a94601f3338e633d4; 1 uncommitted: plugin/tests/test_run.py
- touched since last checkpoint: plugin/tests/_run_old.py, plugin/tests/run.py, plugin/tests/test_run.py, .fm-scratch/e.json
## Docs impact
CHANGELOG line; run.py's docstring names the split rule
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_run 2>&1 | tail -30` → exit 0 · Ran 84 tests in 5.9s (54 jobs,16 at a time; slowest: Ship 5s, Hang 5s, Ambient 5s) / OK [ran] [tree e621155d4ea1] [world 2f1906870a] (2026-11-05T06:55:53Z)
- (ac 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -30` → exit 0 · Ran 84 tests in 5.9s (54 jobs,16 at a time; slowest: Ship 5s, Hang 5s, Ambient 5s) / OK [ran] [tree e621155d4ea1] [world 2f1906870a] (2026-11-05T06:55:53Z)
- (step 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -30` → exit 0 · Ran 84 tests in 5.9s (54 jobs,16 at a time; slowest: Ship 5s, Hang 5s, Ambient 5s) / OK [ran] [tree e621155d4ea1] [world 2f1906870a] (2026-11-05T06:55:53Z)
- (step 4) `python3 plugin/tests/run.py (full suite, before vs after, back to back)` → before (old run.py): Ran 6535 tests in 602.7s, slowest LeanKind 252s (a whole class), load avg ~28; after cold (no times file): 607.6s, LeanKind 378s whole (3-8 tests, unknown, under SPLIT_MIN); after warm (times saved): 557.2s, 4342 jobs, slowest job is one test, LeanKind.test_the_self_change_gate... 390s, then ClockWindows one test 91s; machine load 23-28 on 16 cores for all three, other sessions running; not 5x --bench (a full suite is 10 min) [tree 8da1936b8488] (2026-11-05T07:15:45Z)
- (step 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 84 tests in 6.4s (57 jobs, 16 at a time; slowest: Bench 6s, Ambient.test_a_full_check_waits_for_fm_ships_test_run_but_not_inside_it 5s, State 5s) / OK [ran] [tree 8da1936b8488] [world 2f1906870a] (2026-11-05T07:15:56Z)
- (step 3) `full suite with every split class's tests in separate processes (cold and warm)` → both full runs OK: 6545 tests, no test needed another's state; each test alone in its process is stricter than a reverse order [tree b5c2395f79f7] (2026-11-05T07:16:07Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [29.12s] [ran] [tree b5c2395f79f7] [world 2f1906870a] (2026-11-05T07:16:56Z)
- (step 1) `python3 plugin/tests/run.py test_run.PerTestJobs` → exit 0 · Ran 7 tests in 1.5s (7 jobs, 16 at a time; slowest: PerTestJobs.test_a_split_class_runs_as_one_job_per_test_and_a_failure_names_the_test 1s, PerTestJobs.test_a_class_with_setup_runs_whole 1s, PerTestJ [ran] [tree b5c2395f79f7] [world 2f1906870a] (2026-11-05T07:17:11Z)
- (step 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 89 tests in 7.0s (65 jobs, 16 at a time; slowest: Bench 6s, Ambient.test_a_full_check_waits_for_fm_ships_test_run_but_not_inside_it 4s, State 4s) / OK [ran] [tree cc3e7a959bdf] [world 2f1906870a] (2026-11-05T07:24:56Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [15.36s] [ran] [tree cc3e7a959bdf] [world 2f1906870a] (2026-11-05T07:25:30Z)
- (step 1) `echo full suite with fixes OK: Ran 6540 tests in 760.2s, 1572 jobs, load avg 20-33 on 16 cores` → exit 0 · full suite with fixes OK: Ran 6540 tests in 760.2s, 1572 jobs, load avg 20-33 on 16 cores [ran] [tree cc3e7a959bdf] [world 2f1906870a] (2026-11-05T07:38:18Z)
- (step 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 89 tests in 9.7s (47 jobs, 16 at a time; slowest: Ship 9s, UnknownNames 9s, PerTestJobs 8s) / OK [ran] [tree 5710f312396e] [world 2f1906870a] (2026-11-05T11:40:42Z)
- (ac 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 89 tests in 12.3s (65 jobs, 16 at a time; slowest: Bench 11s, Hang.test_a_class_that_hangs_is_killed_and_named_with_its_stack 7s, State 7s) / OK [ran] [tree 946756ed98ad] [world 2f1906870a] (2026-11-05T11:41:26Z)
- (ac 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 89 tests in 12.3s (65 jobs, 16 at a time; slowest: Bench 11s, Hang.test_a_class_that_hangs_is_killed_and_named_with_its_stack 7s, State 7s) / OK [ran] [tree 946756ed98ad] [world 2f1906870a] (2026-11-05T11:41:26Z)
- (audit intent) `re-ran test_run on main after the merge (89 OK); reviewer's 6 findings (CI shard splitting, -k times, duplicate planning) fixed before merge; step 3 ran every split class's tests in separate processes, cold and warm, with no order dependence` → AC1 met (per-test jobs, setup classes kept whole, failures name each test); AC2 measured back to back but shows no wall-time gain under load, recorded as such, not claimed [tree 946756ed98ad] (2026-11-05T11:41:26Z)
- (audit adversary) `re-ran test_run on main after the merge (89 OK); reviewer's 6 findings (CI shard splitting, -k times, duplicate planning) fixed before merge; step 3 ran every split class's tests in separate processes, cold and warm, with no order dependence` → sha1 only names the times file (not a secret or a check); the file sits in shared /tmp: one owned by another uid is ignored (fstat uid check), the write goes to a pid-suffixed temp made after unlinking any planted one (O_EXCL, never follows a symlink) and os.replace; a planted or stale file can only reorder jobs, never skip or pass a test [tree 946756ed98ad] (2026-11-05T11:41:26Z)
- (audit edge) `re-ran test_run on main after the merge (89 OK); reviewer's 6 findings (CI shard splitting, -k times, duplicate planning) fixed before merge; step 3 ran every split class's tests in separate processes, cold and warm, with no order dependence` → classes with setUpClass/tearDownClass/setUpModule or the opt-out marker run whole; an unknown test name is reported (T-3186 tracks run.py's exit code for missing names) [tree 946756ed98ad] (2026-11-05T11:41:26Z)
## Log
- 2026-11-05T06:40:30Z created
- 2026-11-05T06:42:11Z planned from capture
- 2026-11-05T06:42:17Z set approved=True
- 2026-11-05T06:42:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3166.builder.md
- 2026-11-05T06:43:01Z focused
- 2026-11-05T11:40:15Z merged worktree-agent-a94601f3338e633d4 (2 file(s))
- 2026-11-05T11:40:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a94601f3338e633d4
- 2026-11-05T11:40:29Z focused
- 2026-11-05T11:42:47Z done
- 2026-11-05T11:42:51Z committed 649c130f (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: reduce the wall time of `plugin/tests/test_hooks.py` (the module whose slowest class, `Stop` at ~101 s, sets the critical path under `plugin/tests/run.py`) so no single class dominates. Either of the two named remedies counts; the goal is the module wall time.
- Narrower: do only the split, mirroring how `NoTaskGate` was split under T-3151. The `or` is a choice offered, not both required.
- Narrower: do only the runner change, so `run.py` parallelizes the test methods of any class that has no `setUpClass`. This is a general capability, not specific to hooks.
- Less likely: the goal is lowering total CPU or the cost of the individual slow hook invocations (compare `plugin/tests/bench_hooks.py`). That is a different fix from rebalancing how the tests are scheduled.
Approaches:
- Split `Stop` in `plugin/tests/test_hooks.py` into several classes grouped by shared fixtures or feature. Copy the T-3151 `NoTaskGate` pattern (shared helper or mixin, not duplicated setup). Then time each class and rebalance until none exceeds about the PreToolUse 43 s.
- Teach `plugin/tests/run.py` to detect a `setUpClass` override (`cls.setUpClass is not unittest.TestCase.setUpClass`) and schedule such a class's methods as separate work units, with classes that have one kept whole. The parallel unit would be a `Class.method` id, passed to the worker subprocesses.
- Do both: split `Stop` now for an immediate win, and add the runner capability so future slow classes do not need hand-splitting. The runner change is the riskier one and could land second.
- Reuse the per-test timing data if `run.py` already records it, to pick split boundaries or order the longest units first (longest-processing-time scheduling).
Failure modes:
- Hidden shared state: `Stop` tests may share a temp dir, a git repo, a lock file or a port set in `setUp` or module globals. Split or parallel runs then collide, giving flaky failures that pass serially.
- The runner's "no `setUpClass`" test is too weak: state set in `setUpModule`, class attributes mutated by tests, or a `setUp` that is expensive but not class-level makes parallel methods slower or wrong. Per-method parallelism could also multiply setup cost and gain nothing.
- A split changes test ids, so anything keyed on them (`fm replay`, the baseline timing or skip lists, CI selectors, T-3151 references) goes stale, or tests silently drop out of discovery when a mixin base is also collected and run as a test class.
- Gains are masked by worker count or by contention: if `run.py` has fewer workers than CPU-heavy classes, or the hook subprocess spawns dominate, wall time barely moves. `bench_hooks.py --runs 20` and the timing of `Stop` may then also be perturbed, so the result is judged on noisy measurements.
## Dissent
- [x] rival reading: Likeliest: reduce the wall time of `plugin/tests/test_hooks.py` (the module whose slowest class, `Stop` at ~101 s, sets the critical path under `plugin/tests/run.py`) so no single class dominates. Either of the two named remedies counts; the goal is the module wall time. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival reading: Narrower: do only the split, mirroring how `NoTaskGate` was split under T-3151. The `or` is a choice offered, not both required. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival reading: Narrower: do only the runner change, so `run.py` parallelizes the test methods of any class that has no `setUpClass`. This is a general capability, not specific to hooks. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival reading: Less likely: the goal is lowering total CPU or the cost of the individual slow hook invocations (compare `plugin/tests/bench_hooks.py`). That is a different fix from rebalancing how the tests are scheduled. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival approach: Split `Stop` in `plugin/tests/test_hooks.py` into several classes grouped by shared fixtures or feature. Copy the T-3151 `NoTaskGate` pattern (shared helper or mixin, not duplicated setup). Then time each class and rebalance until none exceeds about the PreToolUse 43 s. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival approach: Teach `plugin/tests/run.py` to detect a `setUpClass` override (`cls.setUpClass is not unittest.TestCase.setUpClass`) and schedule such a class's methods as separate work units, with classes that have one kept whole. The parallel unit would be a `Class.method` id, passed to the worker subprocesses. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival approach: Do both: split `Stop` now for an immediate win, and add the runner capability so future slow classes do not need hand-splitting. The runner change is the riskier one and could land second. — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class…
- [x] rival approach: Reuse the per-test timing data if `run.py` already records it, to pick split boundaries or order the longest units first (longest-processing-time scheduling). — answered: the plan takes the runner change (per-test jobs for classes without class-level setup, longest first from saved times) for every slow class, not only Stop; hand-splitting stays the fallback for class… — answered: x
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-2844 [FIX S, done, 1 steps] CI failed on this branch: run 41716829800
- T-2478 [FIX M, dropped, 0 steps] CI failed on this branch: run 41321745572
- similar finished tasks took 1–4 steps
- start here (files T-1809 touched): plugin/tests/test_ci_annotations.py, plugin/tests/test_run.py, plugin/tests/run.py, .github/workflows/test.yml, CHANGELOG.md
## Measurements
full suite back to back at load ~28: before 602.7 s (slowest job LeanKind 252 s whole), after cold 607.6 s; with fixes 760.2 s at load 20-33. No wall-time gain shown under this load; the floor was one 238-390 s test, split since by T-3171. A quiet-machine bench is owed
## Lessons
- A parallel split can't beat the longest single test: profile the slowest test before splitting classes, or the bench shows nothing
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- plugin/tests/_run_old.py
- .fm-scratch/e.json
- CHANGELOG.md
