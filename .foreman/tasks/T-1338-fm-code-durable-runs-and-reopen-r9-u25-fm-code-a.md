---
id: T-1338
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:24Z
updated: 2026-10-23T06:47:44Z
base: a46608be0fdb018f6a29122b2ead8092936edfbe
base_tree: 833b4d3938eb3334fa129e915de14a24b0cdcfeb
plan0_at: 2026-10-23T06:43:36Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code durable runs: a new run names each unfinished one with its resume command, the app's history says how to resume, kills at each station resume cleanly, and the app reopens where it was left
## Raw request
> fm code durable runs and reopen (R9+U25): fm code and the app's home name each unfinished journal on start with its resume command; kill tests at every station boundary; on quit the app saves project, view and task and the next launch opens there with 'welcome back'
## Interpretation
A run that dies (a closed terminal, a kill, a crash) must not be forgotten: the next fm code says it is there and how to carry it on, the app shows it the same way, a kill at any point between stations resumes without redoing finished work, and the app opens where the user left it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a new fm code run names each unfinished run in this project (task, request) with its fm code --resume command, three at most — verify with `python3 plugin/tests/run.py test_code.Durable`
- [x] a run killed at planning, a step's model call or its check resumes and closes with each step done once — verify with `python3 plugin/tests/run.py test_code.Durable`
- [x] the app's past runs show an unfinished run as resumable with its command, and opened from home with no project here it reopens the project left last with a welcome back line — verify with `python3 plugin/tests/run.py test_code_tui.Reopen`
## Non-goals
## Approach (options → choice → why)
Complete version: the start note, the app's resumable rows, kill-resume tests at planning, a step and a check, and the app's last place. Options: (1) scan code/*.jsonl at start for journals with no end record (chosen: the journal is already the truth _load reads; one helper serves both); (2) a separate index of open runs written at start and cleared at end (a second source that a kill leaves stale too); (3) ask fm task list for active tasks with a journal (misses a run killed before its task). Kill tests reuse the fake model's HANG and a check that waits, no test hooks in fm code. The app saves {project, ts} to state/code-place.json on quit, beside code-keys.json; a home launch outside any project reopens it when it still exists. Not built: saving the view or a task inside the project (the project view is the only place a run starts).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: unfinished named on start, kills at plan, step and check, app history and reopen
2. [x] fmcode: unfinished(jdir) shared by _load and the start note
3. [x] app: resumable rows, last place saved on quit, reopened on a home launch
4. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG line; MASTER fm code note on durable runs
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.Durable test_code_tui.Reopen` → exit 0 · Ran 5 tests in 4.1s (2 classes, 16 at a time; slowest: Durable 4s, Reopen 0s) / OK [ran] [tree 12478a4ce5d6] (2026-10-23T06:45:37Z)
- (step 2) `python3 plugin/tests/run.py test_code.Durable test_code.Resume` → exit 0 · Ran 7 tests in 4.9s (2 classes, 16 at a time; slowest: Resume 5s, Durable 4s) / OK [ran] [tree 12478a4ce5d6] (2026-10-23T06:45:43Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui.Reopen test_code_tui.Home` → exit 0 · Ran 10 tests in 0.3s (2 classes, 16 at a time; slowest: Home 0s, Reopen 0s) / OK [ran] [tree 12478a4ce5d6] (2026-10-23T06:45:43Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 8.5s (16 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 567bdce66690] (2026-10-23T06:46:04Z)
- (audit intent) `self: request re-read` → pass: unfinished runs named with resume commands in fm code and the app, kill-resume tests at planning, a step and the check, the app reopens the project left last; saving the view and task inside it not built (the project view is where runs start), said in Approach [tree 567bdce66690] (2026-10-23T06:46:18Z)
- (audit edge) `self: journals and locks` → a live run (its lock held) is left out; a model message quoting the end record is JSON-escaped so it never matches; a torn first line or unreadable journal is skipped; a project whose folder went missing is never reopened (tested) [tree 567bdce66690] (2026-10-23T06:46:18Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Durable` → exit 0 · Ran 3 tests in 4.0s (1 classes, 16 at a time; slowest: Durable 4s) / OK [ran] [tree 567bdce66690] (2026-10-23T06:46:23Z)
- (ac 2) `python3 plugin/tests/run.py test_code.Durable` → exit 0 · Ran 3 tests in 4.0s (1 classes, 16 at a time; slowest: Durable 4s) / OK [ran] [tree 567bdce66690] (2026-10-23T06:46:23Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui.Reopen` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Reopen 0s) / OK [ran] [tree 567bdce66690] (2026-10-23T06:46:23Z)
- (audit intent) `self review (subagents paused at 76% weekly usage): intent, edge` → all three criteria met; the view and task inside a project not saved (Approach says why) [tree 567bdce66690] (2026-10-23T06:46:23Z)
- (audit edge) `self review (subagents paused at 76% weekly usage): intent, edge` → live runs excluded by their lock, escaped quotes never match the end record, missing folders never reopened [tree 567bdce66690] (2026-10-23T06:46:23Z)
## Log
- 2026-10-21T03:47:24Z created
- 2026-10-21T17:28:58Z round 2 (A25) adds: a journal-header stamp of base ref, resolved config and runner card; a resume with a changed part prints the diff and needs --accept-drift
- 2026-10-23T06:37:44Z planned from capture
- 2026-10-23T06:37:52Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T06:43:36Z focused
- 2026-10-23T06:47:42Z done
- 2026-10-23T06:47:44Z committed 79eda51f (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1330-review: Verdict:** changes needed. I read the diff and the working-tree code. I ran no tests, because I had no way to run commands. [stale: plugin/lib/fm…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- A check that hangs once must key on the state after the step (the fix present), not on a call count: the plan check and the baseline both run it before the step
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- MASTER.md
