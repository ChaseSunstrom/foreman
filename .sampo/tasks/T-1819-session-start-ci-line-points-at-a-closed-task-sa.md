---
id: T-1819
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T08:12:33Z
updated: 2026-10-28T08:13:15Z
base: dee26583060476d4a436ef7f2c2161c99f918057
base_tree: 6ee28de63fac9b95c939041f38c6eb55a130e44b
plan0_at: 2026-10-28T08:12:33Z
plan0_scope: []
verified: strong
---
# Session-start CI line points at a closed task: say it's closed and what to do, not 'fix it first'
## Raw request
> Session-start CI line points at a closed task: say it's closed and what to do, not 'fix it first'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a dropped or archived CI-red task reads '<id> is dropped: push its fix…', never 'fix it first' — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_foresight, then lines() reads the task's status
## Resume here
## Docs impact
none: the line's wording only
## Verification evidence
- `python3 plugin/tests/run.py test_foresight` → ✗ exit 1 · Ran 14 tests in 1.2s (3 classes, 16 at a time; slowest: Foresight 0s, CiMain 0s, ReviewerCostAtScale 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e804d2882be8] (2026-10-28T08:13:06Z)
- `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 14 tests in 0.5s (3 classes, 16 at a time; slowest: Foresight 0s, CiMain 0s, ReviewerCostAtScale 0s) / OK [ran] [tree e804d2882be8] (2026-10-28T08:13:06Z)
- (step 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 14 tests in 0.5s (3 classes, 16 at a time; slowest: Foresight 0s, CiMain 0s, ReviewerCostAtScale 0s) / OK [ran] [tree e804d2882be8] (2026-10-28T08:13:11Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 14 tests in 0.5s (3 classes, 16 at a time; slowest: Foresight 0s, CiMain 0s, ReviewerCostAtScale 0s) / OK [ran] [tree e804d2882be8] (2026-10-28T08:13:12Z)
- (audit edge) `self: read lines() and its one caller (session start); proved red→green` → open task → 'fix it first' as before; dropped, done or archived → names the status and what to do [tree e804d2882be8] (2026-10-28T08:13:12Z)
- (audit maintainer) `self: read lines() and its one caller (session start); proved red→green` → cost at scale — one brief read per session start only when CI is red [tree e804d2882be8] (2026-10-28T08:13:12Z)
- (audit self) `self: read lines() and its one caller (session start); proved red→green` → no findings [tree e804d2882be8] (2026-10-28T08:13:12Z)
## Log
- 2026-10-28T08:12:33Z created
- 2026-10-28T08:12:33Z focused
- 2026-10-28T08:13:14Z done
- 2026-10-28T08:13:15Z committed 5919745d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1797 [FEATURE M, done, 3 steps] CC 2.1.305-2.1.312 adoption: give fm-reviewer/fm-recon an autoCompactWindow; fm doctor poi — lesson: Subagent transcripts carry their p…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
## Why not caught
none: T-1810's test never closed the captured task
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
