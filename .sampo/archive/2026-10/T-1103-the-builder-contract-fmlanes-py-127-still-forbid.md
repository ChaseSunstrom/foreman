---
id: T-1103
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T05:02:24Z
updated: 2026-10-16T07:03:33Z
---
# - The builder CONTRACT (`fmlanes.py:127`) still forbids heredocs, so builders can't use `f
## Raw request
> - The builder CONTRACT (`fmlanes.py:127`) still forbids heredocs, so builders can't use `fm edit` or `fm sub` and nothing says so
> (noticed by an agent; research T-1089-review)
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
- 2026-10-16T05:02:24Z created
- 2026-10-16T07:03:33Z dropped: done by T-1089: the builder contract (fmlanes.py ~131-133) names fm edit --file for batch edits
## Follow-ups captured
