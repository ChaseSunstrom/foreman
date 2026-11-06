---
id: T-3184
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T08:58:29Z
updated: 2026-11-05T09:55:51Z
---
# Sampo lane merge T-3053 failed with 'git merge worktree-agent-a8d6e91bb90952d63 failed…
## Raw request
> sampo lane merge T-3053 failed with 'git merge worktree-agent-a8d6e91bb90952d63 failed and was aborted: fatal: this operation must be run in a work tree' although the lane (foreman.lanes/T-3053, branch foreman/T-3053 holding the kept branch) is a valid worktree and other lanes merged fine; find which git call ran outside a work tree (a GIT_DIR leaked from the self-change gate's scratch trees?)
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
- 2026-11-05T08:58:29Z created
- 2026-11-05T09:55:51Z dropped: explained and fixed: core.bare=true leaked into the real .git/config (T-3185) made every git merge into main fail with 'must be run in a work tree'
## Follow-ups captured
