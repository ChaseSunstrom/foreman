---
id: T-0515
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:34Z
---
# Dependency-aware lane dispatch (C014, value 4/5, effort M, risk low)
## Raw request
> FEATURE: Dependency-aware lane dispatch (C014, value 4/5, effort M, risk low)
>   first version: Make --parallel pick lanes from the fm relate graph plus a predicted file footprint (scope plus fm impact/co-change), and have drive offer the same set; skip solver/cost-prediction extras.
>   what it is: Dispatch the queue as a dependency graph across builder lanes, scheduled by predicted cost, risk and file footprint, with a durable scheduler.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:34Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
