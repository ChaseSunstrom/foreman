---
id: T-3446
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-11-06T15:19:16Z
updated: 2026-11-06T16:29:49Z
base: d44abf1bf2aaa1a637c2f827e12987784415fea1
base_tree: 42342a629535547394bf0c00def6a6252f84c5f7
lane_stop: merged 2026-11-06T15:57:53Z
verified: strong
lane_verified: 255a4a32c208803c591cb131c124cdfb36cc99f8
---
# The post-merge suite reverts a merge whose red classes are red at its parent too…
## Raw request
> FIX: the post-merge suite reverts a merge whose red classes are red at its parent too (T-2911, T-3372 tonight, both red at their parents on CheckSkip/Claims): before reverting, run the red classes at the merge's first parent; red there too means the merge didn't cause it, so record it as inherited, not reverted
## Interpretation
The post-merge suite verifies pending merges oldest first, each at its own commit: one 20-40 min run per merge while merges land every ~8 min, so 18 sat unverified tonight, and old commits carried the slot-pool bug (T-3442) that made false reds and reverted four good merges (T-2911, T-3372, T-3120, T-3398). A green full suite on the newest pending merge covers every older pending merge it contains: verify the newest first, and on green settle the older ones as green (covered by that run); on red, fall back to oldest first, where the existing parent check (T-3213) and alone-rerun (T-3216) assign blame.
## Assumptions (confidence)
## Acceptance criteria
- [x] with several merges pending, a green run on the newest settles every older pending merge it contains as green (one suite run), a red newest one still finds the culprit oldest first — verify with `python3 plugin/tests/run.py test_lanes.PostMergeVerify`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] pm_run verifies the newest pending first and settles the older ones on green; tests red first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c1f085b17ffc] (2026-11-06T15:57:55Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 193 tests in 43.6s (15 jobs, 16 at a time; slowest: LaneRecovery 27s, Lanes 22s, RaceEvidence 9s) / FAILED (1 classes: test_lanes.PostMergeVerify) (start tree + this task's tests) [ran] [tree c1f085b17ffc] [world 2f1906870a] (2026-11-06T15:59:30Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 193 tests in 45.1s (168 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, LaneRecovery.test_every_stop_cause_has_one_recovery_and_a_scenario_that [ran] [tree c1f085b17ffc] [world 2f1906870a] (2026-11-06T15:59:30Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 27 tests in 2.0s (27 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_code_merge_with_a_red_unlinked_class_is_reverted [ran] [tree c1f085b17ffc] [world 2f1906870a] (2026-11-06T16:04:09Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 524d68e9000f] (2026-11-06T16:16:13Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.PostMergeVerify` → exit 0 · Ran 27 tests in 2.4s (27 jobs, 16 at a time; slowest: PostMergeVerify.test_the_real_detached_runner_verifies_a_landed_merge 1s, PostMergeVerify.test_a_class_that_also_fails_alone_still_reverts 1s, Pos [ran] [tree 524d68e9000f] [world 2f1906870a] (2026-11-06T16:16:21Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 524d68e9000f] (2026-11-06T16:16:21Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 524d68e9000f] (2026-11-06T16:16:21Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 524d68e9000f] (2026-11-06T16:16:21Z)
## Log
- 2026-11-06T15:19:16Z created
- 2026-11-06T15:25:25Z set tier=M
- 2026-11-06T15:25:27Z planned: it has criteria and steps
- 2026-11-06T15:33:24Z lane: ~/.claude/foreman.lanes/T-3446 on foreman/T-3446
- 2026-11-06T15:37:44Z review (one fm-reviewer pass): fixed hand-reverted merges being covered, a live-claimed record being covered, the held oldest record left running on an exception; added tests for the probe count and the hand-revert case. Left: probe has no flake rerun (a flaky probe falls back to oldest first, bounded to one probe per newest sha)
- 2026-11-06T15:57:01Z steer: stopped the oldest-first post-merge runner (pid 2426296, spawned without the pause) — it ran at pre-T-3442 shas, hit the slot-pool CheckSkip/Claims false reds again and reverted T-3377 (d44abf1bf); its records stay pending for the newest-first run this task adds
- 2026-11-06T15:57:53Z merged foreman/T-3446 (2 file(s))
- 2026-11-06T15:57:53Z lane removed: ~/.claude/foreman.lanes/T-3446
- 2026-11-06T15:57:54Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py']
- 2026-11-06T15:57:54Z scope: widened at merge to the reviewed lane's own diff (255a4a32c), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T16:17:10Z done
- 2026-11-06T16:29:49Z verified: the full suite is green on 1078ed22d, which contains 255a4a32c
## Follow-ups captured
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A verifier that runs one job per event falls behind when events come faster than a job; batch by the newest state.
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/lanes.py
- plugin/tests/test_lanes.py
