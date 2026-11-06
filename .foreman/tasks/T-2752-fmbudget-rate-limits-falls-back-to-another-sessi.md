---
id: T-2752
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T02:10:28Z
updated: 2026-11-03T02:16:30Z
base: 6534bc4846f26dfed580b7a45e856726a31fb656
base_tree: 3a5a6b8b5af6ba65fea550ec7fb2ba112d932c7e
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T02:14:28Z
plan0_scope: []
verified: strong
---
# fmbudget.rate_limits reads this session's own statusline snapshot first and never one more than six hours older than the newest, so another session's stale reading (a previous subscription's 96%) can't hold subagents
## Raw request
> fmbudget.rate_limits falls back to another session's statusline snapshot when this session's newest has no rate_limits, so a stale 96% from a previous subscription held subagents while the live reading was 11%; prefer this session's snapshot and ignore any older than the newest by more than a few hours
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with this session's snapshot lacking rate_limits and another session's 96% from a day before, rate_limits() returns no weekly reading (not 96%); this session's own reading wins when it has one — verify with `python3 plugin/tests/run.py test_budget`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the session-first, age-bounded read
## Resume here
## Docs impact
none: an internal read; the pause message is unchanged
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_budget test_cost_forecast test_drive_side test_draft` → exit 0 · Ran 37 tests in 10.3s (11 classes, 16 at a time; slowest: SessionStart 10s, TaskCostCap 8s, DriveSide 4s) / OK [ran] [tree b2c319143f7b] [world 2f1906870a] (2026-11-03T02:15:29Z)
- (step 2) `python3 plugin/tests/run.py test_budget test_cost_forecast test_drive_side test_draft` → exit 0 · Ran 37 tests in 10.5s (11 classes, 16 at a time; slowest: SessionStart 10s, TaskCostCap 9s, DriveSide 5s) / OK [ran] [tree b2c319143f7b] [world 2f1906870a] (2026-11-03T02:15:40Z)
- `python3 plugin/tests/run.py test_budget` → ✗ exit 1 · Ran 11 tests in 10.7s (2 classes, 16 at a time; slowest: SessionStart 9s, Budget 2s) / FAILED (1 classes: test_budget.Budget) (start tree + this task's tests) [ran] [tree b2c319143f7b] [world 2f1906870a] (2026-11-03T02:16:00Z)
- `python3 plugin/tests/run.py test_budget` → exit 0 · Ran 11 tests in 9.4s (2 classes, 16 at a time; slowest: SessionStart 9s, Budget 2s) / OK [ran] [tree b2c319143f7b] [world 2f1906870a] (2026-11-03T02:16:00Z)
- (ac 1) `python3 plugin/tests/run.py test_budget` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T02:16:00Z [ran] [tree b2c319143f7b] [world 2f1906870a] (2026-11-03T02:16:01Z)
- `python3 plugin/tests/run.py test_budget test_cost_forecast test_drive_side test_draft` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T02:15:40Z [ran] [tree b2c319143f7b] [world 2f1906870a] (2026-11-03T02:16:01Z)
- (audit edge) `rate_limits and forecast now read _recent_snaps(): the newest three, none more than six hours older than the newest; this session's snapshot without rate_limits no longer falls back to another session's day-old 96%` → two live sessions within six hours still both count (the newest with a reading wins, as before); a lone old snapshot is still read when it is the newest (nothing newer exists) [tree b2c319143f7b] (2026-11-03T02:16:01Z)
- (audit intent) `rate_limits and forecast now read _recent_snaps(): the newest three, none more than six hours older than the newest; this session's snapshot without rate_limits no longer falls back to another session's day-old 96%` → the user switched subscriptions; a previous account's reading held this session's subagents at 96% while the live one read 11% [tree b2c319143f7b] (2026-11-03T02:16:01Z)
- (audit self) `rate_limits and forecast now read _recent_snaps(): the newest three, none more than six hours older than the newest; this session's snapshot without rate_limits no longer falls back to another session's day-old 96%` → no findings [tree b2c319143f7b] (2026-11-03T02:16:01Z)
## Log
- 2026-11-03T02:10:28Z created
- 2026-11-03T02:14:26Z planned from capture
- 2026-11-03T02:14:27Z focused
- 2026-11-03T02:14:28Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T02:15:18Z scope: plugin/lib/fmbudget.py (forecast reads the same bounded snapshots)
- 2026-11-03T02:16:27Z done
- 2026-11-03T02:16:30Z committed 3374ee85 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0320-review: Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests. [stale: plugin/lib/fmbudget…
- research T-0298-review-1: Findings
- research T-1810-review: Verdict:** changes needed. The sweep never runs in a default project (finding 1), and its GitHub path has several failure modes (findings 2–5). […
- decision 2026-10-31: End-of-run exam: one fresh child-authored draw (seed 70, 18 per kind, all six languages, 6 held out per kind), the zero-token arms on all, then the …
## Why not caught
the budget tests wrote one snapshot named s.json, never a stale second session beside a current one
## Files touched
- plugin/tests/test_budget.py
- plugin/lib/fmbudget.py
