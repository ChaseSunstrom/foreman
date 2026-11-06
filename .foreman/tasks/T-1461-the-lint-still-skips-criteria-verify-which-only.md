---
id: T-1461
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T14:45:19Z
updated: 2026-10-22T14:45:48Z
---
# The lint still skips `criteria[].verify`, which only the guard covers. The test suite has
## Raw request
> the lint still skips `criteria[].verify`, which only the guard covers. The test suite has no `/home` route, `e.g.`, `res.ok` or NUL case
> (noticed by an agent; research T-1422-review2)
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
- 2026-10-22T14:45:19Z created
- 2026-10-22T14:45:48Z dropped: duplicate of T-1460 (verify commands rely on the guard alone); the lint half is moot since T-1422 dropped the lint
## Follow-ups captured
