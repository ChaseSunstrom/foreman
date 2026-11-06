---
id: T-2911
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_ambient.py, plugin/tests/test_hooks.py]
depends_on: []
source: discovered
created: 2026-11-04T06:37:23Z
updated: 2026-11-06T03:53:16Z
---
# An automatic criterion run checks off the current step only when the run is about that step, so a drive-test run never proves 'the site rebuilt'
## Raw request
> FIX: an ambient test run recorded while a task is focused must not check off that task's current step unless the command is that step's verify; T-2742 step 7 (the site rebuilt) was checked by a run of the drive tests
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] hooks._auto_evidence (and _runner_evidence) record a passing run as the current step's evidence only when the step's text names the command or shares a subject word with it (a test module's name words, a file it names); otherwise only the criterion gets it and the hook notes 'step N not checked: run its own check'; T-2742's case (step 'the site rebuilt', a run of the drive tests) leaves the step open — verify with `python3 plugin/tests/run.py test_ambient test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: T-2742's case leaves the step open; a step naming test_site_build is checked by that run; the note  <- CURRENT
2. [ ] the subject match in _auto_evidence and _runner_evidence
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T06:37:23Z created
- 2026-11-05T03:36:07Z planned from capture
- 2026-11-05T03:36:08Z set approved=True
- 2026-11-05T03:36:08Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_ambient.py', 'plugin/tests/test_hooks.py']
- 2026-11-05T03:36:08Z blocked: approved; waits for a builder slot (after T-3129, which also edits hooks.py)
- 2026-11-06T03:53:16Z unblocked
## Follow-ups captured
