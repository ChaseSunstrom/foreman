---
id: T-3462
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-06T16:23:29Z
updated: 2026-11-06T16:23:29Z
group: builder regression tests before lane review
---
# Catch it earlier: the builder's own failing test before the fix, then the lane review;…
## Raw request
> T-3456 (The post-merge newest-first probe is skipped whenever any pending merge carries after_reverts, so after one revert every later record runs oldest first on old trees (20 pending, the slot-pool false reds return)) wasn't caught before it shipped: the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
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
- 2026-11-06T16:23:29Z created
## Follow-ups captured
