---
id: T-0532
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:37Z
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:37Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
