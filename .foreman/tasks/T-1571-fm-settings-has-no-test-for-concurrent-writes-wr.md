---
id: T-1571
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T18:10:02Z
updated: 2026-10-22T18:13:26Z
---
# - `fm settings` has no test for concurrent writes, wrong-type values such as `theme = []`,
## Raw request
> - `fm settings` has no test for concurrent writes, wrong-type values such as `theme = []`, or mixed line endings
> (noticed by an agent; research T-1496-review)
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
- 2026-10-22T18:10:02Z created
- 2026-10-22T18:13:26Z dropped: covered in T-1496's second round: wrong-type values (test_settings ~95), mixed line endings (test_code_tui ~877) and the writer's folder lock (test_code_tui ~899) all have tests
## Follow-ups captured
