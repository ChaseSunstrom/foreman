---
id: T-1767
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T08:57:46Z
updated: 2026-10-23T09:03:47Z
base: 26a7bc68f4cde3d74382a08dd73eb187fa0dee47
base_tree: 6d1b89befd09d8242a6a19e651c72e4d65e32513
plan0_at: 2026-10-23T09:02:56Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard hint for a changelog edit with no active task says 'fm focus that task again', but f
## Raw request
> Guard hint for a changelog edit with no active task says 'fm focus that task again', but fm focus refuses a done task: name the way that works (the next task, with a scope note)
## Interpretation
The guard's brief-category hint for a CHANGELOG.md edit with no task says 'or fm focus that task again', but fm focus refuses a done task. Say what works: add the line before fm task finish, or in the next task with a scope note.
## Assumptions (confidence)
## Acceptance criteria
- [x] the changelog hint no longer suggests refocusing a done task and names the scope-note route — verify with `python3 plugin/tests/run.py test_guard.BriefChangelog`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then the hint text
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_guard.BriefChangelog` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: BriefChangelog 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9612a7bd0e20] (2026-10-23T09:02:58Z)
- `python3 plugin/tests/run.py test_guard.BriefChangelog` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: BriefChangelog 0s) / FAILED (1 classes) [ran] [tree 9612a7bd0e20] (2026-10-23T09:02:58Z)
- `python3 plugin/tests/run.py test_guard.BriefChangelog` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: BriefChangelog 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 52398c64d584] (2026-10-23T09:03:04Z)
- `python3 plugin/tests/run.py test_guard.BriefChangelog` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: BriefChangelog 0s) / OK [ran] [tree 52398c64d584] (2026-10-23T09:03:04Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 282 tests in 9.2s (83 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree 52398c64d584] (2026-10-23T09:03:18Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.BriefChangelog` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BriefChangelog 0s) / OK [ran] [tree 52398c64d584] (2026-10-23T09:03:19Z)
- (audit edge) `self review; test_guard green` → the hint text only; the block itself is unchanged, so the guard's decisions and fm replay are unaffected [tree 52398c64d584] (2026-10-23T09:03:19Z)
- (audit self) `self review; test_guard green` → no findings [tree 52398c64d584] (2026-10-23T09:03:19Z)
- (audit edge) `self review; test_guard green` → the hint text only; the block itself is unchanged, so the guard's decisions and fm replay are unaffected [tree 52398c64d584] (2026-10-23T09:03:34Z)
- (audit adversary) `self review; test_guard green` → the diff touches only a returned message string (no condition, category or allow path changed); the refusal still fires for CHANGELOG.md with no task (BriefChangelog asserts blocked) [tree 52398c64d584] (2026-10-23T09:03:34Z)
- (audit self) `self review; test_guard green` → no findings [tree 52398c64d584] (2026-10-23T09:03:34Z)
## Log
- 2026-10-23T08:57:46Z created
- 2026-10-23T08:59:01Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-23T09:02:55Z focused
- 2026-10-23T09:03:45Z done
- 2026-10-23T09:03:47Z committed 0aedfab4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1452 [FIX S, done, 2 steps] Brief refusal of a CHANGELOG edit says where the line goes
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1478 [FIX S, done, 2 steps] fm next skips a task a builder lane holds
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- similar finished tasks took 2–2 steps
- start here (files T-1452 touched): plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
the T-1452 test checked that the hint named fm focus, not that the command it names works on a done task
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
