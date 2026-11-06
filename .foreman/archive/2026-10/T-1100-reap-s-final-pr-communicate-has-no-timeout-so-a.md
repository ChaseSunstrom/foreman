---
id: T-1100
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T04:46:24Z
updated: 2026-10-16T04:59:32Z
---
# - `_reap`'s final `pr.communicate()` has no timeout, so a grandchild that escaped the grou
## Raw request
> - `_reap`'s final `pr.communicate()` has no timeout, so a grandchild that escaped the group via `setsid` and holds the pipes would hang it. This is unchanged from before but worth a bounded wait
> (noticed by an agent; research T-1044-review)
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
- 2026-10-16T04:46:24Z created
- 2026-10-16T04:59:32Z dropped: fixed by the T-1044 builder (review commit 2dc3e56): _reap's drain is bounded at 5 s
## Follow-ups captured
