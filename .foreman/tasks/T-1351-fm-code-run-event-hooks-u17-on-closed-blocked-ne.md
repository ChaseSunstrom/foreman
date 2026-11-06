---
id: T-1351
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_core.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:41Z
updated: 2026-10-23T06:51:44Z
base: 79eda51f753756c4f73461510724c0d1a5eae6b2
base_tree: 567bdce666901afeb0193aa3be38b19f56384856
plan0_at: 2026-10-23T06:48:05Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcore.py, plugin/tests/test_code.py, plugin/tests/test_core.py, README.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code run-event hooks: code.toml [on] closed, blocked and needs-you commands get the event JSON on stdin past the guard; fm state --line names the newest fm code run
## Raw request
> fm code run-event hooks (U17): on = closed|blocked|needs-you commands in the config get the event JSON on stdin (through the guard); fm state --line includes the newest fm code run for tmux and prompt segments
## Interpretation
A user wants fm code to tell their own tools when a run ends (a notification, a tmux refresh, a chat message) and to see the latest run in a status bar, without polling the events file.
## Assumptions (confidence)
## Acceptance criteria
- [x] a code.toml [on] command for closed, blocked or needs-you (blocked or error) runs once with the event's JSON on stdin; one the guard refuses never runs and the run says so — verify with `python3 plugin/tests/run.py test_code.RunHooks`
- [x] fm state --line ends with the newest fm code run's task and state — verify with `python3 plugin/tests/run.py test_code.RunHooks`
## Non-goals
## Approach (options → choice → why)
Complete version: [on] in code.toml (closed, blocked, needs-you), each a shell command run with the event JSON on stdin, past fmguard as a Bash command, bounded by a timeout, its failure a note; the state line's last part names the newest run. Options: (1) code.toml [on] commands run by fm code itself (chosen: code.toml is already where fm code's commands come from, and the guard sees each one); (2) fm notify's existing hook (one command for every Foreman event, no event JSON); (3) a watcher process tailing events files (one more process to keep alive). needs-you means the run stopped and waits on the user: blocked or error. The hook runs with fm code's worker environment (no model API keys), in the project root, with a 30 s timeout.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: hook gets the event, a refused hook never runs, a failing hook never fails the run, the state line
2. [x] fmcode: [on] read from code.toml, run_hook after closed/blocked/error through fmguard
3. [x] fmcore.state_line: the newest code/*.events.jsonl's task and last event
4. [x] docs: README, CHANGELOG, MASTER
## Resume here
## Docs impact
README fm code section ([on], state line), CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.RunHooks` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: RunHooks 3s) / OK [ran] [tree bda36a4ce51c] (2026-10-23T06:49:50Z)
- (step 2) `python3 plugin/tests/run.py test_code.RunHooks` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: RunHooks 3s) / OK [ran] [tree bda36a4ce51c] (2026-10-23T06:49:54Z)
- (step 3) `python3 plugin/tests/run.py test_code.RunHooks` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: RunHooks 3s) / OK [ran] [tree bda36a4ce51c] (2026-10-23T06:49:57Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 8.5s (16 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree bda36a4ce51c] (2026-10-23T06:50:06Z)
- (audit intent) `self: request re-read` → pass: [on] closed/blocked/needs-you commands get the event JSON on stdin through the guard; fm state --line names the newest run [tree bda36a4ce51c] (2026-10-23T06:50:16Z)
- (ac 1) `python3 plugin/tests/run.py test_code.RunHooks` → exit 0 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: RunHooks 3s) / OK [ran] [tree bda36a4ce51c] (2026-10-23T06:50:20Z)
- (ac 2) `python3 plugin/tests/run.py test_code.RunHooks` → exit 0 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: RunHooks 3s) / OK [ran] [tree bda36a4ce51c] (2026-10-23T06:50:20Z)
- (audit intent) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → all criteria met [tree bda36a4ce51c] (2026-10-23T06:50:20Z)
- (audit adversary) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → hook commands come only from FOREMAN_HOME/code.toml, never a repo; each goes past the guard, which fails closed; run_in_background turns off only fmhooks' two foreground rules (fmguard never reads it, grepped); the event JSON goes on stdin, never into the command; the API keys are dropped from its environment; its group is killed at 30 s and registered for the survivor sweep [tree bda36a4ce51c] (2026-10-23T06:50:20Z)
- (audit edge) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → no code folder or no runs gives no state-line part; a live run (lock held) reads running, a killed one stopped; a hook's own notes never trigger hooks [tree bda36a4ce51c] (2026-10-23T06:50:20Z)
## Log
- 2026-10-21T03:47:41Z created
- 2026-10-23T06:40:26Z planned from capture
- 2026-10-23T06:40:34Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_code.py', 'plugin/tests/test_core.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T06:48:04Z focused
- 2026-10-23T06:49:23Z scope: plugin/lib/fmcli.py — fm state --line appends fmcore.code_line
- 2026-10-23T06:49:23Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_core.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T06:51:43Z done
- 2026-10-23T06:51:44Z committed 7c130e63 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- research T-1574-review: Verdict: changes needed.** One MEDIUM bypass of the guard (in code from T-1496, which the new command calls through) and one MEDIUM test gap. I c…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- likely tests for the scope: plugin/tests/test_code.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcode.py, plugin/lib/fmcore.py, plugin/tests/test_code.py, plugin/tests/test_core.py; re-ground the plan against them before editing
## Lessons
- A hook fed on stdin trips the guard's stdin-hang rule: check it as a background call, which turns off only the session's foreground rules
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
- README.md
