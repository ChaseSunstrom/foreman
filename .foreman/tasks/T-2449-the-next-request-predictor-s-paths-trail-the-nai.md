---
id: T-2449
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T06:02:06Z
updated: 2026-11-01T06:36:10Z
base: 08ff330fdef697c6c4e6b6919d5380ada2d6ce60
base_tree: 21a1ceae8531ae60676596cc67bc6ffc69b6b937
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-01T06:22:23Z
plan0_scope: []
verified: strong
---
# The next-request predictor's paths trail the naive baseline on the user's own stream (fm…
## Raw request
> FIX: the next-request predictor's paths trail the naive baseline on the user's own stream (fm exam's replay, T-2409: overlap 0.052 vs 0.086 over 376 held-out requests; type 259 vs 256). Likely cause: fmforesight.predict takes paths from the latest request of the predicted type before the last one (reqs[:-1]), so when the predicted type is the last's own it skips the last request's paths. Fix test-first, then rerun the foresight arm's replay
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the predicted paths come from the newest request of the predicted type, the last included, and keep every path the request touched (up to _requests' 20) — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] fix fmforesight.predict
3. [x] docs: MASTER, CHANGELOG; the replay re-run
## Resume here
## Docs impact
MASTER.md (fmforesight predict T-2449), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_foresight -k test_predicted_paths_come_from` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: PredictionBook 0s) / FAILED (1 classes: test_foresight.PredictionBook) [ran] [tree ff454facd036] (2026-11-01T06:22:31Z)
- (step 2) `python3 plugin/tests/run.py test_foresight test_exam -k PredictionBook -k DraftAhead -k ForecastKind` → exit 0 · Ran 12 tests in 5.1s (3 classes, 16 at a time; slowest: PredictionBook 5s, ForecastKind 3s, DraftAhead 2s) / OK [ran] [tree 72d0d590e815] (2026-11-01T06:22:44Z)
- (step 3) `python3 -c "import sys; sys.path.insert(0, 'plugin/lib'); import fmcore as c, fmexam; r = fmexam.replay_forecast(c.find_project('.')); print(r); assert r['overlap'] >= r['base_overlap'] and r['type_hit'] >= r['base_type_hit']"` → exit 0 · {'held': 376, 'type_hit': 259, 'base_type_hit': 256, 'overlap': 0.088, 'base_overlap': 0.086} [ran] [tree 96d345cc8aad] (2026-11-01T06:23:02Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 27 tests in 5.2s (6 classes, 16 at a time; slowest: PredictionBook 5s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 96d345cc8aad] (2026-11-01T06:23:07Z)
- `python3 plugin/tests/run.py test_foresight -k test_predicted_paths_come_from` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: PredictionBook 0s) / FAILED (1 classes: test_foresight.PredictionBook) (start tree + this task's tests) [ran] [tree 96d345cc8aad] (2026-11-01T06:23:10Z)
- `python3 plugin/tests/run.py test_foresight -k test_predicted_paths_come_from` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: PredictionBook 0s) / OK [ran] [tree 96d345cc8aad] (2026-11-01T06:23:10Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 27 tests in 5.0s (6 classes, 16 at a time; slowest: PredictionBook 5s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 96d345cc8aad] (2026-11-01T06:28:34Z)
- (audit intent) `fm check exit 0 (5520 tests); red→green test (the last request's paths when the type repeats, every path kept); fm task prove proved; the replay over this project's 376 held-out requests: paths 0.052 → 0.088 vs the baseline's 0.086, type 259 vs 256 unchanged` → the predictor now beats the naive baseline on both measures on the user's own history, which is what the prediction book scores against [tree 96d345cc8aad] (2026-11-01T06:28:34Z)
- (audit edge) `fm check exit 0 (5520 tests); red→green test (the last request's paths when the type repeats, every path kept); fm task prove proved; the replay over this project's 376 held-out requests: paths 0.052 → 0.088 vs the baseline's 0.086, type 259 vs 256 unchanged` → a type never seen before falls back to the last request's paths; a request with no paths predicts none; up to 20 paths as _requests keeps them, so rows stay bounded [tree 96d345cc8aad] (2026-11-01T06:28:34Z)
- (audit self) `fm check exit 0 (5520 tests); red→green test (the last request's paths when the type repeats, every path kept); fm task prove proved; the replay over this project's 376 held-out requests: paths 0.052 → 0.088 vs the baseline's 0.086, type 259 vs 256 unchanged` → no findings [tree 96d345cc8aad] (2026-11-01T06:28:34Z)
## Log
- 2026-11-01T06:02:06Z created
- 2026-11-01T06:06:13Z diagnosis (replay over 376 held-out requests): the type's latest request before the last 0.053 overlap; capped at 20 paths instead of 5: 0.070; including the last request too: 0.088 vs the baseline's 0.086. Two causes: reqs[:-1] skips the last request, and [:5] caps a guess at 5 of up to 20 paths
- 2026-11-01T06:22:18Z set tier=S
- 2026-11-01T06:22:22Z planned: it has criteria and steps
- 2026-11-01T06:22:23Z focused
- 2026-11-01T06:22:23Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-01T06:23:15Z scope: plugin/lib/fmforesight.py (predict), plugin/tests/test_foresight.py (the test), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T06:28:56Z done
- 2026-11-01T06:28:59Z committed c22061b5 (4 files)
- 2026-11-01T06:29:04Z guard authorization added: publish
- 2026-11-01T06:36:10Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2409 [FEATURE M, done, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8,…
- T-2406 [FEATURE M, done, 4 steps] Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Missi…
- T-2401 [FIX S, done, 1 steps] #4 exam defect: the oracle misses test-first on goal-rust-860eab (s0-011), so it closes 17/18 and a #4 held-out scenario no arm can close —…
- decision 2026-10-30: [revisited: free arm beats the session arm] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3 plugin/tests/ru…
## Lessons
- Two small cuts compounded: skipping the newest request and capping at 5 paths each cost a third of the overlap; the replay measured each one separately
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
- CHANGELOG.md
- MASTER.md
