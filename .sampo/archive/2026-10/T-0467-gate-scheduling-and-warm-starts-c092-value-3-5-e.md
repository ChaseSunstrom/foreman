---
id: T-0467
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T17:22:11Z
done_in: T-0676
---
# Gate scheduling and warm starts (C092, value 3/5, effort S, risk low)
## Raw request
> FEATURE: Gate scheduling and warm starts (C092, value 3/5, effort S, risk low)
>   first version: Order gates in fm check by (recent failure rate / median runtime) from stored run times, keeping fail-fast; cancel remaining reviewer work on first blocker later.
>   what it is: Order and shard gates by failure odds, duration and return on time, cancelling reviewers on the first blocker.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T15:40:14Z batched into T-0676
- 2026-10-09T17:22:11Z done in T-0676 (batch)
## Follow-ups captured
