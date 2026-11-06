---
id: T-0995
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py,plugin/tests/test_hooks.py,mods/foreman-ui/tools/shot.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-15T23:50:41Z
updated: 2026-10-15T23:51:22Z
base: 0f00ccfd9fae8650929cfeca3ed1cdcbb3cbb511
base_tree: 0215d878ed6c7c2a3a50f67612f9651ad84a3232
verified: strong
---
# The UI harness's interactive session (shot.py) was driven by the Stop hook into the queue: it planned three tasks and took focus from the working session
## Raw request
> The UI harness's interactive session (shot.py) was driven by the Stop hook into the queue: it planned three tasks and took focus from the working session
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] FOREMAN_ONEOFF=1 makes any session one-off (no queue, no drive, no session claim); shot.py starts its claude with it — verify with `python3 plugin/tests/run.py -k OneOff -k test_a_oneoff`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] env switch + shot.py
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_oneoff_headless_session_never_drives` → ✗ exit 1 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: Stop 3s) / FAILED (1 classes) [ran] [tree b0efb2d45ca0] (2026-10-15T23:50:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_oneoff_headless_session_never_drives` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 41119fe21c1a] (2026-10-15T23:51:03Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_oneoff_headless_session_never_drives` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 2c7064ea9049] (2026-10-15T23:51:19Z)
- (ac 1) `python3 plugin/tests/run.py -k OneOff -k test_a_oneoff` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 2c7064ea9049] (2026-10-15T23:51:21Z)
- (audit edge) `self: one env switch in _oneoff (every one-off path already keys off it: SessionStart, UserPromptSubmit, Stop); shot.py sets it on its tmux session; the note no longer says headless` → FOREMAN_ONEOFF unset or not '1' changes nothing; fm run's FOREMAN_DRIVE_TASK sessions are unaffected [tree 2c7064ea9049] (2026-10-15T23:51:21Z)
- (audit adversary) `self: one env switch in _oneoff (every one-off path already keys off it: SessionStart, UserPromptSubmit, Stop); shot.py sets it on its tmux session; the note no longer says headless` → the switch only turns Foreman's drive and queue context off for that session; the guard still applies (the note says so and the test checks the brief line) [tree 2c7064ea9049] (2026-10-15T23:51:21Z)
- (audit self) `self: one env switch in _oneoff (every one-off path already keys off it: SessionStart, UserPromptSubmit, Stop); shot.py sets it on its tmux session; the note no longer says headless` → no findings [tree 2c7064ea9049] (2026-10-15T23:51:21Z)
## Log
- 2026-10-15T23:50:41Z created
- 2026-10-15T23:50:42Z focused
- 2026-10-15T23:51:21Z done
- 2026-10-15T23:51:22Z committed 07bc6b6 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0775 [FIX S, done, 2 steps] One-off headless claude -p sessions answer their prompt and stop; they never drive the queue — lesson: a headless session Foreman didn't st…
- decision 2026-09-26: T-0014 fm run: minimal one-shot worker (fresh claude -p per task, drive scoped to that task via FOREMAN_DRIVE_TASK, per-task timeout, stop on no pro…
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_shot.py
## Why not caught
the harness had only been used with local commands (/fm) or single prompts in projects with drive off; full auto plus a prompt was never tried
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_hooks.py
- mods/foreman-ui/tools/shot.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
