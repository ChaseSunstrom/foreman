---
id: T-2532
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/hooks/hook, plugin/tests/test_hooks.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-11-02T04:14:14Z
updated: 2026-11-02T04:34:46Z
base: 528be07794ba77bb6a8728d0e022d8003a6d387b
base_tree: 1e92bbea5d35b10b9f5d9d5d67dd59d8841fdcf0
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T04:15:16Z
plan0_scope: [plugin/hooks/hook, plugin/tests/test_hooks.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# A non-tool hook event runs from the committed library when the working copy fails to import, logged, never silently off
## Raw request
> FIX: a non-tool hook event (Stop, SessionStart, UserPromptSubmit, SessionEnd, Notification) whose working-copy library fails to import runs from the committed library like tool events do, and every such fallback is logged to hooks.log, so fm doctor shows it; nothing is silently off
## Interpretation
Reading 1: a self-edit that breaks plugin/lib's import must not turn off the drive, the done-gate or the session context; those events run as last committed and leave a hooks.log line fm doctor shows. Reading 2: only make the failure visible (a log line) and keep exiting 0 with nothing run. Chosen: 1, which includes 2; ruled out 2 alone because the drive would still stop silently mid-run.
## Assumptions (confidence)
## Acceptance criteria
- [x] with plugin/lib/fmhooks.py broken in a committed copy, hook SessionStart still prints Foreman's context and hooks.log names SessionStart and the committed library — verify with `python3 plugin/tests/run.py test_hooks`
- [x] the PreToolUse fail-closed and committed-guard tests still pass — verify with `python3 plugin/tests/run.py test_hooks test_guard`
## Non-goals
## Approach (options → choice → why)
1. Every event takes the dispatcher's committed_library() path on a failed import, and log_error names the event. Likely outcome: Stop and SessionStart work through a broken edit; fails if: HEAD lacks fmhooks (then exit 0 with a stderr line, as now). 2. use what exists: committed_library() already loads HEAD's library for tool events; route non-tool events through it. Likely outcome: same as 1, which is this. 3. A stdlib-only marker file the doctor reads, no fallback. Fails if: the drive is still off until the user notices. 4. do less: log only. Fails if: the log writer must guess the state dir without fmcore, and the drive stays off. Choice 1 (85%).
## Risks and rollback
Running Stop or SessionStart from HEAD gives the older behaviour while the edit is broken: intended, as with the guard. A slow fallback (one git show per module) only runs after a failed import. Rollback: revert the dispatcher hunk; the test documents the old exit 0.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0907, T-0908, T-0928, T-0980, T-0985.
## Execution prompt
## Steps
1. [x] red test: a committed copy with a syntax error in fmhooks.py: SessionStart prints its context from the committed library and hooks.log names the event
2. [x] plugin/hooks/hook: every event takes the committed-library path on a failed import; the log line names the event; a double failure stays fail-closed for the guard and exit 0 with a stderr line for the rest
## Resume here
## Docs impact
MASTER (plugin/hooks/hook row), CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Hooks.test_a_broken_working_copy_leaves_non_tool_events_running_as_committed` → ✗ exit 1 · run.py: no test matches test_hooks.Hooks.test_a_broken_working_copy_leaves_non_tool_events_running_as_committed [ran] [tree f8a6484c359d] [world 2f1906870a] (2026-11-02T04:15:29Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.PreToolUse.test_a_broken_working_copy_leaves_non_tool_events_running_as_committed` → ✗ exit 1 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: PreToolUse 1s) / FAILED (1 classes: test_hooks.PreToolUse) [ran] [tree f8a6484c359d] [world 2f1906870a] (2026-11-02T04:15:35Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 556 tests in 57.9s (120 classes, 16 at a time; slowest: Stop 58s, NoTaskGate 30s, PreToolUse 27s) / OK [ran] [tree f6ddcc13564d] [world 2f1906870a] (2026-11-02T04:16:43Z)
- `python3 plugin/tests/run.py test_hooks.PreToolUse.test_a_broken_working_copy_leaves_non_tool_events_running_as_committed` → ✗ exit 1 · Ran 1 tests in 3.2s (1 classes, 16 at a time; slowest: PreToolUse 1s) / FAILED (1 classes: test_hooks.PreToolUse) (start tree + this task's tests) [ran] [tree f6ddcc13564d] [world 2f1906870a] (2026-11-02T04:16:56Z)
- `python3 plugin/tests/run.py test_hooks.PreToolUse.test_a_broken_working_copy_leaves_non_tool_events_running_as_committed` → exit 0 · Ran 1 tests in 3.3s (1 classes, 16 at a time; slowest: PreToolUse 3s) / OK [ran] [tree f6ddcc13564d] [world 2f1906870a] (2026-11-02T04:16:56Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 247 tests in 44.2s (31 classes, 16 at a time; slowest: Stop 44s, NoTaskGate 26s, PreToolUse 22s) / OK [ran] [tree dd52b282260e] [world 2f1906870a] (2026-11-02T04:26:36Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 556 tests in 46.8s (120 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 28s, PreToolUse 25s) / OK [ran] [tree dd52b282260e] [world 2f1906870a] (2026-11-02T04:26:36Z)
- (audit intent) `self-review of the dispatcher hunk: the import-failure branch now calls committed_library() for every event; the guard's fail-closed path and messages are unchanged; non-tool double failures exit 0 with a stderr line` → a self-edit that breaks plugin/lib no longer turns off the drive, the done-gate or the session context; they run as committed and hooks.log names the event, which fm doctor's hook-error row reads [tree dd52b282260e] (2026-11-02T04:26:36Z)
- (audit edge) `self-review of the dispatcher hunk: the import-failure branch now calls committed_library() for every event; the guard's fail-closed path and messages are unchanged; non-tool double failures exit 0 with a stderr line` → no committed copy (not a git checkout, or HEAD lacks fmhooks) keeps the old behaviour: tool events fail closed, the rest exit 0 with a stderr line; an agent adapter that fails to import exits 0 for non-tool events and 2 for tool events; the fallback costs one git show per module only after a failed import [tree dd52b282260e] (2026-11-02T04:26:36Z)
- (audit adversary) `self-review of the dispatcher hunk: the import-failure branch now calls committed_library() for every event; the guard's fail-closed path and messages are unchanged; non-tool double failures exit 0 with a stderr line` → no new allow path: tool events took this branch before; the committed guard still decides, and the working copy can't skip it by breaking its own import [tree dd52b282260e] (2026-11-02T04:26:36Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree dd52b282260e] [world 2f1906870a] (2026-11-02T04:28:42Z)
## Log
- 2026-11-02T04:14:14Z created
- 2026-11-02T04:14:59Z planned from capture
- 2026-11-02T04:15:08Z set approved=True
- 2026-11-02T04:15:15Z set approved=True
- 2026-11-02T04:15:15Z focused
- 2026-11-02T04:15:16Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T04:17:21Z scope: plugin/hooks/hook's import-failure branch routes every event through committed_library(); log_error names the event (was hard-coded PreToolUse); MASTER dispatcher row and CHANGELOG
- 2026-11-02T04:28:07Z done
- 2026-11-02T04:28:10Z committed ee895279 (4 files)
- 2026-11-02T04:28:42Z guard authorization added: publish
- 2026-11-02T04:34:46Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_agents.py, plugin/tests/test_bench.py, plugin/tests/test_board_posture.py, plugin/tests/test_board_sur…
## Why not caught
T-0033 built the committed-library fallback for the guard's half-applied edits and kept 'non-guard failures exit 0' for the rest; no test broke the library and then ran a non-tool event, and a silent exit 0 leaves no hooks.log line, so fm doctor never saw it.
## Lessons
- a fail-safe built for one event (the guard) should be checked against every event the same dispatcher serves; 'non-guard failures exit 0' hid the drive switching off
## Plan gaps
- failed first: step 1 red test: a committed copy with a syntax error in fmhooks.py: SessionStart prints its context from …
## Files touched
- plugin/tests/test_hooks.py
- plugin/hooks/hook
- MASTER.md
- CHANGELOG.md
