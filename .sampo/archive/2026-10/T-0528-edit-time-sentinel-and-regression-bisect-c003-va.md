---
id: T-0528
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:37Z
---
# Edit-time sentinel and regression bisect (C003, value 4/5, effort M, risk med)
## Raw request
> FEATURE: Edit-time sentinel and regression bisect (C003, value 4/5, effort M, risk med)
>   first version: First version: fm sentinel --bisect runs git bisect in a throwaway worktree on a sentinel-failing check and captures the culprit commit/task as a FIX item; edit-time shadow CI deferred.
>   what it is: Run the affected tests as the code is edited, like a shadow CI, with mutation proof of what the sentinel covers.
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
- 2026-10-09T14:30:37Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
