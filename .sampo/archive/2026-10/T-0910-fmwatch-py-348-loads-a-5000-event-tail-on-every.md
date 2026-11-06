---
id: T-0910
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T19:10:34Z
updated: 2026-10-15T19:10:55Z
---
# Fmwatch.py:348` loads a 5000-event tail on every `fm ui --json`, and the poll runs often.
## Raw request
> fmwatch.py:348` loads a 5000-event tail on every `fm ui --json`, and the poll runs often. `today_done` and `done_days` could share one pass over `task_done` events instead
> (noticed by an agent; research T-0909-review)
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
- 2026-10-15T19:10:34Z created
- 2026-10-15T19:10:55Z dropped: done in T-0909: today_done and done_days now share one pass (_closes_since)
## Follow-ups captured
