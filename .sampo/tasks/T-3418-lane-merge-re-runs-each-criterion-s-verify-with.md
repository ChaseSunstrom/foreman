---
id: T-3418
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/tests/test_cli.py, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-11-06T09:42:06Z
updated: 2026-11-07T00:42:47Z
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T09:43:10Z
plan0_scope: []
builder_returned: 2026-11-06T10:09:24Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
---
# Lane merge re-runs each criterion's verify with a fixed 600 s cap, and builders write…
## Raw request
> FIX: lane merge re-runs each criterion's verify with a fixed 600 s cap, and builders write criteria naming whole modules (T-3367: test_lanes test_doctor test_demo test_docs test_cli test_showpieces → exit 124 at load ~20); scale the cap with load like the gates do, and have sampo task ac add/edit warn when a verify names a whole module whose last recorded run took over ~120 s, suggesting the touched classes
## Interpretation
Reading 1: scale the cap by load, tell timeout from red, warn on slow modules. Reading 2 (ruled out): change builders' criteria only, since the cap itself is the bug.
## Assumptions (confidence)
## Acceptance criteria
- [x] a verify that times out is reported as a timeout with seconds and load, not as red — verify with `python3 plugin/tests/run.py test_lanes.VerifyTimeout`
- [x] ac add/edit notes a slow whole-module verify from check_run timing, silent without data — verify with `python3 plugin/tests/run.py test_cli.SlowVerifyNote`
## Non-goals
## Approach (options → choice → why)
1) Do less: only raise the base cap; fails if load stays high, no timeout/red distinction. 2) Use what exists: load_scaled with a larger base plus check_run timing already in the ledger; likely outcome: no new signal. 3) New absolute-load signal (ruled out, T-3391 unifies); fails by duplicating it. Choice 2 (80%): smallest change reusing load_scaled.
## Risks and rollback
Blast radius: lanes.py _verify and cli.py ac note only; revert the commit.
## Execution prompt
## Steps
1. [x] tests then code
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.VerifyTimeout test_cli.SlowVerifyNote` → exit 0 · Ran 4 tests in 18.3s (2 jobs, 16 at a time; slowest: SlowVerifyNote 0s, VerifyTimeout 0s) / OK [ran] [tree b22d98cb8c0c] [world 2f1906870a] (2026-11-06T09:43:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 705 tests in 257.4s (143 jobs, 16 at a time; slowest: AffectedPairs 174s, LaneRecovery 29s, Lanes 19s) / FAILED (1 classes: test_cli.AffectedPairs) [ran] [tree b22d98cb8c0c] [world 2f1906870a] (2026-11-06T09:48:22Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 69.9s (5 jobs, 16 at a time; slowest: AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 46s, AffectedPairs.test_an_affected_run_with_evidence_records_it 31s, AffectedPa [ran] [tree b22d98cb8c0c] [world 2f1906870a] (2026-11-06T09:49:45Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.VerifyTimeout test_cli.SlowVerifyNote` → exit 0 · Ran 8 tests in 10.3s (2 jobs, 16 at a time; slowest: SlowVerifyNote 1s, VerifyTimeout 0s) / OK [ran] [tree b4f32e621853] [world 2f1906870a] (2026-11-06T10:04:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 709 tests in 254.4s (377 jobs, 16 at a time; slowest: AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 40s, AffectedPairs.test_an_affected_run_with_evidence_records_it 32s, Affec [ran] [tree b4f32e621853] [world 2f1906870a] (2026-11-06T10:08:34Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 19.7s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 11s, AffectedPairs.test_only_the_red_first_file_itself_is_left_out 7s, AffectedPairs.te [ran] [tree b4f32e621853] [world 2f1906870a] (2026-11-06T10:09:12Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 581b6a874d1c] (2026-11-06T22:22:13Z)
- `python3 plugin/tests/run.py test_cli test_lanes` → ✗ exit 1 · Ran 381 tests in 49.9s (66 jobs, 16 at a time; slowest: Lanes 41s, LaneRecovery 34s, TaskLifecycle 23s) / FAILED (3 classes: test_cli.SlowVerifyNote, test_lanes.VerifyTimeout, test_cli.SetLists) (start tree + this task's tests) [ran] [tree 581b6a874d1c] [world 2f1906870a] (2026-11-06T22:23:42Z)
- `python3 plugin/tests/run.py test_cli test_lanes` → exit 0 · Ran 381 tests in 34.4s (331 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, StateViews.test_state_md_is_bounded 9s, LanePrecheck 4s) / OK [ran] [tree 581b6a874d1c] [world 2f1906870a] (2026-11-06T22:23:42Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.VerifyTimeout` → exit 0 · Ran 4 tests in 0.8s (1 jobs, 16 at a time; slowest: VerifyTimeout 0s) / OK [ran] [tree 581b6a874d1c] [world 2f1906870a] (2026-11-06T22:23:50Z)
- (ac 2) `python3 plugin/tests/run.py test_cli.SlowVerifyNote` → exit 0 · Ran 4 tests in 2.0s (1 jobs, 16 at a time; slowest: SlowVerifyNote 1s) / OK [ran] [tree 581b6a874d1c] [world 2f1906870a] (2026-11-06T22:23:50Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 581b6a874d1c] (2026-11-06T22:23:50Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 581b6a874d1c] (2026-11-06T22:23:50Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 581b6a874d1c] (2026-11-06T22:23:50Z)
## Log
- 2026-11-06T09:42:06Z created
- 2026-11-06T09:42:57Z planned: it has criteria and steps
- 2026-11-06T09:43:09Z focused
- 2026-11-06T09:43:10Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T17:37:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a44768a190419fcfa (branch worktree-agent-a44768a190419fcfa kept: not merged)
- 2026-11-06T17:37:51Z lane: ~/.claude/foreman.lanes/T-3418 on foreman/T-3418
- 2026-11-06T17:38:43Z focused
- 2026-11-06T21:46:50Z merged foreman/T-3418 in merge train
- 2026-11-06T22:22:13Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_lanes.py']
- 2026-11-06T22:22:13Z scope: widened at merge to the reviewed lane's own diff (5a4a02ee9), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:25:14Z done
- 2026-11-06T22:25:19Z committed 9a0136b67 (1 file)
- 2026-11-07T00:42:47Z lane removed: ~/.claude/foreman.lanes/T-3418; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-2606 [FIX S, done, 2 steps] A criterion whose every recorded run matched no test can have its verify command edited: a command that measured nothing weakens no check —…
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- similar finished tasks took 2–3 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_cli.py
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
