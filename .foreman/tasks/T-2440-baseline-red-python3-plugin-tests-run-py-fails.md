---
id: T-2440
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T20:06:57Z
updated: 2026-11-01T06:06:41Z
trigger: baseline
trigger_key: 6feb1d8673434365
baseline: true
group: red CI and baseline fixes
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_code_worker.Failover.test_a_failure_is_sorted_by_its_exit_and_reply. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
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
- 2026-10-31T20:06:57Z created
- 2026-11-01T06:06:41Z dropped: stale: the test passed in 4 full fm check runs since (5503-5511 tests OK, 2026-11-01) and 3 targeted runs now; a one-time red under load at 20:06Z
## Follow-ups captured
