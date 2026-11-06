---
id: T-3356
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T05:39:06Z
updated: 2026-11-06T05:39:06Z
---
# test_steer.Live.test_a_steer_is_expanded_in_the_background_filed_and_a_low_score_asks_for…
## Raw request
> test_steer.Live.test_a_steer_is_expanded_in_the_background_filed_and_a_low_score_asks_for_a_read races its background expansion: it waits for the filed task, then asserts the decision is already in 'decide --review' (test_steer.py:156); under load the decision lands later, so the ship's full suite failed and nothing was pushed (2026-11-06). Wait for the decision with the same wait_for helper
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
- 2026-11-06T05:39:06Z created
## Follow-ups captured
