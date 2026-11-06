---
id: T-3338
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py]
depends_on: []
source: discovered
created: 2026-11-06T05:03:01Z
updated: 2026-11-06T05:56:01Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a5eff0ac64e71ebfe
lane_branch: worktree-agent-a5eff0ac64e71ebfe
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:01Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_run.py]
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
1. [ ] test with nested(): a killed class is recorded  <- CURRENT
2. [ ] scale the class timer; record killed classes (run.py ~451-454)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:03:01Z created
- 2026-11-06T05:55:33Z planned from capture
- 2026-11-06T05:55:59Z focused
- 2026-11-06T05:56:01Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3367 [FIX S, planned, 1 steps] Six timing tests stop depending on the machine: test_lanes stall test sets the mtime ahead (not now), test_doctor stubs os.cpu_count (cl…
- T-3174 [FIX S, done, 2 steps] A full sampo check's suite gate never times out just because the machine is loaded: its deadline scales with load like targeted runs (load_…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
