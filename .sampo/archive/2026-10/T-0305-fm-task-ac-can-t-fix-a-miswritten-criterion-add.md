---
id: T-0305
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T13:19:17Z
updated: 2026-10-04T13:21:59Z
---
# Fm task ac can't fix a miswritten criterion: add 'fm task ac ID set N --verify …' (a wrong
## Raw request
> fm task ac can't fix a miswritten criterion: add 'fm task ac ID set N --verify …' (a wrong criterion today means dropping the task)
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
- 2026-10-04T13:19:17Z created
- 2026-10-04T13:21:59Z dropped: dropped: an in-place criterion edit invites weakening a failing check; drop-and-recreate is cheap and visible (fm decide)
## Follow-ups captured
