---
id: T-3216
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T15:20:18Z
updated: 2026-11-05T15:24:46Z
base: 3949c329d3f94a7330467a6cfc833c1af8d49cd4
base_tree: 98fe00fa12786f0163fe7450eb8a406dfb5d7f4d
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-05T15:20:20Z
plan0_scope: []
verified: strong
---
# Post-merge verify re-runs the red classes alone before reverting: a class red only inside the full suite (green alone) is a flake, logged, not a revert
## Raw request
> Post-merge verify re-runs the red classes alone before reverting: a class red only inside the full suite (green alone) is a flake, logged, not a revert
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a merge whose full suite is red but whose red classes pass when re-run alone is recorded green with the flaky classes logged and is not reverted; a class that also fails alone still reverts exactly that merge — verify with `python3 plugin/tests/run.py test_lanes.PostMergeVerify`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: flaky red keeps the merge, real red reverts
2. [x] the re-run in pm_verify
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 16 tests in 2.1s (16 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_revert_requeues_the_merges_stacked_on_it 1s, Post [ran] [tree 0cf0faf3e93c] [world 2f1906870a] (2026-11-05T15:20:33Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 180 tests in 17.0s (164 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 10s, ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses [ran] [tree 49a28a08fe15] [world 2f1906870a] (2026-11-05T15:21:02Z)
- `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → ✗ exit 1 · Ran 16 tests in 8.3s (1 jobs, 16 at a time; slowest: PostMergeVerify 6s) / FAILED (1 classes: test_lanes.PostMergeVerify) (start tree + this task's tests) [ran] [tree f0788b42f808] [world 2f1906870a] (2026-11-05T15:21:24Z)
- `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 16 tests in 1.6s (16 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_requeued_merge_is_judged_without_the_merges_that_ [ran] [tree f0788b42f808] [world 2f1906870a] (2026-11-05T15:21:24Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T15:21:24Z [ran] [tree f0788b42f808] [world 2f1906870a] (2026-11-05T15:21:25Z)
- (audit adversary) `test_lanes 180 OK, proved red→green; the false reverts tonight: T-3154 (15:04) and T-3192 (15:16) red only on test_board_verbs.BoardVerbs, which passes alone on main, under --load 24, and in a detached worktree` → the re-run command is built only from class names that fully match [\w.]+, so a test's output can't inject shell; a bare 'suite exit N' red isn't re-run and reverts as before; FM_POSTMERGE_RERUN is the user's own setting [tree f0788b42f808] (2026-11-05T15:21:25Z)
- (audit edge) `test_lanes 180 OK, proved red→green; the false reverts tonight: T-3154 (15:04) and T-3192 (15:16) red only on test_board_verbs.BoardVerbs, which passes alone on main, under --load 24, and in a detached worktree` → a class that also fails alone still reverts exactly that merge (tested); a re-run that times out counts as red (non-zero), so it reverts; flaky classes are logged per merge (postmerge_flaky) for the flaky-tests report [tree f0788b42f808] (2026-11-05T15:21:25Z)
- (audit self) `test_lanes 180 OK, proved red→green; the false reverts tonight: T-3154 (15:04) and T-3192 (15:16) red only on test_board_verbs.BoardVerbs, which passes alone on main, under --load 24, and in a detached worktree` → no findings [tree f0788b42f808] (2026-11-05T15:21:25Z)
## Log
- 2026-11-05T15:20:18Z created
- 2026-11-05T15:20:19Z focused
- 2026-11-05T15:20:20Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-05T15:21:27Z affected tests waived: names that can't match are T-3160's modules, merged and reverted inside this window and not on disk; test_lanes passes (180 OK)
- 2026-11-05T15:21:30Z done
- 2026-11-05T15:21:33Z committed c09f1955 (3 files)
- 2026-11-05T15:24:46Z correction: BoardVerbs was not only a flake: with T-3160 applied, fm doctor's file map check fails (plugin/cards unmapped), so T-3160's red was real and T-3154/T-3189 (merged on top of it) were reverted for T-3160's red (T-3213), not a flake; T-3192's cause unconfirmed. T-3216's re-run-alone guard still stands for true flakes
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3141 [PERFORMANCE M, done, 2 steps] Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge …
- T-3119 [PERFORMANCE M, blocked, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
## Lessons
- An automatic revert must confirm the red outside the noisy run first: re-run the failing classes alone, or one flaky test reverts every merge
## Plan gaps
- failed first: step 1 failing tests: flaky red keeps the merge, real red reverts
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
