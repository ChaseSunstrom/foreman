---
id: T-0518
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
# Context economy (C091, value 4/5, effort M, risk low)
## Raw request
> FEATURE: Context economy (C091, value 4/5, effort M, risk low)
>   first version: Add step-boundary compaction with a curated handoff (extend T-0098's task-boundary rule to M/L steps) and a session rotate when context slope turns bad; reuse checkpoint/resume.
>   what it is: Compact at step boundaries, rotate sessions, serve reads as deltas and share prompt-cache prefixes.
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
- 2026-10-09T14:30:35Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
