---
id: T-2606
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T11:50:10Z
updated: 2026-11-02T12:16:29Z
base: 155db67de3a293b721627c38ead3f7ccab70fdd2
base_tree: 96b53ef08f9efadbff197c1c6804dd5a3852ba8b
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T11:58:00Z
plan0_scope: []
verified: strong
---
# A criterion whose every recorded run matched no test can have its verify command edited: a command that measured nothing weakens no check
## Raw request
> FIX: a criterion whose verify command names a test module that doesn't exist ('run.py: no test matches test_selfgate') can't be edited once any evidence exists (fm task ac edit refuses), and fm task finish reruns it and fails each time; a command whose run matched no test never measured anything, so editing it moves no goalpost: allow the edit when the newest run says no test matched (T-2605)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Brief.edit_ac allows a verify edit when each evidence line for that criterion reports a run that matched no test (run.py's 'no test matches', 'Ran 0 tests', 'no tests ran'); a criterion with any other evidence, failing or passing, still refuses (T-0342) — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_bookkeeping
2. [x] the no-test exception in fmcore.Brief.edit_ac
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 22 tests in 4.3s (10 classes, 16 at a time; slowest: FinishGaps 4s, CommitOwnFiles 4s, StepEvidence 3s) / FAILED (1 classes: test_bookkeeping.FinishGaps) [ran] [tree 8c1c32ee7d8b] [world 2f1906870a] (2026-11-02T11:58:15Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping test_cli` → exit 0 · Ran 167 tests in 21.6s (54 classes, 16 at a time; slowest: TaskLifecycle 21s, CaptureAndIntake 10s, StateViews 10s) / OK [ran] [tree 0ec19e39d506] [world 2f1906870a] (2026-11-02T11:59:21Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping test_core.LazyPatterns` → exit 0 · Ran 25 tests in 11.1s (11 classes, 16 at a time; slowest: FinishGaps 10s, CommitOwnFiles 10s, CommitAfterFocus 8s) / OK [ran] [tree 35e2d4aeb2b6] [world 2f1906870a] (2026-11-02T12:05:41Z)
- `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 22 tests in 4.7s (10 classes, 16 at a time; slowest: FinishGaps 3s, CommitOwnFiles 3s, StepEvidence 3s) / FAILED (1 classes: test_bookkeeping.FinishGaps) (start tree + this task's tests) [ran] [tree 35e2d4aeb2b6] [world 2f1906870a] (2026-11-02T12:16:01Z)
- `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 22 tests in 3.6s (10 classes, 16 at a time; slowest: FinishGaps 3s, CommitOwnFiles 3s, StepEvidence 3s) / OK [ran] [tree 35e2d4aeb2b6] [world 2f1906870a] (2026-11-02T12:16:01Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 22 tests in 3.6s (10 classes, 16 at a time; slowest: FinishGaps 3s, CommitOwnFiles 3s, StepEvidence 3s) / OK [ran] [tree 35e2d4aeb2b6] [world 2f1906870a] (2026-11-02T12:16:05Z)
- (audit intent) `self-review: edit_ac allows a verify edit only when every evidence line for that criterion matches the lazy no-test pattern (run.py's 'no test matches', 'Ran 0 tests', 'no tests ran'); any other evidence keeps the T-0342 refusal; the pattern is lazy per the hook-import rule` → a misspelled test module's criterion can be fixed; one with a real failing run still refuses (test) [tree 35e2d4aeb2b6] (2026-11-02T12:16:05Z)
- (audit adversary) `self-review: edit_ac allows a verify edit only when every evidence line for that criterion matches the lazy no-test pattern (run.py's 'no test matches', 'Ran 0 tests', 'no tests ran'); any other evidence keeps the T-0342 refusal; the pattern is lazy per the hook-import rule` → the exception needs every recorded run to say no test matched, text that fm records from the runner itself; a session can't type evidence into a run line (typed evidence isn't marked ran), and a passing run never carries those words [tree 35e2d4aeb2b6] (2026-11-02T12:16:05Z)
- (audit self) `self-review: edit_ac allows a verify edit only when every evidence line for that criterion matches the lazy no-test pattern (run.py's 'no test matches', 'Ran 0 tests', 'no tests ran'); any other evidence keeps the T-0342 refusal; the pattern is lazy per the hook-import rule` → no findings [tree 35e2d4aeb2b6] (2026-11-02T12:16:05Z)
## Log
- 2026-11-02T11:50:10Z created
- 2026-11-02T11:51:11Z planned from capture
- 2026-11-02T11:57:59Z set approved=True
- 2026-11-02T11:57:59Z focused
- 2026-11-02T11:58:00Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T12:16:26Z done
- 2026-11-02T12:16:29Z committed d2e94748 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1145 [FEATURE S, done, 2 steps] Check a verify command when it is added (fm task ac add/edit, --ac ':: cmd'): a python tes
- research T-2369-review: Verdict: changes needed.** The core loop works: log the miss, lead in `fm next`, refuse finish and done, resolve by run evidence. But the module-…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- similar finished tasks took 2–5 steps
## Lessons
- A lock that protects a measurement shouldn't hold one that never measured: tell 'failed' from 'never ran'
## Plan gaps
- failed first: step 1 red test in test_bookkeeping
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcore.py
- CHANGELOG.md
