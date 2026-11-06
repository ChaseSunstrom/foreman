---
id: T-3313
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T04:11:42Z
updated: 2026-11-06T04:11:42Z
---
# Sampo check and the close's affected run store only ~400 characters of output, so the…
## Raw request
> sampo check and the close's affected run store only ~400 characters of output, so the failing-class list is cut off and nobody can tell load timeouts (the 480 s class kill) from assertions (3 builders and the lead hit it on 2026-11-06): store the full failing-class list with each class's cause (assertion, error, killed at 480 s) and print it in the refusal
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
- 2026-11-06T04:11:42Z created
## Follow-ups captured
