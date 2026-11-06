---
id: T-3452
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_lanes.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-06T15:46:25Z
updated: 2026-11-06T16:16:09Z
base: 9b5639c438e9f1956fa429aabfa14132c50b6872
base_tree: c1f085b17ffcb928ac07079a5783172ca23c7912
lane_stop: merged 2026-11-06T16:08:02Z
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T16:08:05Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# A doc named in passing in a task's Docs impact is claimed as the task's own once the…
## Raw request
> A doc named in passing in a task's Docs impact is claimed as the task's own once the other task that merged it closes (cli._claimed, T-2251), overriding the merge attribution (merged_in, T-2784): T-3442's close was refused for MASTER.md, which only T-3445's merge changed. A file merged_in names another task for stays theirs.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a doc another task's merge brought in stays theirs when this task's Docs impact names it and that task has closed — verify with `python3 plugin/tests/run.py test_lanes.Lanes test_execution`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then skip merged-in files in cli._claimed's soft docs
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_closed_tasks_merged_doc_named_in_docs_impact_stays_theirs` → ✗ exit 1 · Ran 1 tests in 64.3s (1 jobs, 16 at a time; slowest: Lanes 2s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree 9630b8b2fd7d] [world 2f1906870a] (2026-11-06T15:49:43Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes test_execution` → exit 0 · Ran 72 tests in 106.2s (71 jobs, 16 at a time; slowest: Lanes.test_the_edit_gate_in_a_lane_needs_that_lanes_task 2s, Lanes.test_another_lanes_merge_of_a_proved_file_asks_no_proof 2s, Lanes.test_anothe [ran] [tree d2dcdacf63b6] [world 2f1906870a] (2026-11-06T15:53:39Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes test_execution` → exit 0 · Ran 73 tests in 133.8s (59 jobs, 16 at a time; slowest: BoardClose 7s, Lanes.test_finish_after_two_other_merges_has_no_audit_gap 2s, Lanes.test_another_lanes_merge_of_a_proved_file_asks_no_proof 2s) / [ran] [tree 58067dbdda7f] [world 2f1906870a] (2026-11-06T16:02:47Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 524d68e9000f] (2026-11-06T16:08:07Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 195 tests in 120.6s (15 jobs, 16 at a time; slowest: LaneRecovery 26s, Lanes 23s, RaceEvidence 10s) / FAILED (1 classes: test_lanes.Lanes) (start tree + this task's tests) [ran] [tree 524d68e9000f] [world 2f1906870a] (2026-11-06T16:11:18Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 195 tests in 64.6s (144 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, PostMergeVerify 5s, LaneRecovery.test_every_stop_cause_has_one_recovery [ran] [tree 524d68e9000f] [world 2f1906870a] (2026-11-06T16:11:18Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.Lanes test_execution` → exit 0 · Ran 73 tests in 69.1s (59 jobs, 16 at a time; slowest: BoardClose 6s, Lanes.test_a_closed_tasks_merged_doc_named_in_docs_impact_stays_theirs 3s, Lanes.test_another_lanes_merge_of_a_proved_file_asks_no [ran] [tree 524d68e9000f] [world 2f1906870a] (2026-11-06T16:12:31Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 524d68e9000f] (2026-11-06T16:12:31Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 524d68e9000f] (2026-11-06T16:12:31Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 524d68e9000f] (2026-11-06T16:12:31Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 524d68e9000f] (2026-11-06T16:12:31Z)
## Log
- 2026-11-06T15:46:25Z created
- 2026-11-06T15:47:07Z set tier=S
- 2026-11-06T15:47:08Z planned: it has criteria and steps
- 2026-11-06T15:47:26Z criterion 1 removed: a doc another task's merge brought in stays theirs when this task's Docs impact names it and that task has closed — verify with `python3 plugin/tests/run.py test_lanes.LaneMergeSemantics test_execution`
- 2026-11-06T15:47:28Z lane: ~/.claude/foreman.lanes/T-3452 on foreman/T-3452
- 2026-11-06T15:49:43Z start point recorded late (no focus had kept one): its diff starts at c93f915
- 2026-11-06T16:02:48Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md']
- 2026-11-06T16:08:02Z merged foreman/T-3452 (3 file(s))
- 2026-11-06T16:08:02Z lane removed: ~/.claude/foreman.lanes/T-3452
- 2026-11-06T16:08:03Z focused
- 2026-11-06T16:08:05Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T16:08:06Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T16:08:07Z scope: widened at merge to the reviewed lane's own diff (1f53628d3), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T16:16:04Z done
- 2026-11-06T16:16:09Z committed 9ffb73b1a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2784 [FIX M, done, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's l…
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2776 [CLEAN S, done, 1 steps] fm bench duel --ablate stops offering gate-pipe: T-2765 made the gate-pipe note a guard deny, which is never ablatable, so the name leave…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_mint.py, p…
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- Attribution by commit subject must cover every kind of commit a landing makes: merges, their reverts, and docs named in passing.
## Plan gaps
- failed first: step 1 failing test, then skip merged-in files in cli._claimed's soft docs
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/tests/test_lanes.py
