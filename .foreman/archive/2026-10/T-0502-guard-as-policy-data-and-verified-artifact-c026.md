---
id: T-0502
type: SECURITY
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T16:27:38Z
done_in: T-0672
---
# Guard as policy data and verified artifact (C026, value 3/5, effort L, risk high)
## Raw request
> SECURITY: Guard as policy data and verified artifact (C026, value 3/5, effort L, risk high)
>   first version: Cheap first step only: log a rule id per block into the event log and report fire counts in fm friction/replay (decision ledger). Defer the data-table rewrite and IR; a rewrite risks loosening the guard, so gate it on the monotonicity check via fm replay.
>   what it is: Express guard rules as data with origins and fire records, compile them to an effect IR, and prove a rule change can't loosen the guard.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 13 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:17Z created
- 2026-10-09T15:40:13Z batched into T-0672
- 2026-10-09T16:27:38Z done in T-0672 (batch)
## Follow-ups captured
