---
id: T-2036
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T19:54:46Z
updated: 2026-10-29T19:59:42Z
---
# Stop's drive nudge 'background work is still running… end the turn with one line naming…
## Raw request
> PERF: Stop's drive nudge 'background work is still running… end the turn with one line naming what you wait on' fires even when the reply already names the running job id: an extra round trip per background wait; skip the generic nudge when the reply names one of the running ids
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
- 2026-10-29T19:54:46Z created
- 2026-10-29T19:59:42Z dropped: Not doing: the generic wait nudge is T-0364's anti-idle push and exists for exactly the replies that say what they wait on (test_drive_waits_while_a_background_command_runs pins it); skipping it saves one cached round trip per wait set but brings back idling, which the user ranks above token cost
## Follow-ups captured
