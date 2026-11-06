---
id: T-0504
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:30:32Z
---
# Heartbeat for unattended work (C099, value 5/5, effort M, risk low)
## Raw request
> FEATURE: Heartbeat for unattended work (C099, value 5/5, effort M, risk low)
>   first version: First version: fm run/night write a heartbeat file each loop and a preflight (guard fixture replay + fm doctor) before starting; a stale heartbeat triggers the fm notify command. Add a consecutive-failure breaker that stops the run.
>   what it is: Circuit breakers, retry classes, an external dead-man heartbeat and anomaly switches for headless runs.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:32Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
