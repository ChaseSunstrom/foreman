---
id: T-1006
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T01:02:48Z
updated: 2026-10-16T01:07:26Z
---
# Catch it earlier: T-1001's test seeded by-pid records for the killed session, so it never
## Raw request
> T-1003 (Fleet drops a killed session even after a later SessionStart swept its by-pid records) wasn't caught before it shipped: T-1001's test seeded by-pid records for the killed session, so it never covered a later SessionStart sweeping them
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
- 2026-10-16T01:02:48Z created
- 2026-10-16T01:07:26Z dropped: covered: T-1003's test lists a snapshot with no by-pid record at all (the swept case)
## Follow-ups captured
