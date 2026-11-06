---
id: T-2011
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmloop.py]
depends_on: []
source: user
created: 2026-10-29T15:58:28Z
updated: 2026-10-29T16:36:52Z
done_in: T-2012
---
# When the forever loop stops, its decision and fm loop say how many rounds ran and tasks…
## Raw request
> FEATURE: when the forever loop stops, its decision and fm loop say how many rounds ran and tasks closed since it started
> @plugin/lib/fmloop.py
> DONE-WHEN: the loop-off decision names the rounds run and tasks closed :: python3 plugin/tests/run.py test_loop -k says_what_it_shipped
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
- 2026-10-29T15:58:37Z set tier=S
- 2026-10-29T15:58:38Z batched into T-2012
- 2026-10-29T16:36:52Z done in T-2012 (batch)
## Follow-ups captured
