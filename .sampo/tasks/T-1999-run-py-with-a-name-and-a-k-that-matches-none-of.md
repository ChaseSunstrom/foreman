---
id: T-1999
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py]
depends_on: []
source: user
created: 2026-10-29T14:47:35Z
updated: 2026-10-29T15:19:28Z
done_in: T-2001
---
# run.py with a name and a -k that matches none of its tests says only "no test matches…
## Raw request
> FIX: run.py with a name and a -k that matches none of its tests says only "no test matches test_run", as if the module were missing; it now names the -k too, and the usage line lists NAME
> @plugin/tests/run.py @plugin/tests/test_run.py
> DONE-WHEN: the message names the -k patterns that filtered the module out :: python3 plugin/tests/run.py test_run -k UnknownNames
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
- 2026-10-29T14:47:35Z created
- 2026-10-29T14:47:39Z set tier=S
- 2026-10-29T14:47:48Z batched into T-2001
- 2026-10-29T15:19:28Z done in T-2001 (batch)
## Follow-ups captured
