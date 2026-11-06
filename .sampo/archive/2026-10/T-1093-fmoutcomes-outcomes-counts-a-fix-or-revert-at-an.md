---
id: T-1093
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T04:22:34Z
updated: 2026-10-16T04:59:33Z
---
# Fmoutcomes.outcomes` counts a FIX or revert at any later date against a task (fmoutcomes.p
## Raw request
> fmoutcomes.outcomes` counts a FIX or revert at any later date against a task (fmoutcomes.py:39-77), so `fm outcomes` "held" understates failures for old tasks. T-1060 fixes this
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
- 2026-10-16T04:59:33Z dropped: folded into T-1060 (survival grading): its plan adds the 30-day window
## Follow-ups captured
