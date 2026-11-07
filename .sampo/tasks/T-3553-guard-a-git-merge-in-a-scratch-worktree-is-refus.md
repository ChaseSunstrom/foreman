---
id: T-3553
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-07T00:39:09Z
updated: 2026-11-07T00:39:09Z
---
# Guard: a git merge in a scratch worktree is refused with only the lane-merge hint;…
## Raw request
> guard: a git merge in a scratch worktree is refused with only the lane-merge hint; fmguard.py:243-245 checks '; git merge)' before the scratch-worktree hint at :246-249, so the merge hint always wins: when the merge hint fires inside a non-lane worktree, give the cd-to-literal-dir advice instead (2 fires)
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
- 2026-11-07T00:39:09Z created
## Follow-ups captured
