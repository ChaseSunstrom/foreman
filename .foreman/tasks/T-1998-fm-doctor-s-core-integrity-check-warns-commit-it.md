---
id: T-1998
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py]
depends_on: []
source: user
created: 2026-10-29T14:47:35Z
updated: 2026-10-29T15:19:28Z
done_in: T-2001
---
# fm doctor's core-integrity check warns "commit it through a task, or git checkout it…
## Raw request
> FIX: fm doctor's core-integrity check warns "commit it through a task, or git checkout it back" about protected core the focused task is changing inside its own scope (every fm check of a core task shows it); files in the active task's scope pass with a note naming that task, files outside it still warn
> @plugin/lib/fmdoctor.py @plugin/tests/test_doctor.py
> DONE-WHEN: core changed only inside the active task's scope passes and names the task; a file outside it still warns :: python3 plugin/tests/run.py test_doctor -k core_integrity
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
- 2026-10-29T14:47:38Z set tier=S
- 2026-10-29T14:47:48Z batched into T-2001
- 2026-10-29T15:19:28Z done in T-2001 (batch)
## Follow-ups captured
