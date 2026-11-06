---
id: T-0816
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-14T18:02:36Z
updated: 2026-10-14T18:08:11Z
---
# Builders: a PostToolUse nudge when Claude Code says a command is 'isolated in the worktree
## Raw request
> Builders: a PostToolUse nudge when Claude Code says a command is 'isolated in the worktree' (14x in the digest): run from the worktree root, no cd, no VAR=
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
- 2026-10-14T18:02:36Z created
- 2026-10-14T18:08:11Z dropped: Claude Code's own refusal already says how to fix it ('Split it into plain, separate commands and run them from <worktree>'), and the builder contract covers it (T-0399, T-0808); a hook note would repeat both
## Follow-ups captured
