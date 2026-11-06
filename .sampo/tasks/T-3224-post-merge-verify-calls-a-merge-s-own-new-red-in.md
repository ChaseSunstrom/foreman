---
id: T-3224
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T18:08:28Z
updated: 2026-11-05T18:12:29Z
base: 06b9f0f466d8af3efcb1e85b53b0ad2d461579b4
base_tree: f026d9aecbfffc571329ff21a79eeda51db76841
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T18:08:33Z
plan0_scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# Post-merge verify calls a merge's own new red 'inherited' when its first-parent re-run can't run the class (the merge added it): inherited only when the parent run names the same failing classes
## Raw request
> Post-merge verify calls a merge's own new red 'inherited' when its first-parent re-run can't run the class (the merge added it): inherited only when the parent run names the same failing classes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a parent re-run that exits non-zero without naming every red class (no test matches, a crash, a timeout) reverts the merge; one that names them all keeps it as inherited — verify with `python3 plugin/tests/run.py test_lanes.PostMergeVerify`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a new red class absent on the parent reverts
2. [x] inherited only when the parent's failing classes cover the merge's red classes
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 18 tests in 2.2s (18 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_revert_requeues_the_merges_stacked_on_it 1s, Post [ran] [tree b3752753d743] [world 2f1906870a] (2026-11-05T18:08:51Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 184 tests in 28.1s (168 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 13s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree 463f94db1ebc] [world 2f1906870a] (2026-11-05T18:10:16Z)
- `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 18 tests in 13.4s (1 jobs, 16 at a time; slowest: PostMergeVerify 10s) / FAILED (1 classes: test_lanes.PostMergeVerify) (start tree + this task's tests) [ran] [tree 463f94db1ebc] [world 2f1906870a] (2026-11-05T18:10:34Z)
- `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 18 tests in 2.6s (18 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_requeued_merge_is_judged_without_the_merges_that_ [ran] [tree 463f94db1ebc] [world 2f1906870a] (2026-11-05T18:10:34Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 18 tests in 2.4s (18 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_requeued_merge_is_judged_without_the_merges_that_ [ran] [tree 843fa2466bb8] [world 2f1906870a] (2026-11-05T18:10:49Z)
- (audit intent) `self: re-read the parent re-run: reds come from the merge's own run, named from the parent's FAIL/ERROR lines; inherited needs a non-zero parent exit and every red class named there; a timeout or crash names none, so it reverts` → only a red the first parent already fails is kept as inherited [tree 843fa2466bb8] (2026-11-05T18:10:49Z)
- (audit adversary) `self: re-read the parent re-run: reds come from the merge's own run, named from the parent's FAIL/ERROR lines; inherited needs a non-zero parent exit and every red class named there; a timeout or crash names none, so it reverts` → a merge adding its own failing class can no longer pass as inherited through 'no test matches' on the parent [tree 843fa2466bb8] (2026-11-05T18:10:49Z)
- (audit edge) `self: re-read the parent re-run: reds come from the merge's own run, named from the parent's FAIL/ERROR lines; inherited needs a non-zero parent exit and every red class named there; a timeout or crash names none, so it reverts` → a merge red in two classes where the parent fails only one reverts (subset rule); the T-3216 flaky path is untouched [tree 843fa2466bb8] (2026-11-05T18:10:49Z)
- (audit self) `self: re-read the parent re-run: reds come from the merge's own run, named from the parent's FAIL/ERROR lines; inherited needs a non-zero parent exit and every red class named there; a timeout or crash names none, so it reverts` → no findings [tree 843fa2466bb8] (2026-11-05T18:10:49Z)
## Log
- 2026-11-05T18:08:28Z created
- 2026-11-05T18:08:30Z focused
- 2026-11-05T18:08:33Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T18:12:23Z done
- 2026-11-05T18:12:29Z committed f67bbbb9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3213 [FIX S, done, 2 steps] Post-merge verify blames the wrong merge: T-3189 landed on top of T-3160, T-3160 went… — lesson: blame a red on a merge only after the same…
- T-3216 [FIX S, done, 2 steps] Post-merge verify re-runs the red classes alone before reverting: a class red only inside the full suite (green alone) is a flake, logged, …
- T-2943 [FIX S, done, 1 steps] The fmmint and fmtraces shims match the exact old-path shim, so the rename alias test passes — lesson: A new sampo module's old-path shim m…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar finished tasks took 1–2 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py
## Why not caught
T-3213's tests used a re-run hook that never named classes; caught by checking my own close lens against the code
## Lessons
- a fallback that reads any non-zero exit as agreement fails open; compare what both runs name
## Plan gaps
- failed first: step 1 failing test: a new red class absent on the parent reverts
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
