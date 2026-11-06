---
id: T-1423
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T19:53:14Z
updated: 2026-10-21T21:25:32Z
done_in: T-1432
---
# Fm code's Run.usage adds the server's reported token counts with no type check, so a serve
## Raw request
> fm code's Run.usage adds the server's reported token counts with no type check, so a server reporting usage as a string crashes the run with a TypeError (T-1404 builder)
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
- 2026-10-21T19:53:14Z created
- 2026-10-21T20:44:12Z batched into T-1432
- 2026-10-21T21:25:32Z done in T-1432 (batch)
## Follow-ups captured
