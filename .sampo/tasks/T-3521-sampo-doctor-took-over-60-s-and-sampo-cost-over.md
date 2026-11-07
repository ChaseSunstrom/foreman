---
id: T-3521
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:11:50Z
updated: 2026-11-06T19:45:04Z
lane: ~/.claude/foreman.lanes/T-3521
base_note: 
lane_branch: foreman/T-3521
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T19:13:40Z
plan0_scope: []
group: hook, doctor and UI speed
---
# Sampo doctor took over 60 s and sampo cost over 25 s under load: profile each and cut…
## Raw request
> PERFORMANCE: sampo doctor took over 60 s and sampo cost over 25 s under load: profile each and cut the slowest step
## Interpretation
Reading 1: wall time of the doctor and cost commands themselves is dominated by one or two hot steps that can be made cheaper without dropping checks (chosen). Reading 2: the slowness is only machine load and nothing in the code is worth changing; ruled out because the hot steps scale with ledger/repo size and are paid on every landing.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo doctor and sampo cost each name their slowest step and run under half their 2026-11-06 times on the same load (60 s and 25 s), measured before and after — verify with `python3 plugin/tests/run.py test_doctor test_cost`
## Non-goals
## Approach (options → choice → why)
1) cache the slow step by an input key (mtime/HEAD), reusing existing caches; likely outcome: big cut on repeat runs; fails if: the key misses an input and serves stale results. 2) run independent checks concurrently; likely outcome: wall time drops toward the slowest single check; fails if: checks share state or the machine is CPU-bound anyway. 3) make the hot step itself cheaper (fewer subprocesses, read less); likely outcome: a cut on every run, cold or warm; fails if: the cost is irreducible I/O. 4) do less: nothing, accept load-driven times; fails because every merge train pays it. Choice 3 then 1 (85%): profile first and take the smallest correct change at the measured hot spot; a measured hot spot is nearly always cuttable.
## Risks and rollback
## Execution prompt
## Steps
1. [x] profile both, cut the slowest step, measure
## Resume here
## Docs impact
docs/map/files-lib-1.md: the doctor cache's hashed key and content code stamp, and cost's single read (T-3521); no user-facing doc changes (same output, faster).
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_doctor.ScanCache` → ✗ exit 1 · Ran 10 tests in 22.3s (1 jobs, 16 at a time; slowest: ScanCache 0s) / FAILED (1 classes: test_doctor.ScanCache) [ran] [tree e03343ca60a9] [world 2f1906870a] (2026-11-06T19:18:31Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cost.OneRead` → ✗ exit 1 · Ran 1 tests in 47.1s (1 jobs, 16 at a time; slowest: OneRead 1s) / FAILED (1 classes: test_cost.OneRead) [ran] [tree d822a7278cfc] [world 2f1906870a] (2026-11-06T19:24:31Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cost.LinePrefilter` → ✗ exit 1 · Ran 1 tests in 4.9s (1 jobs, 16 at a time; slowest: LinePrefilter 0s) / FAILED (1 classes: test_cost.LinePrefilter) [ran] [tree c4660adc427a] [world 2f1906870a] (2026-11-06T19:36:33Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_doctor.ScanCache` → ✗ exit 1 · Ran 12 tests in 43.8s (1 jobs, 16 at a time; slowest: ScanCache 0s) / FAILED (1 classes: test_doctor.ScanCache) [ran] [tree 5a2df9cefad5] [world 2f1906870a] (2026-11-06T19:41:30Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_doctor test_cost test_perf_cost` → ✗ exit 1 · Ran 163 tests in 33.9s (70 jobs, 16 at a time; slowest: ViewsRepair 6s, StepCompact 4s, LockProbe 4s) / FAILED (2 classes: test_doctor.Checks, test_docs.MapShards) [ran] [tree 1b43c566aae6] [world 2f1906870a] (2026-11-06T19:42:35Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_doctor test_cost test_perf_cost test_docs` → exit 0 · Ran 277 tests in 46.0s (97 jobs, 16 at a time; slowest: Fences 14s, ViewsRepair 6s, StepCompact 4s) / OK [ran] [tree d7a6d11d3cf7] [world 2f1906870a] (2026-11-06T19:44:51Z)
## Log
- 2026-11-06T19:11:50Z created
- 2026-11-06T19:12:36Z set tier=M
- 2026-11-06T19:12:37Z planned: it has criteria and steps
- 2026-11-06T19:12:42Z lane: ~/.claude/foreman.lanes/T-3521 on foreman/T-3521
- 2026-11-06T19:13:39Z focused
- 2026-11-06T19:13:40Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T19:39:14Z profile: doctor's slowest = model pins (19-46 s, 2 real model calls a run): doctor-cache.json passed its 64 KB read cap (usage burn's key named every transcript), so no cached check ever hit; cost's slowest = _entries (49 of 67 s profiled): transcripts parsed twice, timing held all entries (GC doubled the parse), api-request-blob lines (20% of bytes) parsed for nothing
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
## Measurements
sampo doctor wall, median of 3: 43.1 s (load 21-26) → 20.4 s (load 19-25; warm runs 20.3/20.4, the cold refill run 39.3); a later 3 at load 28-46: 99.3 (cache clobbered by an old-code doctor, fable probe timed out) / 30.7 / 28.3. Slowest step before: model pins 19-46 s, a cache miss every run. sampo cost wall, median of 3: 47.7 s (load 25-34) → 23.5 s (load 30-34). Slowest step before: _entries, 49 of 67 s profiled (two parses). Frozen 506 MB copy: 9.6-13.6 s → 5.4-6.2 s, output identical.
