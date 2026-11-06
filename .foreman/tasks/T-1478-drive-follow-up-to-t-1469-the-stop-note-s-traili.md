---
id: T-1478
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T16:38:04Z
updated: 2026-10-22T16:44:08Z
base: 6cb8f3cd31887784295cbf3d32ed01cccb238574
base_tree: e71f982fb8ec83e06288ffccef36905e3010f3b2
plan0_at: 2026-10-22T16:38:56Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
verified: strong
---
# fm next skips a task a builder lane holds
## Raw request
> Drive follow-up to T-1469: the Stop note's trailing 'Next: T-x: fm focus T-x' (fm next's next_action) still names a task a builder lane holds; next_action should skip lane-held briefs the same way _drive now does
## Interpretation
_next_for (fmcore.py ~2866) picks the first queued brief even when a builder lane holds it, so fm next and the Stop note say 'fm focus T-x', which fm focus refuses.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a lane-held task queued first, fm next names the free one — verify with `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld.test_fm_next_skips_a_task_a_lane_holds`
## Non-goals
## Approach (options → choice → why)
In the main checkout (no p.lane), its 'mine' filter also skips briefs with meta builder that aren't closed; a lane's own view is unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] skip lane-held in _next_for
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld.test_fm_next_skips_a_task_a_lane_holds` → ✗ exit 1 · Ran 1 test in 2.428s / FAILED (failures=1) [ran] [tree 888c93c5b67e] (2026-10-22T16:43:12Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld.test_fm_next_skips_a_task_a_lane_holds` → exit 0 · Ran 1 test in 2.027s / OK [ran] [tree 6a469ec0ab69] (2026-10-22T16:43:16Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld.test_fm_next_skips_a_task_a_lane_holds` → exit 0 · Ran 1 test in 1.865s / OK [ran] [tree 9697b3331b2a] (2026-10-22T16:43:38Z)
- (audit edge) `self: _next_for's 'mine' filter skips, in the main checkout only, briefs with meta builder that aren't closed; a lane's own view is unchanged. test_drive_side (LaneHeld, both) and test_core green.` → inside a lane (p.lane set) the lane's own held task is still its next [tree 9697b3331b2a] (2026-10-22T16:43:38Z)
- (audit intent) `self: _next_for's 'mine' filter skips, in the main checkout only, briefs with meta builder that aren't closed; a lane's own view is unchanged. test_drive_side (LaneHeld, both) and test_core green.` → completes T-1469's fix for the trailing Next line [tree 9697b3331b2a] (2026-10-22T16:43:38Z)
- (audit self) `self: _next_for's 'mine' filter skips, in the main checkout only, briefs with meta builder that aren't closed; a lane's own view is unchanged. test_drive_side (LaneHeld, both) and test_core green.` → no findings [tree 9697b3331b2a] (2026-10-22T16:43:38Z)
## Log
- 2026-10-22T16:38:04Z created
- 2026-10-22T16:38:42Z planned from capture
- 2026-10-22T16:38:55Z focused
- 2026-10-22T16:44:06Z done
- 2026-10-22T16:44:08Z committed 50ff43b3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1469 [FIX S, done, 2 steps] Drive counts builder lanes as background work
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_core.py
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/lib/fmcore.py
- plugin/tests/test_drive_side.py
- CHANGELOG.md
