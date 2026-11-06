---
id: T-2274
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T05:20:46Z
updated: 2026-10-31T08:20:27Z
---
# fm code's planner (fmcode._make_task) writes one reading and no Risks section, so an L…
## Raw request
> fm code's planner (fmcode._make_task) writes one reading and no Risks section, so an L task it makes can never pass T-2269's plan gate: give L plans 2+ readings and a Risks and rollback section
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
- 2026-10-31T05:20:46Z created
- 2026-10-31T08:20:27Z dropped: premise doesn't hold: fmcode.check_plan refuses any tier but S or M (fmcode.py:209), so _make_task never makes an L task and T-2269's L plan gate can't be hit from fm code
## Follow-ups captured
