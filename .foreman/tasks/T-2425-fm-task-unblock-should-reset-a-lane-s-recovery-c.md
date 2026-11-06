---
id: T-2425
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T15:56:34Z
updated: 2026-11-02T01:12:08Z
---
# fm task unblock` should reset a lane's recovery count
## Raw request
> fm task unblock` should reset a lane's recovery count
> (noticed by an agent; research T-2354-review)
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
- 2026-10-31T15:56:34Z created
- 2026-11-02T01:12:08Z dropped: already built: fm task unblock pops recoveries, lane_stop and revisit (fmcli.py, T-2354, 7eb8e771, 2026-10-31), so an unblocked lane starts with a fresh recovery count; the review note predates it
## Follow-ups captured
