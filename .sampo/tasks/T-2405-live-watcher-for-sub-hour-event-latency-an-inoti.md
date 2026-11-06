---
id: T-2405
type: FEATURE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T14:24:16Z
updated: 2026-11-02T00:30:21Z
revisit: 2026-12-01
---
# Live watcher for sub-hour event latency (an inotify or poll daemon beside the hourly…
## Raw request
> Live watcher for sub-hour event latency (an inotify or poll daemon beside the hourly tick; Mission 8 approach C, not built in gen 1: build it once a red main has waited past one tick twice; installing it is a system ask for the user's yes)
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
- 2026-10-31T14:24:16Z created
- 2026-11-02T00:29:54Z deferred: its trigger can't occur yet: no night tick has ever run here (0 night_tick events: the hourly timers wait for the user's install, fm night --install is theirs), so no red main has waited past a tick; revisit once ticks run and one has waited twice (revisit 2026-12-01)
- 2026-11-02T00:30:21Z correction: the hourly tick IS installed and runs (systemd foreman-tick timer, last 18:00 CST: '0 order(s) fired, 0 captured'); it logs night_tick only when something happened, so 0 events means no tick has caught a red main, not that none ran. The deferral stands on that: the trigger (a red main waiting past a tick, twice) hasn't occurred
## Follow-ups captured
