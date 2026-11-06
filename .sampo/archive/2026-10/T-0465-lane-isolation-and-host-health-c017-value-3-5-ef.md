---
id: T-0465
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T17:43:16Z
done_in: T-0675
---
# Lane isolation and host health (C017, value 3/5, effort S, risk low)
## Raw request
> FEATURE: Lane isolation and host health (C017, value 3/5, effort S, risk low)
>   first version: First step: fm run --parallel and drive lane offers check os.getloadavg/free memory and cut lane count; fm lane rm reaps leftover processes. Skip microVMs and CoW trees.
>   what it is: Give each lane its own runtime, copy-on-write tree, file leases and sandbox, and admit lanes by machine load.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T15:40:14Z batched into T-0675
- 2026-10-09T17:43:16Z done in T-0675 (batch)
## Follow-ups captured
