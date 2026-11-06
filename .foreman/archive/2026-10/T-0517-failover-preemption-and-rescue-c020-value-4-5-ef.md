---
id: T-0517
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:35Z
---
# Failover, preemption and rescue (C020, value 4/5, effort M, risk low)
## Raw request
> FEATURE: Failover, preemption and rescue (C020, value 4/5, effort M, risk low)
>   first version: First step: fm run/drive detect a session with no progress for N minutes (ledger/transcript mtime), kill and resume it from the checkpoint, and on a usage limit hand the task to another installed agent via fm session.
>   what it is: Continue a task on another agent or harness when quota runs out or a session dies, and park and resume lanes at the exact step.
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:35Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
