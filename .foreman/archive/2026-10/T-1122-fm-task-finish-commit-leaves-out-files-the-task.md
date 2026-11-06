---
id: T-1122
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_close_gates.py]
depends_on: []
source: discovered
created: 2026-10-16T06:12:33Z
updated: 2026-10-16T06:18:03Z
base: 902edc0e12a5229e3c1a62951d28b8a2d503a7cf
base_tree: 19b77293ea0b42579e5328492fcc7d5573eb342f
verified: strong
---
# Fm task finish --commit leaves out files the task changed through Bash (a python or heredo
## Raw request
> fm task finish --commit leaves out files the task changed through Bash (a python or heredoc edit of CHANGELOG/MASTER) even when the task log names them in a 'scope:' reason: they stay uncommitted and need a manual commit (T-1042, T-1073, T-1086 today); commit the files a scope reason names (and that differ from HEAD) with the task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A file this task's scope or a 'scope:' log reason names is committed with it, even when another task touched it since this task's first focus and the edit's touched record isn't in yet — verify with `python3 plugin/tests/run.py test_close_gates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then count scope and scope-log files as this task's in _theirs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_close_gates` → ✗ exit 1 · Ran 13 tests in 12.0s (1 classes, 16 at a time; slowest: CloseGates 12s) / FAILED (1 classes) [ran] [tree c8cd92bad214] (2026-10-16T06:16:06Z)
- (step 1) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 13 tests in 26.8s (1 classes, 16 at a time; slowest: CloseGates 27s) / OK [ran] [tree 6cb5b539b60d] (2026-10-16T06:16:53Z)
- (ac 1) `python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 13 tests in 20.5s (1 classes, 16 at a time; slowest: CloseGates 20s) / OK [ran] [tree 172f0a284dd3] (2026-10-16T06:17:23Z)
- (audit self) `self: reproduced the exact miss (left out 1 file only other tasks edited: CHANGELOG.md), fixed at _theirs where every commit routes; this close's own CHANGELOG edit is the live check` → no findings [tree 172f0a284dd3] (2026-10-16T06:17:23Z)
## Log
- 2026-10-16T06:12:33Z created
- 2026-10-16T06:15:44Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_close_gates.py']
- 2026-10-16T06:15:45Z focused
- 2026-10-16T06:17:02Z scope: CHANGELOG.md — release note
- 2026-10-16T06:18:03Z done
- 2026-10-16T06:18:03Z committed de89974 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- A hook record written after the command can't vouch for edits the command itself made; let the task's own words (scope, scope log) count too
## Plan gaps
- failed first: step 1 Failing test, then count scope and scope-log files as this task's in _theirs
## Files touched
- plugin/tests/test_close_gates.py
- plugin/lib/fmcli.py
- CHANGELOG.md
