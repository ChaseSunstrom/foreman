---
id: T-3338
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T05:03:01Z
updated: 2026-11-06T05:03:01Z
---
# Load-proof the timing tests: at host load 90 every builder's affected check goes red on…
## Raw request
> Load-proof the timing tests: at host load 90 every builder's affected check goes red on timing alone and builders burn ~1 h rerunning. Named tonight: test_hooks.NoTaskGate/NoTaskGateMulti (3 s fm task new timeout), test_lanes.LaneRecovery stall window FM_STALL_MIN=0.02, test_doctor.Checks busy() reads live load, test_demo 20 s wall check, test_docs.Fences 2 s panel budget, test_cli.CaptureAndIntake parallel captures, test_proof 480 s class timer. Each: scale with helpers.busy_factor() or use a controlled clock or stubbed load, never the live machine. Related T-3305, T-3308
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:03:01Z created
## Follow-ups captured
