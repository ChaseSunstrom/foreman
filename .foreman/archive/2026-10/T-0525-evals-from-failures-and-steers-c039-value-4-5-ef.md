---
id: T-0525
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:36Z
---
# Evals from failures and steers (C039, value 4/5, effort M, risk low)
## Raw request
> FEATURE: Evals from failures and steers (C039, value 4/5, effort M, risk low)
>   first version: Auto-run fm evals when a task is blocked and log guard false positives (user steer after a block) into an eval inbox; gate releases on fm bench gate plus these cases. Skip predictive failure and randomized trials.
>   what it is: Capture an eval automatically from every block, steer or guard false positive and gate releases on them.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 14 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:36Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
