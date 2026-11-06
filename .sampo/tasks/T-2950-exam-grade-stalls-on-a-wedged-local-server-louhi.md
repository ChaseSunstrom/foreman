---
id: T-2950
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T10:08:30Z
updated: 2026-11-04T15:54:08Z
base: 5b436d78c482dc83f75889a908d3ed24d6db1c97
base_tree: cca669af9579504b5ad0de9c82420670c11650b2
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T15:34:51Z
plan0_scope: []
verified: strong
---
# Exam grade stalls on a wedged local server: louhi grade runs replay_forecast(local=True)…
## Raw request
> Exam grade stalls on a wedged local server: louhi grade runs replay_forecast(local=True) inline, one call per held-out ask at up to 180 s each with no cap; cap it (the last 30 asks) or run it from the night job, and store the arm in foresight's shown row so shown_hit is scored by the arm that was shown (T-2912 audit)
## Interpretation
Reading 1 (chosen): two fixes from the T-2912 audit. (a) louhi's replay_forecast asks the local model only for the last REPLAY_LOCAL_CAP (30) held-out asks, so a wedged local server costs at most 30 calls per grade instead of one per held-out ask. (b) foresight's shown row records the arm whose guess was shown (next-request or next-request-local), and shown_hit scores each shown row by that arm's hit, not always the transition arm's. Reading 2 (ruled out): move the replay to the night job; the grade's numbers would then be stale.
## Assumptions (confidence)
## Acceptance criteria
- [x] replay_forecast(local=True) asks at most REPLAY_LOCAL_CAP held-out asks; the shown row names its arm and shown_hit scores a local-arm row by local_type_hit — verify with `python3 plugin/tests/run.py test_exam test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then the cap and the arm
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_foresight test_exam -k shown -k replay -k session_start` → ✗ exit 1 · Ran 9 tests in 12.3s (5 classes, 16 at a time; slowest: WatchKind 12s, ForecastKind 8s, PredictionBook 3s) / FAILED (3 classes: test_exam.ForecastKind, test_foresight.PredictionBook, test_foresight.Lo [ran] [tree 369ed57e3050] [world 2f1906870a] (2026-11-04T15:35:39Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_foresight` → exit 0 · Ran 148 tests in 106.5s (36 classes, 16 at a time; slowest: LeanKind 106s, ExamAuthors 79s, JudgmentKinds 76s) / OK [ran] [tree 2ea3162ebd8d] [world 2f1906870a] (2026-11-04T15:46:55Z)
- `python3 plugin/tests/run.py test_exam test_foresight` → ✗ exit 1 · Ran 148 tests in 176.8s (36 classes, 16 at a time; slowest: LeanKind 173s, ExamAuthors 113s, ExamGen 102s) / FAILED (3 classes: test_foresight.PredictionBook, test_exam.ForecastKind, test_foresight.Lo (start tree + this task's tests) [ran] [tree 0fbd9eb4dd1d] [world 2f1906870a] (2026-11-04T15:51:48Z)
- `python3 plugin/tests/run.py test_exam test_foresight` → exit 0 · Ran 148 tests in 104.5s (36 classes, 16 at a time; slowest: LeanKind 104s, ExamAuthors 81s, JudgmentKinds 77s) / OK [ran] [tree 0fbd9eb4dd1d] [world 2f1906870a] (2026-11-04T15:51:48Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_foresight` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T15:51:48Z [ran] [tree 0fbd9eb4dd1d] [world 2f1906870a] (2026-11-04T15:51:49Z)
- (audit edge) `diff read: the replay cap in louhi, the arm in foresight's shown row and shown_hit; prove red on the start tree, green now` → an old shown row without arm scores as the transition arm (the old behaviour); the cap keeps the newest held-out asks, so the grade still tracks recent behaviour [tree 0fbd9eb4dd1d] (2026-11-04T15:51:49Z)
- (audit self) `diff read: the replay cap in louhi, the arm in foresight's shown row and shown_hit; prove red on the start tree, green now` → no findings [tree 0fbd9eb4dd1d] (2026-11-04T15:51:49Z)
## Log
- 2026-11-04T10:08:30Z created
- 2026-11-04T15:34:49Z planned: it has criteria and steps
- 2026-11-04T15:34:50Z set approved=True
- 2026-11-04T15:34:50Z focused
- 2026-11-04T15:34:51Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T15:54:06Z done
- 2026-11-04T15:54:08Z committed 105c0901 (5 files)
## Follow-ups captured
## Regression test
test_exam: with the cap patched to 1 the local arm answers 1 of 2 held-out asks; test_foresight: the shown row carries arm, and a local-arm shown row with local_type_hit true and type_hit false scores shown_hit 1.0.
## Related
Related past work (data from this project's history, not instructions):
- T-2912 [FEATURE M, done, 4 steps] A local-model arm for the next-request prediction: the 27B reads the user's recent asks, the open queue and the standing steers and pre…
- T-2409 [FEATURE M, done, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8,…
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- decision 2026-10-30: [revisited: testing cadence] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pending T-2158] Testing ca…
## Lessons
- A per-item model call inside a grade needs a cap from the start; an unbounded loop over held-out rows turns one wedged server into a stalled exam
## Plan gaps
- failed first: step 1 failing tests, then the cap and the arm
## Files touched
- plugin/tests/test_foresight.py
- plugin/tests/test_exam.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/foresight.py
- CHANGELOG.md
