---
id: T-2704
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:42Z
updated: 2026-11-02T23:19:40Z
trigger: genesis-review
trigger_key: 75373bf83f7d2f02
---
# FIX: cross-cutting review gen-3 #11 (what is being measured wrong): survival counts only…
## Raw request
> FIX: cross-cutting review gen-3 #11 (what is being measured wrong): survival counts only "134 finished the window" and reports 4% lost, while "1641 still in it (64 lost so far)" carries ten times as many losses; after T-2610 the headline rate rests on the oldest 8% of closes and "days since a lost task: 0" contradicts it in the same line. [6 lost (4%)]
> genesis-review 3:11
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
- 2026-11-02T23:14:42Z created
- 2026-11-02T23:19:40Z dropped: review.md marks it gap
## Follow-ups captured
