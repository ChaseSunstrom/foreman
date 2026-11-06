---
id: T-1128
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T07:44:11Z
updated: 2026-10-16T07:47:43Z
base: 673cb87d6913e4f08c9f87b6a6f09df175148269
base_tree: 7a1b35d639c5ee7a9ee01e6c0fa70b6c85cbdf96
plan0_at: 2026-10-16T07:44:12Z
plan0_scope: []
verified: strong
---
# A verify run that ran zero tests counts as never ran, so its criterion stays editable
## Raw request
> A verify run that ran zero tests counts as never ran, so its criterion stays editable
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] never_ran() names 'no tests ran' for unittest's NO TESTS RAN / Ran 0 tests and pytest's 'no tests ran' on a failing exit, so edit_ac allows the fix — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then extend never_ran
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_never_ran test_core` → exit 0 · Ran 71 tests in 3.5s (17 classes, 16 at a time; slowest: NeverRanUnlocks 3s, PreToolUse 2s, WritesAndLocks 2s) / OK [ran] [tree d1e36bea7949] (2026-10-16T07:44:52Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 68 tests in 1.8s (16 classes, 16 at a time; slowest: WritesAndLocks 2s, PreToolUse 1s, RunCommand 0s) / OK [ran] [tree 168cc5744727] (2026-10-16T07:45:02Z)
- `python3 plugin/tests/run.py test_never_ran` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: NeverRanUnlocks 2s) / OK [ran] [tree 168cc5744727] (2026-10-16T07:45:02Z)
- (audit self) `self: only the last three non-empty output lines count, so a run whose zero-test suite is followed by a suite that failed stays locked (tested); a passing exit never counts; the T-0342 lock on real failing checks is untouched` → no findings [tree 168cc5744727] (2026-10-16T07:45:02Z)
- `python3 plugin/tests/run.py test_never_ran` → ✗ exit 1 · Ran 3 tests in 5.4s (1 classes, 16 at a time; slowest: NeverRanUnlocks 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 168cc5744727] (2026-10-16T07:46:02Z)
- `python3 plugin/tests/run.py test_never_ran` → exit 0 · Ran 3 tests in 4.8s (1 classes, 16 at a time; slowest: NeverRanUnlocks 5s) / OK [ran] [tree 168cc5744727] (2026-10-16T07:46:02Z)
- `python3 plugin/tests/run.py test_never_ran` → exit 0 · Ran 3 tests in 5.6s (1 classes, 16 at a time; slowest: NeverRanUnlocks 5s) / OK [ran] [tree 168cc5744727] (2026-10-16T07:46:08Z)
- (audit self) `self: only the last three non-empty output lines count, so a run whose zero-test suite is followed by a suite that failed stays locked (tested); a passing exit never counts; the T-0342 lock on real failing checks is untouched` → no findings [tree 168cc5744727] (2026-10-16T07:46:08Z)
## Log
- 2026-10-16T07:44:11Z created
- 2026-10-16T07:44:12Z focused
- 2026-10-16T07:44:58Z scope: CHANGELOG.md — release note; plugin/lib/fmcore.py, plugin/tests/test_never_ran.py
- 2026-10-16T07:47:41Z done
- 2026-10-16T07:47:43Z committed d6de8f0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one [stale: plugin/tests/ru…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- T-0985 [FIX M, done, 2 steps] A run that never reached the check doesn't lock a criterion: fm task ac edit can fix a wrong verify path — lesson: A lock meant to stop wea…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Lessons
- A run that checked nothing is no evidence either way, so it can't lock anything
## Files touched
- plugin/tests/test_never_ran.py
- plugin/lib/fmcore.py
- CHANGELOG.md
