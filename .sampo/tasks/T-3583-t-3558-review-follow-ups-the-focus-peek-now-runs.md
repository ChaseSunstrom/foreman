---
id: T-3583
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:02:55Z
updated: 2026-11-07T04:45:16Z
lane: ~/.claude/foreman.lanes/T-3583
lane_branch: foreman/T-3583
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T04:25:22Z
plan0_scope: []
---
# T-3558 review follow-ups: the focus peek now runs before the refusal checks, so a focus…
## Raw request
> T-3558 review follow-ups: the focus peek now runs before the refusal checks, so a focus that will be refused (plan gaps, lane_only, held_elsewhere) still pays a git snapshot, recall and predict — run those checks on the peek first; add tests for each recompute key family (recall query/scope, paused_tree rebase), two concurrent focuses ending with one active, and the views-lock timeout; put regen_views in a finally after _save_dirty
## Interpretation
T-3558 review follow-ups, all in cmd_focus (cli.py) and test_focus_lock.py: (1) a focus that will be refused (closed, lane_only on main, plan gaps, held by another checkout) still pays the peek's blast map, git snapshot, recall and predict: run the refusal checks on the peek first; (2) tests for each recompute key family (recall query/scope, paused_tree rebase), two concurrent focuses ending with one active, and the views-lock timeout; (3) regen_views in a finally after _save_dirty. Tier M, not L: one function in one file plus tests, no schema/API change.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a refused focus (plan gaps, lane_only, held elsewhere) runs no snapshot, recall or predict; regen_views runs even when _save_dirty raises; recompute keys, concurrent focus and views-lock timeout are pinned by tests — verify with `nice -n 10 python3 plugin/tests/run.py test_focus_lock`
- [ ] focus, doors, lanes and dirty-at-focus tests still pass — verify with `nice -n 10 python3 plugin/tests/run.py test_focus_lock test_judgment test_triggers test_lanes test_dirty_at_focus`
## Non-goals
## Approach (options → choice → why)
1) use what exists: the refusal checks already in cmd_focus's locked block, moved into one _focus_refusal(p, b) helper raised on the peek and again under the lock; likely outcome: a refused focus pays no blast map, snapshot, recall or predict and never queues on the project lock; fails if: a check depends on state only the lock makes current (the locked re-check covers that).
2) run the checks on the peek only to skip the slow pass, raise only under the lock; likely outcome: same savings but a refused focus still waits on the project lock; fails if: lanes queue behind refusals.
3) do the slow pass after the locked checks (back to holding the lock for git); fails if: the T-3558 lock-hold win (2.2 s -> 0.04 s) is lost.
Choice 1 (85%): smallest diff, keeps T-3558's win, and the locked re-check still catches a change made meanwhile. Test-gap findings get tests that pin the behaviour; one that passes first try is reported as not-a-defect.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests in test_focus_lock.py: refused focus pays nothing, regen after a _save_dirty failure, recall/rebase recompute keys, two concurrent focuses, views-lock timeout  <- CURRENT
2. [x] fix cmd_focus: _focus_refusal on the peek and under the lock; regen_views in a finally after _save_dirty
3. [x] targeted focus/doors/lane tests green
## Resume here
## Docs impact
none: internal ordering of fm focus's refusal checks and view regeneration; no verb, flag or output changes
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_focus_lock` → ✗ exit 1 · Ran 9 tests in 1.7s (9 jobs, 16 at a time; slowest: FocusLock.test_an_input_edited_during_the_peek_is_read_again_under_the_lock 1s, FocusLock.test_a_wedged_views_lock_costs_the_views_not_the_focus 1s, [ran] [tree b4f990c2eb38] [world 2f1906870a] (2026-11-07T04:27:39Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_focus_lock` → exit 0 · Ran 9 tests in 7.3s (9 jobs, 16 at a time; slowest: FocusLock.test_a_pause_snapshot_moved_during_the_peek_is_re_based_again 2s, FocusLock.test_an_input_edited_during_the_peek_is_read_again_under_the_l [ran] [tree 97c5e6814bb8] [world 2f1906870a] (2026-11-07T04:29:13Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_focus_lock test_judgment.DoorPark` → exit 0 · Ran 29 tests in 252.5s (29 jobs, 16 at a time; slowest: DoorPark.test_the_digest_counts_parks_and_asks_by_door 15s, DoorPark.test_the_finish_receipt_tallies_each_one_way_step_and_how_it_was_undone_or_ [ran] [tree a131f14ebc70] [world 2f1906870a] (2026-11-07T04:41:38Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_focus_lock test_judgment test_triggers test_lanes test_dirty_at_focus test_race test_execution test_drive_side` → exit 0 · Ran 353 tests in 215.8s (101 jobs, 16 at a time; slowest: Lanes 129s, LaneRecovery 70s, RaceEvidence 31s) / OK [ran] [tree a131f14ebc70] [world 2f1906870a] (2026-11-07T04:45:16Z)
## Log
- 2026-11-07T03:02:55Z created
- 2026-11-07T04:24:48Z set tier=M
- 2026-11-07T04:24:53Z planned: it has criteria and steps
- 2026-11-07T04:25:08Z criterion 2 verify: `nice -n 10 python3 plugin/tests/run.py test_focus_lock test_doors` → `nice -n 10 python3 plugin/tests/run.py test_focus_lock test_judgment test_triggers test_lanes test_dirty_at_focus`
- 2026-11-07T04:25:08Z criterion 2 text: focus and doors tests still pass → focus, doors, lanes and dirty-at-focus tests still pass
- 2026-11-07T04:25:09Z lane: ~/.claude/foreman.lanes/T-3583 on foreman/T-3583
- 2026-11-07T04:25:22Z focused
- 2026-11-07T04:25:22Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:37:29Z the first ordering (refusals before doors.check) broke unparking: plan_gaps reads the doors the gate re-marks, so a parked task the gate could now snapshot was refused forever (test_judgment.DoorPark.test_a_parked_task_the_gate_can_now_snapshot_focuses red on it, green on base); the peek refusal now runs after doors.check on a fresh read
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- T-3558 [PERFORMANCE M, active, 3 steps] Sampo focus holds the project lock 1.8-7.3 s (sampled from /proc/locks while 8 lanes…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- the similar finished task took 2 steps
