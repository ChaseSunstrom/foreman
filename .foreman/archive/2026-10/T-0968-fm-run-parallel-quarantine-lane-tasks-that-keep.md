---
id: T-0968
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-15T21:56:47Z
updated: 2026-10-15T22:57:54Z
base: afd361943d016d6fb82bbfdcf5adf2eb5471624f
base_tree: 6f6a9156c095b6a32262572090558dd1d6903bf4
verified: strong
---
# Fm run --parallel: quarantine lane tasks that keep ending unfinished (block them when the
## Raw request
> fm run --parallel: quarantine lane tasks that keep ending unfinished (block them when the FAILS_MAX breaker trips, as the single-session path does), with a lane-stub test
## Interpretation
fm run --parallel: a lane session that ends with no progress (its lane has no work) frees the task, and the next run picks it again forever. The single-session path blocks a no-progress task (T-0955); lanes should too.
## Assumptions (confidence)
## Acceptance criteria
- [x] Two lane tasks whose sessions make no progress are blocked with 'no progress in its lane' and the next fm run --parallel has nothing runnable; a lane with work is kept, not blocked — verify with `python3 plugin/tests/run.py -k test_a_lane_with_no_progress_is_blocked`
## Non-goals
## Approach (options → choice → why)
Options: when a lane ends unfinished with an empty lane (no progress) and not on a usage limit, block the task through fm task block with the reason, and keep going (chosen: same rule as the single-session path, one place); block only when the breaker trips (a batch of two never trips it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in Parallel
2. [x] Block no-progress lane tasks in cmd_run
## Resume here
## Docs impact
none: fm run behaviour already documented as quarantining no-progress tasks
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_lane_with_no_progress_is_blocked` → ✗ exit 1 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: Parallel 2s) / FAILED (1 classes) [ran] [tree 8ab32cc97943] (2026-10-15T22:55:51Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_lane_with_no_progress_is_blocked` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: Parallel 2s) / OK [ran] [tree dacbdf4a1b2a] (2026-10-15T22:57:22Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_lane_with_no_progress_is_blocked` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: Parallel 2s) / OK [ran] [tree dacbdf4a1b2a] (2026-10-15T22:57:52Z)
- (step 2) `python3 plugin/tests/run.py test_parallel test_serve` → exit 0 · Ran 40 tests in 27.3s (7 classes, 16 at a time; slowest: Parallel 27s, Run 15s, Serve 3s) / OK [ran] [tree dacbdf4a1b2a] (2026-10-15T22:57:52Z)
- (audit self) `self: red then green; the parallel and serve suites pass` → an empty lane after an unfinished session blocks the task through fm task block, as a single no-progress session does; a lane with work is kept, a usage limit isn't a failure [tree dacbdf4a1b2a] (2026-10-15T22:57:52Z)
## Log
- 2026-10-15T21:56:47Z created
- 2026-10-15T22:55:38Z focused
- 2026-10-15T22:57:53Z done
- 2026-10-15T22:57:54Z committed 9d73e16 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0955 [FEATURE M, done, 3 steps] fm run and night: quarantine a no-progress task across runs, keep the machine awake, print a timer line — lesson: A side door that sets…
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- T-0709 [FEATURE M, done, 4 steps] Frontier 09 — Orchestrators of orchestrators — lesson: Partitioning by graph needs the test-to-source links first: without them tests d…
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
## Plan gaps
- failed first: step 1 Failing test in Parallel
## Files touched
- plugin/tests/test_parallel.py
- plugin/lib/fmserve.py
