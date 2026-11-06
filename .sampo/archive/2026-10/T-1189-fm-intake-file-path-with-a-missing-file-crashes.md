---
id: T-1189
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_intake.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T12:38:40Z
updated: 2026-10-16T12:43:50Z
base: 1301275eebf705dffe275c212076dc2dab339c03
base_tree: f036102e04551cd54bb7dfdafe7aa3926ff08fef
plan0_at: 2026-10-16T12:39:36Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_intake.py, CHANGELOG.md]
verified: strong
---
# Fm intake --file PATH with a missing file crashes with a Python traceback instead of a usa
## Raw request
> fm intake --file PATH with a missing file crashes with a Python traceback instead of a usage error naming the file
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm intake --file missing.txt exits 2 with a usage error naming the file, no traceback — verify with `python3 plugin/tests/run.py -k test_a_missing_file_argument_is_a_usage_error`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test + the guarded read
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_missing_file_argument_is_a_usage_error` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: CaptureAndIntake 0s) / FAILED (1 classes) [ran] [tree 829a6c740b81] (2026-10-16T12:39:57Z)
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 103 tests in 52.4s (28 classes, 16 at a time; slowest: TaskLifecycle 52s, StateViews 10s, AuditPrep 8s) / OK [ran] [tree 7429ae73b33c] (2026-10-16T12:40:56Z)
- `python3 plugin/tests/run.py -k test_a_missing_file_argument_is_a_usage_error` → ✗ exit 1 · Ran 1 tests in 4.3s (1 classes, 16 at a time; slowest: CaptureAndIntake 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4eb3f91df65d] (2026-10-16T12:41:22Z)
- `python3 plugin/tests/run.py -k test_a_missing_file_argument_is_a_usage_error` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 4eb3f91df65d] (2026-10-16T12:41:22Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_missing_file_argument_is_a_usage_error` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 4eb3f91df65d] (2026-10-16T12:41:26Z)
- (audit edge) `self: one handler in main for every --file reader (intake, research add, edit, others): a FileNotFound/IsADirectory/Permission error whose filename is on the command line is a usage error; any other is re-raised` → --file=X form matched; a missing internal file still raises (not hidden) [tree 4eb3f91df65d] (2026-10-16T12:41:26Z)
- (audit self) `self: one handler in main for every --file reader (intake, research add, edit, others): a FileNotFound/IsADirectory/Permission error whose filename is on the command line is a usage error; any other is re-raised` → no findings [tree 4eb3f91df65d] (2026-10-16T12:41:26Z)
## Log
- 2026-10-16T12:38:40Z created
- 2026-10-16T12:39:35Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_intake.py', 'CHANGELOG.md']
- 2026-10-16T12:39:35Z focused
- 2026-10-16T12:39:56Z criterion 1 verify: `python3 plugin/tests/run.py test_intake` → `python3 plugin/tests/run.py test_cli`
- 2026-10-16T12:41:11Z scope: the test lives in test_cli (CaptureAndIntake), not a new test_intake
- 2026-10-16T12:41:13Z criterion 1 verify: `python3 plugin/tests/run.py test_cli` → `python3 plugin/tests/run.py -k test_a_missing_file_argument_is_a_usage_error`
- 2026-10-16T12:43:46Z done
- 2026-10-16T12:43:50Z committed 9639b132 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r1-edge: sh` is missing, and will raise `UnicodeDecodeError` if the command's stdout/stderr contains bytes that aren't valid UTF‑8 (binary output, or any …
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Plan gaps
- failed first: step 1 Failing test + the guarded read
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
