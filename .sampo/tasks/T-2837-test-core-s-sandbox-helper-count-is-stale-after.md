---
id: T-2837
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T20:34:27Z
updated: 2026-11-03T20:35:25Z
base: f491d6fd28668f48f760ae26bcd25bfd5e479de7
base_tree: d99d817a3b0539b71ed4dd7c0dc7c9e5b5e26aec
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T20:34:28Z
plan0_scope: []
verified: strong
---
# test_core's sandbox-helper count is stale after T-2835 (long 2, louhi 5): the suite is red on foreman/build
## Raw request
> test_core's sandbox-helper count is stale after T-2835 (long 2, louhi 5): the suite is red on foreman/build
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_core.SandboxEnv passes with long 2 and louhi 5 — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] update the counts with the T-2835 reason
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 142 tests in 7.0s (29 classes, 16 at a time; slowest: ConfidenceRoutes 7s, BriefIndex 3s, WritesAndLocks 2s) / OK [ran] [tree ca561fc0097e] [world 2f1906870a] (2026-11-03T20:35:05Z)
- (step 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 142 tests in 7.0s (29 classes, 16 at a time; slowest: ConfidenceRoutes 7s, BriefIndex 3s, WritesAndLocks 2s) / OK [ran] [tree ca561fc0097e] [world 2f1906870a] (2026-11-03T20:35:05Z)
- (audit intent) `self: the count test now expects long 2 and louhi 5, matching the calls T-2835 added (long._recur_state, louhi._model_env)` → the suite is green again on foreman/build [tree ca561fc0097e] (2026-11-03T20:35:05Z)
- (audit edge) `self: the count test now expects long 2 and louhi 5, matching the calls T-2835 added (long._recur_state, louhi._model_env)` → the counts still catch a builder that copies its own filter back in [tree ca561fc0097e] (2026-11-03T20:35:05Z)
- (audit self) `self: the count test now expects long 2 and louhi 5, matching the calls T-2835 added (long._recur_state, louhi._model_env)` → no findings [tree ca561fc0097e] (2026-11-03T20:35:05Z)
## Log
- 2026-11-03T20:34:27Z created
- 2026-11-03T20:34:27Z focused
- 2026-11-03T20:34:28Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T20:35:24Z done
- 2026-11-03T20:35:25Z committed 08338749 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2814 [FIX S, done, 2 steps] Baseline red:… — lesson: Run the suite on the oldest supported Python before shipping: argparse's subparser prog changed in 3.14
- T-2835 [CLEAN S, done, 2 steps] louhi._run, _tool_out, _sh and long.py ~825 keep FOREMAN_* in model-written runs, so the… — lesson: Every subprocess that runs model-writ…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-10-31: Narrow the code freeze during the long-tier runs: lanes off the session path (T-2294 builder doc, T-2156 ci-watch, T-2279 doctor, T-2296 friction di…
- similar finished tasks took 2–3 steps
## Regression test
none: the fix is to the test itself (its expected counts); the red is the test failing on the start tree (AssertionError: 2 != 1 : long, reported by T-2789's builder), green after
## Why not caught
test_core reads louhi.py and long.py as text, so the map links it to neither; T-2835's affected run skipped it (captured as T-2838)
## Lessons
- After changing call sites a source-counting test guards, run that test by name: the map can't link a test to files it only reads as text
## Files touched
- plugin/tests/test_core.py
