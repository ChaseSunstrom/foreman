---
id: T-0568
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:44Z
---
# Instruction tuning across models (C042, value 3/5, effort M, risk med)
## Raw request
> FEATURE: Instruction tuning across models (C042, value 3/5, effort M, risk med)
>   first version: Run fm evolve --drop over rules/skills on each new model id via bench models, report files that earn no tokens. Skip fuzzing, shadow runs and bake-off as duplicates of evolve+bench.
>   what it is: Tune, shrink and ablate instructions per model, delete crutches on new models and test instruction variants in shadow.
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
- 2026-10-09T14:30:44Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
