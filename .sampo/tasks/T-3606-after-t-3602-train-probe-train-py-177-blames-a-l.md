---
id: T-3606
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T04:27:47Z
updated: 2026-11-07T04:27:47Z
---
# After T-3602, train._probe (train.py ~177) blames a lane with 'fail on the base: exit N'…
## Raw request
> PERFORMANCE: after T-3602, train._probe (train.py ~177) blames a lane with 'fail on the base: exit N' whenever _red returns [] (uncertain parse), which T-3602 makes more common; rerun the whole affected command once before blaming the base, so a flake or an unparsed failure never parks a good lane (T-3602 review)
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
- 2026-11-07T04:27:47Z created
## Follow-ups captured
