---
id: T-1117
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_close_gates.py]
depends_on: []
source: discovered
created: 2026-10-16T05:49:29Z
updated: 2026-10-16T06:04:45Z
base: c299f04be53a61aa708863bd0a6bea0a9c7b2698
base_tree: add2be3a71267b1c4d2d8daab2e1c5d4ff518e32
verified: strong
---
# Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the
## Raw request
> Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the changed files) and refuses on a new failure; a full-suite run that is red becomes an urgent baseline FIX automatically (once per failing set), hoisted by fm next — T-1089 broke test_builder and every later close missed it because finish ran only each task's own criteria
## Interpretation
Foreman has to keep the main suite green on its own. Today a close runs only that task's criteria, so a change that breaks another module's test (T-1089 → test_builder) lands, and later closes treat the red suite as pre-existing forever. Done means: the close runs the tests linked to what it changed and refuses a new failure; any red full run becomes one urgent task by itself; and full runs happen in the background without anyone remembering.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish refuses when the affected tests fail and the failure is new; passes with a note when it was already red in the last full run — verify with `python3 plugin/tests/run.py test_close_gates`
- [x] A red full-gate run captures one urgent baseline FIX naming the failing tests, once per failing set; a later green run says the baseline is green again — verify with `python3 plugin/tests/run.py test_close_gates`
- [x] After a close, a detached full fm check starts when the last full run is older than 3 closes or 60 minutes — verify with `python3 plugin/tests/run.py test_close_gates`
## Non-goals
## Approach (options → choice → why)
Options: (a) finish runs the full gates (≈190 s per close: too slow for every close); (b) finish runs fm check --affected (tests linked to the changed files) and refuses on a failure the last full run didn't already have; plus a red full-suite run captures one urgent baseline FIX per failing set; plus a detached full fm check after a close when the last full run is older than 3 closes or 60 min, so the baseline is checked without anyone remembering. Choice: (b): it catches T-1089-style breaks at the close that caused them, keeps closes fast, and makes a red baseline someone's task automatically.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for the three criteria
2. [x] Affected tests at finish with the pre-existing comparison
3. [x] Baseline FIX capture in cmd_check
4. [x] Detached sentinel after a close
5. [x] Docs (README, MASTER, rules if needed), CHANGELOG
## Resume here
T-1117 waiting on review; working T-1082
<!-- auto -->
- 2026-10-16T05:58:39Z step 5/5: Docs (README, MASTER, rules if needed), CHANGELOG
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/tests/test_close_gates.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/tests/test_close_gates.py, MASTER.md
- failures met: bash: line 0: bc: command not found
## Docs impact
README.md fm check paragraph; MASTER.md Close gates; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_close_gates` → ✗ exit 1 · Ran 2 tests in 2.9s (1 classes, 16 at a time; slowest: CloseGates 3s) / FAILED (1 classes) [ran] [tree 8b2953de173a] (2026-10-16T05:50:43Z)
- (step 2) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 4 tests in 16.4s (1 classes, 16 at a time; slowest: CloseGates 16s) / OK [ran] [tree 350162239528] (2026-10-16T05:54:08Z)
- (step 3) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 4 tests in 16.4s (1 classes, 16 at a time; slowest: CloseGates 16s) / OK [ran] [tree 350162239528] (2026-10-16T05:54:25Z)
- (step 4) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 4 tests in 17.6s (1 classes, 16 at a time; slowest: CloseGates 17s) / OK [ran] [tree 350162239528] (2026-10-16T05:54:43Z)
- (step 3) `python3 plugin/tests/run.py test_close_gates test_nudges` → exit 0 · Ran 17 tests in 10.4s (4 classes, 16 at a time; slowest: CloseGates 10s, Revisit 4s, QuietHints 4s) / OK [ran] [tree 0e9a6a9f2e5a] (2026-10-16T05:58:17Z)
- (step 2) `python3 plugin/tests/run.py test_close_gates` → ✗ exit 1 · Ran 2 tests in 8.9s (1 classes, 16 at a time; slowest: CloseGates 9s) / FAILED (1 classes) [ran] [tree 5aa08c708f01] (2026-10-16T05:59:32Z)
- (step 2) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 11 tests in 9.0s (1 classes, 16 at a time; slowest: CloseGates 9s) / OK [ran] [tree efabe7d6a8c2] (2026-10-16T06:00:41Z)
- (step 3) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 12 tests in 10.0s (1 classes, 16 at a time; slowest: CloseGates 10s) / OK [ran] [tree b26035418394] (2026-10-16T06:03:27Z)
- (ac 1) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 12 tests in 10.1s (1 classes, 16 at a time; slowest: CloseGates 10s) / OK [ran] [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (ac 2) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 12 tests in 10.1s (1 classes, 16 at a time; slowest: CloseGates 10s) / OK [ran] [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (ac 3) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 12 tests in 10.1s (1 classes, 16 at a time; slowest: CloseGates 10s) / OK [ran] [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (step 5) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 12 tests in 10.1s (1 classes, 16 at a time; slowest: CloseGates 10s) / OK [ran] [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (audit intent) `review: one fm-reviewer full pass; 11 findings: 9 fixed test-first (sentinel tree pin, one-at-a-time pid, own red run excluded, flake rerun, env failures noted, timeout message, --json clean, affected keyed on the closing task, redundant scope), 2 answered (lock split acceptable, dead filter removed); full suite run twice: only the known load flake, now skipped by the baseline capture` → a close can no longer land a change that breaks the tests linked to it; a red full run is someone's urgent task automatically; full runs happen without anyone remembering [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (audit adversary) `review: one fm-reviewer full pass; 11 findings: 9 fixed test-first (sentinel tree pin, one-at-a-time pid, own red run excluded, flake rerun, env failures noted, timeout message, --json clean, affected keyed on the closing task, redundant scope), 2 answered (lock split acceptable, dead filter removed); full suite run twice: only the known load flake, now skipped by the baseline capture` → the baseline task text is fm's own (cmd + parsed test names); a waiver is logged with its reason; no path lets a task's own red run excuse its close [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (audit edge) `review: one fm-reviewer full pass; 11 findings: 9 fixed test-first (sentinel tree pin, one-at-a-time pid, own red run excluded, flake rerun, env failures noted, timeout message, --json clean, affected keyed on the closing task, redundant scope), 2 answered (lock split acceptable, dead filter removed); full suite run twice: only the known load flake, now skipped by the baseline capture` → mid-task red-first runs, gates without test names, known flakes, environment failures, a tree edited during a sentinel run and a second sentinel all capture nothing [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (audit operator) `review: one fm-reviewer full pass; 11 findings: 9 fixed test-first (sentinel tree pin, one-at-a-time pid, own red run excluded, flake rerun, env failures noted, timeout message, --json clean, affected keyed on the closing task, redundant scope), 2 answered (lock split acceptable, dead filter removed); full suite run twice: only the known load flake, now skipped by the baseline capture` → the close runs only linked tests (one rerun); --skip-affected exists for runners fm can't read; the sentinel line prints before Landed and never under --json [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
- (audit maintainer) `review: one fm-reviewer full pass; 11 findings: 9 fixed test-first (sentinel tree pin, one-at-a-time pid, own red run excluded, flake rerun, env failures noted, timeout message, --json clean, affected keyed on the closing task, redundant scope), 2 answered (lock split acceptable, dead filter removed); full suite run twice: only the known load flake, now skipped by the baseline capture` → _close_affected, _baseline, _sentinel, _known_flaky in fmcli; check_run now stores failing names per gate; FOREMAN_SENTINEL=off|sync for tests [tree 8317eb4dcd50] (2026-10-16T06:03:56Z)
## Log
- 2026-10-16T05:49:29Z created
- 2026-10-16T05:49:55Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmeco.py', 'plugin/tests/test_check_paths.py', 'plugin/tests/test_task_finish.py']
- 2026-10-16T05:50:02Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmeco.py', 'plugin/tests/test_close_gates.py']
- 2026-10-16T05:50:02Z criterion 1 verify: `python3 plugin/tests/run.py test_task_finish` → `python3 plugin/tests/run.py test_close_gates`
- 2026-10-16T05:50:02Z criterion 2 verify: `python3 plugin/tests/run.py test_check_paths` → `python3 plugin/tests/run.py test_close_gates`
- 2026-10-16T05:50:03Z criterion 3 verify: `python3 plugin/tests/run.py test_task_finish` → `python3 plugin/tests/run.py test_close_gates`
- 2026-10-16T05:50:21Z set approved=True
- 2026-10-16T05:50:21Z focused
- 2026-10-16T05:50:55Z paused: focus moved to T-1118
- 2026-10-16T05:51:46Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T05:51:46Z focused
- 2026-10-16T05:55:00Z scope: README.md, MASTER.md, CHANGELOG.md — docs for the close gates (step 5)
- 2026-10-16T05:56:29Z paused: focus moved to T-1082
- 2026-10-16T05:57:55Z focused
- 2026-10-16T05:58:22Z scope: MASTER.md — the narrowed capture rule (after the last edit)
- 2026-10-16T05:58:40Z paused: focus moved to T-1082
- 2026-10-16T05:59:10Z focused
- 2026-10-16T05:59:11Z review: sentinel can capture a baseline from the next task's red-first file; no in-flight guard; _close_affected refuses on env failures, unparseable runners, flakes, its own earlier red run; fixed timeout; prints under --json; affected() keyed on the active brief. Fixing test-first.
- 2026-10-16T06:00:41Z scope: CHANGELOG.md — updated for the review fixes (after the last edit)
- 2026-10-16T06:03:39Z scope: MASTER.md — flake skip and waiver (after the last edit)
- 2026-10-16T06:04:44Z done
- 2026-10-16T06:04:45Z committed f76fffc (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
this change is the catch: the close now runs the linked tests T-1089 skipped
## Lessons
- A gate the agent is told to run is a gate that gets skipped: run it from the close itself, and turn a red result into a task, not a note
## Plan gaps
- failed first: step 1 Failing tests for the three criteria
## Files touched
- plugin/tests/test_close_gates.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- README.md
