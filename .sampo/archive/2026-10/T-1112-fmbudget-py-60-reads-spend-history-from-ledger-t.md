---
id: T-1112
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T05:36:57Z
updated: 2026-10-16T05:42:05Z
---
# Fmbudget.py ~60 reads spend history from ledger_tail(p, 20000), which covers ~12 days here
## Raw request
> fmbudget.py ~60 reads spend history from ledger_tail(p, 20000), which covers ~12 days here and misses rolled months; use c.ledger_events with a since
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
- 2026-10-16T05:36:57Z created
- 2026-10-16T05:42:05Z dropped: premise false: fmbudget reads its own spend.jsonl (1,051 rows in 12 days here, never rolled), not the project ledger; a 20,000-row tail covers about 200 days
## Follow-ups captured
