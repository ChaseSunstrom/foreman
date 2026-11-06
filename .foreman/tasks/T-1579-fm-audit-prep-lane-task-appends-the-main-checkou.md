---
id: T-1579
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_audit_run.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T18:25:41Z
updated: 2026-10-22T18:45:51Z
base: d8b2e25c66675a11110274d834fc447b3c5bc4dc
base_tree: c4ecb36739329c0090bf70ba780d5180aba138f1
plan0_at: 2026-10-22T18:43:58Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_audit_run.py, CHANGELOG.md]
verified: strong
---
# Fm audit prep LANE-TASK appends the main checkout's uncommitted diff (another task's files
## Raw request
> fm audit prep LANE-TASK appends the main checkout's uncommitted diff (another task's files) to the lane branch's diff, so the reviewer sees and the gates flag files the lane never touched (seen: T-1574/T-1503 diffs carried T-1473's fmguard.py, test_guard.py, CHANGELOG.md hunks)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane task's prep diff leaves out another focused task's uncommitted edits; T-1296's case (the lane task itself focused in main) still includes them — verify with `python3 plugin/tests/run.py test_audit_run`
## Non-goals
## Approach (options → choice → why)
Grounded: fmcli.py audit prep (~4458, T-1296) appends git diff HEAD <worktree tree> whenever the task has a lane branch, so the main checkout's uncommitted edits for whatever task is focused there land in a lane task's review diff (T-1574, T-1503 and T-1572 all carried T-1473's fmguard.py, test_guard.py and CHANGELOG.md hunks). Options: (1) chosen: append the uncommitted pair only when this task is the main checkout's active task (fmcore.active_brief(load_briefs(p)) with lane None has this id), which is exactly T-1296's case (a lane task focused in main after merge-back); (2) filter the uncommitted diff to the task's scope: rejected, scope lists are often broad (CHANGELOG.md is in most scopes) so it would still leak; (3) drop T-1296: rejected, it caught real edits.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: another task focused in main with an uncommitted edit, lane task prep diff must not hold it
2. [x] append the uncommitted pair only when the lane task is the main checkout's active task
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_audit_run` → red as expected (exit 1) · Ran 6 tests in 5.5s (1 classes, 16 at a time; slowest: AuditRun 5s) / FAILED (1 classes) [ran] [tree 18feaf9d5d12] (2026-10-22T18:44:36Z)
- `python3 plugin/tests/run.py test_audit_run` → ✗ exit 1 · Ran 6 tests in 6.0s (1 classes, 16 at a time; slowest: AuditRun 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 614d9d5a4028] (2026-10-22T18:44:59Z)
- `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 6 tests in 5.7s (1 classes, 16 at a time; slowest: AuditRun 6s) / OK [ran] [tree 614d9d5a4028] (2026-10-22T18:44:59Z)
- (step 2) `python3 plugin/tests/run.py test_audit_run test_audit` → exit 0 · Ran 26 tests in 6.1s (16 classes, 16 at a time; slowest: AuditRun 6s, ImportCards 3s, TaskLifecycle 2s) / OK [ran] [tree 614d9d5a4028] (2026-10-22T18:45:05Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 6 tests in 5.8s (1 classes, 16 at a time; slowest: AuditRun 6s) / OK [ran] [tree 614d9d5a4028] (2026-10-22T18:45:11Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 6 tests in 5.8s (1 classes, 16 at a time; slowest: AuditRun 6s) / OK [ran] [tree 3ab4e37df117] (2026-10-22T18:45:24Z)
- (audit maintainer) `self: intent: a lane task's review diff drops another task's uncommitted edits, T-1296's case kept · adversary: no input path, read-only diff selection · edge: no active task in main → lane diff only; the lane task focused in main after merge-back → included · operator: no install/docs change beyond CHANGELOG · maintainer: new test fails without the change` → test_prep_diff_of_a_lane_task_leaves_out_another_tasks_uncommitted_edits red on the start tree [tree 3ab4e37df117] (2026-10-22T18:45:24Z)
- (audit self) `self: intent: a lane task's review diff drops another task's uncommitted edits, T-1296's case kept · adversary: no input path, read-only diff selection · edge: no active task in main → lane diff only; the lane task focused in main after merge-back → included · operator: no install/docs change beyond CHANGELOG · maintainer: new test fails without the change` → no findings [tree 3ab4e37df117] (2026-10-22T18:45:24Z)
## Log
- 2026-10-22T18:25:41Z created
- 2026-10-22T18:27:12Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_audit_run.py', 'CHANGELOG.md']
- 2026-10-22T18:43:57Z focused
- 2026-10-22T18:45:50Z done
- 2026-10-22T18:45:51Z committed 7c0359e1 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1296 [FIX S, done, 2 steps] fm audit prep's diff includes every changed file of the task, committed or not, so a reviewer never sees only the CHANGELOG hunk
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
T-1296's test had only one task, so the working tree's owner was never in question
## Lessons
- A diff assembled from 'whatever is uncommitted here' needs an owner check: the working tree belongs to the focused task, not to every task that asks
## Files touched
- plugin/tests/test_audit_run.py
- plugin/lib/fmcli.py
- CHANGELOG.md
