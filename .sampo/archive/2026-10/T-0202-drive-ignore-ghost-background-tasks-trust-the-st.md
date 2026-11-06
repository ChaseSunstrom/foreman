---
id: T-0202
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T04:07:01Z
updated: 2026-10-04T04:14:30Z
---
# Drive: ignore ghost background tasks — trust the Stop payload's background_tasks when pres
## Raw request
> Drive: ignore ghost background tasks — trust the Stop payload's background_tasks when present and empty; shorten the 2h bg_start backstop (fmhooks.py _running ~1306, drive_wait ~1365)
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
- 2026-10-04T04:07:01Z created
- 2026-10-04T04:14:30Z dropped: premise false: of the last 25 drive waits none named a task already finished (events.jsonl bg_done before the wait); the engine's background_tasks list is already preferred (fmhooks.py _drive). Every wait was real background work.
## Follow-ups captured
