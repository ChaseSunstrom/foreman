---
id: T-2411
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T14:45:31Z
updated: 2026-10-31T17:43:19Z
---
# Recurring failure across 4 tasks: posttoolusefailure 0.0 0.0 0 [0]
## Raw request
> Recurring failure across 4 tasks: posttoolusefailure 0.0 0.0 0 [0]
> recurring-failure 4e4aaf9cc1ee
> (hit in T-0776, T-0785, T-0802, T-1713: find the cause and fix it once; fm recall and fm whyred help)
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
- 2026-10-31T14:45:31Z created
- 2026-10-31T17:43:19Z dropped: stale: the same PostToolUseFailure bench line as T-2410 (last hit T-1713, 2026-10-23); the fixture benches at p95 50 ms under its 150 ms budget today; a new hit refiles it
## Follow-ups captured
