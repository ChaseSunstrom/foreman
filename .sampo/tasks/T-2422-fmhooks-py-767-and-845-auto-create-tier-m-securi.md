---
id: T-2422
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T15:23:25Z
updated: 2026-11-02T01:57:48Z
---
# fmhooks.py:767 and 845 auto-create tier M SECURITY tasks with no Interpretation or…
## Raw request
> fmhooks.py:767 and 845 auto-create tier M SECURITY tasks with no Interpretation or Approach, so each needs a manual plan before focus
> (noticed by an agent; research T-2335-review)
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
- 2026-10-31T15:23:25Z created
- 2026-11-02T01:57:48Z dropped: fixed by T-2335: both hook paths (fmhooks first-brief and queue-requests) pass --harness-plan=hook, and plan_gaps skips Interpretation, Approach and the content gate for a harness_plan brief (fmcore.plan_gaps), so an auto-created SECURITY M task focuses without a manual plan; the review note predates it
## Follow-ups captured
