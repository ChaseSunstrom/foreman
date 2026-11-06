---
id: T-0838
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-14T19:33:51Z
updated: 2026-10-14T19:45:33Z
---
# Later from T-0834: signal-and-leftover check for long-running verbs (fm serve, fm run, fm
## Raw request
> Later from T-0834: signal-and-leftover check for long-running verbs (fm serve, fm run, fm watch): ended by SIGTERM/SIGHUP, nothing stale left (T-0819 fixed fm bus watch) — later: no incident yet
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
- 2026-10-14T19:33:51Z created
- 2026-10-14T19:45:33Z dropped: Checked: fm run/night's heartbeat is removed at any exit Python sees and deliberately left on a kill, where stale_beats reports it as wedged or killed (fmserve.py:565-590); fm claude session records check pid liveness (fmsession.py:458,494); fm bus watch was the only leftover and T-0819 fixed it
## Follow-ups captured
