---
id: T-0876
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T14:17:12Z
updated: 2026-10-15T15:11:42Z
group: fm check and evidence correctness
base: 6eed14fb271d16e8372f73d6f657316be06c0975
base_tree: d92a57383cf696c66f93e0e5647144d877b02232
verified: strong
---
# Evidence runs never read a .pyc older than its source (a same-second, same-size edit reused stale bytecode)
## Raw request
> fm task evidence --run can record a stale result when a fix keeps the file's size and mtime second (python reuses __pycache__): evidence runs set PYTHONDONTWRITEBYTECODE=1 or compare by content
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an evidence run after a same-second same-size edit sees the new code — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_cli, then run_command drops racy .pyc of changed .py files first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli test_diff_gates test_gate_friction` → exit 0 · Ran 106 tests in 18.1s (27 classes, 16 at a time; slowest: TaskLifecycle 18s, DiffGates 8s, StateViews 7s) / OK [ran] [tree 20f0c447b3e2] (2026-10-15T15:00:31Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 88 tests in 18.0s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 20f0c447b3e2] (2026-10-15T15:01:07Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 88 tests in 17.7s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Checks 4s) / OK [ran] [tree 20f0c447b3e2] (2026-10-15T15:01:07Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_bench_family test_diff_gates` → exit 0 · Ran 112 tests in 18.5s (30 classes, 16 at a time; slowest: TaskLifecycle 18s, Judged 11s, DiffGates 8s) / OK [ran] [tree 8729127cd57b] (2026-10-15T15:09:05Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 88 tests in 17.9s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8729127cd57b] (2026-10-15T15:11:23Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 88 tests in 17.6s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree 8729127cd57b] (2026-10-15T15:11:23Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 88 tests in 17.7s (24 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 6s, Checks 4s) / OK [ran] [tree 8729127cd57b] (2026-10-15T15:11:41Z)
- (audit adversary) `self review: run_command drops any .pyc not newer than its source before running, found by a pruned os.walk (no git: a git call there ran a bench session's planted fsmonitor, caught by test_bench_family)` → the first draft's git ls-files ran core.fsmonitor in a bench worktree a session had configured (gate caught it); the walk runs no command, only unlinks .pyc files Python would rebuild anyway, and skips dot-dirs, node_modules and site-packages [tree 8729127cd57b] (2026-10-15T15:11:41Z)
- (audit edge) `self review: run_command drops any .pyc not newer than its source before running, found by a pruned os.walk (no git: a git call there ran a bench session's planted fsmonitor, caught by test_bench_family)` → an unrelated .pyc with no source beside it is left alone; walk cost 0.01 s here, 0.2 s over all of HOME [tree 8729127cd57b] (2026-10-15T15:11:41Z)
- (audit self) `self review: run_command drops any .pyc not newer than its source before running, found by a pruned os.walk (no git: a git call there ran a bench session's planted fsmonitor, caught by test_bench_family)` → no findings [tree 8729127cd57b] (2026-10-15T15:11:41Z)
## Log
- 2026-10-15T14:17:12Z created
- 2026-10-15T14:58:54Z planned from capture
- 2026-10-15T14:58:55Z focused
- 2026-10-15T15:11:42Z done
- 2026-10-15T15:11:42Z committed 8f7865c (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- playbook Strategic Compact Skill (skills/playbooks/references/context/strategic-compact.md)
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-14: Block T-0760 rather than edit its failing AC, since the AC already has evidence
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Why not caught
none: Python's own same-second mtime check, not a Foreman path; found by running evidence after a scripted edit
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcore.py
