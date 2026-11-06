---
id: T-2927
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-04T08:08:36Z
updated: 2026-11-05T01:19:43Z
trigger: baseline
trigger_key: e8fc0f9eb5564070
baseline: true
group: test_left_out missed by lane checks
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_left_out.LeftOut.test_no_silent_cut_in_fmcli. Captured by sampo check: the gates are red, so fix this before new work (it may not be this task's doing).
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
- 2026-11-04T08:08:36Z created
- 2026-11-05T01:19:43Z dropped: stale: test_left_out.LeftOut.test_no_silent_cut_in_fmcli passes at 53d75b0e (run 2026-11-05); fixed by a later change since the capture on 2026-11-04
## Follow-ups captured
