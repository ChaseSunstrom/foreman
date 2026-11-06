---
id: T-3317
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T04:23:07Z
updated: 2026-11-06T04:23:07Z
---
# Edits outside the repo stale a task's audits: hooks.py:3129 attributes every Write/Edit…
## Raw request
> Edits outside the repo stale a task's audits: hooks.py:3129 attributes every Write/Edit to the active task, scratchpad and memory files included, and core.last_change (core.py:3424) counts them, so T-3297's five audits read 'predate the last change' after I wrote a diagram in the scratchpad and a memory note; no repo file had changed. last_change should count only files under p.root (the diff reviewers saw); test: an out-of-repo touched event leaves audits fresh
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
- 2026-11-06T04:23:07Z created
## Follow-ups captured
