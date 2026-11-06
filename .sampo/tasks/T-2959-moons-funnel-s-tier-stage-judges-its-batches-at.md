---
id: T-2959
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T12:01:22Z
updated: 2026-11-04T12:02:52Z
base: e6c9d8cdb7f9f70fd9718f886d32d8ebac644ec8
base_tree: fdcd3b8030cfcb5db8bcebb316cd064410bd7840
plan0_at: 2026-11-04T12:01:23Z
plan0_scope: []
verified: strong
unproven: [perf-typed]
---
# Moons funnel's tier stage judges its batches at once too (the kill stage's pool, T-2953), applying the verdicts and the low-tier merges in batch order: ~75 tier batches at ~3 min each, one at a time, would add ~3.75 h after the 10k kill stage
## Raw request
> Moons funnel's tier stage judges its batches at once too (the kill stage's pool, T-2953), applying the verdicts and the low-tier merges in batch order: ~75 tier batches at ~3 min each, one at a time, would add ~3.75 h after the 10k kill stage
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with slots 2 the tier stage has two batches in flight, every candidate gets its tier fate, and the merges read survivors in batch order as before — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then one _judged helper shared by kill and tier
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · Ran 90 tests in 11.1s (25 classes, 16 at a time; slowest: Night 11s, NightTick 3s, NightGuards 3s) / OK [ran] [tree f2b53f21cdad] [world 2f1906870a] (2026-11-04T12:02:32Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 43 tests in 2.4s (11 classes, 16 at a time; slowest: Funnel 2s, Grow 1s, Cli 1s) / OK [ran] [tree f2b53f21cdad] [world 2f1906870a] (2026-11-04T12:02:35Z)
- (audit edge) `self: _judged only parallelises the judge calls; _tier still applies verdicts and low-tier merges in batch order on this thread, so a merge reads the same survivors as before; the counters stay under _lock (T-2953)` → a None answer stops the stage after its round drains, as the kill stage does; the next run judges the unanswered batch [tree f2b53f21cdad] (2026-11-04T12:02:35Z)
- (audit self) `self: _judged only parallelises the judge calls; _tier still applies verdicts and low-tier merges in batch order on this thread, so a merge reads the same survivors as before; the counters stay under _lock (T-2953)` → no findings [tree f2b53f21cdad] (2026-11-04T12:02:35Z)
## Log
- 2026-11-04T12:01:22Z created
- 2026-11-04T12:01:23Z focused
- 2026-11-04T12:02:20Z focused
- 2026-11-04T12:02:51Z done
- 2026-11-04T12:02:52Z committed 68b803d5 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2953 [PERFORMANCE S, done, 1 steps] Moons funnel's kill stage judges its batches at once, up to the local profile's slots (the 10k run judged one 20-moon batch every ~…
- T-2869 [FEATURE M, done, 2 steps] Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI embe…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
## Measurements
tier batches in flight with a 2-slot local profile: 1 → 2 (test: 41 moons, 3 calls, peak 2); on the 10k run the kill stage's same pool went 6.2 → 9.7 verdicts a minute (1,480 kill verdicts by 12:01 UTC), and the ~75 tier batches at ~3 min each drop from ~3.75 h to about half
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
