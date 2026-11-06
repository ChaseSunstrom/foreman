---
id: T-2010
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py]
depends_on: []
source: user
created: 2026-10-29T15:58:28Z
updated: 2026-10-29T16:36:52Z
done_in: T-2012
---
# One suite wait helper for fm check and fm ship, which says when it stops waiting and…
## Raw request
> CLEAN: one suite wait helper for fm check and fm ship, which says when it stops waiting and goes ahead
> @plugin/lib/fmcore.py
> DONE-WHEN: fm check, fm ship use c.wait_while; a wait that times out says so :: python3 plugin/tests/run.py test_core -k wait_while
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
- 2026-10-29T15:58:36Z set tier=S
- 2026-10-29T15:58:38Z batched into T-2012
- 2026-10-29T16:36:52Z done in T-2012 (batch)
## Follow-ups captured
