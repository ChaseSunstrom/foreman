---
id: T-1326
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:04Z
updated: 2026-10-21T03:32:15Z
base: 5f59d05ccb54b0ca87867e283ec3e8e6d05ea7d2
base_tree: f6a0f5e337e62a0c4e0b70cca829879e289d1709
plan0_at: 2026-10-21T03:24:20Z
plan0_scope: []
verified: strong
---
# Stopping fm code (the TUI's stop or quit, a closed terminal, kill) stops the planner and worker CLIs it started too
## Raw request
> Stopping fm code (the TUI's stop or quit, a closed terminal, kill) stops the planner and worker CLIs it started too
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a planner or worker CLI started by fm code is gone within 5 s of fm code getting SIGTERM or SIGHUP — verify with `python3 plugin/tests/run.py test_code_worker`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a sleeping fake CLI as planner and as worker, SIGTERM fm code, check the CLI is gone
2. [x] SIGTERM/SIGHUP handlers in fm code raise SystemExit so every finally kills its child's group; _cli kills its group when interrupted
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker.Worker.test_stopping_fm_code_stops_the_worker_it_started test_code_worker.Worker.test_stopping_fm_code_stops_the_planner_it_started` → ✗ exit 1 · Ran 2 tests in 13.8s (1 classes, 16 at a time; slowest: Worker 13s) / FAILED (1 classes) [ran] [tree 6b8cdc448aa8] (2026-10-21T03:26:04Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_code` → exit 0 · Ran 151 tests in 88.6s (25 classes, 16 at a time; slowest: Worker 88s, Bench 40s, Review 29s) / OK [ran] [tree 15496d48c88f] (2026-10-21T03:28:02Z)
- `python3 plugin/tests/run.py test_code_worker.Worker.test_stopping_fm_code_stops_the_worker_it_started test_code_worker.Worker.test_stopping_fm_code_stops_the_planner_it_started` → ✗ exit 1 · Ran 2 tests in 13.8s (1 classes, 16 at a time; slowest: Worker 12s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 15496d48c88f] (2026-10-21T03:28:19Z)
- `python3 plugin/tests/run.py test_code_worker.Worker.test_stopping_fm_code_stops_the_worker_it_started test_code_worker.Worker.test_stopping_fm_code_stops_the_planner_it_started` → exit 0 · Ran 2 tests in 2.6s (1 classes, 16 at a time; slowest: Worker 2s) / OK [ran] [tree 15496d48c88f] (2026-10-21T03:28:19Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 33 tests in 79.3s (1 classes, 16 at a time; slowest: Worker 79s) / OK [ran] [tree e65de4ba50ca] (2026-10-21T03:29:54Z)
- (audit edge) `self: read the diff: SIGTERM/SIGHUP raise SystemExit in fm code, so run_bounded's finally (killpg of the worker's group, orphans reaped) and _cli's new finally (kill_group when the CLI is still running) both run` → a signal mid-judge still runs the judge (it's in work's finally); a CLI that already exited isn't signalled (poll() first) [tree e65de4ba50ca] (2026-10-21T03:29:54Z)
- (audit adversary) `self: read the diff: SIGTERM/SIGHUP raise SystemExit in fm code, so run_bounded's finally (killpg of the worker's group, orphans reaped) and _cli's new finally (kill_group when the CLI is still running) both run` → no new exec path; the handlers only turn a stop into an unwind [tree e65de4ba50ca] (2026-10-21T03:29:54Z)
- (audit self) `self: read the diff: SIGTERM/SIGHUP raise SystemExit in fm code, so run_bounded's finally (killpg of the worker's group, orphans reaped) and _cli's new finally (kill_group when the CLI is still running) both run` → no findings [tree e65de4ba50ca] (2026-10-21T03:29:54Z)
## Log
- 2026-10-21T03:24:04Z created
- 2026-10-21T03:24:19Z focused
- 2026-10-21T03:28:34Z scope: CHANGELOG.md, the release note; plugin/lib/fmmodels.py, where the planner CLI is started
- 2026-10-21T03:32:13Z done
- 2026-10-21T03:32:15Z committed 038047b8 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1283 [FEATURE L, done, 7 steps] Foreman Code TUI: a beautiful, customizable, extendable terminal UI for fm code — the conv — lesson: When a user says a UI has too much…
- T-1300 [FEATURE L, done, 7 steps] Foreman Code TUI in motion: a truecolor renderer, eased animation (pulse, spinner, travelling light, rolling counters, growing bars, fl…
- research T-1320-review: Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards. [stale: plugin/lib/fmcl…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Why not caught
no test stopped fm code while a CLI was running; the TUI's stop path was only tested with a fake that started nothing
## Plan gaps
- failed first: step 1 Failing test: a sleeping fake CLI as planner and as worker, SIGTERM fm code, check the CLI is gone
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- plugin/lib/fmmodels.py
- CHANGELOG.md
