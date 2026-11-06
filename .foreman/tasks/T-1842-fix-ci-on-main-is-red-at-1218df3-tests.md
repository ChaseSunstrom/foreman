---
id: T-1842
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py, .github/workflows/test.yml, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-28T16:33:25Z
updated: 2026-10-28T16:53:32Z
base: 15586b5f6e1f27582083e918e8cc66ce7bc370c5
base_tree: ba2226f2e0a608ae743eb3f4752ddc6c30f2b528
plan0_at: 2026-10-28T16:48:08Z
plan0_scope: []
verified: strong
---
# FIX: CI tests time out: split the suite into 2 shards per job
## Raw request
> FIX: CI on main is red at 1218df3 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/foreman/commit/1218df33a87ffe1f53b44061c960048557b97154
> CI-red: 1218df33a87ffe1f53b44061c960048557b97154
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py --shard K/N runs a disjoint 1/N of the classes and the shards cover all; the CI matrix runs 2 shards — verify with `python3 plugin/tests/run.py -k test_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: --shard parse + disjoint cover
2. [x] run.py --shard and test.yml shard matrix
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_run.Args` → ✗ exit 1 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Args 0s) / FAILED (1 classes) [ran] [tree 48fde86904ac] (2026-10-28T16:48:33Z)
- (step 1) `python3 plugin/tests/run.py -k test_run` → exit 0 · Ran 50 tests in 4.6s (29 classes, 16 at a time; slowest: Hang 4s, Bench 3s, TimeoutWithoutProc 2s) / OK [ran] [tree 0e09a8817f76] (2026-10-28T16:49:19Z)
- (step 2) `python3 plugin/tests/run.py --shard 2/2 -k test_run -k test_ci_annotations` → exit 0 · Ran 24 tests in 2.6s (15 classes, 16 at a time; slowest: Bench 2s, TimeoutWithoutProc 2s, Repeats 2s) / OK [ran] [tree 0e09a8817f76] (2026-10-28T16:49:34Z)
- `python3 plugin/tests/run.py -k test_run.Args` → exit 0 · Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: Args 0s) / OK (start tree + this task's tests) [ran] [tree 376bfc759b8e] (2026-10-28T16:49:49Z)
- `python3 plugin/tests/run.py -k test_run.Args` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Args 0s) / OK [ran] [tree 376bfc759b8e] (2026-10-28T16:49:49Z)
- (ac 1) `python3 plugin/tests/run.py -k test_run` → exit 0 · Ran 50 tests in 4.5s (29 classes, 16 at a time; slowest: Hang 4s, Bench 3s, Timeout 2s) / OK [ran] [tree 376bfc759b8e] (2026-10-28T16:53:25Z)
- (audit intent) `self: read the diff; matrix.shard is static workflow data, no untrusted input reaches run:, no new permissions or secrets` → each CI job runs half the classes (round-robin over biggest-first), so the job that hit 1380 s at 92-100% gets about half [tree 376bfc759b8e] (2026-10-28T16:53:25Z)
- (audit adversary) `self: read the diff; matrix.shard is static workflow data, no untrusted input reaches run:, no new permissions or secrets` → no expression takes event or PR data; includes add to original combos only, so macOS gets exactly 2 jobs [tree 376bfc759b8e] (2026-10-28T16:53:25Z)
- (audit edge) `self: read the diff; matrix.shard is static workflow data, no untrusted input reaches run:, no new permissions or secrets` → bad K/N (0/2, 3/2, 1/0, a/b, 2) errors; a shard left empty by -k exits 1 'NO TESTS RAN'; class order is deterministic (sorted discover + stable sort), so shards never overlap [tree 376bfc759b8e] (2026-10-28T16:53:25Z)
- (audit operator) `self: read the diff; matrix.shard is static workflow data, no untrusted input reaches run:, no new permissions or secrets` → CI job names gain the shard number; no code reads job names [tree 376bfc759b8e] (2026-10-28T16:53:25Z)
- (audit self) `self: read the diff; matrix.shard is static workflow data, no untrusted input reaches run:, no new permissions or secrets` → no findings [tree 376bfc759b8e] (2026-10-28T16:53:25Z)
## Log
- 2026-10-28T16:33:25Z created
- 2026-10-28T16:48:07Z planned from capture
- 2026-10-28T16:48:08Z focused
- 2026-10-28T16:48:12Z set scope=['plugin/tests/run.py', 'plugin/tests/test_run.py', '.github/workflows/test.yml', 'CHANGELOG.md']
- 2026-10-28T16:53:31Z done
- 2026-10-28T16:53:32Z committed efe0e552 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1816 [FIX M, dropped, 0 steps] FIX: CI on main is red at eba6705 (tests)
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- decision 2026-10-23: Pause the feature backlog (112 FEATURE items: 77 M, 34 S, 1 L) until weekly usage is back on pace; every FIX, SECURITY, PERFORMANCE and CLEAN item i…
- similar finished tasks took 1–4 steps
## Regression test
test_run.Args.test_shards_split_the_classes_disjointly_and_cover_them_all: red on the start tree (step 1 evidence, exit 1, before run.py changed), green now. fm task prove can't show it: run.py lives in plugin/tests, so prove copies it onto the start tree too (T-1845).
## Plan gaps
- failed first: step 1 test: --shard parse + disjoint cover
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- .github/workflows/test.yml
- CHANGELOG.md
