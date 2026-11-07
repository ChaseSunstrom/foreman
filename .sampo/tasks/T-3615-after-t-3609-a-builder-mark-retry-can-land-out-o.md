---
id: T-3615
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T04:44:35Z
updated: 2026-11-07T04:44:35Z
---
# After T-3609, a builder mark retry can land out of order: a Stop mark waiting up to 3x5…
## Raw request
> FIX: after T-3609, a builder mark retry can land out of order: a Stop mark waiting up to 3x5 s in cli.mutate can land after a resumed builder's Start cleared builder_returned, so a live builder reads as returned; and mutate saves and logs a builder_mark event even when mark changed nothing. In hooks.py _mark_builder's mark (~4863), skip when the brief is already in the wanted state, and order marks by a start/stop sequence or timestamp so a later Start wins (T-3609 review)
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
- 2026-11-07T04:44:35Z created
## Follow-ups captured
