---
id: T-2432
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T17:53:44Z
updated: 2026-11-02T01:27:49Z
---
# Drive bounce burns context: with every lane slot full and a lane merge running in the…
## Raw request
> Drive bounce burns context: with every lane slot full and a lane merge running in the background, the Stop hook re-offers the same blocked task every turn (T-2387 eight times in a row at ~520k context each); it should recognise 'slots full + merge in flight' as waiting and stay quiet until a notification
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
- 2026-10-31T17:53:44Z created
- 2026-11-02T01:27:49Z dropped: fixed since: the drive offers each task once per stage per session (T-2513: made id:status, never re-offered after an active-task change) and at most OFFERS_MAX (3) per active task (T-0401), so the same blocked task can't be offered eight Stops running; the Stop tests test_a_new_background_set_does_not_offer_the_same_side_task_again and test_a_side_task_planned_since_its_offer_is_offered_once_more_for_its_draft pass
## Follow-ups captured
