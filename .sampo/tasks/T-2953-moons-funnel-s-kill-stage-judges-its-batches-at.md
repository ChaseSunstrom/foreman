---
id: T-2953
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T10:25:54Z
updated: 2026-11-04T10:46:40Z
base: da18f15a1b5f3976e83a9436e045ce9770311d5b
base_tree: d7a293e7b7e4f9e5efffc046a32e88d5b3cb59d8
plan0_at: 2026-11-04T10:25:55Z
plan0_scope: []
verified: strong
unproven: [perf-typed]
---
# Moons funnel's kill stage judges its batches at once, up to the local profile's slots (the 10k run judged one 20-moon batch every ~3 min, one at a time, while the endpoint serves 2)
## Raw request
> Moons funnel's kill stage judges its batches at once, up to the local profile's slots (the 10k run judged one 20-moon batch every ~3 min, one at a time, while the endpoint serves 2)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with slots 2 the kill stage has two batches in flight and every candidate gets its kill fate; r's counters stay exact — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then a pool in _kill and a lock around _judge's counters
## Resume here
<!-- auto -->
- 2026-11-04T10:26:49Z steps 1/1 done
- git: foreman/build; 2 uncommitted: plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py
- touched since last checkpoint: plugin/tests/test_moons_scale.py, plugin/lib/sampo/moonscale.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 43 tests in 2.0s (11 classes, 16 at a time; slowest: Funnel 2s, Grow 1s, Cli 1s) / OK [ran] [tree 567114cc7b86] [world 2f1906870a] (2026-11-04T10:26:43Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 43 tests in 5.3s (11 classes, 16 at a time; slowest: Grow 5s, Funnel 4s, Cli 4s) / OK [ran] [tree 1f227889dde2] [world 2f1906870a] (2026-11-04T10:43:38Z)
- (audit edge) `self: the pool only runs batches no other batch reads; _judge's counters (calls, fails, paid, models) now change under _lock so --max-calls and FAILS stay exact; the test pins peak concurrency 2 and three calls for 41 moons` → a round waits for its slowest batch (ponytail note); a None from one batch returns after the pool drains, so that round's other answer waits for the next run [tree 1f227889dde2] (2026-11-04T10:43:38Z)
- (audit self) `self: the pool only runs batches no other batch reads; _judge's counters (calls, fails, paid, models) now change under _lock so --max-calls and FAILS stay exact; the test pins peak concurrency 2 and three calls for 41 moons` → no findings [tree 1f227889dde2] (2026-11-04T10:43:38Z)
## Log
- 2026-11-04T10:25:54Z created
- 2026-11-04T10:25:54Z focused
- 2026-11-04T10:26:49Z paused: focus moved to T-2918
- 2026-11-04T10:38:26Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T10:38:26Z focused
- 2026-11-04T10:46:40Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-04: Moon growth runs both endpoint slots with reasoning off; reasoning on stays an A/B sample (32 rows) judged by the funnel
- T-2894 [FEATURE M, done, 4 steps] Model bench part 2: every held-out closed task's raw request as data (not only shadow rows), option descriptions for every decision (sy…
- T-2893 [FEATURE M, done, 5 steps] Local generation done right: per-profile request extras and a reasoning switch (chat_template_kwargs enable_thinking, a max_tokens budg…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar past tasks were M: consider --tier M
## Measurements
kill verdicts per minute on the 10k run: 6.2 before (560 in 90 min, one 20-moon batch at a time) → 10.3 after (120 in 11.6 min, two batches at once on the profile's 2 slots), 1.66x
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
