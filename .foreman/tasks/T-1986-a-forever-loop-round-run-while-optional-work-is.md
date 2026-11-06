---
id: T-1986
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T13:23:04Z
updated: 2026-10-29T13:33:15Z
done_in: T-1987
---
# A forever-loop round run while optional work is dropped (risk or usage budget) counts towa
## Raw request
> FIX: a forever-loop round run while optional work is dropped (risk or usage budget) counts toward the dry streak although it had no ideas fan-out, so a spent budget can end the loop as "2 dry rounds"; a budget-limited round leaves the dry streak as it was and says so
> DONE-WHEN: fm loop yield 1 with the budget degraded keeps the dry count :: python3 plugin/tests/run.py test_loop
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
- 2026-10-29T13:23:04Z created
- 2026-10-29T13:23:09Z batched into T-1987
- 2026-10-29T13:33:15Z done in T-1987 (batch)
## Follow-ups captured
