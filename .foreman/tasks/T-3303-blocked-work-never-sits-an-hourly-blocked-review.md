---
id: T-3303
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T03:55:07Z
updated: 2026-11-06T03:55:09Z
---
# Blocked work never sits: an hourly blocked review unblocks what's ready, refuses capacity as a block reason, and escalates the rest
## Raw request
> Blocked work never sits: an hourly blocked review unblocks what's ready, refuses capacity as a block reason, and escalates the rest
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo blocked review unblocks every blocked task whose depends_on and named T-ids are all closed, and every one blocked only for a builder slot or the merge queue (capacity is never a block: the task stays planned), logging each with its reason — verify with `python3 plugin/tests/run.py test_blocked_review`
- [ ] sampo task block refuses a reason that is only capacity (builder slot, lanes, merge queue) and says to leave the task planned — verify with `python3 plugin/tests/run.py test_blocked_review`
- [ ] the hourly tick and the drive run the review; a block older than 48 h that still can't move is named in the drive line with its reason and one proposed action (decide, drop as superseded, split, or the user's one ask), and the user-only ones go once a day into the report — verify with `python3 plugin/tests/run.py test_blocked_review test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: deps closed -> unblocked; slot-only reason -> unblocked and block refused; 48 h stale -> drive line  <- CURRENT
2. [ ] blocked.py: review(p) + the block-reason check in task block
3. [ ] wire into tick and the drive line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T03:55:07Z created
## Follow-ups captured
