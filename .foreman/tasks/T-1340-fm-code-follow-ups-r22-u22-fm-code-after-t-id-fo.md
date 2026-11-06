---
id: T-1340
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:27Z
updated: 2026-10-23T10:10:12Z
base: 69e3b1dbf7f51c27254d0645d1d42b03ed9fe7e3
base_tree: b399090b0cd06eed58690e0e4f8e23fcd3088647
plan0_at: 2026-10-23T10:04:13Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close
## Raw request
> fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close or an answer in the app) plans a new task carrying the closed task's request, plan, answer and changed files; a question typed during a run is answered read-only beside it
## Interpretation
fm code --after T-ID "<follow-up>": the earlier run's events file gives its request, plan, how it ended and the files it changed; they reach the planner as data (fenced: the plan was a model's), and the new task's raw request names the earlier task. In the app, Enter after a close (no log line selected) opens the request prompt as that follow-up; n stays a fresh request. The third part, a question typed during a run answered read-only beside it, is captured as its own item.
## Assumptions (confidence)
## Acceptance criteria
- [x] a follow-up's planner sees the earlier request, plan, end and files; an unknown id exits 1 naming it; Enter after a close starts the next run with --after — verify with `python3 plugin/tests/run.py test_code.FollowUp test_code_tui.FollowUpKey`
## Non-goals
## Approach (options → choice → why)
Options: --from (it promotes an inbox capture, not a link); depends_on (a blocked earlier task would hold the new one); context as data plus the earlier id in the raw request. Choice: the last, beside piped context in _context_note.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then follow_up, --after and the app's Enter
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.FollowUp test_code_tui.FollowUpKey` → ✗ exit 1 · Ran 3 tests in 2.7s (2 classes, 16 at a time; slowest: FollowUp 2s, FollowUpKey 0s) / FAILED (2 classes) [ran] [tree dffbca721aa9] (2026-10-23T10:04:22Z)
- (step 1) `python3 plugin/tests/run.py test_code.FollowUp test_code_tui.FollowUpKey` → exit 0 · Ran 3 tests in 4.0s (2 classes, 16 at a time; slowest: FollowUp 4s, FollowUpKey 0s) / OK [ran] [tree ed5b3bcb135e] (2026-10-23T10:06:56Z)
- (ac 1) `python3 plugin/tests/run.py test_code.FollowUp test_code_tui.FollowUpKey` → ✗ exit 1 · Ran 3 tests in 3.0s (2 classes, 16 at a time; slowest: FollowUp 3s, FollowUpKey 0s) / FAILED (1 classes) [ran] [tree ed5b3bcb135e] (2026-10-23T10:06:59Z)
- (step 1) `python3 plugin/tests/run.py test_code.FollowUp test_code_tui.FollowUpKey` → exit 0 · Ran 3 tests in 4.1s (2 classes, 16 at a time; slowest: FollowUp 4s, FollowUpKey 0s) / OK [ran] [tree 04ed1fe1a914] (2026-10-23T10:08:43Z)
- (ac 1) `python3 plugin/tests/run.py test_code.FollowUp test_code_tui.FollowUpKey` → exit 0 · Ran 3 tests in 4.0s (2 classes, 16 at a time; slowest: FollowUp 4s, FollowUpKey 0s) / OK [ran] [tree 04ed1fe1a914] (2026-10-23T10:08:48Z)
- (audit intent) `self review; test_code, test_code_tui and test_code_worker green; the follow-up class 8/8 after the stale-.pyc fix` → a follow-up's planner sees the earlier request, plan, end and changed files; the new task's request names the earlier one; an unknown id exits 1; Enter after a close starts the next run with --after and n doesn't (tests) [tree 04ed1fe1a914] (2026-10-23T10:08:48Z)
- (audit edge) `self review; test_code, test_code_tui and test_code_worker green; the follow-up class 8/8 after the stale-.pyc fix` → the earlier plan was a model's, so it travels fenced as data; Run.after is a method, so the id lives in after_tid; a test rewrite of calc.py at the same size in the same second hit a stale .pyc (2 of 6 runs), now written at a new size [tree 04ed1fe1a914] (2026-10-23T10:08:48Z)
## Log
- 2026-10-21T03:47:27Z created
- 2026-10-23T09:49:54Z set tier=M, scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T10:04:12Z focused
- 2026-10-23T10:10:11Z done
- 2026-10-23T10:10:12Z committed 2de6404f (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1320-review: Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards. [stale: plugin/lib/fmcl…
- T-1335 [FEATURE M, done, 4 steps] fm code runner pings: fm code runners --ping [NAME] asks each runner one tiny read-only question and sorts the answer (ok, not logged i…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Before adding an attribute to a class with many methods, grep 'def NAME': an instance attribute silently shadows the method and fails far from the assignment
## Plan gaps
- failed first: step 1 failing tests, then follow_up, --after and the app's Enter
## Files touched
- plugin/tests/test_code.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py
