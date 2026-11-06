---
id: T-3372
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_cli.py, plugin/tests/test_cli_ergonomics.py, plugin/tests/test_task_ergonomics.py]
depends_on: []
source: discovered
created: 2026-11-06T06:20:54Z
updated: 2026-11-06T15:03:41Z
base: 735341d1e3d024f2e2db249c8a3956505bbf0b44
base_tree: 1e9db50aa1dd2dbc25d432a868fbfebbcd210343
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:46:12Z
plan0_scope: []
builder_returned: 2026-11-06T09:26:24Z
lane_stop: refused 2026-11-06T15:03:41Z
verified: strong
unproven: [docs, meaning]
postmerge_red: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims
postmerge_sha: d6022265ffea536a702b7a4e36042522be0dccc3
---
# Sampo task ac ID list silently adds a criterion named 'list' (T-3266 builder); unknown…
## Raw request
> FIX: sampo task ac ID list silently adds a criterion named 'list' (T-3266 builder); unknown ac verbs must be refused, and an 'ac rm N' verb is missing
## Interpretation
Reading 1: ac gains list and rm N; a lone lowercase word is refused instead of added. Reading 2 (ruled out): keep every unknown word as text, because the bug is exactly that.
## Assumptions (confidence)
## Acceptance criteria
- [x] ac list prints, rm removes (refused with evidence or out of range), bare word refused — verify with `python3 plugin/tests/run.py test_task_ergonomics`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: mirror task step (choices, remove_step pattern), refuse bare words in task_ac; likely outcome: works, fails if a one-word criterion was wanted. 2) Do less: refuse only in _task_shape, no rm; likely outcome: rm stays missing. 3) Require explicit add for ac; fails if scripts call ac ID text. Choice 1 (80%): smallest, same pattern as step.
## Risks and rollback
Blast radius: task_ac only. Revert the commit.
## Execution prompt
## Steps
1. [x] tests, then implement
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics` → ✗ exit 1 · Ran 38 tests in 70.8s (4 jobs, 16 at a time; slowest: SplitVerify 4s, TaskErgonomics 3s, ExpectFail 1s) / FAILED (2 classes: test_task_ergonomics.SplitVerify, test_task_ergonomics.TaskErgonomics) [ran] [tree 16b2dc7ed13e] [world 2f1906870a] (2026-11-06T08:47:32Z)
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics` → exit 0 · Ran 38 tests in 52.3s (4 jobs, 16 at a time; slowest: SplitVerify 5s, TaskErgonomics 3s, ExpectFail 1s) / OK [ran] [tree 297767be9489] [world 2f1906870a] (2026-11-06T08:48:45Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_docs test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_task_ergonomics test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 807 tests in 51.8s (197 jobs, 16 at a time; slowest: AffectedPairs 28s, KalevalaStep 9s, TaskLifecycle 8s) / FAILED (9 classes: test_cli.TaskLifecycle, test_cli.CaptureAndIntake, test_cli.AuditPre [ran] [tree 297767be9489] [world 2f1906870a] (2026-11-06T08:49:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_docs test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_task_ergonomics test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 807 tests in 50.0s (288 jobs, 16 at a time; slowest: AffectedPairs.test_only_the_red_first_file_itself_is_left_out 49s, AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 41s, Affe [ran] [tree b6742c918b2e] [world 2f1906870a] (2026-11-06T08:52:31Z)
- (step 1) `python3 plugin/tests/run.py test_task_ergonomics test_cli` → exit 0 · Ran 198 tests in 76.4s (59 jobs, 16 at a time; slowest: TaskLifecycle 20s, TaskErgonomics 10s, CaptureAndIntake 9s) / OK [ran] [tree b6742c918b2e] [world 2f1906870a] (2026-11-06T08:54:20Z)
- (step 1) `python3 plugin/tests/run.py test_cli_ergonomics test_task_ergonomics` → exit 0 · Ran 44 tests in 92.9s (36 jobs, 16 at a time; slowest: CliErgonomics 4s, SplitVerify.test_a_check_that_couldnt_import_its_test_module_can_be_corrected 3s, SplitVerify.test_a_small_tasks_steps_close_on [ran] [tree aaef08ee01a1] [world 2f1906870a] (2026-11-06T09:13:01Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_cli_ergonomics test_core test_docs test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_task_ergonomics test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 809 tests in 117.8s (354 jobs, 16 at a time; slowest: AffectedPairs.test_only_the_red_first_file_itself_is_left_out 42s, AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 32s, Kal [ran] [tree aaef08ee01a1] [world 2f1906870a] (2026-11-06T09:15:07Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree bf1e1ab6396f] (2026-11-06T10:51:17Z)
- (ac 1) `python3 plugin/tests/run.py test_task_ergonomics` → exit 0 · Ran 38 tests in 3.8s (21 jobs, 16 at a time; slowest: TaskErgonomics 3s, ExpectFail 1s, SplitVerify.test_a_small_tasks_steps_close_on_its_passing_criteria 1s) / OK [ran] [tree bf1e1ab6396f] [world 2f1906870a] (2026-11-06T10:51:23Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree bf1e1ab6396f] (2026-11-06T10:51:23Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree bf1e1ab6396f] (2026-11-06T10:51:23Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree bf1e1ab6396f] (2026-11-06T10:51:23Z)
## Log
- 2026-11-06T06:20:54Z created
- 2026-11-06T08:45:56Z planned: it has criteria and steps
- 2026-11-06T08:46:11Z focused
- 2026-11-06T08:46:12Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T10:51:15Z merged worktree-agent-a1137862daf6713c4 (6 file(s))
- 2026-11-06T10:51:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1137862daf6713c4
- 2026-11-06T10:51:16Z focused
- 2026-11-06T10:51:17Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'MASTER.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_cli_ergonomics.py', 'plugin/tests/test_task_ergonomics.py']
- 2026-11-06T10:51:17Z scope: widened at merge to the reviewed lane's own diff (d6022265f), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:51:57Z done
- 2026-11-06T10:52:00Z committed 3a2cf8460 (1 file)
- 2026-11-06T15:03:41Z red after merge: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims; d6022265f reverted (reached by: MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_cli.py, plugin/tests/test_cli_ergonomics.py, 1 left out)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-11-04: The gen-4 Mission brainstorms ran without their --deepen rounds: sampo ideas dropped them on its own because today's risk budget is spent (8 of 6: 6…
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 tests, then implement
## Files touched
- plugin/tests/test_task_ergonomics.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
- MASTER.md
- plugin/tests/test_cli.py
- plugin/tests/test_cli_ergonomics.py
- CHANGELOG.md
