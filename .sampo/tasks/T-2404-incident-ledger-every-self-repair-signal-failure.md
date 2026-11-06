---
id: T-2404
type: FEATURE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T14:24:14Z
updated: 2026-11-02T00:21:21Z
revisit: 2026-12-01
---
# Incident ledger: every self-repair signal (failures, steer checks, CI red, doctor FAILs,…
## Raw request
> Incident ledger: every self-repair signal (failures, steer checks, CI red, doctor FAILs, corrections) feeds one record per cause, so one cause files one task (Mission 8 approach B, not built in gen 1: build it once one cause has filed two tasks from two signals, twice)
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
- 2026-10-31T14:24:14Z created
- 2026-11-02T00:21:21Z deferred: its own trigger isn't met: across the task record one cause filed duplicates from two different signals once (T-0705: discovered + followup), not twice; the duplicates that do pile up come from one signal (ci: T-2462 got 9, T-2441 3), which a per-cause key in ci-watch fixes (captured) (revisit 2026-12-01)
## Follow-ups captured
