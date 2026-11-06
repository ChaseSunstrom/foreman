---
id: T-2506
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T19:36:43Z
updated: 2026-11-01T21:28:29Z
base: 1dd778d8acdc4d2df94fbaeafcdf4bfd12c9eafc
base_tree: 236112e36bd5bd0cb984eae8c113d88b169f6ba5
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T21:26:10Z
plan0_scope: []
verified: strong
---
# Genesis review grounding needs a path or a number of 3+ digits
## Raw request
> FIX: genesis review grounding: a bare number of 2 characters ('10') occurs in almost any input, so it grounds nothing; require a path (contains / or .) or a number of 3+ digits, with a test that '10' is dropped and '1556' kept (T-2501 review, edge lens)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finding grounded on '10' is dropped, on '1556' or 'plugin/x.py' kept — verify with `python3 plugin/tests/run.py test_genesis.GenerationReview`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then tighten the ground filter
## Resume here
## Docs impact
none: the filter's docstring and MASTER's 'a path or number' still hold
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenerationReview.test_a_short_number_grounds_nothing_but_a_path_or_a_long_number_does` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenerationReview 0s) / FAILED (1 classes: test_genesis.GenerationReview) [ran] [tree d0860871bee8] (2026-11-01T21:26:49Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenerationReview` → exit 0 · Ran 6 tests in 9.4s (1 classes, 16 at a time; slowest: GenerationReview 9s) / OK [ran] [tree 002b2dd7f539] (2026-11-01T21:27:18Z)
- `python3 plugin/tests/run.py test_genesis.GenerationReview.test_a_short_number_grounds_nothing_but_a_path_or_a_long_number_does` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: GenerationReview 0s) / FAILED (1 classes: test_genesis.GenerationReview) (start tree + this task's tests) [ran] [tree 002b2dd7f539] (2026-11-01T21:27:20Z)
- `python3 plugin/tests/run.py test_genesis.GenerationReview.test_a_short_number_grounds_nothing_but_a_path_or_a_long_number_does` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GenerationReview 0s) / OK [ran] [tree 002b2dd7f539] (2026-11-01T21:27:20Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenerationReview` → exit 0 · Ran 6 tests in 14.2s (1 classes, 16 at a time; slowest: GenerationReview 14s) / OK [ran] [tree 002b2dd7f539] (2026-11-01T21:27:36Z)
- (audit edge) `self-review: a ground now needs / or . (a path or file) or 3+ digits; the rest of the filter (a listed key, the ground occurring in the inputs) is unchanged` → '84%' (2 digits) no longer grounds alone; '1556' or 'plugin/x.py' does; a version like '3.14' passes by its dot [tree 002b2dd7f539] (2026-11-01T21:27:36Z)
- (audit self) `self-review: a ground now needs / or . (a path or file) or 3+ digits; the rest of the filter (a listed key, the ground occurring in the inputs) is unchanged` → no findings [tree 002b2dd7f539] (2026-11-01T21:27:36Z)
## Log
- 2026-11-01T19:36:43Z created
- 2026-11-01T21:15:53Z planned from capture
- 2026-11-01T21:26:09Z focused
- 2026-11-01T21:26:10Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T21:27:21Z scope: fmgenesis review grounding filter, test_genesis GenerationReview test
- 2026-11-01T21:28:24Z done
- 2026-11-01T21:28:29Z committed f95fac52 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2205-review: Verdict: changes needed (2 MEDIUM intent/edge, 1 MEDIUM edge, 4 LOW); reviewer ran nothing (read-only).
- research T-2246-review: Verdict:** approve with nits. I read the diff and the surrounding code but did not run the tests. [stale: plugin/lib/fmgenesis.py, plugin/tests/t…
- T-2501 [FEATURE L, done, 4 steps] Generation cross-cutting review: after the Mission critiques, one cold reviewer on a… — lesson: a new genesis stage needs the shared te…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were L: consider --tier L
## Plan gaps
- failed first: step 1 red test, then tighten the ground filter
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
