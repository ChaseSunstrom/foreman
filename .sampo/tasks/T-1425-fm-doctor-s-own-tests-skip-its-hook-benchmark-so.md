---
id: T-1425
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T20:05:45Z
updated: 2026-10-21T20:21:56Z
---
# fm doctor's own tests skip its hook benchmark, so they don't time out under load
## Raw request
> fm doctor's own tests skip its hook benchmark, so they don't time out under load
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] test_doctor.Command and test_resilience.ViewsRepair run fm doctor without the hook bench (13 of its 18 s here at load 44) and pass under one busy process per core — verify with `python3 plugin/tests/run.py test_doctor test_resilience`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] a FOREMAN_DOCTOR_BENCH=0 environment switch in fmdoctor.run_all that reports the three bench checks as 'not measured (FOREMAN_DOCTOR_BENCH=0)' WARN; the two tests set it; a test pins that the switch skips the bench and names it  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-21T20:05:45Z created
- 2026-10-21T20:21:56Z dropped: folded into T-1379: the same cause (fm doctor's hook bench inside the tests' 30 s limit) and the same fix
## Follow-ups captured
