---
id: T-0367
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-08T23:40:40Z
updated: 2026-10-08T23:52:53Z
base: c7228f0b12d6b9da6b5ed15870ecddcd23df5c92
base_tree: 1201c5f81088d833d43618e494c5ace8a0993404
verified: ok
---
# fm doctor doesn't time hooks on a busy machine: one bench run for exit codes, latency reported as not measured
## Raw request
> fm doctor's hook bench (_bench_and_injection) takes ~21 s (136 hook runs) on a loaded machine (JARVIS, load 35), tripping the doctor test's 30 s limit: fewer runs when load is high, or a time budget
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with load above the core count, hook latency is WARN 'not measured' and the bench runs once — verify with `python3 plugin/tests/run.py -k test_a_busy_machine_skips_hook_timing`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: busy → one run, latency WARN
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k test_a_busy_machine_skips_hook_timing` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 87198d7b76de] (2026-10-08T23:52:53Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_busy_machine_skips_hook_timing` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 87198d7b76de] (2026-10-08T23:52:53Z)
- (audit self) `self: busy() falls back to None where getloadavg is missing; exit codes still checked with one run; only the latency verdict changes` → no findings [tree 87198d7b76de] (2026-10-08T23:52:53Z)
## Log
- 2026-10-08T23:40:40Z created
- 2026-10-08T23:51:27Z planned from capture
- 2026-10-08T23:51:28Z focused
- 2026-10-08T23:52:53Z done
- 2026-10-08T23:52:53Z committed 4767a9b (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0224-review-2: HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit. [stale: plugin/lib/fmevolve.py, plugin/lib/fmguard.…
- playbook Benchmark Optimization Loop (skills/playbooks/references/perf/benchmark-loop.md)
- research T-0295-review-1: MEDIUM — `~/.claude/foreman/MASTER.md:10`.** It says "the bench judge and soak ... run through `fmideas.run_child`". Nothing in `plug…
- decision 2026-09-26: bench_hooks added as a 4th fm check gate (it exits 1 over budget); --runs 20 keeps fm check ~2 min
- likely tests for the scope: plugin/tests/test_doctor.py
## Measurements
fm doctor --json on JARVIS (load 27.5 on 8 cores, clean HOME): 16.6 s before → 11.1 s after; hook latency: false FAIL risk under load → WARN 'not measured'. Local idle machine unchanged (5 runs).
## Lessons
- A latency check on a shared machine measures the machine: gate it on load, keep the correctness half
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
