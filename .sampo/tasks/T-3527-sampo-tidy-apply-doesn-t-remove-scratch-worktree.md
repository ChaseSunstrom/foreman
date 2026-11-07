---
id: T-3527
type: CLEAN
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:26:57Z
updated: 2026-11-06T19:27:24Z
---
# Sampo tidy --apply doesn't remove scratch worktrees git still lists under the temp dir…
## Raw request
> CLEAN: sampo tidy --apply doesn't remove scratch worktrees git still lists under the temp dir (7 fm-verify-*/sampo-train-* today, fits.tidy counts them) nor merged worktree-agent-* branches (101); prune gone ones, remove hour-old temp ones, delete merged agent branches
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
- 2026-11-06T19:26:57Z created
- 2026-11-06T19:27:24Z dropped: duplicate: T-3507 (tidy removes the stale scratch worktrees, built, queued) and T-3515 (the merged worktree-agent-* branches)
## Follow-ups captured
