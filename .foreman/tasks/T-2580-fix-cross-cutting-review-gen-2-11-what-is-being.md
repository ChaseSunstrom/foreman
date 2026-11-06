---
id: T-2580
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:27Z
updated: 2026-11-02T08:25:38Z
trigger: genesis-review
trigger_key: c5fcac593a181af5
---
# FIX: cross-cutting review gen-2 #11 (what is being measured wrong): The 306-scenario and…
## Raw request
> FIX: cross-cutting review gen-2 #11 (what is being measured wrong): The 306-scenario and 249-scenario lines are oracle arms scoring 100%; the only foreman lines are a 3-scenario smoke (s32-015) and a haiku run, so the scorecard measures the answer key, not the harness. [s21-013 (oracle): 306 scenarios; found 261/261, 0 false alarms, fixed 414/414, 0 exam defects]
> genesis-review 2:11
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
- 2026-11-02T08:23:27Z created
- 2026-11-02T08:25:38Z dropped: review.md marks it dismissed: the scorecard counts only foreman held-out lines and reads 0/13 saying so; oracle lines exist to validate the keys
## Follow-ups captured
