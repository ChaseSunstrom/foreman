---
id: T-1682
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T21:48:44Z
updated: 2026-10-22T21:49:45Z
---
# Style.css:233 has a dead fallback `var(--muted, #898781)`. The variable is defined, so the
## Raw request
> style.css:233 has a dead fallback `var(--muted, #898781)`. The variable is defined, so the fallback can go
> (noticed by an agent; research T-1609-review)
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
- 2026-10-22T21:48:44Z created
- 2026-10-22T21:49:45Z dropped: fixed in T-1609: the dead var(--muted, …) fallback was removed
## Follow-ups captured
