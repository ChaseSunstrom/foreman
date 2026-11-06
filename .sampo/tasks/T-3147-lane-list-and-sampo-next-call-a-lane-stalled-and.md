---
id: T-3147
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:36:32Z
updated: 2026-11-05T06:01:24Z
base: 732c3ca6888b7d09e02135a5c8bd5b95eae2f38d
base_tree: 9030f718dbed0db1a6ed527720abd6c0a8acc147
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T05:50:23Z
plan0_scope: []
verified: strong
---
# A returned or merged builder lane is never called STALLED: untracked leftovers, the T-3145 return mark and any earlier lane_merge event all mean it waits on a merge or is done
## Raw request
> lane list and sampo next call a lane STALLED and advise 'stop its agent, fm lane recover' when its builder already returned a commit and the lane only waits on a merge (T-3113, T-3083 after T-3145): a lane with a commit ahead of base and a returned builder should read 'waits on merge', not stalled
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] lanes._stalled skips a live builder's lane that has commits ahead of main with no tracked changes (untracked leftovers such as node_modules ignored), one marked builder_returned, and one with a lane_merge event anywhere in its recent ledger, while a quiet lane with no commit ahead still reads stalled — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the three returned shapes are not stalled; a quiet uncommitted lane still is
2. [x] the fix in lanes._stalled
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled` → ✗ exit 1 · Ran 1 tests in 11.3s (1 classes, 16 at a time; slowest: LaneRecovery 10s) / FAILED (1 classes: test_lanes.LaneRecovery) [ran] [tree e62658ef591b] [world 2f1906870a] (2026-11-05T05:53:36Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 162 tests in 72.8s (14 classes, 16 at a time; slowest: Lanes 72s, LaneRecovery 52s, RaceEvidence 32s) / OK [ran] [tree 7c9a5adbaf4d] [world 2f1906870a] (2026-11-05T05:55:48Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 162 tests in 41.6s (14 classes, 16 at a time; slowest: Lanes 41s, LaneRecovery 39s, RaceEvidence 17s) / OK [ran] [tree 11fbe480e133] [world 2f1906870a] (2026-11-05T05:59:33Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled` → exit 0 · Ran 1 tests in 10.3s (1 classes, 16 at a time; slowest: LaneRecovery 10s) / OK [ran] [tree 11fbe480e133] [world 2f1906870a] (2026-11-05T05:59:33Z)
- (audit edge) `self: two skips in lanes._stalled before any git or ledger work: the T-3145 builder_returned mark and a merged lane_stop; the clean-tree check ignores untracked files; a quiet lane with nothing committed still reads stalled (tested)` → a builder that committed once and keeps working only in new untracked files reads as returned, not stalled; acceptable since a hang then shows in the merge review, and tracked edits still count [tree 11fbe480e133] (2026-11-05T05:59:33Z)
- (audit self) `self: two skips in lanes._stalled before any git or ledger work: the T-3145 builder_returned mark and a merged lane_stop; the clean-tree check ignores untracked files; a quiet lane with nothing committed still reads stalled (tested)` → no findings [tree 11fbe480e133] (2026-11-05T05:59:33Z)
## Log
- 2026-11-05T05:36:32Z created
- 2026-11-05T05:46:30Z planned from capture
- 2026-11-05T05:50:22Z focused
- 2026-11-05T05:50:23Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T06:01:20Z done
- 2026-11-05T06:01:24Z committed c1cbcefa (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- T-2354 [FEATURE M, done, 3 steps] Stopped and stalled lanes recover by cause without being told (Mission 8, #9) — lesson: Liveness read from the wrong process makes ever…
- research T-2354-review: Verdict: changes needed.** I could not run anything (read-only), so these are from reading the code. [stale: plugin/lib/fmlanes.py, plugin/tests/…
- decision 2026-10-31: [reverses: a later Mission's lane waits only for earlier-Mission lanes launched before it] Mission-order merging, revised: lanes that are ready merg…
## Plan gaps
- failed first: step 1 failing tests: the three returned shapes are not stalled; a quiet uncommitted lane still is
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
