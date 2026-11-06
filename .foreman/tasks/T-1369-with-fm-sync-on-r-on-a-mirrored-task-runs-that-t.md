---
id: T-1369
type: SECURITY
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T07:33:21Z
updated: 2026-10-23T07:49:07Z
base: db53acc9d02ed2a0e48917f65cf0ffd57df3a920
base_tree: e9c1fd292108a16da53505204675b359e84728c8
plan0_at: 2026-10-23T07:45:58Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code.py, CHANGELOG.md]
verified: strong
---
# fm code --task runs a task still waiting for the user's yes (a brief pulled by fm sync, imported, or written by a replay): its verify command runs on one key in the app; refuse it before any command runs
## Raw request
> with `fm sync on`, `r` on a mirrored task runs that task's verify command after a single keypress. The guard allows it, so consider a confirmation
> (noticed by an agent; research T-1330-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code --task on a task waiting for the user's own yes refuses before any command runs, saying why and naming fm ask ID confirm; the same task once granted runs — verify with `python3 plugin/tests/run.py test_code.TaskRun`
## Non-goals
## Approach (options → choice → why)
One check in _load_task, the door every --task run (CLI or the app's r) goes through: fmcore.needs_approval(b) with a confirm flag → CodeError naming confirm_why and 'fm ask ID confirm' (its Next), before the baseline runs anything. Options: a second key press in the app (the CLI path stays open); hiding mirrored tasks from the app (they still run from the CLI); the check at the door (chosen).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a confirm-waiting brief with a verify that writes a marker; fm code --task must refuse and the marker never appear; then the check in _load_task
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: TaskRun 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7ffc79b39fe0] (2026-10-23T07:46:01Z)
- `python3 plugin/tests/run.py test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: TaskRun 0s) / FAILED (1 classes) [ran] [tree 7ffc79b39fe0] (2026-10-23T07:46:01Z)
- `python3 plugin/tests/run.py test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: TaskRun 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f1395e9f3c0f] (2026-10-23T07:46:11Z)
- `python3 plugin/tests/run.py test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given` → exit 0 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: TaskRun 2s) / OK [ran] [tree f1395e9f3c0f] (2026-10-23T07:46:11Z)
- `python3 plugin/tests/run.py test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given` → ✗ exit 1 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: TaskRun 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8aa4ab9cd28a] (2026-10-23T07:46:32Z)
- `python3 plugin/tests/run.py test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given` → exit 0 · Ran 1 tests in 3.1s (1 classes, 16 at a time; slowest: TaskRun 3s) / OK [ran] [tree 8aa4ab9cd28a] (2026-10-23T07:46:32Z)
- (step 1) `python3 plugin/tests/run.py test_code.TaskRun test_code_tui.Home` → exit 0 · Ran 14 tests in 10.4s (2 classes, 16 at a time; slowest: TaskRun 10s, Home 0s) / OK [ran] [tree 8aa4ab9cd28a] (2026-10-23T07:46:52Z)
- (audit adversary) `self: the door every --task run uses` → pass: a confirm-waiting brief's verify never runs (marker test); fm code --task from the CLI and the app's r both pass _load_task; only the user's own yes (allow confirm) opens it; approved= or full autonomy don't [tree da72c2c94a20] (2026-10-23T07:46:53Z)
- (ac 1) `python3 plugin/tests/run.py test_code.TaskRun` → exit 0 · Ran 6 tests in 10.4s (1 classes, 16 at a time; slowest: TaskRun 10s) / OK [ran] [tree da72c2c94a20] (2026-10-23T07:47:04Z)
- (audit adversary) `self: adversary, intent` → the check sits in _load_task before the baseline, so neither the CLI nor the app runs a confirm-waiting task's commands; only allow confirm (the user's yes) opens it [tree da72c2c94a20] (2026-10-23T07:47:04Z)
- (audit intent) `self: adversary, intent` → the one-key run of a mirrored task's verify is gone without a second-key prompt the CLI would bypass [tree da72c2c94a20] (2026-10-23T07:47:04Z)
- (audit self) `self: adversary, intent` → no findings [tree da72c2c94a20] (2026-10-23T07:47:04Z)
## Log
- 2026-10-21T07:33:21Z created
- 2026-10-23T07:44:45Z planned from capture
- 2026-10-23T07:44:46Z set priority=urgent, scope=['plugin/lib/fmcode.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-10-23T07:45:58Z focused
- 2026-10-23T07:49:05Z done
- 2026-10-23T07:49:07Z committed a4e5e4fb (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1573-review: Verdict:** approve with nits. I found no way for a kept value to differ from the previewed one, or for the app to stay in the previewed look afte…
- research T-1330-review: Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands. [stale: plugin/lib/fm…
- T-1339 [FEATURE M, done, 4 steps] fm code run friction: a blocked, stalled or killed run, or one that fails before its task exists, counts as friction with fm code in Fo…
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Why not caught
T-1750 made pulled briefs wait for a yes, but only fm next and the drive read that flag; fm code --task never asked
## Lessons
- A flag that holds work back must be checked at every door that runs it, not only where work is picked
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- CHANGELOG.md
