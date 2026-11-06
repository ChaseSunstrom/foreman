---
id: T-2003
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py]
depends_on: []
source: user
created: 2026-10-29T15:20:28Z
updated: 2026-10-29T15:56:04Z
done_in: T-2005
---
# run.py's "no test matches test_doctor with -k core_integrity" gives no way forward when…
## Raw request
> FIX: run.py's "no test matches test_doctor with -k core_integrity" gives no way forward when the test is named CoreIntegrity; it now suggests up to three test ids that match once case and underscores are ignored ("did you mean -k CoreIntegrity?")
> @plugin/tests/run.py @plugin/tests/test_run.py
> DONE-WHEN: a -k differing only in case and underscores gets the real name suggested :: python3 plugin/tests/run.py test_run -k UnknownNames
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
Options: (a) make -k case/underscore-insensitive (breaks parity with unittest -k, which run_one passes through), (b) on a miss, rediscover with no filter and suggest ids whose folded form (lowercase, no underscores) contains the folded pattern, (c) difflib close matches over test ids. Choice (b): exact for the common snake-vs-Camel slip, costs one discovery only on the error path; difflib is fuzzier and noisier.
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-29T15:20:28Z created
- 2026-10-29T15:20:33Z set tier=S
- 2026-10-29T15:48:04Z batched into T-2005
- 2026-10-29T15:56:04Z done in T-2005 (batch)
## Follow-ups captured
