---
id: T-3354
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/bus.py, plugin/tests/test_bus.py, plugin/tests/test_claims.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:36:49Z
updated: 2026-11-06T05:39:43Z
base: fde3bac8292c81e534ce8bd1be577b65938fd62d
base_tree: 0158b73648485323a9d872744037cdd980f8034b
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T05:37:34Z
plan0_scope: [plugin/lib/sampo/bus.py, plugin/tests/test_bus.py, plugin/tests/test_claims.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
verified: strong
---
# Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be refused (T-3283 made it a note, so Sampo auto-reverted the merge, 3648d96de), and test_batch_edit.LaneMax expects lane max 50 to be refused (T-3297 raised the ceiling to 100)
## Raw request
> Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be refused (T-3283 made it a note, so Sampo auto-reverted the merge, 3648d96de), and test_batch_edit.LaneMax expects lane max 50 to be refused (T-3297 raised the ceiling to 100)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the revert is reverted (T-3283's bus.py change back), test_claims expects the take to succeed with a note naming the pre-claim, LaneMax refuses 101 and above, and test_bus, test_claims, test_batch_edit and test_diff_gates pass — verify with `python3 plugin/tests/run.py test_bus test_claims test_batch_edit test_diff_gates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] git revert the revert; update test_claims and LaneMax expectations
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus test_claims test_batch_edit` → ✗ exit 1 · Ran 71 tests in 6.0s (48 jobs, 16 at a time; slowest: ClaimsReview 5s, Lease 5s, Stop 4s) / FAILED (2 classes: test_bus.Lease, test_claims.Claims.test_a_lane_brief_preclaims_its_concrete_scope_and_nam [ran] [tree 727c9a2130e0] [world 2f1906870a] (2026-11-06T05:38:03Z)
- (step 1) `python3 plugin/tests/run.py test_bus test_claims test_batch_edit test_diff_gates` → exit 0 · Ran 85 tests in 6.9s (73 jobs, 16 at a time; slowest: DiffGates.test_run_py_repeats_p 6s, Approvals 4s, Stop 4s) / OK [ran] [tree d82f5fe4aced] [world 2f1906870a] (2026-11-06T05:38:21Z)
- `python3 plugin/tests/run.py test_bus test_claims test_batch_edit` → ✗ exit 1 · Ran 71 tests in 12.5s (16 jobs, 16 at a time; slowest: BatchEdit 10s, Claims 8s, Watch 6s) / FAILED (2 classes: test_claims.Claims, test_bus.Lease) (start tree + this task's tests) [ran] [tree d82f5fe4aced] [world 2f1906870a] (2026-11-06T05:38:54Z)
- `python3 plugin/tests/run.py test_bus test_claims test_batch_edit` → exit 0 · Ran 71 tests in 5.4s (54 jobs, 16 at a time; slowest: Lease 5s, Approvals 4s, Stop 4s) / OK [ran] [tree d82f5fe4aced] [world 2f1906870a] (2026-11-06T05:38:54Z)
- (audit self) `the bus.py change is byte-identical to the reviewed T-3283 merge (git diff against the pre-revert tree: 0 lines); test_claims now expects the advisory take, LaneMax checks the 100 ceiling (50 ok, 101 refused); the closes missed both because the affected selection didn't link them (T-3306)` → no findings [tree d82f5fe4aced] (2026-11-06T05:38:54Z)
- (ac 1) `python3 plugin/tests/run.py test_bus test_claims test_batch_edit test_diff_gates` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T05:38:21Z [ran] [tree d82f5fe4aced] [world 2f1906870a] (2026-11-06T05:39:01Z)
- (audit self) `self audit after the last change; red to green proved` → no findings [tree d82f5fe4aced] (2026-11-06T05:39:01Z)
## Log
- 2026-11-06T05:36:49Z created
- 2026-11-06T05:37:31Z focused
- 2026-11-06T05:37:34Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T05:39:38Z done
- 2026-11-06T05:39:43Z committed 68960f03f (13 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3283 [FIX S, done, 2 steps] A builder's lease take isn't refused by another lane's brief pre-claim (advisory since T-1138 for edits, still refusing in fm lease take) —…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- wrong turn 2026-11-05: "Merge T-3283: A builder's lease take isn't refused by another lane's brief pre-claim (advisory since T-1138 for edits, still refusing in fm lease…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bus.py
## Lessons
- A close's affected run picks tests by file links, so a test that asserts the old behaviour from another module (test_claims for bus.py's lease rule) stays unrun until the post-merge check reverts the merge; grep the tests for the behaviour's own words when a change flips a rule.
## Plan gaps
- failed first: step 1 git revert the revert; update test_claims and LaneMax expectations
## Files touched
- plugin/tests/test_bus.py
- plugin/tests/test_claims.py
- plugin/tests/test_batch_edit.py
- plugin/lib/sampo/bus.py
