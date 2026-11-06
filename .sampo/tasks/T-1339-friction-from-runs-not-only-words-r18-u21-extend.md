---
id: T-1339
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_code_worker.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:25Z
updated: 2026-10-23T07:32:05Z
base: 5ff4cad9214aaf2a37b0549ee01149fd30228215
base_tree: 79e706d5ea04c1a692fc49439100c6468e157c0a
plan0_at: 2026-10-23T07:25:32Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_code_worker.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code run friction: a blocked, stalled or killed run, or one that fails before its task exists, counts as friction with fm code in Foreman's own project, one log line per new cause, and the app's home shows it under Foreman noticed
## Raw request
> Friction from runs, not only words (R18+U21, extends T-1332): a blocked, stalled or killed fm code run, or a failed preflight, counts as friction for the 'fm code' area (deduped per cause) and the app's home shows it under 'Foreman noticed'
## Interpretation
Foreman already turns the user's complaints about an area into an improvement round (T-1332); a run that goes wrong is the same signal without words, so it should feed the same round, without piling up duplicates, and the app should show it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a blocked run, a stall, a run left unfinished by a kill and a failure before the task exists each log their cause onto Foreman's own 'Improve fm code' friction task (made once), the same cause only once — verify with `python3 plugin/tests/run.py test_code.RunFriction`
- [x] the app's home shows a Foreman noticed row naming that task and its causes, and Enter opens Foreman's project — verify with `python3 plugin/tests/run.py test_code_tui.Noticed`
## Non-goals
## Approach (options → choice → why)
Complete version: run_friction(cause, detail) files into Foreman's own project (foreman_home, as fm bench's findings do) through fmcli.capture_friction with 'fm code run …' text (area fm code, one task, urgent on a second complaint within 7 days), but only when the cause key (cause plus the reason's first words, digits dropped) isn't in that task's log yet; it then logs 'run friction: KEY'. Called at Blocked, the first stall a turn, each unfinished run a new start finds, and a CodeError or ModelError before the task exists. noticed() lists open friction tasks there with their causes; the app's home puts a Foreman noticed row first, Enter opens that project. Options: (1) Foreman's own project (chosen: the user's repo shouldn't get tasks about improving fm code); (2) the run's project (mixes Foreman's work into theirs); (3) a separate friction file read by fm friction (a second store beside the task the round already uses). Never fails a run: every error in it is swallowed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: causes logged and deduped, the home row
2. [x] fmcode: run_friction, called at blocked, stalled, an unfinished run found, and an early failure; noticed()
3. [x] app: the Foreman noticed row
4. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.RunFriction test_code_tui.Noticed` → exit 0 · Ran 3 tests in 6.3s (2 classes, 16 at a time; slowest: RunFriction 6s, Noticed 0s) / OK [ran] [tree bc27894b1bef] (2026-10-23T07:29:34Z)
- (step 2) `python3 plugin/tests/run.py test_code.RunFriction test_code_worker.Worker.test_a_turn_that_prints_nothing_is_named_no_output_since_launch` → exit 0 · Ran 3 tests in 6.9s (2 classes, 16 at a time; slowest: RunFriction 7s, Worker 4s) / OK [ran] [tree bc27894b1bef] (2026-10-23T07:29:41Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui.Noticed test_code_tui.Home test_code_tui.Reopen` → exit 0 · Ran 11 tests in 0.5s (3 classes, 16 at a time; slowest: Noticed 0s, Home 0s, Reopen 0s) / OK [ran] [tree bc27894b1bef] (2026-10-23T07:29:43Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 10.2s (16 classes, 16 at a time; slowest: Fences 10s, TaskLifecycle 3s, Site 2s) / OK [ran] [tree 4a6f3225066a] (2026-10-23T07:29:55Z)
- (step 2) `python3 plugin/tests/run.py test_code.RunFriction test_code_worker.Worker.test_a_turn_that_prints_nothing_is_named_no_output_since_launch` → exit 0 · Ran 3 tests in 4.3s (2 classes, 16 at a time; slowest: RunFriction 4s, Worker 3s) / OK [ran] [tree 6c9036235d05] (2026-10-23T07:30:28Z)
- (audit intent) `self: request re-read` → pass: blocked, stalled, killed and preflight failures logged once per cause on Foreman's own fm code round; the app's home shows it first [tree 6c9036235d05] (2026-10-23T07:30:29Z)
- (ac 1) `python3 plugin/tests/run.py test_code.RunFriction` → exit 0 · Ran 2 tests in 4.0s (1 classes, 16 at a time; slowest: RunFriction 4s) / OK [ran] [tree 6c9036235d05] (2026-10-23T07:30:34Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.Noticed` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Noticed 0s) / OK [ran] [tree 6c9036235d05] (2026-10-23T07:30:34Z)
- (audit intent) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → both criteria met [tree 6c9036235d05] (2026-10-23T07:30:34Z)
- (audit adversary) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → the round lands in Foreman's own project, never the user's; its text is the fixed cause name, and the log's dedupe key is eight plain, redacted words of the reason, so a failing test's output can't write the task [tree 6c9036235d05] (2026-10-23T07:30:34Z)
- (audit edge) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → a busy lock or full disk never touches the run (everything in run_friction is swallowed); a closed round starts a new one; the noticed row is skipped when matching the current or last project; an App given its own projects lists no noticed rows unless given them [tree 6c9036235d05] (2026-10-23T07:30:34Z)
## Log
- 2026-10-21T03:47:25Z created
- 2026-10-23T07:24:00Z planned from capture
- 2026-10-23T07:24:09Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:25:29Z scope: plugin/tests/test_code_worker.py — the stall test also checks the stall's friction
- 2026-10-23T07:25:30Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_code_worker.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:25:31Z focused
- 2026-10-23T07:32:03Z done
- 2026-10-23T07:32:05Z committed 7267bf0c (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- T-1332 [FEATURE M, done, 2 steps] Foreman notices on its own when a feature area needs a brainstorm and an improvement round — lesson: Friction is a signal to act on, no…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_code_worker.py; re-ground the plan against them before editing
## Lessons
- A signal filed from a run's failure carries repo text: file the fixed cause and keep the excerpt short, plain and redacted
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- MASTER.md
