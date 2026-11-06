---
id: T-3131
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/selfgate.py, plugin/tests/bench_hooks.py, plugin/tests/test_selfgate.py, plugin/tests/fixtures/selfgate-aa/**, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-05T03:45:15Z
updated: 2026-11-05T04:17:25Z
base: afbd9bf8e7fb42bd0c50c8936f3b22af1d5eac84
base_tree: 58383cc6ea8a3ac455cca04a225c2cce27352316
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-05T03:45:38Z
plan0_scope: [plugin/lib/sampo/selfgate.py, plugin/tests/bench_hooks.py, plugin/tests/test_selfgate.py, plugin/tests/fixtures/selfgate-aa/**, CHANGELOG.md]
verified: strong
unproven: [docs]
---
# The self-change gate judges a hook's median CPU time and holds only a rise seen in every pair, so identical code no longer holds by chance
## Raw request
> The self-change gate judges a hook's median CPU time and holds only a rise seen in every pair, so identical code no longer holds by chance
## Interpretation
Reading 1 (chosen): measured 2026-11-05: an A/A bench (the same tree against itself, the gate's own order) shows a second/first CPU ratio of median 1.000 (no order bias) but single-pair 'rises' of up to +78%, because bench_hooks' p95 of 10 runs is the slowest run; with 16 hooks and 2 of 3 pairs needed, a chance hold is likely (10 holds in a day on diffs that touch none of the held hooks). Judge on the median CPU time (a new cpu_p50 from bench_hooks) and require the rise in every pair; the budget check needs every pair too. Reading 2: more pairs at the old statistic; rejected, each pair costs a full bench and the max of 10 stays noisy.
## Assumptions (confidence)
## Acceptance criteria
- [x] bench_hooks reports cpu_p50 per hook; the gate judges a rise on cpu_p50 when both sides have it, else as before — verify with `python3 plugin/tests/run.py test_selfgate`
- [x] a rise or an over-budget p95 holds only when it shows in every pair: a rise in one or two of three pairs passes, a real +30% median rise in all three holds — verify with `python3 plugin/tests/run.py test_selfgate`
- [x] the six A/A benches recorded 2026-11-05 (fixtures) judged by _paired hold nothing — verify with `python3 plugin/tests/run.py test_selfgate`
## Non-goals
## Approach (options → choice → why)
1) use what exists: bench_hooks already times each run's CPU (RUSAGE_CHILDREN) and the gate already has PAIRS and HOLD; add cpu_p50 beside cpu_p95, have _ms prefer it, set HOLD = PAIRS; likely outcome: chance holds vanish, a real median rise still holds every time. 2) do less: only set HOLD = PAIRS on today's p95; fails if: the max of 10 runs still swings +78% in one pair, so real holds need three wild draws while noise keeps one-pair failures common under load. 3) a per-hook significance test over raw samples; fails if: the bench exposes only summaries and the gate gets heavier. 4) normalise by the median ratio across hooks; fails if: a real slowdown of every hook (a heavy import in hooks.py) is divided away. Choice 1 (80%)
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1316, T-1378, T-1380, T-1404.
## Execution prompt
## Steps
1. [x] failing tests: cpu_p50 preferred, two of three passes, the A/A fixtures hold nothing, every-pair rise holds
2. [x] cpu_p50 in bench_hooks, _ms and HOLD in selfgate
## Resume here
## Docs impact
docs/map/files-lib-3.md fmselfgate entry: the median CPU basis and every-pair rule; CHANGELOG line.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · Ran 9 tests in 0.7s (4 classes, 16 at a time; slowest: LoadedWallCheck 0s, AaFixtures 0s, MedianCpu 0s) / FAILED (2 classes: test_selfgate.Interleaved, test_selfgate.MedianCpu) [ran] [tree 22bdbd3bf568] [world 2f1906870a] (2026-11-05T03:45:56Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 9 tests in 0.6s (4 classes, 16 at a time; slowest: MedianCpu 0s, AaFixtures 0s, Interleaved 0s) / OK [ran] [tree b29872e21256] [world 2f1906870a] (2026-11-05T03:46:18Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 9 tests in 0.8s (4 classes, 16 at a time; slowest: Interleaved 0s, MedianCpu 0s, AaFixtures 0s) / OK [ran] [tree 26aef57c7bd7] [world 2f1906870a] (2026-11-05T03:47:14Z)
- (ac 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 9 tests in 0.8s (4 classes, 16 at a time; slowest: AaFixtures 0s, Interleaved 0s, MedianCpu 0s) / OK [ran] [tree 26aef57c7bd7] [world 2f1906870a] (2026-11-05T03:47:16Z)
- (ac 3) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 9 tests in 0.9s (4 classes, 16 at a time; slowest: LoadedWallCheck 0s, Interleaved 0s, MedianCpu 0s) / OK [ran] [tree 26aef57c7bd7] [world 2f1906870a] (2026-11-05T03:47:18Z)
- `python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · Ran 9 tests in 2.8s (4 classes, 16 at a time; slowest: MedianCpu 0s, LoadedWallCheck 0s, AaFixtures 0s) / FAILED (2 classes: test_selfgate.Interleaved, test_selfgate.MedianCpu) (start tree + this task's tests) [ran] [tree 26aef57c7bd7] [world 2f1906870a] (2026-11-05T03:47:28Z)
- `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 9 tests in 0.7s (4 classes, 16 at a time; slowest: MedianCpu 0s, AaFixtures 0s, LoadedWallCheck 0s) / OK [ran] [tree 26aef57c7bd7] [world 2f1906870a] (2026-11-05T03:47:28Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 11 tests in 0.5s (4 classes, 16 at a time; slowest: MedianCpu 0s, Interleaved 0s, AaFixtures 0s) / OK [ran] [tree 6d824d2df7bd] [world 2f1906870a] (2026-11-05T03:51:58Z)
- (ac 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 11 tests in 0.5s (4 classes, 16 at a time; slowest: MedianCpu 0s, LoadedWallCheck 0s, AaFixtures 0s) / OK [ran] [tree 6d824d2df7bd] [world 2f1906870a] (2026-11-05T03:51:59Z)
- (ac 3) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 11 tests in 0.4s (4 classes, 16 at a time; slowest: MedianCpu 0s, Interleaved 0s, AaFixtures 0s) / OK [ran] [tree 6d824d2df7bd] [world 2f1906870a] (2026-11-05T03:52:00Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate test_bench_hooks test_lanes` → exit 0 · Ran 171 tests in 42.7s (20 classes, 16 at a time; slowest: Lanes 42s, LaneRecovery 30s, RaceEvidence 13s) / OK [ran] [tree 6d824d2df7bd] [world 2f1906870a] (2026-11-05T03:52:44Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 11 tests in 0.9s (4 classes, 16 at a time; slowest: MedianCpu 0s, AaFixtures 0s, Interleaved 0s) / OK [ran] [tree 14f63f2c42c3] [world 2f1906870a] (2026-11-05T03:53:18Z)
- (ac 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 11 tests in 0.9s (4 classes, 16 at a time; slowest: MedianCpu 0s, AaFixtures 0s, Interleaved 0s) / OK [ran] [tree 14f63f2c42c3] [world 2f1906870a] (2026-11-05T03:53:18Z)
- (ac 3) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 11 tests in 0.9s (4 classes, 16 at a time; slowest: MedianCpu 0s, AaFixtures 0s, Interleaved 0s) / OK [ran] [tree 14f63f2c42c3] [world 2f1906870a] (2026-11-05T03:53:18Z)
- (audit intent) `fm-reviewer (adversary + edge) on the first version: changes needed (no wall check on a quiet bench, tail-only slowdowns unseen, fixtures without cpu_p50); all three adopted with tests, the harness-import hole captured as T-3132; self re-check of the final diff` → identical trees benched in the gate's order (twice, at load 8 and at ~2 per core) hold nothing under the new rule; a real median rise in every pair still holds; ten recorded holds were on hooks their diffs never touched [tree 14f63f2c42c3] (2026-11-05T03:53:18Z)
- (audit adversary) `fm-reviewer (adversary + edge) on the first version: changes needed (no wall check on a quiet bench, tail-only slowdowns unseen, fixtures without cpu_p50); all three adopted with tests, the harness-import hole captured as T-3132; self re-check of the final diff` → a branch can't loosen its judge here: the gate runs the base's bench_hooks and replay copied into the branch tree (selfgate :222-226); a hook that sleeps or does I/O holds by its wall median on a quiet bench and by the wall doubling under load; a slowdown on a minority of calls holds by the tail bar; the remaining hole (branch fmguard imported in the bench process) is pre-existing and filed as T-3132 [tree 14f63f2c42c3] (2026-11-05T03:53:18Z)
- (audit edge) `fm-reviewer (adversary + edge) on the first version: changes needed (no wall check on a quiet bench, tail-only slowdowns unseen, fixtures without cpu_p50); all three adopted with tests, the harness-import hole captured as T-3132; self re-check of the final diff` → an old base bench without cpu_p50 against a new branch bench falls back to the p95 path (the first merge after this change); a missing base entry is judged by budget only; bool and missing keys guarded; HOLD = PAIRS lowers sensitivity near the threshold (a +20% rise seen in 80% of pairs holds about half the time), stated in the docs [tree 14f63f2c42c3] (2026-11-05T03:53:18Z)
- (audit intent) `fm-reviewer (adversary + edge) on the first version: changes needed (no wall check on a quiet bench, tail-only slowdowns unseen, fixtures without cpu_p50); all three adopted with tests, the harness-import hole captured as T-3132; self re-check of the final diff` → identical trees benched in the gate's order (twice, at load 8 and at ~2 per core) hold nothing under the new rule; a real median rise in every pair still holds; ten recorded holds were on hooks their diffs never touched [tree b4cda6269003] (2026-11-05T04:09:12Z)
- (audit adversary) `fm-reviewer (adversary + edge) on the first version: changes needed (no wall check on a quiet bench, tail-only slowdowns unseen, fixtures without cpu_p50); all three adopted with tests, the harness-import hole captured as T-3132; self re-check of the final diff` → a branch can't loosen its judge here: the gate runs the base's bench_hooks and replay copied into the branch tree (selfgate :222-226); a hook that sleeps or does I/O holds by its wall median on a quiet bench and by the wall doubling under load; a slowdown on a minority of calls holds by the tail bar; the remaining hole (branch fmguard imported in the bench process) is pre-existing and filed as T-3132 [tree b4cda6269003] (2026-11-05T04:09:12Z)
- (audit edge) `fm-reviewer (adversary + edge) on the first version: changes needed (no wall check on a quiet bench, tail-only slowdowns unseen, fixtures without cpu_p50); all three adopted with tests, the harness-import hole captured as T-3132; self re-check of the final diff` → an old base bench without cpu_p50 against a new branch bench falls back to the p95 path (the first merge after this change); a missing base entry is judged by budget only; bool and missing keys guarded; HOLD = PAIRS lowers sensitivity near the threshold (a +20% rise seen in 80% of pairs holds about half the time) [tree b4cda6269003] (2026-11-05T04:09:12Z)
## Log
- 2026-11-05T03:45:15Z created
- 2026-11-05T03:45:22Z set approved=True
- 2026-11-05T03:45:22Z set scope=['plugin/lib/sampo/selfgate.py', 'plugin/tests/bench_hooks.py', 'plugin/tests/test_selfgate.py', 'plugin/tests/fixtures/selfgate-aa/**', 'CHANGELOG.md']
- 2026-11-05T03:45:36Z focused
- 2026-11-05T03:45:38Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-05T03:47:12Z scope: docs/map/files-lib-3.md (the fmselfgate entry names the new rule)
- 2026-11-05T03:51:02Z review (fm-reviewer, adversary + edge) adopted: (1) a quiet bench now checks the wall median for a hook that waits (CPU time misses sleeps and I/O), median only, never the noisy p95; (2) a tail-only rise holds past +50% and 25 ms on p95 in every pair; (3) the A/A fixtures are re-recorded with cpu_p50 so the median path is what they test. Rejected for now: benching in a subprocess that doesn't import the branch's lib (pre-existing, affects p95 equally; captured)
- 2026-11-05T04:08:44Z scope: plugin/tests/test_code_tui.py: T-3055's live_theme default wasn't added to the settings test's known names, so the test failed on main and blocked this close; one entry added (T-3055's gap, fixed inline as it blocks)
- 2026-11-05T04:17:21Z done
- 2026-11-05T04:17:25Z committed 35f127cf (12 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- T-2798 [FIX M, done, 2 steps] fm doctor's hook SLO judges only PreToolUse runs taken at normal host load: each hook_ms event records load per CPU, and runs above LOAD_BA…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- decision 2026-11-05: builder order revised: T-3091 (the self-change gate's noise filter) goes first when a slot frees, before T-3113 and T-3101; 9 holds in a day on diff…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_selfgate.py
## Why not caught
the gate's tests used synthetic benches with fixed timings and never an A/A run of real benches, so the chance-hold rate of a p95-of-10 across 16 hooks was never measured; the A/A fixtures now pin it
## Lessons
- Before blaming load or order for a gate's false alarms, bench the old code against itself with the gate's own rule: the A/A run showed no order bias but a p95-of-10 that is the slowest run, and 16 hooks given three chances each make a chance hold likely; fix the statistic, keep the checks a reviewer can name.
## Plan gaps
- failed first: step 1 failing tests: cpu_p50 preferred, two of three passes, the A/A fixtures hold nothing, every-pair ri…
## Files touched
- plugin/tests/fixtures/selfgate-aa/1a.json
- plugin/tests/fixtures/selfgate-aa/1b.json
- plugin/tests/fixtures/selfgate-aa/2a.json
- plugin/tests/fixtures/selfgate-aa/2b.json
- plugin/tests/fixtures/selfgate-aa/3a.json
- plugin/tests/fixtures/selfgate-aa/3b.json
- plugin/tests/test_selfgate.py
- plugin/tests/bench_hooks.py
- plugin/lib/sampo/selfgate.py
- docs/map/files-lib-3.md
- CHANGELOG.md
- plugin/tests/test_code_tui.py
