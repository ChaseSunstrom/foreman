---
id: T-3456
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: user
created: 2026-11-06T16:09:17Z
updated: 2026-11-06T16:23:30Z
base: 9ffb73b1a984e5f89c47e12877653a346cf94ea9
base_tree: 524d68e9000f6be618cbb64b328d8e0f01c8ab6a
lane_stop: merged 2026-11-06T16:21:16Z
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T16:21:19Z
plan0_scope: [plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# The post-merge newest-first probe is skipped whenever any pending merge carries after_reverts, so after one revert every later record runs oldest first on old trees (20 pending, the slot-pool false reds return)
## Raw request
> The post-merge newest-first probe is skipped whenever any pending merge carries after_reverts, so after one revert every later record runs oldest first on old trees (20 pending, the slot-pool false reds return)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] pending merges requeued after a revert are still settled by one green run on the newest — verify with `python3 plugin/tests/run.py test_lanes.PostMergeVerify`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then drop the after_reverts condition from pm_run's probe
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify.test_merges_requeued_after_a_revert_are_still_settled_by_the_newest` → ✗ exit 1 · Ran 1 tests in 1.3s (1 jobs, 16 at a time; slowest: PostMergeVerify 0s) / FAILED (1 classes: test_lanes.PostMergeVerify) [ran] [tree 39693111bbf8] [world 2f1906870a] (2026-11-06T16:12:11Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 28 tests in 34.1s (28 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_red_newest_merge_still_finds_the_culprit_oldest_ [ran] [tree 05dd494cedde] [world 2f1906870a] (2026-11-06T16:13:21Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 29 tests in 3.3s (29 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_red_newest_merge_still_finds_the_culprit_oldest_f [ran] [tree aa26e9442c77] [world 2f1906870a] (2026-11-06T16:16:13Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree d2acb35adfec] (2026-11-06T16:21:22Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 197 tests in 56.3s (15 jobs, 16 at a time; slowest: LaneRecovery 28s, Lanes 28s, RaceEvidence 11s) / FAILED (1 classes: test_lanes.PostMergeVerify) (start tree + this task's tests) [ran] [tree d2acb35adfec] [world 2f1906870a] (2026-11-06T16:22:48Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 197 tests in 23.8s (144 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, PostMergeVerify 6s, LaneRecovery.test_every_stop_cause_has_one_recovery [ran] [tree d2acb35adfec] [world 2f1906870a] (2026-11-06T16:22:48Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 29 tests in 4.3s (29 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_red_newest_merge_still_finds_the_culprit_oldest_f [ran] [tree d2acb35adfec] [world 2f1906870a] (2026-11-06T16:22:57Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree d2acb35adfec] (2026-11-06T16:22:57Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree d2acb35adfec] (2026-11-06T16:22:57Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree d2acb35adfec] (2026-11-06T16:22:57Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree d2acb35adfec] (2026-11-06T16:22:57Z)
## Log
- 2026-11-06T16:09:17Z created
- 2026-11-06T16:09:26Z lane: ~/.claude/foreman.lanes/T-3456 on foreman/T-3456
- 2026-11-06T16:12:11Z start point recorded late (no focus had kept one): its diff starts at 1f53628
- 2026-11-06T16:21:16Z merged foreman/T-3456 (2 file(s))
- 2026-11-06T16:21:16Z lane removed: ~/.claude/foreman.lanes/T-3456
- 2026-11-06T16:21:16Z focused
- 2026-11-06T16:21:19Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T16:21:21Z set scope=['plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T16:21:22Z scope: widened at merge to the reviewed lane's own diff (7e6233bfe), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T16:23:27Z done
- 2026-11-06T16:23:30Z committed e325b09c2 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3446 [FIX M, done, 1 steps] The post-merge suite reverts a merge whose red classes are red at its parent too… — lesson: A verifier that runs one job per event falls be…
- T-3454 [FIX S, planned, 1 steps] Re-land T-3377: auto-reverted (d44abf1bf) by a post-merge runner that ran at a pre-T-3442 sha, on the same CheckSkip/Claims slot-pool fa…
- T-3450 [FIX S, done, 1 steps] Re-land T-3120: auto-reverted on the same CheckSkip/Claims/CloseGates reds the slot-pool bug (T-3442) made — lesson: A post-merge revert ne…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py, plugin/tests/test_verify_unittest_form.py
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A batching shortcut needs the same tree the slow path judges: the newest merge predates later reverts, main's HEAD doesn't.
## Plan gaps
- failed first: step 1 failing test, then drop the after_reverts condition from pm_run's probe
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/lanes.py
- plugin/tests/test_lanes.py
