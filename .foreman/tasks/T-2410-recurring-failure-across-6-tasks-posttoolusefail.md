---
id: T-2410
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T14:45:30Z
updated: 2026-10-31T17:42:51Z
---
# Recurring failure across 6 tasks: posttoolusefailure 0.0 0.0 0 [0] over budget
## Raw request
> Recurring failure across 6 tasks: posttoolusefailure 0.0 0.0 0 [0] over budget
> recurring-failure 80615a794e05
> (hit in T-0776, T-0780, T-0781, T-0785, T-0802, T-1372: find the cause and fix it once; fm recall and fm whyred help)
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
- 2026-10-31T14:45:30Z created
- 2026-10-31T17:42:51Z dropped: stale: its last hit was T-1372 (2026-10-21), from a bench run when the budget table gave PostToolUseFailure 0 ms; today the fixture benches at p95 50 ms against the 150 ms default budget and exits 0 (bench_hooks --runs 3, 2026-10-31). Nothing to fix; a new hit refiles it
## Follow-ups captured
