---
id: T-2056
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsettingsserve.py, plugin/tests/test_settings_serve.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T21:29:49Z
updated: 2026-10-29T21:38:46Z
base: 16e394ce9fb41bb55ce78de306186408cf2eaf67
base_tree: 1bb9856a0f18169ab27dacb525bfc431d88e962a
plan0_at: 2026-10-29T21:36:49Z
plan0_scope: [plugin/lib/fmsettingsserve.py, plugin/tests/test_settings_serve.py, CHANGELOG.md]
verified: strong
---
# FIX: CI on main is red at 36f32f4 (tests)
## Raw request
> FIX: CI on main is red at 36f32f4 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/foreman/commit/36f32f4dd8ef0beb259086f4431bcf3883d26c92
> CI-red: 36f32f4dd8ef0beb259086f4431bcf3883d26c92
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] SIGTERM ends fm settings serve through its loop (prints stopped, exit 0), no exception thrown into running code — verify with `python3 plugin/tests/run.py test_settings_serve`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] stop flag instead of sys.exit in the SIGTERM handler; test asserts stopped
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_settings_serve` → ✗ exit 1 · Ran 16 tests in 9.8s (1 classes, 16 at a time; slowest: Serve 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bb70d2b6a009] (2026-10-29T21:37:22Z)
- `python3 plugin/tests/run.py test_settings_serve` → ✗ exit 1 · Ran 16 tests in 8.5s (1 classes, 16 at a time; slowest: Serve 8s) / FAILED (1 classes) [ran] [tree bb70d2b6a009] (2026-10-29T21:37:22Z)
- `python3 plugin/tests/run.py test_settings_serve` → ✗ exit 1 · Ran 16 tests in 9.3s (1 classes, 16 at a time; slowest: Serve 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 94fc960426ba] (2026-10-29T21:37:50Z)
- `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 9.5s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree 94fc960426ba] (2026-10-29T21:37:50Z)
- (step 1) `python3 plugin/tests/run.py test_settings_serve test_eco` → exit 0 · Ran 40 tests in 9.5s (11 classes, 16 at a time; slowest: Serve 9s, HarnessCanary 3s, Sweep 1s) / OK [ran] [tree 94fc960426ba] (2026-10-29T21:38:08Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 9.5s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree 94fc960426ba] (2026-10-29T21:38:27Z)
- (audit edge) `self: diff is 3 lines; the handler only sets an Event the loop already polls every 0.5 s, so no exception is thrown into select, thread start or locks; the swipe server (fmeco run caller) shares it; red→green proved (stopped now printed)` → SIGTERM during an in-flight request: handle_request finishes it, then the loop exits within 0.5 s; Ctrl-C still raises KeyboardInterrupt and is caught [tree 94fc960426ba] (2026-10-29T21:38:27Z)
- (audit self) `self: diff is 3 lines; the handler only sets an Event the loop already polls every 0.5 s, so no exception is thrown into select, thread start or locks; the swipe server (fmeco run caller) shares it; red→green proved (stopped now printed)` → no findings [tree 94fc960426ba] (2026-10-29T21:38:27Z)
## Log
- 2026-10-29T21:29:49Z created
- 2026-10-29T21:36:44Z set tier=S, scope=['plugin/lib/fmsettingsserve.py', 'plugin/tests/test_settings_serve.py', 'CHANGELOG.md']
- 2026-10-29T21:36:48Z planned: it has criteria and steps
- 2026-10-29T21:36:49Z focused
- 2026-10-29T21:38:44Z done
- 2026-10-29T21:38:46Z committed ee079813 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1842 [FIX S, done, 2 steps] FIX: CI tests time out: split the suite into 2 shards per job
- T-1901 [FIX S, done, 3 steps] FIX: CI on main is red at 06e55c1 (tests) — lesson: A test of a race must model the other side faithfully: a writer that re-creates the tre…
- T-2014 [FIX M, dropped, 0 steps] FIX: CI on main is red at 104c441 (tests)
- decision 2026-10-23: T-1259: build the compaction storm and the window sweep, tested with the bench's fakes; the measured sweep (real Haiku sessions) waits until weekly …
- similar finished tasks took 2–3 steps
- start here (files T-1842 touched): plugin/tests/test_run.py, plugin/tests/run.py, .github/workflows/test.yml, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_serve.py
## Why not caught
the hang needs a loaded 3.14 runner; locally the exception path happened to unwind cleanly, and the test never checked the loop's own exit line
## Lessons
- Never raise from a signal handler in threaded server code: set a flag the loop reads
## Files touched
- plugin/tests/test_settings_serve.py
- plugin/lib/fmsettingsserve.py
