---
id: T-1124
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-10-16T06:49:04Z
updated: 2026-10-16T06:56:54Z
base: b8eaa12cf8b26d6a5e1d4bfc8221a40da569382e
base_tree: 5db6aef5704954d77e42f554ec8962b000d92145
verified: strong
---
# Fm task set ID --section A --text x --section B --text y applies only the last pair silent
## Raw request
> fm task set ID --section A --text x --section B --text y applies only the last pair silently (T-1082's Interpretation and T-1094's were lost this way); apply every pair in order, or refuse more than one
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task set ID --section A --text x --section B --text y sets both sections; a section without its own text is refused — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then pair every --section with its --text
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 100 tests in 19.9s (28 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 7s, AuditPrep 6s) / FAILED (1 classes) [ran] [tree 17b47b0f2e61] (2026-10-16T06:54:09Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_planning test_bookkeeping` → ✗ exit 1 · Ran 121 tests in 21.2s (44 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 9s, AuditPrep 7s) / FAILED (1 classes) [ran] [tree 2b3873556576] (2026-10-16T06:54:41Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_planning test_bookkeeping` → exit 0 · Ran 121 tests in 21.7s (44 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 9s, AuditPrep 8s) / OK [ran] [tree 023c62f3c223] (2026-10-16T06:55:40Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 100 tests in 20.4s (28 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 8s, AuditPrep 6s) / OK [ran] [tree 0291311ce466] (2026-10-16T06:56:14Z)
- (audit self) `self: reproduced in a scratch project (both sections land), test covers two pairs and the mismatched-count refusal; the Build vs reuse approval check reads every pair` → no findings [tree 0291311ce466] (2026-10-16T06:56:14Z)
## Log
- 2026-10-16T06:49:04Z created
- 2026-10-16T06:53:40Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py']
- 2026-10-16T06:53:41Z focused
- 2026-10-16T06:55:53Z scope: CHANGELOG.md — release note
- 2026-10-16T06:56:54Z done
- 2026-10-16T06:56:54Z committed 48918c8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-04: Friction pass deferred to the next day
- similar finished tasks took 2–6 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- A repeated flag without action=append keeps only its last value: silent data loss in a CLI meant to be called in one shot
## Plan gaps
- failed first: step 1 Failing test, then pair every --section with its --text
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
