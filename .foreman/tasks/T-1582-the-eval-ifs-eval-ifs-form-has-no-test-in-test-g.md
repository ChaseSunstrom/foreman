---
id: T-1582
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T18:32:06Z
updated: 2026-10-22T18:32:46Z
---
# The `eval 'IFS=…'; eval "…\$IFS…"` form has no test in test_guard.py or test_guard_pipes.p
## Raw request
> the `eval 'IFS=…'; eval "…\$IFS…"` form has no test in test_guard.py or test_guard_pipes.py. Lines 960-961 cover only the unescaped forms
> (noticed by an agent; research T-1473-review)
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
- 2026-10-22T18:32:06Z created
- 2026-10-22T18:32:46Z dropped: covered in T-1473: SeparatorProse tests the eval…\$IFS forms
## Follow-ups captured
