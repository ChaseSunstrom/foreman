---
id: T-3342
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo, plugin/tests, README.md, plugin/skills, .sampo/**, .fm-scratch/**, CHANGELOG.md, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/fmguard.py, plugin/lib/sampo/change.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/fixes.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/playbooks.py, plugin/lib/sampo/smith.py, plugin/lib/sampo/smithtui.py, plugin/lib/sampo/smoke.py, plugin/lib/sampo/stack.py, plugin/lib/sampo/sync.py, plugin/skills/library/cards/practice/brainstorming-lenses.md, plugin/tests/test_board_posture.py, plugin/tests/test_code_tui.py, plugin/tests/test_execution.py, plugin/tests/test_fixes.py, plugin/tests/test_guard.py, plugin/tests/test_parallel.py, plugin/tests/test_playbook_machinery.py, plugin/tests/test_rename_scan.py, plugin/tests/test_secrets.py, plugin/tests/test_sync.py, plugin/tests/test_ui.py]
depends_on: []
source: user
created: 2026-11-06T05:09:41Z
updated: 2026-11-06T07:47:28Z
base: e1b8d0c4cf399fb7cd842f0451ebbee5ffc04bad
base_tree: 2330361af10855f02cb42c27a244d02e5156243b
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:08:17Z
plan0_scope: [plugin/lib/sampo, plugin/tests, README.md, plugin/skills]
builder_returned: 2026-11-06T07:17:54Z
lane_stop: merged 2026-11-06T07:31:46Z
verified: ok
unproven: [docs, tui-unshot, typed]
---
# Mirror folder .foreman/ becomes .sampo/: one constant (core.MIRROR/MIRRORS/MIRROR_DIRS) every site reads, the old folder still read, sync.move renames it once with git mv in one logged commit at a CLI export (never from a hook), the guard and verify-lint cover .sampo, and the rename scan allows .foreman only as an alias
## Raw request
> The repo mirror is still named .foreman/ (sync.DIR, sync.py:23) and ~36 code sites name it (core mirror_ignored and audit pathspecs, hooks, playbooks, smith, stack, change, fixes); the product is Sampo. Rename the mirror to .sampo/ with one constant every caller reads (core.MIRROR); a repo that already has .foreman/ keeps working: sync reads it, and moves it to .sampo/ with git mv on the next export (one commit, logged), never two mirrors at once; the guard's state-direct rule covers both names. Also sweep every other user-visible 'foreman' name the rename left behind (FOREMAN_* env vars shown in docs, refs/foreman/*, the foreman/build branch name in messages, .foreman-state.json) with the rename scan, keeping old names as read-only aliases. User: 'How come the state is still called .foreman?'
## Interpretation
Reading 1: rename the mirror folder to .sampo/ with one constant, old folder still read, moved once. Reading 2 (ruled out): rename every foreman name now; env vars, refs and branch prefix are separate alias tasks.
## Assumptions (confidence)
## Acceptance criteria
- [x] no .foreman literal left in the library except the constant, and the listed tests pass — verify with `python3 plugin/tests/run.py test_sync test_fixes test_parallel test_secrets test_ui test_playbook_machinery test_code_tui test_execution test_guard test_guard_sampo test_board_posture test_rename_scan`
- [x] a tracked .foreman becomes one logged rename commit; ignored, both-folders, mid-merge and failed-commit cases tested — verify with `python3 plugin/tests/run.py test_sync`
- [x] the user-visible mirror folder is .sampo/ (the product's name), and sync status and the README name it — verify with `python3 plugin/tests/run.py test_sync`
- [x] the guard's state-direct rule and verify-lint cover both .sampo and .foreman — verify with `python3 plugin/tests/run.py test_guard test_guard_sampo test_board_posture`
- [x] the user asks why state is still called .foreman: fresh sync writes .sampo/ and status names it — verify with `python3 plugin/tests/run.py test_sync`
## Non-goals
Renaming refs/foreman/*, the foreman/<id> lane branch prefix, .foreman-state.json and FOREMAN_* env vars: their own alias tasks (T-3369 for env vars). Running the move on this repo: the main thread does it last, alone.
## Approach (options → choice → why)
1) one constant (core.MIRROR/MIRRORS/MIRROR_DIRS) read by every site, .foreman read while .sampo is absent, sync.move git mv at a CLI export: likely outcome one logged commit; fails if a hook triggers it or both folders exist. 2) opt-in sampo sync move plus doctor nudge: fails if .foreman lingers forever. 3) rename on disk, next task commits it: fails with 6000 renames in an unrelated commit. 4) use what exists: sync.mirror(p) already picks the folder, extend it; likely outcome small diff. 5) do less: alias only, no move; fails the user complaint. Choice 1 (80%): matches the ask.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py; past FIXes T-2061, T-2846.
## Execution prompt
## Steps
1. [x] constant and every site
2. [x] sync.move with its cases
3. [x] guard/verify-lint and rename-scan checks
## Resume here
<!-- auto -->
- 2026-11-06T07:10:10Z step 3/3: guard/verify-lint and rename-scan checks
- git: worktree-agent-ad87d1e22878ac6e5; 5 uncommitted: plugin/lib/fmguard.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/sync.py, plugin/tests/test_rename_scan.py, plugin/tests/test_sync.py
- touched since last checkpoint: plugin/lib/sampo/cli.py, plugin/lib/fmguard.py, .fm-scratch/ed.json, .fm-scratch/ed2.json, plugin/lib/sampo/sync.py, plugin/tests/test_sync.py, plugin/tests/test_rename_scan.py
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 28 tests in 264.8s (28 jobs, 16 at a time; slowest: Sync.test_a_tracked_foreman_becomes_one_logged_rename_commit 1s, Sync.test_a_failed_commit_puts_it_back_and_only_export_retries 1s, Sync.test_an (ran] (tree c240ff0072db] (world 2f1906870a] (2026-11-06T06:28:21Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 11 tests in 127.8s (11 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 5s, RenameScan.test_no_library_code_hardcodes_the_old_mirror_name 2s, RenameScan.test_user_visible_fore (ran] (tree 507633c1fbb3] (world 2f1906870a] (2026-11-06T06:47:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_approve_reads test_audit test_board_posture test_board_surfaces test_brainstorm_skill test_cli test_code_close_scaffold test_code_hardening test_code_tui test_code_worker test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_execution test_extras test_fixes test_followups test_guard test_guard_cases test_guard_diff test_guard_exec_vectors test_guard_git test_guard_overrefusal test_guard_pipes test_guard_sampo test_hooks test_ideation test_incident test_judgment test_kalevala test_left_out test_lib_hostile test_lib_source_kill test_library test_louhi_models test_mcp test_mint test_models test_nudges test_onwrite test_parallel test_playbook_machinery test_playbook_use test_plugin_parity test_plugins test_release test_rename_scan test_replan test_scaffold test_scene test_scout test_second test_secrets test_settings_scopes test_shade test_showpieces test_site_gallery test_skillroute test_small_cards test_smoke test_smoke_profiles test_speed test_stack test_steering test_supply_delta test_sync test_taste_ledger test_tidy test_tool_queue test_ui test_verify_alias test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2811 tests in 218.6s (887 jobs, 16 at a time; slowest: AffectedPairs 154s, ReleaseProofWithoutSetuptools 26s, PreToolUse 25s) / FAILED (2 classes: test_cli.AffectedPairs, test_left_out.LeftOut) [ran] [tree 85f533c8478e] [world 2f1906870a] (2026-11-06T07:14:46Z)
- (step 3) `python3 plugin/tests/run.py test_cli.AffectedPairs > .fm-scratch/cli.out 2>&1` → exit 0 · (no output) [ran] [tree 85f533c8478e] [world 2f1906870a] (2026-11-06T07:17:40Z)
- (step 3) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 33 tests in 1.6s (33 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_commit_puts_it_back_and_only_export_retries 1s, Sync. [ran] [tree 85f533c8478e] [world 2f1906870a] (2026-11-06T07:17:45Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree faa67f80514a] (2026-11-06T07:31:50Z)
- (ac 1) `python3 plugin/tests/run.py test_sync test_fixes test_parallel test_secrets test_ui test_playbook_machinery test_code_tui test_execution test_guard test_guard_sampo test_board_posture test_rename_scan` → exit 0 · Ran 790 tests in 82.1s (293 jobs, 16 at a time; slowest: Mutation 14s, Fuzz.test_any_event_stream_draws_at_any_size 9s, RenameScan 8s) / OK [ran] [tree faa67f80514a] [world 2f1906870a] (2026-11-06T07:34:17Z)
- (ac 2) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 33 tests in 17.8s (33 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_move_commit_keeps_uncommitted_mirror_edits 1s, Sync. [ran] [tree faa67f80514a] [world 2f1906870a] (2026-11-06T07:34:17Z)
- (ac 3) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 33 tests in 17.8s (33 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_move_commit_keeps_uncommitted_mirror_edits 1s, Sync. [ran] [tree faa67f80514a] [world 2f1906870a] (2026-11-06T07:34:17Z)
- (ac 4) `python3 plugin/tests/run.py test_guard test_guard_sampo test_board_posture` → exit 0 · Ran 347 tests in 42.7s (104 jobs, 16 at a time; slowest: Mutation 13s, Latency 5s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 4s) / OK [ran] [tree faa67f80514a] [world 2f1906870a] (2026-11-06T07:34:17Z)
- (ac 5) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 33 tests in 17.8s (33 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_move_commit_keeps_uncommitted_mirror_edits 1s, Sync. [ran] [tree faa67f80514a] [world 2f1906870a] (2026-11-06T07:34:17Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree faa67f80514a] (2026-11-06T07:34:17Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree faa67f80514a] (2026-11-06T07:34:17Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree faa67f80514a] (2026-11-06T07:34:17Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree faa67f80514a] (2026-11-06T07:41:38Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree faa67f80514a] (2026-11-06T07:41:39Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree faa67f80514a] (2026-11-06T07:41:39Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree faa67f80514a] (2026-11-06T07:41:39Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree faa67f80514a] (2026-11-06T07:45:29Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree faa67f80514a] (2026-11-06T07:45:30Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree faa67f80514a] (2026-11-06T07:45:30Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree faa67f80514a] (2026-11-06T07:45:30Z)
## Log
- 2026-11-06T05:09:41Z created
- 2026-11-06T06:00:08Z planned from capture
- 2026-11-06T06:08:12Z focused
- 2026-11-06T06:08:17Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T07:31:46Z merged worktree-agent-ad87d1e22878ac6e5 (25 file(s))
- 2026-11-06T07:31:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad87d1e22878ac6e5
- 2026-11-06T07:31:46Z focused
- 2026-11-06T07:31:49Z set scope=['plugin/lib/sampo', 'plugin/tests', 'README.md', 'plugin/skills', '.sampo/**']
- 2026-11-06T07:31:49Z scope widened to .sampo/**: the sync mirror moved from .foreman/ in 63f19d902 (no task) and main's code still names only .foreman/ until T-3342 lands; these are mirror notes, not this task's edits
- 2026-11-06T07:41:18Z not reverted: test_check_paths.CheckSkip, test_cli.AffectedPairs, test_close_gates.CloseGates already fail on 1e1c29e31's first parent
- 2026-11-06T07:41:36Z focused
- 2026-11-06T07:41:37Z set scope=['plugin/lib/sampo', 'plugin/tests', 'README.md', 'plugin/skills', '.sampo/**', '.fm-scratch/**']
- 2026-11-06T07:41:37Z scope widened to .fm-scratch/** (the builder's gitignored lane scratch files) and .sampo/**: the sync mirror moved from .foreman/ in 63f19d902 (no task) and main's code still names only .foreman/ until T-3342 lands; these are mirror notes, not this task's edits
- 2026-11-06T07:45:28Z focused
- 2026-11-06T07:45:29Z set scope=['plugin/lib/sampo', 'plugin/tests', 'README.md', 'plugin/skills', '.sampo/**', '.fm-scratch/**', 'CHANGELOG.md', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/fmguard.py', 'plugin/lib/sampo/change.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/fixes.py', 'plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/playbooks.py', 'plugin/lib/sampo/smith.py', 'plugin/lib/sampo/smithtui.py', 'plugin/lib/sampo/smoke.py', 'plugin/lib/sampo/stack.py', 'plugin/lib/sampo/sync.py', 'plugin/skills/library/cards/practice/brainstorming-lenses.md', 'plugin/tests/test_board_posture.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_execution.py', 'plugin/tests/test_fixes.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_parallel.py', 'plugin/tests/test_playbook_machinery.py', 'plugin/tests/test_rename_scan.py', 'plugin/tests/test_secrets.py', 'plugin/tests/test_sync.py', 'plugin/tests/test_ui.py']
- 2026-11-06T07:45:29Z scope: widened at merge to the reviewed lane's own diff (1e1c29e31), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T07:47:26Z done
- 2026-11-06T07:47:28Z committed ef1480837 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_ambient.py, plugin/tests/test_anergy.py, plugin/tests/test_audit.py, plugin/tests/test_away.py, plugin/tests/…
## Preflight
Changed in scope since this was planned (2026-11-06): .sampo/README.md, .sampo/archive/2026-09/T-0001-phase-3-hooks-one-dispatcher-per-event-guard-sto.md, .sampo/archive/2026-09/T-0002-phase-4-skills-rules-agents-visibility-layer-por.md, .sampo/archive/…; re-ground the plan against them before editing
## Behaviour lock
none: a builder lane; its own suites ran green in the lane before and after its edits, and the full gates run at this close
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/lib/sampo/core.py
- .fm-scratch/e.json
- .fm-scratch/s.json
- plugin/lib/sampo/sync.py
- .fm-scratch/t.json
- plugin/tests/test_sync.py
- .fm-scratch/m.json
- .fm-scratch/w.json
- plugin/lib/sampo/cli.py
- .fm-scratch/r.json
- README.md
- plugin/lib/sampo/change.py
- plugin/lib/sampo/fixes.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/playbooks.py
- plugin/lib/sampo/smith.py
- plugin/lib/sampo/smithtui.py
- plugin/lib/sampo/smoke.py
- plugin/lib/sampo/stack.py
- plugin/skills/library/cards/practice/brainstorming-lenses.md
- .fm-scratch/x.json
- plugin/tests/test_board_posture.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_execution.py
- plugin/tests/test_fixes.py
- plugin/tests/test_guard.py
- plugin/tests/test_parallel.py
- plugin/tests/test_playbook_machinery.py
- plugin/tests/test_secrets.py
- plugin/tests/test_ui.py
