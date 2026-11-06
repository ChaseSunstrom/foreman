---
id: T-1901
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/tests/helpers.py, plugin/tests/test_second.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T03:06:07Z
updated: 2026-10-29T03:21:41Z
base: 7b3d96def44eed9d58466e3d90bb5e4dc5344ad4
base_tree: 0d14d19ff4dc9542dd53fc043987c48dc12c1ffb
plan0_at: 2026-10-29T03:10:19Z
plan0_scope: [plugin/tests/helpers.py, plugin/tests/test_second.py, CHANGELOG.md]
verified: strong
---
# FIX: CI on main is red at 06e55c1 (tests)
## Raw request
> FIX: CI on main is red at 06e55c1 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/foreman/commit/06e55c153ef56ac6b09d981d120047a6dd7cf629
> CI-red: 06e55c153ef56ac6b09d981d120047a6dd7cf629
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A test's cleanup survives a child still writing into its folder — verify with `python3 plugin/tests/run.py test_second`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a writer thread races tearDown (Errno 39)
2. [x] ForemanTestCase.tearDown retries cleanup for up to 5 s
3. [x] CHANGELOG line
## Resume here
<!-- auto -->
- 2026-10-29T03:12:03Z steps 3/3 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/tests/helpers.py, plugin/tests/test_second.py
- touched since last checkpoint: plugin/tests/test_second.py, CHANGELOG.md, plugin/tests/helpers.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k child_still_writing test_second` → red as expected (exit 1) · Ran 17 tests in 2.0s (10 classes, 16 at a time; slowest: Session 2s, Debate 1s, LensSkills 1s) / FAILED (1 classes) [ran] [tree 5cd40a05d1c5] (2026-10-29T03:10:26Z)
- (step 2) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 17 tests in 2.1s (10 classes, 16 at a time; slowest: Session 2s, Cleanup 1s, LensSkills 1s) / OK [ran] [tree be0aaaad3d80] (2026-10-29T03:10:33Z)
- (step 3) `grep -c T-1901 CHANGELOG.md` → exit 0 · 1 [ran] [tree be0aaaad3d80] (2026-10-29T03:10:33Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 03:06 UTC; claude plugin test mods/foreman-ui → [ran] [tree be0aaaad3d80] (2026-10-29T03:14:33Z)
- (step 2) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 17 tests in 2.1s (10 classes, 16 at a time; slowest: Session 2s, Debate 1s, Cleanup 1s) / OK [ran] [tree 7369195c52bc] (2026-10-29T03:15:59Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 03:06 UTC; claude plugin test mods/foreman-ui → [ran] [tree 7369195c52bc] (2026-10-29T03:20:10Z)
- (ac 1) `python3 plugin/tests/run.py test_second` → exit 0 · Ran 17 tests in 2.0s (10 classes, 16 at a time; slowest: Session 2s, Debate 1s, LensSkills 1s) / OK [ran] [tree 7369195c52bc] (2026-10-29T03:20:29Z)
- (audit intent) `S: lenses only; the new test proven red 4/5 without the retry and green 8/8 under --load 16 with it; full gates exit 0, no flake` → CI's Errno 39 on Ubuntu 3.14 was a detached child writing into state/ during rmtree; the shared tearDown now retries the cleanup for 5 s scaled by busy_factor, then re-raises [tree 7369195c52bc] (2026-10-29T03:20:29Z)
- (audit edge) `S: lenses only; the new test proven red 4/5 without the retry and green 8/8 under --load 16 with it; full gates exit 0, no flake` → a child that never stops writing still fails the test after the window, as it should; the test's own writer stops once the folder is gone, so a cleanup that succeeds mid-write can't be undone by it [tree 7369195c52bc] (2026-10-29T03:20:29Z)
- (audit self) `S: lenses only; the new test proven red 4/5 without the retry and green 8/8 under --load 16 with it; full gates exit 0, no flake` → no findings [tree 7369195c52bc] (2026-10-29T03:20:29Z)
- `python3 plugin/tests/run.py test_second -k Cleanup` → exit 0 · Ran 19 tests in 2.7s (11 classes, 16 at a time; slowest: Session 2s, CleanupGate 1s, Debate 1s) / OK (start tree + this task's tests) [ran] [tree 7369195c52bc] (2026-10-29T03:21:05Z)
- `python3 plugin/tests/run.py test_second -k Cleanup` → exit 0 · Ran 19 tests in 2.0s (11 classes, 16 at a time; slowest: Session 2s, CleanupGate 1s, LensSkills 1s) / OK [ran] [tree 7369195c52bc] (2026-10-29T03:21:05Z)
- (audit intent) `S: lenses only; the new test proven red 4/5 without the retry and green 8/8 under --load 16 with it; full gates exit 0, no flake` → CI's Errno 39 on Ubuntu 3.14 was a detached child writing into state/ during rmtree; the shared tearDown now retries the cleanup for 5 s scaled by busy_factor, then re-raises [tree 7369195c52bc] (2026-10-29T03:21:13Z)
- (audit edge) `S: lenses only; the new test proven red 4/5 without the retry and green 8/8 under --load 16 with it; full gates exit 0, no flake` → a child that never stops writing still fails the test after the window, as it should; the test's own writer stops once the folder is gone, so a cleanup that succeeds mid-write can't be undone by it [tree 7369195c52bc] (2026-10-29T03:21:13Z)
- (audit self) `S: lenses only; the new test proven red 4/5 without the retry and green 8/8 under --load 16 with it; full gates exit 0, no flake` → no findings [tree 7369195c52bc] (2026-10-29T03:21:13Z)
## Log
- 2026-10-29T03:06:07Z created
- 2026-10-29T03:10:14Z set type=FIX, tier=S, scope=['plugin/tests/helpers.py', 'plugin/tests/test_second.py', 'CHANGELOG.md'], priority=urgent
- 2026-10-29T03:10:14Z planned: it has criteria and steps
- 2026-10-29T03:10:18Z focused
- 2026-10-29T03:21:39Z done
- 2026-10-29T03:21:41Z committed ed4ec490 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1842 [FIX S, done, 2 steps] FIX: CI tests time out: split the suite into 2 shards per job
- T-1816 [FIX M, dropped, 0 steps] FIX: CI on main is red at eba6705 (tests)
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- decision 2026-10-23: T-1259: build the compaction storm and the window sweep, tested with the bench's fakes; the measured sweep (real Haiku sessions) waits until weekly …
- similar finished tasks took 2–4 steps
- start here (files T-1842 touched): plugin/tests/test_run.py, plugin/tests/run.py, .github/workflows/test.yml, CHANGELOG.md
## Regression test
test_second.Cleanup.test_a_child_still_writing_into_state_does_not_fail_the_cleanup; the code under change is plugin/tests/helpers.py (ForemanTestCase.tearDown), so fm task prove copies it to the start tree. Red without the retry: 4 of 5 runs FAILED (Errno 39) in a scratch worktree at 7b3d96de; green with it: 8 of 8 under --load 16, and the full suite.
## Lessons
- A test of a race must model the other side faithfully: a writer that re-creates the tree it writes into makes any cleanup look leaky, so the first version of this test was itself flaky
## Files touched
- plugin/tests/test_second.py
- CHANGELOG.md
- plugin/tests/helpers.py
