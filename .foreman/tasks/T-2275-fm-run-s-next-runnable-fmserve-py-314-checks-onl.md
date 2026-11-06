---
id: T-2275
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T05:26:03Z
updated: 2026-10-31T05:48:38Z
---
# fm run's _next_runnable (fmserve.py:~314) checks only waits_on_user, not plan_gaps, so a…
## Raw request
> fm run's _next_runnable (fmserve.py:~314) checks only waits_on_user, not plan_gaps, so a headless run can pick a task fm focus would refuse (an unplanned brief) and stall until no progress is made: skip briefs with plan gaps, naming them
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
- 2026-10-31T05:26:03Z created
- 2026-10-31T05:48:38Z dropped: not a stall: fm run hands the task to a headless agent session, and a plan gap refused at focus names its fix (fm task set ID --section …), which the session fills before focusing; skipping gated tasks would leave planned work unrun
## Follow-ups captured
