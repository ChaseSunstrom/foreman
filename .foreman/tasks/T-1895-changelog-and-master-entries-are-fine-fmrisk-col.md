---
id: T-1895
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T02:35:25Z
updated: 2026-10-29T02:36:36Z
---
# CHANGELOG and MASTER entries are fine. `fmrisk.collisions` is not memoized the way `status
## Raw request
> CHANGELOG and MASTER entries are fine. `fmrisk.collisions` is not memoized the way `status` is, which only matters if more callers appear
> (noticed by an agent; research T-1875-review)
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
- 2026-10-29T02:35:25Z created
- 2026-10-29T02:36:36Z dropped: YAGNI: only matters if more callers appear
## Follow-ups captured
