---
id: T-3392
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:54:39Z
updated: 2026-11-06T06:54:39Z
inferred_deps: [T-3329]
inferred_why: T-3329: named in its request
---
# lanes.py:~874 calls next_id with the network on inside the lane race loop, which may run…
## Raw request
> FIX: lanes.py:~874 calls next_id with the network on inside the lane race loop, which may run under a lock a hook holds; pass net=False there once T-3329 lands (T-3329 builder)
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
- 2026-11-06T06:54:39Z created
## Follow-ups captured
