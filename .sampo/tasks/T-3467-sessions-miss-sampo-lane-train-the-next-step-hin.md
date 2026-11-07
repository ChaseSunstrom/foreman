---
id: T-3467
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/cli.py, plugin/tests/test_lanes.py, plugin/tests/test_recall.py, plugin/tests/test_which.py, CHANGELOG.md, plugin/lib/sampo/hooks.py, plugin/tests/test_backlog.py, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: user
created: 2026-11-06T16:29:07Z
updated: 2026-11-06T21:59:32Z
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: 4292d2cb372e7e78d517e0b86024e6a8727f7921
lane_stop: merged 2026-11-06T18:26:22Z
verified: strong
---
# Sessions miss sampo lane train: the next-step hint lists one 'sampo lane merge' per finished lane, the lane help's 'train [ID,ID…]' comma hides it from sampo which and capture's covered check, and only FEATURE captures see a close done task
## Raw request
> Sessions miss sampo lane train: the next-step hint lists one 'sampo lane merge' per finished lane, the lane help's 'train [ID,ID…]' comma hides it from sampo which and capture's covered check, and only FEATURE captures see a close done task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 2+ finished lanes are offered as one sampo lane train; sampo which finds lane train; a PERFORMANCE capture names a close done task — verify with `python3 plugin/tests/run.py test_lanes test_recall test_which`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then the hint, the help text and the capture note
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_several_finished_lanes_are_offered_as_one_train test_which.Which.test_the_merge_train_is_found_by_what_it_does test_backlog.Capture` → ✗ exit 1 · Ran 9 tests in 2.4s (3 jobs, 16 at a time; slowest: Capture 2s, Lanes 1s, Which 0s) / FAILED (3 classes: test_backlog.Capture, test_lanes.Lanes, test_which.Which) [ran] [tree f21aace2a352] [world 2f1906870a] (2026-11-06T16:31:17Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_recall test_which test_backlog` → exit 0 · Ran 290 tests in 15.8s (214 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, Which 6s, OtherProjects 5s) / OK [ran] [tree 8e5d1c5d57a0] [world 2f1906870a] (2026-11-06T16:33:21Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 7eb34e580c8c] (2026-11-06T18:30:12Z)
- `python3 plugin/tests/run.py test_backlog test_lanes test_which` → ✗ exit 1 · Ran 267 tests in 26.4s (26 jobs, 16 at a time; slowest: LaneRecovery 25s, Lanes 18s, Reverify 8s) / FAILED (4 classes: test_lanes.Lanes, test_which.Which, test_backlog.Reverify, test_backlog.Capture) (start tree + this task's tests) [ran] [tree 7eb34e580c8c] [world 2f1906870a] (2026-11-06T18:30:52Z)
- `python3 plugin/tests/run.py test_backlog test_lanes test_which` → exit 0 · Ran 267 tests in 10.6s (156 jobs, 16 at a time; slowest: Reverify 10s, LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, PostMergeVerify 5s) / OK [ran] [tree 7eb34e580c8c] [world 2f1906870a] (2026-11-06T18:30:52Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_recall test_which` → exit 0 · Ran 275 tests in 12.7s (186 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, SelfChangeGate 6s, Which 4s) / OK [ran] [tree 7eb34e580c8c] [world 2f1906870a] (2026-11-06T18:31:07Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 7eb34e580c8c] (2026-11-06T18:31:07Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 7eb34e580c8c] (2026-11-06T18:31:07Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 7eb34e580c8c] (2026-11-06T18:31:07Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 7eb34e580c8c] (2026-11-06T18:31:07Z)
## Log
- 2026-11-06T16:29:07Z created
- 2026-11-06T16:29:14Z criterion 1 removed: 2+ finished lanes are offered as one sampo lane train; sampo which finds lane train; a PERFORMANCE capture names a close done task — verify with `python3 plugin/tests/run.py test_lanes test_recall test_capture_ergonomics`
- 2026-11-06T16:29:15Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_recall.py', 'plugin/tests/test_which.py', 'CHANGELOG.md']
- 2026-11-06T16:30:10Z lane: ~/.claude/foreman.lanes/T-3467 on foreman/T-3467
- 2026-11-06T16:31:17Z start point recorded late (no focus had kept one): its diff starts at b2637ff
- 2026-11-06T16:33:22Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_recall.py', 'plugin/tests/test_which.py', 'CHANGELOG.md', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_backlog.py']
- 2026-11-06T18:26:22Z merged foreman/T-3467 in merge train
- 2026-11-06T18:30:11Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_recall.py', 'plugin/tests/test_which.py', 'CHANGELOG.md', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_backlog.py', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T18:30:12Z scope: widened at merge to the reviewed lane's own diff (1b885f196), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:32:00Z done
- 2026-11-06T18:32:03Z committed a7106f410 (1 file)
- 2026-11-06T21:59:32Z lane removed: ~/.claude/foreman.lanes/T-3467; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A built verb nobody is pointed at goes unused: the next-step hint is the pointer, and a help text's punctuation decides whether search finds it.
## Plan gaps
- failed first: step 1 failing tests, then the hint, the help text and the capture note
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/hooks.py
- plugin/tests/test_backlog.py
- plugin/tests/test_lanes.py
- plugin/tests/test_which.py
