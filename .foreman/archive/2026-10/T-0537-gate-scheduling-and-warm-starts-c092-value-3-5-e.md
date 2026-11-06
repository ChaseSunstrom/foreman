---
id: T-0537
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:38Z
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:38Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
