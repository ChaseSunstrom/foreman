---
id: T-1979
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T12:10:02Z
updated: 2026-10-29T12:25:19Z
done_in: T-1980
---
# C.first_touch counts a Write outside the project (a scratchpad file) as the task's first e
## Raw request
> FIX: c.first_touch counts a Write outside the project (a scratchpad file) as the task's first edit, unlike task_touches, so a CLEAN ship task that edited no repo file was refused for a missing behaviour lock (T-1975). first_touch keeps only project files, as task_touches does (fmcore first_touch).
> DONE-WHEN: a CLEAN task whose only edit is outside the project closes without a behaviour lock :: python3 plugin/tests/run.py test_close_gates
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
- 2026-10-29T12:10:02Z created
- 2026-10-29T12:10:05Z batched into T-1980
- 2026-10-29T12:25:19Z done in T-1980 (batch)
## Follow-ups captured
