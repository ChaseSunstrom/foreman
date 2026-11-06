---
id: T-2706
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:43Z
updated: 2026-11-02T23:19:42Z
trigger: genesis-review
trigger_key: b0eaf6e26404798e
---
# FIX: cross-cutting review gen-3 #13 (what is being measured wrong): the FEATURE M record…
## Raw request
> FIX: cross-cutting review gen-3 #13 (what is being measured wrong): the FEATURE M record is 578 closes with "548 still in the 30-day window", so every held rate in the track record is computed over about 5% of its bucket and FIX M's "7 of 9 held" is a nine-sample claim. [29 of 30 held]
> genesis-review 3:13
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
- 2026-11-02T23:14:43Z created
- 2026-11-02T23:19:42Z dropped: review.md marks it dismissed: the track record line already prints its sample beside each rate ('22 of 23 held, 433 still in the 30-day window'), so a nine-sample claim reads as nine samples
## Follow-ups captured
