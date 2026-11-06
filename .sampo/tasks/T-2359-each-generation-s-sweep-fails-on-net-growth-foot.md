---
id: T-2359
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/lib/fmcost.py]
depends_on: [T-2358]
source: user
created: 2026-10-31T14:01:03Z
updated: 2026-10-31T15:12:23Z
base: dc773f27a1c761186a0d94bb2f72be5b51777987
base_tree: 327edb624a3eda8b406e974a0bc10b5bbda51d4f
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T15:00:44Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/lib/fmcost.py]
verified: strong
---
# Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12)
## Raw request
> Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12)
## Interpretation
Gap map #12 'lean ratchet per generation' and 'add/remove balance gate'. gen-0 §6: each generation removes, merges or slims at least as much as it adds, and hook p95, rules size and injected context may not grow. Nothing records a generation's start or compares its end.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis put of a generation's seed records its footprint and verb count; fm genesis sweep fails that generation when any metric ends above its start (no band on any metric; hook p95 is the median of three bench_hooks runs to damp timing noise), naming each; equal or lower passes; a generation whose seed was put before this record existed (gen 1) is measured from the tree at the commit its seed was filed in — verify with `python3 plugin/tests/run.py test_genesis`
- [x] The sweep lists what the generation removed, merged or slimmed against what it added (verbs, always-on chars, hook ms) — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) fm genesis put of a generation's seed records the footprint metrics and the verb count (fm burden --by-verb); fm genesis sweep fails the generation when any metric ends above its start, naming each, and lists what the generation removed, merged or slimmed against what it added. 2) per-ship only - rejected: a generation can creep under every 2% step. 3) count lines of code - rejected: gen-0 names context, latency and verbs, not lines. Choice 1.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_genesis.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py; past FIXes T-1127, T-2083, T-2084, T-2100, T-2101.
## Execution prompt
## Steps
1. [x] red tests: start record; growth fails; equal passes; the added/removed list
2. [x] the record at seed put and the sweep row
3. [x] docs: MASTER genesis line, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis -k heavier_than -k no_start_record` → exit 0 · Ran 2 tests in 3.5s (1 classes, 16 at a time; slowest: GenesisSweep 3s) / OK [ran] [tree 3c462e1e9cd3] (2026-10-31T15:05:13Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_doctor` → exit 0 · Ran 260 tests in 20.6s (47 classes, 16 at a time; slowest: GenesisRead 20s, GenesisCheck 17s, GenesisLive 15s) / OK [ran] [tree 3c462e1e9cd3] (2026-10-31T15:05:35Z)
- (step 3) `grep -q 'T-2359' MASTER.md && grep -q 'T-2359' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 64b4ac0fd317] (2026-10-31T15:05:56Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_doctor` → exit 0 · Ran 261 tests in 16.9s (47 classes, 16 at a time; slowest: GenesisRead 16s, GenesisCheck 13s, GenesisSweep 13s) / OK [ran] [tree 83f956bf8a2b] (2026-10-31T15:09:28Z)
- `python3 plugin/tests/run.py test_genesis -k heavier_than -k no_start_record -k median_of_three` → ✗ exit 1 · Ran 3 tests in 5.5s (1 classes, 16 at a time; slowest: GenesisSweep 3s) / FAILED (1 classes: test_genesis.GenesisSweep) (start tree + this task's tests) [ran] [tree 83f956bf8a2b] (2026-10-31T15:09:48Z)
- `python3 plugin/tests/run.py test_genesis -k heavier_than -k no_start_record -k median_of_three` → exit 0 · Ran 3 tests in 3.7s (1 classes, 16 at a time; slowest: GenesisSweep 3s) / OK [ran] [tree 83f956bf8a2b] (2026-10-31T15:09:48Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 168 tests in 32.9s (17 classes, 16 at a time; slowest: GenesisRead 32s, GenesisCheck 24s, GenesisSweep 20s) / OK [ran] [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 168 tests in 32.9s (17 classes, 16 at a time; slowest: GenesisRead 32s, GenesisCheck 24s, GenesisSweep 20s) / OK [ran] [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed, all fixed test-first: hook p95 is the median of three 60-run bench runs of the PreToolUse fixtures only (run_bench only=), CPU time when loaded, one decimal; judged only when the running fm is this tree's; the lean row can't crash the sweep (one red row); put's wiring is tested through put itself; removed/added listed as one line each so the 8-line clip never cuts them; a fallback with 0 verbs isn't growth; 261 tests OK` → a generation ending above its start on chars, verbs or hook p95 fails, no band, naming each; equal passes; gen 1 measured from its seed's commit (tested) [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed, all fixed test-first: hook p95 is the median of three 60-run bench runs of the PreToolUse fixtures only (run_bench only=), CPU time when loaded, one decimal; judged only when the running fm is this tree's; the lean row can't crash the sweep (one red row); put's wiring is tested through put itself; removed/added listed as one line each so the 8-line clip never cuts them; a fallback with 0 verbs isn't growth; 261 tests OK` → hook time isn't judged when the start had none or the running fm is another checkout, and the row says so; a measuring error is a red row, not a lost sweep [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed, all fixed test-first: hook p95 is the median of three 60-run bench runs of the PreToolUse fixtures only (run_bench only=), CPU time when loaded, one decimal; judged only when the running fm is this tree's; the lean row can't crash the sweep (one red row); put's wiring is tested through put itself; removed/added listed as one line each so the 8-line clip never cuts them; a fallback with 0 verbs isn't growth; 261 tests OK` → hook_p95 runs only the 2 guard fixtures x 60 x 3 (not 15 fixtures), and only at a seed put or a sweep [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed, all fixed test-first: hook p95 is the median of three 60-run bench runs of the PreToolUse fixtures only (run_bench only=), CPU time when loaded, one decimal; judged only when the running fm is this tree's; the lean row can't crash the sweep (one red row); put's wiring is tested through put itself; removed/added listed as one line each so the 8-line clip never cuts them; a fallback with 0 verbs isn't growth; 261 tests OK` → archive and tar come from git's own output into a temp dir; git runs with hooksPath=/dev/null and fsmonitor=false [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed, all fixed test-first: hook p95 is the median of three 60-run bench runs of the PreToolUse fixtures only (run_bench only=), CPU time when loaded, one decimal; judged only when the running fm is this tree's; the lean row can't crash the sweep (one red row); put's wiring is tested through put itself; removed/added listed as one line each so the 8-line clip never cuts them; a fallback with 0 verbs isn't growth; 261 tests OK` → the bench's only= filter keeps one timing path for doctor, ship and the sweep [tree 83f956bf8a2b] (2026-10-31T15:10:22Z)
## Log
- 2026-10-31T14:01:03Z created
- 2026-10-31T15:00:41Z focused
- 2026-10-31T15:00:44Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:04:19Z hypothesis: the lean row and hook_p95 (median of three bench runs) meet the revised criteria; test_genesis and test_doctor show it
- 2026-10-31T15:05:56Z scope: plugin/lib/fmgenesis.py, plugin/lib/fmdoctor.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T15:09:29Z scope: plugin/tests/bench_hooks.py (run_bench only= filter)
- 2026-10-31T15:12:20Z done
- 2026-10-31T15:12:23Z committed 1f2bb1dc (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2358 [FEATURE M, planned, 3 steps] The lean ratchet measures what gen-0 names: hook p95 and injected context, and only a cut pays for growth (Mission 8, #12)
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-2281 [FEATURE M, done, 3 steps] Lean ratchet (Mission 8/#12): each ship records the always-on footprint (rules chars, descriptions chars, SKILL bodies, hook p50) and f…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cost.py, plugin/tests/test_genesis.py
## Lessons
- A no-band ratchet needs a low-noise measure first; the max of 20 samples isn't a p95
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/bench_hooks.py
