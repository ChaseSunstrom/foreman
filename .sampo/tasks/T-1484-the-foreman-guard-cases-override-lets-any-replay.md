---
id: T-1484
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T17:20:00Z
updated: 2026-10-22T17:31:42Z
---
# The `FOREMAN_GUARD_CASES` override lets any replay be recorded as green (the MEDIUM findin
## Raw request
> the `FOREMAN_GUARD_CASES` override lets any replay be recorded as green (the MEDIUM finding above). `fm code bench` is not covered by the new gate
> (noticed by an agent; research T-1401-review)
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
- 2026-10-22T17:20:00Z created
- 2026-10-22T17:31:42Z dropped: fixed in T-1401 (d52876df): a replay under FOREMAN_GUARD_CASES is recorded as substitute and never passes the gate
## Follow-ups captured
