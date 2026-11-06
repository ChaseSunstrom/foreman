---
id: T-1219
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:32:58Z
updated: 2026-10-16T15:35:29Z
base: 33ea5f472496f95fed462cc1724096cff14ac13d
base_tree: 263236ccc4c2dc10b4cc8734bd5c8a35b7ae0a34
plan0_at: 2026-10-16T15:32:59Z
plan0_scope: []
verified: ok
---
# Doctor's busy check sees a sudden CPU burst, so hook latency isn't failed under load
## Raw request
> Doctor's busy check sees a sudden CPU burst, so hook latency isn't failed under load
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] busy() reports a machine whose CPU pressure (/proc/pressure/cpu some avg10) is 10% or more as busy, and doctor checks again after the bench, so a burst that starts during it turns the latency FAIL into a not-measured WARN; the release-check test passes while 16 CPU burners run — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing unit tests for busy() with a PSI file and for the after-bench recheck
2. [x] busy() reads CPU pressure first; doctor rechecks after the bench
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_cpu_pressure_counts_as_busy_before_the_load_average_catches_up` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Checks 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 91452c0d9196] (2026-10-16T15:33:18Z)
- `python3 plugin/tests/run.py -k test_cpu_pressure_counts_as_busy_before_the_load_average_catches_up` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 91452c0d9196] (2026-10-16T15:33:18Z)
- (step 1) `python3 plugin/tests/run.py -k test_cpu_pressure_counts_as_busy_before_the_load_average_catches_up` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 77844eb52470] (2026-10-16T15:34:01Z)
- (step 2) `bash scratchpad/underload.sh: 16 CPU burners, then the release-check test` → before the fix: FAIL hook latency (UserPromptSubmit p95 241 ms > 150, PreToolUse:Bash:script 462 > 300) with load 13.8 on 16 cores; after: OK [tree 77844eb52470] (2026-10-16T15:34:01Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 51 tests in 31.9s (18 classes, 16 at a time; slowest: Command 32s, ViewsRepair 26s, Fix 1s) / OK [ran] [tree 77844eb52470] (2026-10-16T15:34:34Z)
- (audit self) `self: reproduced the release gate's flake under 16 CPU burners (doctor's hook latency FAIL while the 1-minute load read 13.8 on 16 cores); PSI avg10 catches it in seconds; the after-bench recheck covers a burst that starts mid-bench; without PSI (macOS) the load average decides as before; real slow hooks on an idle machine still FAIL` → no findings [tree 77844eb52470] (2026-10-16T15:34:34Z)
## Log
- 2026-10-16T15:32:58Z created
- 2026-10-16T15:32:59Z focused
- 2026-10-16T15:34:02Z scope: CHANGELOG line
- 2026-10-16T15:35:28Z done
- 2026-10-16T15:35:29Z committed 9cb94f42 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0805 [FIX S, done, 2 steps] The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate — lesson: a latency gate on a shared mac…
- T-0367 [PERFORMANCE S, done, 1 steps] fm doctor doesn't time hooks on a busy machine: one bench run for exit codes, latency reported as not measured — lesson: A latency …
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-04: Drop T-0305 (edit a criterion in place)
- similar finished tasks took 1–3 steps
- start here (files T-0805 touched): plugin/tests/test_bench_hooks.py, plugin/tests/bench_hooks.py
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
