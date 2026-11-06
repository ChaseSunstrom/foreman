---
id: T-2454
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T06:49:35Z
updated: 2026-11-01T07:04:02Z
base: 4e0a1989f87c1262affa97739e64661979617e28
base_tree: e404109831e78e6f2fa9f174b848bdce6de74d10
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-01T06:57:24Z
plan0_scope: []
verified: strong
---
# fmforesight._requests takes files touched outside the project (a scratchpad path…
## Raw request
> FIX: fmforesight._requests takes files touched outside the project (a scratchpad path relpath'd to ../../..) as a request's paths, so the live next-request prediction and draft-ahead keys carry them; drop paths that leave the repo (start with .. or are absolute) — seen in the live book row P-1 (after T-2447)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a request's paths keep only files inside the project: scope and touched files that are absolute outside it or start with .. are dropped — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] drop paths outside the project in fmforesight._requests
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_foresight -k test_files_touched_outside_the_repo` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PredictionBook 0s) / FAILED (1 classes: test_foresight.PredictionBook) [ran] [tree 81234c56b7d6] (2026-11-01T06:57:31Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_exam -k PredictionBook -k DraftAhead -k ForecastKind` → exit 0 · Ran 13 tests in 5.3s (3 classes, 16 at a time; slowest: PredictionBook 5s, ForecastKind 3s, DraftAhead 2s) / OK [ran] [tree 8593cacfc9e9] (2026-11-01T06:57:50Z)
- `python3 plugin/tests/run.py test_foresight -k test_files_touched_outside_the_repo` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: PredictionBook 0s) / FAILED (1 classes: test_foresight.PredictionBook) (start tree + this task's tests) [ran] [tree 8593cacfc9e9] (2026-11-01T06:58:01Z)
- `python3 plugin/tests/run.py test_foresight -k test_files_touched_outside_the_repo` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PredictionBook 0s) / OK [ran] [tree 8593cacfc9e9] (2026-11-01T06:58:01Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 28 tests in 5.2s (6 classes, 16 at a time; slowest: PredictionBook 5s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 8593cacfc9e9] (2026-11-01T06:58:07Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 28 tests in 5.1s (6 classes, 16 at a time; slowest: PredictionBook 5s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 8593cacfc9e9] (2026-11-01T07:03:41Z)
- (audit self) `self: fm check exit 0 (5524 tests); red→green test (an absolute path outside the repo, a ../ path and an in-repo absolute path: only the in-repo files stay); fm task prove proved; the replay over 376 held-out requests: paths 0.116 vs the baseline's 0.115, type 259 vs 256` → no findings [tree 8593cacfc9e9] (2026-11-01T07:03:41Z)
## Log
- 2026-11-01T06:49:35Z created
- 2026-11-01T06:57:23Z set tier=S
- 2026-11-01T06:57:23Z planned: it has criteria and steps
- 2026-11-01T06:57:24Z focused
- 2026-11-01T06:57:24Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-01T06:58:07Z scope: plugin/lib/fmforesight.py (_requests) and plugin/tests/test_foresight.py (the test); replay after: type 259 vs 256, paths 0.116 vs 0.115
- 2026-11-01T07:04:00Z done
- 2026-11-01T07:04:02Z committed 3be300c5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2406 [FEATURE M, done, 4 steps] Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Missi…
- T-2449 [FIX S, done, 3 steps] The next-request predictor's paths trail the naive baseline on the user's own stream (fm… — lesson: Two small cuts compounded: skipping the…
- T-2035 [FIX S, done, 1 steps] PostToolUseValidate syntax-checks .py files outside the project (a scratchpad method… — lesson: A validator that blocks should stop at the …
- decision 2026-10-31: [cites: T-2178; gen-0 §2 #13; decisions 2026-10-30 T-2105] Genesis self-start (gen-0 #13, reconciling T-2105): under full autonomy, a drained queue …
## Lessons
- A ledger path is the repo's only after relpath shows it doesn't climb out; check that before using it as a request's file
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
