---
id: T-2711
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:46Z
updated: 2026-11-02T23:16:29Z
trigger: genesis-review
trigger_key: 6962da574b95c228
---
# FIX: cross-cutting review gen-3 #18 (what is presented ahead of its proof): fm drill…
## Raw request
> FIX: cross-cutting review gen-3 #18 (what is presented ahead of its proof): fm drill --restore's first run is presented as a pass while one project did not read back; the one that failed is the case a host wipe rehearsal exists for. [22 of 23 projects]
> genesis-review 3:18
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
- 2026-11-02T23:14:46Z created
- 2026-11-02T23:16:29Z dropped: the CHANGELOG states the failure ('read back 22 of 23 projects and found a ledger torn mid-file'), and T-2664 fixed the class; rerun today: still 22 of 23 because the newest snapshot (1.2.50, 2026-11-02T13:08) predates volt's --accept-damage, while the live volt ledger verifies OK (damage accepted); the next upgrade snapshot carries it
## Follow-ups captured
