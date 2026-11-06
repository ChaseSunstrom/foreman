---
id: T-2581
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:27Z
updated: 2026-11-02T08:25:40Z
trigger: genesis-review
trigger_key: 24b6d0872f2b412f
---
# FIX: cross-cutting review gen-2 #12 (what is being measured wrong): The CHANGELOG…
## Raw request
> FIX: cross-cutting review gen-2 #12 (what is being measured wrong): The CHANGELOG compares the cleaned history to the old history and omits the exam's own naive 0.116; against the baseline the gain is 0.002 on one decimal of noise. [overlap 0.118 against 0.113]
> genesis-review 2:12
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
- 2026-11-02T08:23:27Z created
- 2026-11-02T08:25:40Z dropped: review.md marks it dismissed: folded into #22 (T-2591): CHANGELOG numbers carry their counts and baselines
## Follow-ups captured
