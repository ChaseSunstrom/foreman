---
id: T-3492
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/risk.py, plugin/tests/test_risk.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: user
created: 2026-11-06T18:43:48Z
updated: 2026-11-07T00:42:49Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T18:46:44Z
plan0_scope: [plugin/lib/sampo/risk.py, plugin/tests/test_risk.py, CHANGELOG.md]
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
---
# A revert that was itself undone (a re-land reverting it) still spends 3 risk points, so false post-merge reverts (4 of today's 6, re-landed by T-3445/T-3450/T-3454) used up the risk budget and paused the self-improvement pass
## Raw request
> A revert that was itself undone (a re-land reverting it) still spends 3 risk points, so false post-merge reverts (4 of today's 6, re-landed by T-3445/T-3450/T-3454) used up the risk budget and paused the self-improvement pass
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a revert whose commit a later commit reverts (Revert "Revert…" or a re-land citing 'This reverts commit <sha>') costs nothing, and neither does the undoing commit — verify with `python3 plugin/tests/run.py test_risk`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the revert count skips undone reverts
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_risk` → ✗ exit 1 · Ran 12 tests in 24.8s (1 jobs, 16 at a time; slowest: Risk 2s) / FAILED (1 classes: test_risk.Risk) [ran] [tree 71504275aed6] [world 2f1906870a] (2026-11-06T18:47:32Z)
- (step 1) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 12 tests in 9.6s (1 jobs, 16 at a time; slowest: Risk 2s) / OK [ran] [tree f2708229cb6a] [world 2f1906870a] (2026-11-06T18:48:15Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree f05c3d5253a6] (2026-11-06T22:21:09Z)
- (ac 1) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 12 tests in 9.2s (1 jobs, 16 at a time; slowest: Risk 3s) / OK [ran] [tree f05c3d5253a6] [world 2f1906870a] (2026-11-06T22:21:22Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree f05c3d5253a6] (2026-11-06T22:21:22Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree f05c3d5253a6] (2026-11-06T22:21:22Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree f05c3d5253a6] (2026-11-06T22:21:22Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree f05c3d5253a6] (2026-11-06T22:21:22Z)
## Log
- 2026-11-06T18:43:48Z created
- 2026-11-06T18:45:14Z lane: ~/.claude/foreman.lanes/T-3492 on foreman/T-3492
- 2026-11-06T18:46:43Z focused
- 2026-11-06T18:46:44Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T21:46:50Z merged foreman/T-3492 in merge train
- 2026-11-06T22:21:08Z set scope=['plugin/lib/sampo/risk.py', 'plugin/tests/test_risk.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T22:21:08Z scope: widened at merge to the reviewed lane's own diff (8486fc5ea), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:22:04Z done
- 2026-11-06T22:22:10Z committed e1e639be0 (1 file)
- 2026-11-07T00:42:49Z lane removed: ~/.claude/foreman.lanes/T-3492; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3454 [FIX S, done, 1 steps] Re-land T-3377: auto-reverted (d44abf1bf) by a post-merge runner that ran at a pre-T-3442 sha, on the same CheckSkip/Claims slot-pool false…
- T-3213 [FIX S, done, 2 steps] Post-merge verify blames the wrong merge: T-3189 landed on top of T-3160, T-3160 went… — lesson: blame a red on a merge only after the same…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- T-3354 [FIX S, done, 1 steps] Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be r…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_risk.py
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A brake fed by false alarms stops the very work that would fix them: measure the alarm's truth before it spends.
## Plan gaps
- failed first: step 1 failing test, then the revert count skips undone reverts
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/risk.py
- plugin/tests/test_risk.py
