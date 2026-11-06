---
id: T-3309
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T04:01:16Z
updated: 2026-11-06T04:01:16Z
---
# Other verbs in cli.py (around lines 2382, 2454, 2497, 2910) run a whole-repo 'git…
## Raw request
> Other verbs in cli.py (around lines 2382, 2454, 2497, 2910) run a whole-repo 'git worktree prune' after removing their scratch worktree, which drops other stale worktree records that lanes rely on (the bug T-3269's review fixed in bisect): remove only their own admin record
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
- 2026-11-06T04:01:16Z created
## Follow-ups captured
