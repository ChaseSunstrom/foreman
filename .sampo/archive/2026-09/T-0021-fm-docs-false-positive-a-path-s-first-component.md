---
id: T-0021
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-09-26T14:58:56Z
updated: 2026-09-26T15:07:44Z
---
# Fm docs false positive: a path's first component counts as 'in the repo' if it merely exis
## Raw request
> fm docs false positive: a path's first component counts as 'in the repo' if it merely exists on disk; Claude Code's .claude/scheduled_tasks.lock (ignored) made .claude/ exist, so '.claude/tdd/' in a playbook reference became drift. Count only top-level names with tracked or untracked-not-ignored content
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
- 2026-09-26T14:58:56Z created
- 2026-09-26T15:07:44Z dropped: fixed inline in T-0014 (b212907)
## Follow-ups captured
