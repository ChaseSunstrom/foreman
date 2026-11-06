---
id: T-0967
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T21:40:46Z
updated: 2026-10-15T22:48:27Z
---
# - MASTER.md lines are very long, so grep output is truncated. That makes the map hard to a
## Raw request
> - MASTER.md lines are very long, so grep output is truncated. That makes the map hard to audit
> (noticed by an agent; research T-0964-workflow)
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
- 2026-10-15T21:40:46Z created
- 2026-10-15T22:48:27Z dropped: fm outline MASTER.md and Read with an offset are the intended ways to read it; hard-wrapping ~250 long bullets churns every line and breaks grep-by-bullet for a truncation that only Foreman's own 400-char output cap causes
## Follow-ups captured
