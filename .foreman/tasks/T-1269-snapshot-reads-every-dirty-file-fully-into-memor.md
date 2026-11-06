---
id: T-1269
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T14:05:19Z
updated: 2026-10-20T14:15:26Z
---
# - `_snapshot` reads every dirty file fully into memory, so a huge untracked file can exhau
## Raw request
> - `_snapshot` reads every dirty file fully into memory, so a huge untracked file can exhaust RAM
> (noticed by an agent; research T-1214-review)
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
- 2026-10-20T14:05:19Z created
- 2026-10-20T14:15:26Z dropped: duplicate of T-1214, captured from the review's text
## Follow-ups captured
