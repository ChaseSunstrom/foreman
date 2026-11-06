---
id: T-3152
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:56:14Z
updated: 2026-11-05T06:25:39Z
base: c1cbcefa3264fe82b1d53cbf8f23f0c9a20b1661
base_tree: 11fbe480e13318c4d58750db5292d37bf683200e
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T06:01:39Z
plan0_scope: []
verified: strong
---
# Moons' local-only fill names why no local model answered and tries the next local model (this box's GPU) before it stops
## Raw request
> Moons fill has added nothing since about 22:59: every run ends 'no local model answered (MOONS_LOCAL)' while Jarvis's HTTPS endpoint is up (401 without a key) and the local GPU has gpu-mimo9 and gemma loaded: find why the local-only fill gets no answer, and fall back to this box's GPU models when Jarvis doesn't answer
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] moonscale._ask in local-only mode: when the first local profile errors or replies empty, the next usable local profile answers the call; when none does, the LocalOnly message names each model tried and its error — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a failing first local profile falls through to a second; the stop message names both errors
2. [x] the fallthrough and the named causes in moonscale._ask and _local
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moons_scale.Route.test_a_failing_local_model_falls_through_to_the_next_and_the_stop_names_each_error` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Route 0s) / FAILED (1 classes: test_moons_scale.Route) [ran] [tree d745daa138b2] [world 2f1906870a] (2026-11-05T06:03:46Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 89 tests in 11.5s (16 classes, 16 at a time; slowest: StoreLock 11s, Yield 5s, KeepGrow 5s) / FAILED (1 classes: test_moons_scale.Grow) [ran] [tree 324f88749b81] [world 2f1906870a] (2026-11-05T06:09:16Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_exam test_foresight test_night` → exit 0 · Ran 288 tests in 243.5s (67 classes, 16 at a time; slowest: LeanKind 234s, ExamAuthors 84s, JudgmentKinds 81s) / OK [ran] [tree 6eee99809991] [world 2f1906870a] (2026-11-05T06:13:58Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 89 tests in 8.7s (16 classes, 16 at a time; slowest: Yield 8s, KeepGrow 7s, Funnel 6s) / OK [ran] [tree 6eee99809991] [world 2f1906870a] (2026-11-05T06:16:25Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale.Route.test_a_failing_local_model_falls_through_to_the_next_and_the_stop_names_each_error` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Route 0s) / OK [ran] [tree 6eee99809991] [world 2f1906870a] (2026-11-05T06:16:25Z)
- (audit edge) `self: _locals yields usable local profiles lazily (MOONS_LOCAL still pins one), _ask tries each, records each error, and skips a failed profile for DOWN_S=600 s; the reasoning-budget cut is counted but doesn't mark the model down; callers of _local are unchanged` → every local model failing gives a LocalOnly naming each one's error, or falls to Haiku when not local-only; a model whose reply was cut by its reasoning budget is retried next call, not skipped; two workers marking _down under the lock [tree 6eee99809991] (2026-11-05T06:16:25Z)
- (audit adversary) `self: _locals yields usable local profiles lazily (MOONS_LOCAL still pins one), _ask tries each, records each error, and skips a failed profile for DOWN_S=600 s; the reasoning-budget cut is counted but doesn't mark the model down; callers of _local are unchanged` → the error text a server returns is folded to one line and cut to 160 characters before it reaches the log; no key or header is in it (models.complete's errors carry the profile name and status) [tree 6eee99809991] (2026-11-05T06:16:25Z)
- (audit self) `self: _locals yields usable local profiles lazily (MOONS_LOCAL still pins one), _ask tries each, records each error, and skips a failed profile for DOWN_S=600 s; the reasoning-budget cut is counted but doesn't mark the model down; callers of _local are unchanged` → no findings [tree 6eee99809991] (2026-11-05T06:16:25Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_small_cards test_ideas test_exam test_foresight test_night` → exit 0 · Ran 338 tests in 391.0s (77 classes, 16 at a time; slowest: LeanKind 376s, ExamAuthors 138s, ExamGen 136s) / OK [ran] [tree af7f2ca2c607] [world 2f1906870a] (2026-11-05T06:24:38Z)
- (audit edge) `self: _locals yields usable local profiles lazily (MOONS_LOCAL still pins one), _ask tries each, records each error, and skips a failed profile for DOWN_S=600 s; the reasoning-budget cut is counted but doesn't mark the model down; direct callers of _local are unchanged; every test that sends _ask through a mocked picker now mocks _locals (found with an untruncated grep)` → every local model failing gives a LocalOnly naming each one's error, or falls to Haiku when not local-only; a model whose reply was cut by its reasoning budget is retried next call, not skipped; two workers marking _down under the lock [tree af7f2ca2c607] (2026-11-05T06:24:48Z)
- (audit adversary) `self: _locals yields usable local profiles lazily (MOONS_LOCAL still pins one), _ask tries each, records each error, and skips a failed profile for DOWN_S=600 s; the reasoning-budget cut is counted but doesn't mark the model down; direct callers of _local are unchanged; every test that sends _ask through a mocked picker now mocks _locals (found with an untruncated grep)` → the error text a server returns is folded to one line and cut to 160 characters before it reaches the log; no key or header is in it [tree af7f2ca2c607] (2026-11-05T06:24:48Z)
- (audit self) `self: _locals yields usable local profiles lazily (MOONS_LOCAL still pins one), _ask tries each, records each error, and skips a failed profile for DOWN_S=600 s; the reasoning-budget cut is counted but doesn't mark the model down; direct callers of _local are unchanged; every test that sends _ask through a mocked picker now mocks _locals (found with an untruncated grep)` → no findings [tree af7f2ca2c607] (2026-11-05T06:24:48Z)
## Log
- 2026-11-05T05:56:14Z created
- 2026-11-05T05:57:29Z planned from capture
- 2026-11-05T06:01:37Z focused
- 2026-11-05T06:01:39Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T06:25:35Z done
- 2026-11-05T06:25:39Z committed c51a8108 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3105 [FEATURE M, blocked, 3 steps] Fill the card library to 30,000 kept across every grid, local writers first, the night growing it and the live page showing progress…
- T-2916 [FEATURE M, done, 3 steps] The night shift runs on the local models: sampo night adds zero-dollar moons grow and moons funnel jobs while an own or loopback model …
- T-2878 [FEATURE L, blocked, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-04: T-3006's arm comparison runs on local models (gemma 12B, MiMo 9B) instead of the 27B: the Jarvis profiles need LLM_API_KEY, which is never stored, s…
- similar past tasks were M: consider --tier M
## Lessons
- A sweep for callers or mocks must never be piped through head: a truncated grep hid a test that would have called a real model
## Plan gaps
- failed first: step 1 failing tests: a failing first local profile falls through to a second; the stop message names both…
- failed first: step 2 the fallthrough and the named causes in moonscale._ask and _local
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- CHANGELOG.md
- plugin/tests/test_small_cards.py
