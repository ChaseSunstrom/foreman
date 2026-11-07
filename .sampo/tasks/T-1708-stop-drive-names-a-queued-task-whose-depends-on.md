---
id: T-1708
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-23T01:27:12Z
updated: 2026-10-23T01:35:18Z
base: 28249367784728d5033c34f772310ae1a92a9467
base_tree: 83954d14bc7d42bc6658d2a462b1e2f306689f99
plan0_at: 2026-10-23T01:29:38Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
verified: strong
---
# Drive and fm next skip a queued task whose dependency is still open
## Raw request
> Stop drive names a queued task whose depends_on is still open (T-1637 while T-1636 is in a lane): fmhooks.py:3422 work selection skips only waiting/held, never checks c._deps against open briefs; _next_request (fmhooks.py:799) already has the test; also the more lists (3514, 3534) and _side_work (3611)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a task's depends_on held by a lane, neither the Stop drive nor fm next offers it, and free work is offered instead — verify with `python3 plugin/tests/run.py test_drive_side.LaneHeld`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] skip open-dependency tasks in next_for and the drive
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/wt1708 && python3 plugin/tests/run.py test_drive_side.LaneHeld` → red as expected (exit 1) · Ran 3 tests in 11.0s (1 classes, 16 at a time; slowest: LaneHeld 10s) / FAILED (1 classes) [ran] [tree 83954d14bc7d] (2026-10-23T01:30:16Z)
- (step 2) `cd /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/wt1708 && python3 plugin/tests/run.py test_drive_side test_core` → exit 0 · Ran 75 tests in 6.3s (19 classes, 16 at a time; slowest: LaneHeld 6s, DriveSide 6s, PreToolUse 3s) / OK [ran] [tree 83954d14bc7d] (2026-10-23T01:32:55Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_side.LaneHeld` → exit 0 · Ran 3 tests in 11.2s (1 classes, 16 at a time; slowest: LaneHeld 11s) / OK [ran] [tree cd53a90448bd] (2026-10-23T01:33:45Z)
- `python3 plugin/tests/run.py test_drive_side.LaneHeld` → ✗ exit 1 · Ran 3 tests in 12.5s (1 classes, 16 at a time; slowest: LaneHeld 10s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree cd53a90448bd] (2026-10-23T01:34:08Z)
- `python3 plugin/tests/run.py test_drive_side.LaneHeld` → exit 0 · Ran 3 tests in 9.0s (1 classes, 16 at a time; slowest: LaneHeld 9s) / OK [ran] [tree cd53a90448bd] (2026-10-23T01:34:08Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_side.LaneHeld` → exit 0 · Ran 3 tests in 3.5s (1 classes, 16 at a time; slowest: LaneHeld 3s) / OK [ran] [tree cd53a90448bd] (2026-10-23T01:34:19Z)
- (audit intent) `self-review: next_for's mine filter and the drive's work pick both skip a task with any open dependency (fmcore._deps, so inferred deps count unless urgent); the active task is never filtered; side lists skip them too; prove: red on the start tree, green now` → a queued task waiting on an open dependency (a lane's task) is never offered; free work is offered instead [tree cd53a90448bd] (2026-10-23T01:34:19Z)
- (audit edge) `self-review: next_for's mine filter and the drive's work pick both skip a task with any open dependency (fmcore._deps, so inferred deps count unless urgent); the active task is never filtered; side lists skip them too; prove: red on the start tree, green now` → an urgent task's inferred deps don't hold it back (_deps); a dependency that is closed or unknown never blocks; if every queued task is dependency-blocked the drive falls through to the inbox/held-lanes notes as before [tree cd53a90448bd] (2026-10-23T01:34:19Z)
- (audit self) `self-review: next_for's mine filter and the drive's work pick both skip a task with any open dependency (fmcore._deps, so inferred deps count unless urgent); the active task is never filtered; side lists skip them too; prove: red on the start tree, green now` → no findings [tree cd53a90448bd] (2026-10-23T01:34:19Z)
## Log
- 2026-10-23T01:27:12Z created
- 2026-10-23T01:29:28Z planned from capture
- 2026-10-23T01:29:29Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_drive_side.py', 'CHANGELOG.md']
- 2026-10-23T01:29:30Z set priority=urgent
- 2026-10-23T01:29:36Z focused
- 2026-10-23T01:35:16Z done
- 2026-10-23T01:35:18Z committed 8478ac90 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1478 [FIX S, done, 2 steps] fm next skips a task a builder lane holds
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1469 [FIX S, done, 2 steps] Drive counts builder lanes as background work
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 2–3 steps
- start here (files T-1478 touched): plugin/lib/fmcore.py, plugin/tests/test_drive_side.py, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Why not caught
the drive's tests covered held lanes but not a task that depends on one
## Lessons
- Every picker of 'the next task' must apply the same readiness test; a shared predicate beats three hand-copied filters
## Files touched
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/tests/test_drive_side.py
- CHANGELOG.md
