---
id: T-0462
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T16:27:38Z
done_in: T-0672
---
# Cleanup as a done gate (C036, value 3/5, effort S, risk low)
## Raw request
> SECURITY: Cleanup as a done gate (C036, value 3/5, effort S, risk low)
>   first version: In fm check/finish, list untracked files and stray tmp/worktrees the task created that are outside its scope and warn (block only with a flag). Reuse fmtidy lists.
>   what it is: Sweep leftovers after every task, treat cleanup as a done obligation and run a recurring janitor with deletion-safety proof.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T15:40:13Z batched into T-0672
- 2026-10-09T16:27:38Z done in T-0672 (batch)
## Follow-ups captured
