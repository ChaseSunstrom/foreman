---
id: T-1994
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py]
depends_on: []
source: user
created: 2026-10-29T14:38:56Z
updated: 2026-10-29T14:46:29Z
done_in: T-1996
---
# run.py test_cli -k pattern runs all of test_cli (names and -k are unioned), so a…
## Raw request
> PERF: run.py test_cli -k pattern runs all of test_cli (names and -k are unioned), so a per-step check meant to run one test runs the whole module; with both given, names pick the modules and -k filters within them, as pytest does
> @plugin/tests/run.py @plugin/tests/test_run.py
> DONE-WHEN: run.py with a name and a -k runs only the tests matching both :: python3 plugin/tests/run.py -k test_run
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
- 2026-10-29T14:38:56Z created
- 2026-10-29T14:39:00Z set tier=S
- 2026-10-29T14:39:06Z batched into T-1996
- 2026-10-29T14:46:29Z done in T-1996 (batch)
## Follow-ups captured
