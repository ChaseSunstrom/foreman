---
id: T-1285
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T18:21:00Z
updated: 2026-10-20T23:32:01Z
---
# Fm code tui` can't send a request that is literally "tui". A worker that writes `.git/conf
## Raw request
> fm code tui` can't send a request that is literally "tui". A worker that writes `.git/config` is a gap in `fm code`'s own guard, separate from the TUI
> (noticed by an agent; research T-1283-review)
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
- 2026-10-20T18:21:00Z created
- 2026-10-20T23:32:01Z dropped: both parts already hold: a request that is literally 'tui' runs with fm code -- tui (the tui rewrite only applies to the token right after code), and the worker judge puts back .git/config, config.worktree and the global git config (fmcode._snapshot 'own', T-1270)
## Follow-ups captured
