---
id: T-1695
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T22:27:21Z
updated: 2026-10-22T22:27:56Z
---
# _rgb` accepts a bare int such as `3` as black (plugin/lib/fmraster.py:55)
## Raw request
> _rgb` accepts a bare int such as `3` as black (plugin/lib/fmraster.py:55)
> (noticed by an agent; research T-1631-review)
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
- 2026-10-22T22:27:21Z created
- 2026-10-22T22:27:56Z dropped: fixed in T-1631: _rgb rejects a bare int
## Follow-ups captured
