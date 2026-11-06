---
id: T-0781
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:39:46Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
base: b763f8adf9bbe0238396d354b6f70430a5d55972
base_tree: d60c5f4b593bc54d107a6ac583e3e02c996c05c7
verified: strong
---
# Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes
## Raw request
> FEATURE: SessionStart titles a new session after the active task
> CONTEXT: T-0760, cluster session-greeting. SessionStart hookSpecificOutput.sessionTitle (same as /rename) applies on startup/resume/fork; ignored if the plugin installs after SessionStart. Only set on startup with an active task, so a user's own name on resume is kept.
> DONE-WHEN: the SessionStart hook returns sessionTitle "T-NNNN <short title>" on source startup when a task is active, nothing otherwise; a hook test pins it.
## Interpretation
Foreman sets the terminal tab title (OSC 0, fmhooks.py:175) but not Claude Code's own session name, which the resume picker and /resume list show. hookSpecificOutput.sessionTitle (same as /rename) works on SessionStart (startup/resume/fork) and UserPromptSubmit (2.1.94). Set it to 'T-NNNN <short title>' when a task is active and differs from the one this session was last named after; never on a one-off headless session; never rename back and forth for the same task.
## Assumptions (confidence)
## Acceptance criteria
- [x] SessionStart and the first UserPromptSubmit after a focus change return sessionTitle 'T-NNNN …'; repeated prompts on the same task return none — verify with `cd plugin/tests && python3 -m unittest test_hooks.UserPromptSubmit.test_session_is_named_after_its_task`
## Non-goals
## Approach (options → choice → why)
Options: SessionStart only (stale after a focus change); every prompt (renames over a user's own /rename each turn); on change of the active task only. Chose on change.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing hook test
2. [x] sessionTitle on active-task change
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.UserPromptSubmit.test_session_is_named_after_its_task` → ✗ exit 1 · Ran 1 test in 0.936s / FAILED (failures=1) [ran] [tree 8a07228c8c68] (2026-10-14T16:29:47Z)
- (step 2) `python3 plugin/tests/run.py -k test_hooks -k test_core` → exit 0 · Ran 204 tests in 61.7s (34 classes, 16 at a time; slowest: Stop 62s, PreToolUse 31s, SessionStart 29s) / OK [ran] [tree 4d406f6c0878] (2026-10-14T16:31:05Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.UserPromptSubmit.test_session_is_named_after_its_task` → exit 0 · Ran 1 test in 1.850s / OK [ran] [tree 4d406f6c0878] (2026-10-14T16:31:08Z)
- `cd plugin/tests && python3 -m unittest test_hooks.UserPromptSubmit.test_session_is_named_after_its_task` → ✗ exit 1 · Ran 1 test in 1.151s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 4d406f6c0878] (2026-10-14T16:31:12Z)
- `cd plugin/tests && python3 -m unittest test_hooks.UserPromptSubmit.test_session_is_named_after_its_task` → exit 0 · Ran 1 test in 2.726s / OK [ran] [tree 4d406f6c0878] (2026-10-14T16:31:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.UserPromptSubmit.test_session_is_named_after_its_task` → exit 0 · Ran 1 test in 1.667s / OK [ran] [tree 4d406f6c0878] (2026-10-14T16:39:44Z)
- (audit edge) `self: diff read; _session_title names the session 'T-NNNN <title ≤50>' only when the active task differs from the one this session was last named after (a per-session file SessionStart clears), on SessionStart startup/resume/fork and on UserPromptSubmit; control characters and ; stripped` → no active task gives no name; a user's own /rename lasts until the focus moves; a one-off headless session never reaches this code (T-0775 returns earlier) [tree 4d406f6c0878] (2026-10-14T16:39:44Z)
- (audit self) `self: diff read; _session_title names the session 'T-NNNN <title ≤50>' only when the active task differs from the one this session was last named after (a per-session file SessionStart clears), on SessionStart startup/resume/fork and on UserPromptSubmit; control characters and ; stripped` → no findings [tree 4d406f6c0878] (2026-10-14T16:39:44Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:07:44Z planned from capture
- 2026-10-14T16:29:29Z focused
- 2026-10-14T16:39:45Z done
- 2026-10-14T16:39:46Z committed d78959c (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0785 [FEATURE S, active, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for
- T-0775 [FIX S, done, 2 steps] One-off headless claude -p sessions answer their prompt and stop; they never drive the queue — lesson: a headless session Foreman didn't st…
- T-0436 [SECURITY M, done, 3 steps] fm pause: one flag stops everything Foreman runs unattended — lesson: a kill switch is one flag every launcher checks at its own entry…
- decision 2026-10-09: Added JARVIS (<user>@<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- a rename the user can also do must fire on change, not every turn
## Plan gaps
- failed first: step 1 Failing hook test
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
