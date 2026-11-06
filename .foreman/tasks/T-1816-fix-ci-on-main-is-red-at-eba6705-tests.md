---
id: T-1816
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T07:37:17Z
updated: 2026-10-28T07:40:18Z
---
# FIX: CI on main is red at eba6705 (tests)
## Raw request
> FIX: CI on main is red at eba6705 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/foreman/commit/eba670508b1a0db5ab47bb61d37ba5dd39e90471
> CI-red: eba670508b1a0db5ab47bb61d37ba5dd39e90471
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
- 2026-10-28T07:37:17Z created
- 2026-10-28T07:40:18Z dropped: false alarm from T-1810's first sweep: main's newest tests run (be5743a6) was cancelled because the experimental macOS job hit its 35-min limit (T-1809) after both Ubuntu jobs passed; the sweep skipped the cancelled run and let eba6705's older failure speak. Fixed in T-1810: a cancelled newest run now says nothing
## Follow-ups captured
