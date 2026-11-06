---
id: T-1968
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T10:39:34Z
updated: 2026-10-29T10:52:29Z
base: 9cd7e4477dbcb0e67527f6e7e885441c1527c8f3
base_tree: 53f59661335e09e252640c81f6c77f70d8712c28
plan0_at: 2026-10-29T10:41:37Z
plan0_scope: []
verified: strong
---
# Fm task finish's affected-test pass (fmcli affected with the closing brief) counts other t
## Raw request
> FIX: fm task finish's affected-test pass (fmcli affected with the closing brief) counts other tasks' changed files, as _landed already leaves them out with _theirs: T-1958, which landed nothing, ran 108 s of tests on T-1963's uncommitted files while T-1963's full gates ran. DONE-WHEN: a close of a task that changed no files of its own runs no affected tests
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a close of a task with no files of its own runs no affected tests — verify with `python3 plugin/tests/run.py test_close_gates -k another_tasks_files`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a task closing while another task's linked file is dirty runs no affected tests
2. [x] affected() drops _theirs files for the closing brief
## Resume here
<!-- auto -->
- 2026-10-29T10:45:58Z step 1/2: red test: a task closing while another task's linked file is dirty runs no affected tests
- git: foreman/build; 2 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_close_gates.py
- touched since last checkpoint: plugin/tests/test_close_gates.py, plugin/lib/fmcli.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_close_gates -k own` → ✗ exit 1 · Ran 196 tests in 19.8s (141 classes, 16 at a time; slowest: CloseGates 20s, KnownFixes 12s, Mutation 8s) / FAILED (1 classes) [ran] [tree dd84556f88cb] (2026-10-29T10:42:16Z)
- (step 1) `python3 plugin/tests/run.py test_close_gates -k another_tasks_files` → ✗ exit 1 · Ran 1 tests in 17.6s (1 classes, 16 at a time; slowest: CloseGates 17s) / FAILED (1 classes) [ran] [tree 374920e56248] (2026-10-29T10:43:01Z)
- (step 2) `python3 plugin/tests/run.py test_close_gates test_board_verbs test_diff_gates test_board_hooks test_cli test_core test_pass5 test_pass4 test_hooks test_second test_task_ergonomics test_bookkeeping test_handoff test_relate` → exit 0 · Ran 551 tests in 53.8s (126 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 40s, PreToolUse 36s) / OK [ran] [tree 7553058a731d] (2026-10-29T10:45:58Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.3    45.6     150  [0] / SessionEnd                  35.8    38.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree d56126ff7c25] (2026-10-29T10:51:35Z)
- (ac 1) `python3 plugin/tests/run.py test_close_gates -k another_tasks_files` → exit 0 · Ran 16 tests in 15.7s (1 classes, 16 at a time; slowest: CloseGates 15s) / OK [ran] [tree d56126ff7c25] (2026-10-29T10:52:01Z)
- (step 1) `python3 plugin/tests/run.py test_close_gates -k another_tasks_files` → exit 0 · Ran 16 tests in 15.7s (1 classes, 16 at a time; slowest: CloseGates 15s) / OK [ran] [tree d56126ff7c25] (2026-10-29T10:52:01Z)
- (audit edge) `self-review of both _theirs filters (affected with the closing brief, _task_files' shell-changed files); 551 related tests + full gates 4183 OK` → a file both tasks touched stays the closer's (mine wins), so its tests still run; a never-focused task falls back to its created time in _others [tree d56126ff7c25] (2026-10-29T10:52:01Z)
- (audit adversary) `self-review of both _theirs filters (affected with the closing brief, _task_files' shell-changed files); 551 related tests + full gates 4183 OK` → a file only another task touched leaves this close but that task's own close and commit still answer for it, so nothing goes unchecked [tree d56126ff7c25] (2026-10-29T10:52:01Z)
- (audit self) `self-review of both _theirs filters (affected with the closing brief, _task_files' shell-changed files); 551 related tests + full gates 4183 OK` → no findings [tree d56126ff7c25] (2026-10-29T10:52:01Z)
## Log
- 2026-10-29T10:39:34Z created
- 2026-10-29T10:39:43Z set tier=S
- 2026-10-29T10:41:36Z planned: it has criteria and steps
- 2026-10-29T10:41:37Z focused
- 2026-10-29T10:42:43Z criterion 1 verify: `python3 plugin/tests/run.py test_close_gates -k own` → `python3 plugin/tests/run.py test_close_gates -k another_tasks_files`
- 2026-10-29T10:44:24Z steer: _task_files (scope and sensitive-file checks at close) had the same gap: a scoped task closing while another task's file was dirty was refused as out of scope; both now drop _theirs
- 2026-10-29T10:52:27Z done
- 2026-10-29T10:52:29Z committed 7983e6c8 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-1467 [PERFORMANCE S, done, 3 steps] A file that co-changes with every test no longer runs them all
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- decision 2026-10-23: fm code's spend counts toward fm budget's day cap like any other Foreman spend
- similar finished tasks took 3–5 steps
- start here (files T-1117 touched): plugin/tests/test_close_gates.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, README.md
## Plan gaps
- failed first: step 1 red test: a task closing while another task's linked file is dirty runs no affected tests
## Files touched
- plugin/tests/test_close_gates.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
