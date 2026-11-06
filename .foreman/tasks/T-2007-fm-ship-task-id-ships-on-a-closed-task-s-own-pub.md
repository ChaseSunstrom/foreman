---
id: T-2007
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrelease.py]
depends_on: []
source: user
created: 2026-10-29T15:58:28Z
updated: 2026-10-29T16:36:52Z
done_in: T-2012
---
# fm ship --task ID ships on a closed task's own publish grant, so a finished task ships…
## Raw request
> FEATURE: fm ship --task ID ships on a closed task's own publish grant, so a finished task ships without a separate ship task
> @plugin/lib/fmrelease.py
> DONE-WHEN: fm ship --task T-N pushes on T-N's grant and spends it; a task without the grant is refused, nothing pushed :: python3 plugin/tests/run.py test_ship -k ship_on_a_named_tasks_grant
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
- 2026-10-29T15:58:28Z created
- 2026-10-29T15:58:38Z batched into T-2012
- 2026-10-29T16:36:52Z done in T-2012 (batch)
## Follow-ups captured
