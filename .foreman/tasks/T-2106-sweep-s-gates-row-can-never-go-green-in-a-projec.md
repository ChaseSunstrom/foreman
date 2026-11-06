---
id: T-2106
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T06:17:51Z
updated: 2026-10-30T06:18:09Z
---
# Sweep's gates row can never go green in a project with no configured checks, because `fm…
## Raw request
> sweep's gates row can never go green in a project with no configured checks, because `fm check` refuses to run there
> (noticed by an agent; research T-2104-review)
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
- 2026-10-30T06:17:51Z created
- 2026-10-30T06:18:09Z dropped: handled in T-2104: the gates row now says 'no gates configured: fm check add' instead of a run that refuses; no gates stays not-green on purpose
## Follow-ups captured
