---
id: T-1471
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T16:03:59Z
updated: 2026-10-22T16:04:06Z
---
# Fmmodels.py:103-104` has the OpenAI rows out of date order (2025-07-28 before 2025-10-27).
## Raw request
> fmmodels.py:103-104` has the OpenAI rows out of date order (2025-07-28 before 2025-10-27). This is harmless but inconsistent
> (noticed by an agent; research T-1433-deprecations)
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
- 2026-10-22T16:03:59Z created
- 2026-10-22T16:04:06Z dropped: folded into T-1433, which rewrites _RETIRED_ROWS and can order it by date
## Follow-ups captured
