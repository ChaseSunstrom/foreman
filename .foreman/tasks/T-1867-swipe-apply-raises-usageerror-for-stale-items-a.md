---
id: T-1867
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T22:34:59Z
updated: 2026-10-28T22:40:10Z
---
# Swipe_apply` raises `UsageError` for stale items. A `--apply` batch aborts all-or-nothing,
## Raw request
> swipe_apply` raises `UsageError` for stale items. A `--apply` batch aborts all-or-nothing, which is fine. Interactive callers now need per-item handling (see the edge finding)
> (noticed by an agent; research T-1866-review)
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
- 2026-10-28T22:34:59Z created
- 2026-10-28T22:40:10Z dropped: done in T-1866: swipe_loop and the app catch UsageError per item (test_an_item_changed_elsewhere…, test_a_row_changed_elsewhere…)
## Follow-ups captured
