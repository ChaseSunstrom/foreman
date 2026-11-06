---
id: T-1370
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T07:33:21Z
updated: 2026-10-21T13:37:44Z
---
# --task t-0003` (lowercase) reports "no task", because `find_brief` uppercases the id but `
## Raw request
> --task t-0003` (lowercase) reports "no task", because `find_brief` uppercases the id but `_load_task` compares it as typed
> (noticed by an agent; research T-1330-review)
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
- 2026-10-21T07:33:21Z created
- 2026-10-21T13:37:44Z dropped: fixed in T-1330: _load_task upper-cases the id (tested with a lowercase id)
## Follow-ups captured
