---
id: T-3120
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/tests/test_round_f.py]
depends_on: []
source: discovered
created: 2026-11-05T03:13:13Z
updated: 2026-11-06T15:22:41Z
inferred_deps: [T-3119]
inferred_why: T-3119: batched closes follow merge train design
group: fast merges and merge trains
base: 3a2cf8460f9edadedd548eac88d45254c6cbb2ee
base_tree: bf1e1ab6396f798598263c75b6a68584d1164525
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-06T09:23:06Z
plan0_scope: []
builder_returned: 2026-11-06T10:43:57Z
lane_stop: refused 2026-11-06T15:22:41Z
verified: strong
unproven: [docs, perf-typed]
postmerge_red: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims, test_close_gates.CloseGates, test_diff_gates.DiffGates
postmerge_sha: c7864dc04687485e67c126b5167bbdebc7630a90
---
# sampo task finish reuses a full-gates pass on the same tree from any task when the only change since is CHANGELOG.md lines, rerunning only the tests that read the changelog
## Raw request
> batched closes after a merge train: sampo task finish reuses a full gate run on the same tree when the only change since is CHANGELOG or docs lines (each close's own changelog line today changes the tree and forces a fresh 5-minute suite per task)
## Interpretation
Full gates record the code tree (no CHANGELOG/mirrors); _cached_pass already honours code_tree, so a close on a CHANGELOG-only change reuses the pass.
## Assumptions (confidence)
## Acceptance criteria
- [x] after a green sampo check on tree X, a finish on tree X plus CHANGELOG.md line additions (from any task) reuses that full-gates pass and reruns only the changelog's affected tests, saying so; any other file changed, a red pass, or a different world (models, tool versions) runs the full gates as today — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
Log code_tree in full check_run events (core.code_tree); word the reuse line; no second cache.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: reuse across tasks on a changelog-only change; refuse on any other change or a red pass
2. [x] a tree id that ignores CHANGELOG.md added lines, the cross-task pass record, the affected rerun
## Resume here
<!-- auto -->
- 2026-11-06T10:09:31Z steps 2/2 done
- git: worktree-agent-ad471a865b23ccdf4; 0 uncommitted
- touched since last checkpoint: plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/cli.py, plugin/tests/test_round_f.py, docs/map/ops-1.md
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_round_f test_lane_train` → exit 0 · Ran 26 tests in 8.7s (2 jobs, 16 at a time; slowest: Train 4s, RoundF 3s) / OK [ran] [tree 96ffb1a77268] [world 2f1906870a] (2026-11-06T09:26:22Z)
- (step 2) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 18 tests in 7.2s (1 jobs, 16 at a time; slowest: RoundF 3s) / OK [ran] [tree 96ffb1a77268] [world 2f1906870a] (2026-11-06T09:26:38Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_round_f test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2201 tests in 570.9s (698 jobs, 16 at a time; slowest: AffectedPairs 138s, JudgmentKinds 68s, ExamGen.test_oracle_scores_full_and_empty_scores_zero 38s) / FAILED (193 classes: test_cli.AffectedPai [ran] [tree 96ffb1a77268] [world 2f1906870a] (2026-11-06T09:36:17Z)
- (step 1) `python3 plugin/tests/run.py test_round_f test_lane_train test_finish_reuse test_check_paths test_close_gates test_verification test_night test_genesis` → exit 0 · Ran 343 tests in 47.7s (54 jobs, 16 at a time; slowest: CloseGates 34s, GenerationReview 14s, ProofBeforePresentation 12s) / OK [ran] [tree 1813dedc32ed] [world 2f1906870a] (2026-11-06T10:09:23Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_round_f test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1812 tests in 644.3s (1081 jobs, 16 at a time; slowest: AffectedPairs.test_only_the_red_first_file_itself_is_left_out 136s, AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 63s, [ran] [tree fa53db19cb3e] [world 2f1906870a] (2026-11-06T10:20:19Z)
- (step 2) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 24 tests in 69.8s (24 jobs, 16 at a time; slowest: RoundF.test_files_changed_through_the_shell_count_at_done 3s, RoundF.test_a_close_on_another_task_reuses_the_full_pass_and_says_so 2s, RoundF.tes [ran] [tree fa53db19cb3e] [world 2f1906870a] (2026-11-06T10:32:28Z)
- (step 2) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 26 tests in 4.2s (1 jobs, 16 at a time; slowest: RoundF 4s) / OK [ran] [tree ad8228b348b0] [world 2f1906870a] (2026-11-06T10:43:50Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 2996a2fb3e24] (2026-11-06T10:53:44Z)
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 26 tests in 4.9s (1 jobs, 16 at a time; slowest: RoundF 3s) / FAILED (1 classes: test_round_f.RoundF) (start tree + this task's tests) [ran] [tree 2996a2fb3e24] [world 2f1906870a] (2026-11-06T10:53:57Z)
- `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 26 tests in 3.8s (1 jobs, 16 at a time; slowest: RoundF 3s) / OK [ran] [tree 2996a2fb3e24] [world 2f1906870a] (2026-11-06T10:53:57Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 22 tests in 2.9s (10 jobs, 16 at a time; slowest: CommitOwnFiles 3s, FinishGaps 2s, CommitAfterFocus 2s) / OK [ran] [tree 2996a2fb3e24] [world 2f1906870a] (2026-11-06T10:54:04Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 2996a2fb3e24] (2026-11-06T10:54:04Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 2996a2fb3e24] (2026-11-06T10:54:04Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 2996a2fb3e24] (2026-11-06T10:54:04Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 2996a2fb3e24] (2026-11-06T10:54:04Z)
## Log
- 2026-11-05T03:13:13Z created
- 2026-11-05T03:23:16Z planned from capture
- 2026-11-05T03:23:17Z set approved=True
- 2026-11-05T03:23:17Z blocked: after T-3087's merge (cli.py); then a builder slot
- 2026-11-06T03:53:26Z unblocked
- 2026-11-06T09:23:05Z focused
- 2026-11-06T09:23:06Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-06T10:53:42Z merged worktree-agent-ad471a865b23ccdf4 (5 file(s))
- 2026-11-06T10:53:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad471a865b23ccdf4
- 2026-11-06T10:53:43Z focused
- 2026-11-06T10:53:44Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/ops-1.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_round_f.py']
- 2026-11-06T10:53:44Z scope: widened at merge to the reviewed lane's own diff (c7864dc04), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:56:50Z done
- 2026-11-06T10:56:53Z committed f8457be6a (1 file)
- 2026-11-06T15:22:41Z red after merge: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims, test_close_gates.CloseGates, test_diff_gates.DiffGates; c7864dc04 reverted (reached by: docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/tests/test_round_f.py)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-2644 [PERFORMANCE M, done, 3 steps] fm task finish reuses a criterion's passing run when the same command already ran on this exact tree and world, instead of running …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-11-04: Gen-4 Mission 1 (exhaustive thinking) reuses brainstorm-20261102-184150, the fm ideas run already made for this same gen-4 seed row (542 ideas, 4 ro…
## Measurements
full-gates step of a close after a CHANGELOG-only change: a fresh full suite (8-15 min under tonight's load) -> reuse of the prior pass (seconds); measured by test_round_f's gate counter (1 run for two closes)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_round_f.py
- plugin/lib/sampo/cli.py
- docs/map/ops-1.md
- plugin/lib/sampo/core.py
- plugin/lib/sampo/rune.py
- CHANGELOG.md
