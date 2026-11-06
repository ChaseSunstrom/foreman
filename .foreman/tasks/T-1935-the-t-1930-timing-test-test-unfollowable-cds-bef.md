---
id: T-1935
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T08:02:51Z
updated: 2026-10-29T08:08:26Z
base: 6237a09344bd6a03646d89381844e05a51e0fbef
base_tree: fc2761ef26c66162cd5197e596a8b588c4423fdb
plan0_at: 2026-10-29T08:04:38Z
plan0_scope: []
verified: strong
---
# The T-1930 timing test (test_unfollowable_cds_before_substitutions…, < 2 s wall) fails und
## Raw request
> FIX: the T-1930 timing test (test_unfollowable_cds_before_substitutions…, < 2 s wall) fails under CPU contention from ambient test runs; measure CPU time (time.process_time) as the guard's own budget does
## Interpretation
The 2 s wall-clock limit in the T-1930 test trips when other test runs share the CPU; the regression it guards (thousands of stats) is CPU time, so measure that.
## Assumptions (confidence)
## Acceptance criteria
- [x] the T-1930 timing test passes with 16 CPU burners running — verify with `python3 plugin/tests/run.py -k test_unfollowable_cds_before --load 16 test_guard`
## Non-goals
## Approach (options → choice → why)
time.process_time over time.monotonic (chosen: precedent at test_guard_exec_vectors.py:337, counts stat syscalls as system time); a looser wall limit (loses the regression signal); retry on failure (hides it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Measure CPU time (time.process_time) instead of wall time, as test_guard_exec_vectors.py:337 does
## Resume here
<!-- auto -->
- 2026-10-29T08:05:36Z steps 1/1 done
- git: foreman/build; 1 uncommitted: plugin/tests/test_guard.py
- touched since last checkpoint: plugin/tests/test_guard.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_unfollowable_cds_before --load 16 test_guard` → exit 0 · Ran 299 tests in 24.8s (88 classes, 16 at a time; slowest: Mutation 24s, GuardAgainstBash 19s, Trust 11s) / OK [ran] [tree e835d5b0c7d9] (2026-10-29T08:05:36Z)
- `python3 plugin/tests/run.py -k test_unfollowable_cds_before --load 16 test_guard` → exit 0 · Ran 299 tests in 22.6s (88 classes, 16 at a time; slowest: Mutation 22s, GuardAgainstBash 17s, Trust 10s) / OK (start tree + this task's tests) [ran] [tree e835d5b0c7d9] (2026-10-29T08:07:44Z)
- `python3 plugin/tests/run.py -k test_unfollowable_cds_before --load 16 test_guard` → exit 0 · Ran 299 tests in 22.2s (88 classes, 16 at a time; slowest: Mutation 22s, GuardAgainstBash 17s, Trust 10s) / OK [ran] [tree e835d5b0c7d9] (2026-10-29T08:07:44Z)
- (ac 1) `python3 plugin/tests/run.py -k test_unfollowable_cds_before --load 16 test_guard` → exit 0 · Ran 299 tests in 23.2s (88 classes, 16 at a time; slowest: Mutation 23s, GuardAgainstBash 18s, Trust 11s) / OK [ran] [tree e835d5b0c7d9] (2026-10-29T08:08:14Z)
- (audit edge) `Timing test now measures the guard process's CPU time, as the exec-vectors timing test does; red at 2.4 s wall with 16 burners before, green under the same load after` → a pathological guard still spends CPU, so a slow-path regression still fails the 2 s bound [tree e835d5b0c7d9] (2026-10-29T08:08:14Z)
- (audit adversary) `Timing test now measures the guard process's CPU time, as the exec-vectors timing test does; red at 2.4 s wall with 16 burners before, green under the same load after` → test-only change; the guard is untouched [tree e835d5b0c7d9] (2026-10-29T08:08:14Z)
- (audit self) `Timing test now measures the guard process's CPU time, as the exec-vectors timing test does; red at 2.4 s wall with 16 burners before, green under the same load after` → no findings [tree e835d5b0c7d9] (2026-10-29T08:08:14Z)
## Log
- 2026-10-29T08:02:51Z created
- 2026-10-29T08:04:31Z set tier=S
- 2026-10-29T08:04:31Z planned: it has criteria and steps
- 2026-10-29T08:04:37Z focused
- 2026-10-29T08:08:24Z done
- 2026-10-29T08:08:26Z committed e03ea2bb (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0805 [FIX S, done, 2 steps] The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate — lesson: a latency gate on a shared mac…
- research T-1930-review: Approve. I could not break either claim. I read the code only and ran nothing, because this session has no Bash tool. [stale: plugin/tests/test_g…
- T-1730 [FIX M, done, 3 steps] Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil… — lesson: Judge an…
- decision 2026-10-15: T-0970 dropped as a duplicate of T-0705's ambient runner; ambient tests switched on in this repo; stays opt-in by default (CPU on the user's machine…
## Regression test
none: the change is the test itself; the failure was load-dependent (red at 2.4 s wall under 16 burners once, recorded in the brief's log), so prove can't replay it deterministically
## Lessons
- Timing bounds in tests measure process_time, never wall time: parallel suites share the box
## Files touched
- plugin/tests/test_guard.py
