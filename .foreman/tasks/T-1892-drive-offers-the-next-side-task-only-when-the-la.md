---
id: T-1892
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T01:37:38Z
updated: 2026-10-29T01:45:04Z
---
# Drive offers the next side task only when the last offer was taken (briefed for a lane or
## Raw request
> Drive offers the next side task only when the last offer was taken (briefed for a lane or started): an ignored offer means the session judged side work not worth it, so three offers per set of jobs cost three empty turns
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
- 2026-10-29T01:37:38Z created
- 2026-10-29T01:45:04Z dropped: conflicts with T-0401's never-idle design (the user: make sure it doesnt sit idle); an ignored offer would let the turn end, and three short turns per set of jobs cost less than an idle session
## Follow-ups captured
