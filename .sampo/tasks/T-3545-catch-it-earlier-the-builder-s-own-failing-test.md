---
id: T-3545
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-06T22:22:08Z
updated: 2026-11-06T22:22:08Z
group: builder regression tests before lane review
---
# Catch it earlier: the builder's own failing test before the fix, then the lane review;…
## Raw request
> T-3492 (A revert that was itself undone (a re-land reverting it) still spends 3 risk points, so false post-merge reverts (4 of today's 6, re-landed by T-3445/T-3450/T-3454) used up the risk budget and paused the self-improvement pass) wasn't caught before it shipped: the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
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
- 2026-11-06T22:22:08Z created
## Follow-ups captured
