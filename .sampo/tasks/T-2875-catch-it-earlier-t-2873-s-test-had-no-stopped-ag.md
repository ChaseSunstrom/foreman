---
id: T-2875
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-11-04T03:18:39Z
updated: 2026-11-04T03:19:19Z
---
# Catch it earlier: T-2873's test had no stopped agent in the window
## Raw request
> T-2874 (The drive's T-2873 union added every agent the event scan saw start, finished ones too, so two done agents held the drive; only the scan's still-running agents join the engine's list) wasn't caught before it shipped: T-2873's test had no stopped agent in the window
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
- 2026-11-04T03:18:39Z created
- 2026-11-04T03:19:19Z dropped: done in T-2874: test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive now starts and stops an agent in the window and asserts it stays out
## Follow-ups captured
