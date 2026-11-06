---
id: T-2153
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T12:46:27Z
updated: 2026-10-30T12:46:47Z
---
# fm genesis` mutations don't regenerate the other views (STATE.md, `badge.txt`,…
## Raw request
> fm genesis` mutations don't regenerate the other views (STATE.md, `badge.txt`, `progress.line`) either. That is the same root cause as the finding above
> (noticed by an agent; research T-2118-review)
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
- 2026-10-30T12:46:27Z created
- 2026-10-30T12:46:47Z dropped: fixed by T-2118: cmd_genesis now runs regen_views (STATE.md, badge, progress line, status.json) after every tower edit
## Follow-ups captured
