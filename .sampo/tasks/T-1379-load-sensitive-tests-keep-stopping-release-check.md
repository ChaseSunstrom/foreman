---
id: T-1379
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T15:35:10Z
updated: 2026-10-21T20:49:50Z
base: 6a305bcc6937fcc428f6e78fdd022f32721cec16
base_tree: 7b580e3a8c475c4212f75dbad83077a3f1a384a3
plan0_at: 2026-10-21T20:40:48Z
plan0_scope: []
verified: ok
---
# test_breaker's pause test and test_scout's dry-run test pass at any machine load
## Raw request
> Load-sensitive tests keep stopping release checks: test_breaker.Breaker.test_three_failures_pause_an_event_visibly_and_a_success_resets_it and test_scout.Scout.test_fm_scout_dry_runs_from_the_cli failed in release 1.2.48's check at load ~40 (both pass alone; each now failed twice). Find the timing each depends on and make it load-proof, as T-1378 does for the multi-request hook test
## Interpretation
Both failed in release 1.2.48's check at load ~40 and pass alone; 4 more runs at load 17-30 passed, and the check kept no failure output. Reproduce under a set load, find the timing each relies on, remove it.
## Assumptions (confidence)
## Acceptance criteria
- [x] with one busy process per core running, test_breaker and test_scout pass 5 runs in a row — verify with `python3 plugin/tests/run.py test_breaker test_scout`
- [x] with one busy process per core, test_doctor and test_resilience also pass 5 runs in a row — verify with `python3 plugin/tests/run.py test_doctor test_resilience`
## Non-goals
## Approach (options → choice → why)
Options: (A) FOREMAN_DOCTOR_BENCH=0 skips doctor's hook bench, reporting its three checks as WARN 'not measured (FOREMAN_DOCTOR_BENCH=0)'; the test helpers' base environment sets it, so every fm doctor a test starts (directly or through fm scout) skips a benchmark no test asserts on; bench-specific tests call the check functions directly (chosen: removes the load-scaled work instead of waiting longer for it); (B) raise the helpers' 30 s limit (hides it; flakes again at more load); (C) skip under load (loses coverage). One test pins that the switch skips the bench and names it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce each under CPU burners; read the failing assertion
2. [x] Replace the timing it relies on with a wait on the condition; 5 runs under load
3. [x] fmdoctor.run_all honours FOREMAN_DOCTOR_BENCH=0; helpers.py's base env sets it; a test pins the WARN text; then 5 runs of test_breaker test_scout test_doctor test_resilience under 16 busy processes
## Resume here
## Docs impact
CHANGELOG line; the variable is a test seam, named in the WARN it causes
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_doctor.Command.test_the_tests_skip_the_hook_bench_and_doctor_says_so` → ✗ exit 1 · Ran 1 tests in 27.8s (1 classes, 16 at a time; slowest: Command 27s) / FAILED (1 classes) [ran] [tree 78645f34570a] (2026-10-21T20:42:05Z)
- (step 3) `python3 plugin/tests/run.py test_doctor test_resilience test_breaker test_scout` → exit 0 · Ran 77 tests in 35.8s (25 classes, 16 at a time; slowest: Scout 35s, Mutation 22s, Breaker 12s) / OK [ran] [tree 32e132c14eca] (2026-10-21T20:43:15Z)
- (step 1) `python3 -m cProfile plugin/bin/fm doctor at load 44; test_doctor and test_resilience under load ~60 (this session)` → fm doctor took 18 s, 13 s of it _bench_and_injection (~100 hook subprocesses); test_doctor.Command and test_resilience.ViewsRepair failed with subprocess.TimeoutExpired at the helpers' 30 s limit; test_breaker's pause test runs fm doctor and test_scout's dry run runs fm scout --dry, whose probe_doctor runs fm doctor --json — the same wait [tree 32e132c14eca] (2026-10-21T20:46:30Z)
- (step 3) `sh /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/burn5.sh` → exit 0 · run 5: pass (load 66.72) / 5 of 5 passed [ran] [tree 13fd8974fe28] (2026-10-21T20:47:55Z)
- (step 2) `sh scratchpad/burn5.sh (16 CPU burners; test_breaker test_scout test_doctor test_resilience x5)` → 5 of 5 passed, load 66.7 at the last round; the timing the tests relied on (fm doctor's hook bench inside a 30 s limit) is gone rather than waited for [tree 009d2f12e9ff] (2026-10-21T20:48:19Z)
- (ac 1) `python3 plugin/tests/run.py test_breaker test_scout` → exit 0 · Ran 20 tests in 45.5s (4 classes, 16 at a time; slowest: Scout 45s, ScoutDrive 13s, Breaker 12s) / OK [ran] [tree 009d2f12e9ff] (2026-10-21T20:49:27Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor test_resilience` → exit 0 · Ran 58 tests in 15.7s (22 classes, 16 at a time; slowest: Mutation 15s, Command 9s, ViewsRepair 6s) / OK [ran] [tree 009d2f12e9ff] (2026-10-21T20:49:27Z)
- (audit intent) `self: 9 lines in fmdoctor.run_all — FOREMAN_DOCTOR_BENCH=0 raises a private _NoBench inside the existing try, reporting the three bench checks WARN 'not measured'; helpers' base env sets it; the bench-specific tests call check_hook_latency etc. directly and still run; a real fm doctor (no variable) is unchanged` → test_breaker, test_scout, test_doctor and test_resilience pass 5 rounds in a row under one busy process per core (load 67) [tree 009d2f12e9ff] (2026-10-21T20:49:27Z)
- (audit edge) `self: 9 lines in fmdoctor.run_all — FOREMAN_DOCTOR_BENCH=0 raises a private _NoBench inside the existing try, reporting the three bench checks WARN 'not measured'; helpers' base env sets it; the bench-specific tests call check_hook_latency etc. directly and still run; a real fm doctor (no variable) is unchanged` → the variable is honoured only as the exact string '0'; fm scout's probe_doctor inherits it through os.environ; a user's own fm doctor never sets it [tree 009d2f12e9ff] (2026-10-21T20:49:27Z)
## Log
- 2026-10-21T15:35:10Z created
- 2026-10-21T15:36:51Z planned from capture
- 2026-10-21T15:37:54Z grounded (read, not yet reproduced): test_breaker's bad() runs the hook with timeout=10 and test_scout's fm scout --dry goes through helpers.fm's timeout=30 while fmscout runs a nested fm subprocess (line ~120, its own 120 s); at load ~40 a python start plus Foreman's import can pass those budgets, so the likely failure is a harness TimeoutExpired, not a wrong result. Reproduction with CPU burners waits until release 1.2.48 is out (burners now would trip its check). Second plan skipped: the read names the suspects; the reproduction decides.
- 2026-10-21T15:37:59Z sharper: fm scout --dry runs probe_doctor, a nested fm doctor --json (hook latency benches and all), inside the test helper's 30 s; at load that alone can pass 30 s. Fix direction: the test gives the scout a doctor result (an env or a probe stub) or the dry run skips the heavy probe; breaker: its 10 s hook budget.
- 2026-10-21T20:21:50Z grounded 2026-10-21: the shared cause is fm doctor's hook benchmark (_bench_and_injection: ~100 hook subprocesses, 13 of doctor's 18 s at load 44, 36-62 s at load 60). test_breaker's pause test runs fm doctor; test_scout's dry run runs fm scout --dry, whose probe_doctor runs fm doctor --json; test_doctor.Command and test_resilience.ViewsRepair run fm doctor — all under the helpers' 30 s subprocess limit. None of them checks the bench.
- 2026-10-21T20:40:46Z focused
- 2026-10-21T20:46:52Z paused: focus moved to T-1409
- 2026-10-21T20:48:17Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T20:48:17Z focused
- 2026-10-21T20:49:44Z done
- 2026-10-21T20:49:50Z committed d29c6db7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1378 [FIX M, done, 3 steps] Queueing a multi-request prompt fits every request in the hook's time on a loaded machine: one pass, one view refresh — lesson: Profile bef…
- T-1201 [FIX S, done, 1 steps] test_parallel mid-batch test waits for the slow session's pid instead of racing it
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
- similar finished tasks took 1–3 steps
## Regression test
test_doctor.Command.test_the_tests_skip_the_hook_bench_and_doctor_says_so: red before (the bench ran, 27.8 s, the checks weren't WARN), green after; plus the 5-round load run
## Why not caught
no run of the suite under deliberate load before release checks; T-1379's reproduction now records it
## Lessons
- A load flake is often real work inside a fixed timeout: profile the slow call and remove work the test doesn't read before raising any limit
## Plan gaps
- failed first: step 3 fmdoctor.run_all honours FOREMAN_DOCTOR_BENCH=0; helpers.py's base env sets it; a test pins the WAR…
## Files touched
- plugin/tests/test_doctor.py
- plugin/tests/helpers.py
- plugin/lib/fmdoctor.py
