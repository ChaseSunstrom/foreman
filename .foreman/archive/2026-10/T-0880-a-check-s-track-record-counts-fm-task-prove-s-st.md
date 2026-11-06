---
id: T-0880
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:11:58Z
updated: 2026-10-15T15:14:36Z
base: 8f7865c7aba1f4afc5efbcb65bcc7f890ca5182a
base_tree: 8729127cd57b7ad45c854e2d5d9b581e1b3f392c
verified: strong
---
# A check's track record counts fm task prove's start-tree failure
## Raw request
> A check's track record counts fm task prove's start-tree failure
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a check that failed red under prove no longer reads 'never failed' at the close — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then catch_rates reads prove events
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verifying test_cli` → exit 0 · Ran 96 tests in 17.7s (31 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree f7716b332d9f] (2026-10-15T15:12:34Z)
- `python3 plugin/tests/run.py test_verifying` → ✗ exit 1 · Ran 8 tests in 0.8s (7 classes, 16 at a time; slowest: Claims 0s, Verifier 0s, Stale 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f7716b332d9f] (2026-10-15T15:12:36Z)
- `python3 plugin/tests/run.py test_verifying` → exit 0 · Ran 8 tests in 0.6s (7 classes, 16 at a time; slowest: Claims 0s, Verifier 0s, Stale 0s) / OK [ran] [tree f7716b332d9f] (2026-10-15T15:12:36Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 88 tests in 17.6s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree f7716b332d9f] (2026-10-15T15:14:35Z)
- (audit edge) `self review: catch_rates reads prove events (red, green) as two runs of the command in that task, so a red→green prove counts as a caught failure` → a prove event from before red/green were recorded (no 'red' key) is skipped; a prove whose start tree passed counts as two passing runs [tree f7716b332d9f] (2026-10-15T15:14:35Z)
- (audit self) `self review: catch_rates reads prove events (red, green) as two runs of the command in that task, so a red→green prove counts as a caught failure` → no findings [tree f7716b332d9f] (2026-10-15T15:14:35Z)
## Log
- 2026-10-15T15:11:58Z created
- 2026-10-15T15:11:58Z focused
- 2026-10-15T15:14:36Z done
- 2026-10-15T15:14:36Z committed ef97387 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0809 [FIX S, dropped, 2 steps] fm task prove treats only test files as tests, not every file in a tests folder
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- decision 2026-09-26: Order after T-0016: T-0022 and T-0023 (user requests, explore items: take the recommendation after self-critique in full autonomy), then T-0018's ro…
- the similar finished task took 2 steps
## Why not caught
none: T-0749 added the close's runs but prove's ledger event was never read; seen as a false warning at T-0876's close
## Files touched
- plugin/tests/test_verifying.py
- plugin/lib/fmcli.py
