---
id: T-3338
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py, plugin/lib/sampo/core.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-11-06T05:03:01Z
updated: 2026-11-06T07:02:27Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a5eff0ac64e71ebfe
lane_branch: worktree-agent-a5eff0ac64e71ebfe
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:01Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_run.py]
builder_returned: 2026-11-06T07:02:27Z
---
# Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's time as at least SPLIT_S, so the next run splits it instead of killing Lanes/Proof at 480 s every rerun
## Raw request
> Load-proof the timing tests: at host load 90 every builder's affected check goes red on timing alone and builders burn ~1 h rerunning. Named tonight: test_hooks.NoTaskGate/NoTaskGateMulti (3 s fm task new timeout), test_lanes.LaneRecovery stall window FM_STALL_MIN=0.02, test_doctor.Checks busy() reads live load, test_demo 20 s wall check, test_docs.Fences 2 s panel budget, test_cli.CaptureAndIntake parallel captures, test_proof 480 s class timer. Each: scale with helpers.busy_factor() or use a controlled clock or stubbed load, never the live machine. Related T-3305, T-3308
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a hanging class killed with --timeout 1 shows up in the times file and is split next run; the class timer scales with load — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test with nested(): a killed class is recorded
2. [ ] scale the class timer; record killed classes (run.py ~451-454)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_run` → ✗ exit 1 · Ran 94 tests in 284.7s (68 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 175s, UnknownNames.test_a_red_runs_last_line_names_the_failing_class 126s, DiffGates (ran] (tree d1e4477fc1e0] (world 2f1906870a] (2026-11-06T06:23:15Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths.CheckSkip test_run.PerTestJobs` → ✗ exit 1 · Ran 20 tests in 638.9s (14 jobs, 16 at a time; slowest: CheckSkip 635s, PerTestJobs.test_a_k_run_keeps_a_whole_class_time_and_a_full_run_records_it 454s, PerTestJobs.test_a_split_class_runs_as_one_job (ran] (tree 6e7f444796ce] (world 2f1906870a] (2026-11-06T06:34:08Z)
## Log
- 2026-11-06T05:03:01Z created
- 2026-11-06T05:55:33Z planned from capture
- 2026-11-06T05:55:59Z focused
- 2026-11-06T05:56:01Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:54:03Z set scope=['plugin/tests/run.py', 'plugin/tests/test_run.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_core.py']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3367 [FIX S, planned, 1 steps] Six timing tests stop depending on the machine: test_lanes stall test sets the mtime ahead (not now), test_doctor stubs os.cpu_count (cl…
- T-3174 [FIX S, done, 2 steps] A full sampo check's suite gate never times out just because the machine is loaded: its deadline scales with load like targeted runs (load_…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
