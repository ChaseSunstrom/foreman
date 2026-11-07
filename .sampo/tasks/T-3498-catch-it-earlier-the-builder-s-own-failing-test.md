---
id: T-3498
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-06T19:02:08Z
updated: 2026-11-06T19:02:08Z
group: builder regression tests before lane review
---
# Catch it earlier: the builder's own failing test before the fix, then the lane review;…
## Raw request
> T-3478 (Self-check: the landing rate: N finished lanes wait, M landed in the last 2 h (minutes each), the pile clears in H hours at that rate; a wait the user had to ask about ('why is this taking so long just to push?') is the miss) wasn't caught before it shipped: the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
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
- 2026-11-06T19:02:08Z created
## Follow-ups captured
