---
id: T-3475
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T17:41:39Z
updated: 2026-11-06T17:41:39Z
group: guard refuses legitimate lane and task work
---
# The Ward refuses git merge in a builder worktree under the main checkout…
## Raw request
> The Ward refuses git merge in a builder worktree under the main checkout (.claude/worktrees/agent-*) whatever the lane's focus, and in a lane beside the repo whenever the main checkout has an active task, so a train's left-out lanes can't have their conflicts resolved in place by me or a fixer agent; today 16 lanes had to be moved (lane rm --why, lane new) to merge their old branches (guard design: for the user)
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
- 2026-11-06T17:41:39Z created
## Follow-ups captured
