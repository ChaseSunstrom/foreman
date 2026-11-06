---
id: T-1092
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T04:22:34Z
updated: 2026-10-16T04:59:32Z
---
# Fmcost._task_at` (fmcost.py:143) never returns None after the first ledger event, so the "
## Raw request
> fmcost._task_at` (fmcost.py:143) never returns None after the first ledger event, so the "(no task)" bucket in `fm cost` hides work done outside tasks. The label misleads
> (noticed by an agent; research wave1-plan-a306a171bb6861f90)
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
- 2026-10-16T04:22:34Z created
- 2026-10-16T04:59:32Z dropped: folded into T-1079 (unexplained spend): its plan replaces the misleading (no task) bucket with a session/gap attribution
## Follow-ups captured
