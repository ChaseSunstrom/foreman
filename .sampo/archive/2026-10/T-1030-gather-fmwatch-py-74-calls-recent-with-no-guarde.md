---
id: T-1030
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T02:22:02Z
updated: 2026-10-16T02:28:38Z
---
# Gather()` (`fmwatch.py:74`) calls `_recent` with no `_guarded`, so one bad ledger line tak
## Raw request
> gather()` (`fmwatch.py:74`) calls `_recent` with no `_guarded`, so one bad ledger line takes down the whole view
> (noticed by an agent; research T-1026-review)
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
- 2026-10-16T02:22:02Z created
- 2026-10-16T02:28:38Z dropped: covered in T-1026: _recent and _history take str(ts), so a malformed ledger time no longer raises in gather()
## Follow-ups captured
