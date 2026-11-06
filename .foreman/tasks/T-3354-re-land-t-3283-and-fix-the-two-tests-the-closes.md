---
id: T-3354
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/bus.py, plugin/tests/test_bus.py, plugin/tests/test_claims.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:36:49Z
updated: 2026-11-06T05:36:50Z
---
# Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be refused (T-3283 made it a note, so Sampo auto-reverted the merge, 3648d96de), and test_batch_edit.LaneMax expects lane max 50 to be refused (T-3297 raised the ceiling to 100)
## Raw request
> Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be refused (T-3283 made it a note, so Sampo auto-reverted the merge, 3648d96de), and test_batch_edit.LaneMax expects lane max 50 to be refused (T-3297 raised the ceiling to 100)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the revert is reverted (T-3283's bus.py change back), test_claims expects the take to succeed with a note naming the pre-claim, LaneMax refuses 101 and above, and test_bus, test_claims, test_batch_edit and test_diff_gates pass — verify with `python3 plugin/tests/run.py test_bus test_claims test_batch_edit test_diff_gates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] git revert the revert; update test_claims and LaneMax expectations  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:36:49Z created
## Follow-ups captured
