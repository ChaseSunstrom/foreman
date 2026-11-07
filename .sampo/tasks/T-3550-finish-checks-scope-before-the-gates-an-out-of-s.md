---
id: T-3550
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_diff_gates.py, plugin/tests/test_round_f.py]
depends_on: []
source: discovered
created: 2026-11-07T00:29:11Z
updated: 2026-11-07T01:47:04Z
lane: ~/.claude/foreman.lanes/T-3550
lane_branch: foreman/T-3550
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:36:28Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_diff_gates.py]
---
# Finish checks scope before the gates: an out-of-scope edit refusal comes from done()…
## Raw request
> Finish checks scope before the gates: an out-of-scope edit refusal comes from done() after the full gate run (T-3163's close ran its gates, then was refused for one file outside scope). Add the scope-drift check to the pre-check gaps in cli.py (~line 1440, beside _finish_gaps) so it refuses with 'nothing ran'. Also: a base snapshot taken before another task removed an untracked file counts that removal as this task's edit (smap.changed vs base_tree; deleted files get touches=now, so a logged 'scope:' reason can never cover them) — a deleted file that was untracked at base and is absent from HEAD is no task's edit to scope.
## Interpretation
task finish refuses an out-of-scope edit only from done(), after every gate ran; move the same check into finish's 'nothing ran' pre-check gaps. And _task_files counts a deleted file that was untracked at base (removed by someone else) as this task's edit, which no scope reason can cover: leave such a file out.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a finish with an out-of-scope edit refuses with 'nothing ran' and runs no gate command; a removed untracked file present at base isn't counted — verify with `nice -n 10 python3 plugin/tests/run.py test_diff_gates`
## Non-goals
## Approach (options → choice → why)
Options: (a) a _scope_gaps(p,b) helper reusing _task_files + scope_drift + scope_reason_covers, added to finish's gaps; (b) run done()'s blockers dry before gates (too broad); (c) move the check out of done() (done must keep it). Choice: (a), sharing the reason text with done(). Deleted-untracked: in _task_files skip a changed file that no longer exists, is not in HEAD (git cat-file -e HEAD:f) and is not in this task's touches.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: finish refuses scope before gates; removed untracked base file not counted
2. [x] add the scope gap to finish's pre-checks and skip deleted untracked files in _task_files
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_diff_gates` → ✗ exit 1 · Ran 16 tests in 40.7s (2 jobs, 16 at a time; slowest: DiffGates 26s, LiveVerify 2s) / FAILED (1 classes: test_diff_gates.DiffGates) [ran] [tree fd4d46fd10a3] [world 2f1906870a] (2026-11-07T00:37:18Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_diff_gates` → exit 0 · Ran 16 tests in 2.9s (16 jobs, 16 at a time; slowest: DiffGates.test_edits_outside_scope_need_a_reason 2s, DiffGates.test_a_repo_with_no_commits_still_judges_the_task_by_its_own_changes 2s, DiffGates. [ran] [tree 88b8f60add55] [world 2f1906870a] (2026-11-07T00:38:04Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_diff_gates test_round_f test_close_gates test_bash_touch test_lanes test_diagnosis` → ✗ exit 1 · Ran 284 tests in 100.8s (44 jobs, 16 at a time; slowest: Lanes 100s, LaneRecovery 40s, CloseGates 37s) / FAILED (1 classes: test_round_f.RoundF) [ran] [tree 88b8f60add55] [world 2f1906870a] (2026-11-07T00:39:49Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_diff_gates test_round_f test_close_gates test_bash_touch test_lanes test_diagnosis` → exit 0 · Ran 284 tests in 91.3s (262 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, CloseGates.test_a_close_starts_a_full_run_when_the_last_one_is_old 6s, [ran] [tree c150ee5b9e2c] [world 2f1906870a] (2026-11-07T00:42:59Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_diff_gates` → ✗ exit 1 · Ran 16 tests in 42.8s (16 jobs, 16 at a time; slowest: DiffGates.test_edits_outside_scope_need_a_reason 3s, DiffGates.test_uncommitted_work_from_before_the_task_is_not_its_change 2s, DiffGates.test_an [ran] [tree bdd9fe50a630] [world 2f1906870a] (2026-11-07T00:50:54Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_diff_gates test_round_f test_close_gates test_bash_touch test_lanes test_diagnosis test_safety test_task_ergonomics test_cli` → exit 0 · Ran 521 tests in 166.8s (439 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 10s, StateViews.test_state_md_is_bounded 9s, RoundF.test_a_close_on_anothe [ran] [tree 8d6708719f6b] [world 2f1906870a] (2026-11-07T00:53:46Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_diff_gates` → exit 0 · Ran 16 tests in 5.6s (16 jobs, 16 at a time; slowest: DiffGates.test_edits_outside_scope_need_a_reason 3s, DiffGates.test_a_repo_with_no_commits_still_judges_the_task_by_its_own_changes 3s, DiffGates. [ran] [tree 8d6708719f6b] [world 2f1906870a] (2026-11-07T00:53:59Z)
## Log
- 2026-11-07T00:29:11Z created
- 2026-11-07T00:30:46Z set type=FIX, tier=S
- 2026-11-07T00:30:48Z planned: it has criteria and steps
- 2026-11-07T00:30:49Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_diff_gates.py']
- 2026-11-07T00:36:24Z lane: ~/.claude/foreman.lanes/T-3550 on foreman/T-3550
- 2026-11-07T00:36:27Z focused
- 2026-11-07T00:36:28Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T00:41:27Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_diff_gates.py', 'plugin/tests/test_round_f.py']
- 2026-11-07T01:47:04Z left out of a merge train: its merge turns the gates red: python3 plugin/tests/run.py on 181 affected test module(s), failing test_diff_gates.DiffGates
    stderr:fm: refused: T-0001 can't be marked done — one call settles most of it: sampo task finish T-0001 --run "<test cmd>" --audit "<how>":
      - edited outside scope [src/**]: docs/old.md; widen it (sampo task set T-0001 scope=…) or say why after your last edit of docs/old.md (sampo task log T-0001 "scope: <why>"; a reason logged before an edit doesn't cover it)
    Next: sampo next
    
    
    ----------------------------------------------------------------------
    Ran 1 test in 0.927s
    
    FAILED (failures=1)
    
      failed class: test_diff_gates.DiffGates.test_an_untracked_file_removed_since_the_start_is_not_this_tasks_edit
    
    Ran 5191 tests in 248.6s (2500 jobs, 16 at a time; slowest: Rendered 104s, LeanKindGateHookDelay 93s, LeanKindGateSessionLine 74s)
    
    FAILED (1 classes: test_diff_gates.DiffGates.test_an_untracked_file_removed_since_the_start_is_not_this_tasks_edit)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-2610 [FIX M, done, 3 steps] Calibration reads compare like with like: a close or a task or choice bet counts once its 30-day window finished — lesson: When one read of…
- decision 2026-11-05: T-3082 merges with night wired and drive left for a follow-up
- similar finished tasks took 2–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_sca…
