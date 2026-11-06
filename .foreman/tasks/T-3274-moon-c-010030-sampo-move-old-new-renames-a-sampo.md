---
id: T-3274
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/movemod.py, plugin/tests/test_movemod.py, plugin/lib/sampo/cli.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-11-06T02:27:49Z
updated: 2026-11-06T04:34:16Z
builder: 2026-11-06T02:27:56Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a426fb9da61abd0f7
lane_branch: worktree-agent-a426fb9da61abd0f7
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:32Z
plan0_scope: [plugin/lib/sampo/movemod.py, plugin/tests/test_movemod.py, plugin/lib/sampo/cli.py, CHANGELOG.md, MASTER.md]
builder_returned: 2026-11-06T04:34:16Z
---
# Moon C-010030: sampo move OLD NEW renames a sampo module and rewrites every import and reference, then proves it by importing every module
## Raw request
> Moon C-010030: sampo move OLD NEW renames a sampo module and rewrites every import and reference, then proves it by importing every module
## Interpretation
Reading 1 (chosen): a module mover for Sampo's own package: sampo move OLD NEW renames plugin/lib/sampo/OLD.py and rewrites every reference, proven by importing every module. Reading 2 (ruled out): moving arbitrary files in any codebase; sampo rewrite already renames identifiers, and a generic mover needs per-language import rules, too big for one lane. Partial: rewrite exists at plugin/lib/sampo/change.py:202 (identifiers only, no file move, no import proof).
## Assumptions (confidence)
## Acceptance criteria
- [ ] dry run lists the files and sites it would change and writes nothing; --apply git-mvs the module and rewrites its imports, dotted uses, file-path mentions and test names in code, tests and docs, leaving no alias — verify with `python3 plugin/tests/run.py test_movemod`
- [ ] --apply refuses a NEW that already exists or an OLD that is not a module, and --alias leaves a sys.modules shim like plugin/lib/fmcli.py — verify with `python3 plugin/tests/run.py test_movemod`
- [ ] after --apply every module under plugin/lib/sampo imports in a fresh interpreter and the proof prints the affected tests to run; a failed import rolls the move back — verify with `python3 plugin/tests/run.py test_movemod`
## Non-goals
## Approach (options → choice → why)
1. New movemod.py: regex plan over git ls-files for import, dotted and path forms, git mv, subprocess import proof, rollback. Likely outcome: small, no collision with big files, covers the real alias pain.
2. Extend change.rewrite with a file-move mode. Likely outcome: reuses token rewriting but change.py grows and the identifier rule does not fit dotted module paths.
3. Use Python ast/libcst for exact import rewriting. fails if: libcst is not installed and docs and tests mention paths as text anyway.
4. Do less: only print the plan, no apply. Likely outcome: leaves the risky edit by hand, little value.

Choice 1 (85%): isolated new module, regex is enough because the proof import and the tests catch misses. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] write test_movemod.py first: a temp git repo with a tiny package (a.py imported by b.py, a test and a doc), red  <- CURRENT
2. [x] write plugin/lib/sampo/movemod.py: plan finds files and sites by regex on import, dotted and path forms; apply does git mv and atomic writes; prove imports every module in a subprocess python -I; rollback on failure; --alias writes the shim
3. [x] register move in cli.py with lazy() next to rewrite (flags --apply --alias)
4. [x] CHANGELOG line and a MASTER.md mention beside rewrite; run test_movemod
## Resume here
<!-- auto -->
- 2026-11-06T04:31:06Z step 1/4: write test_movemod.py first: a temp git repo with a tiny package (a.py imported by b.py, a test and a doc), red
- git: worktree-agent-a426fb9da61abd0f7; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_movemod` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 1.5s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree d4b356c33d2b] [world 2f1906870a] (2026-11-06T02:31:21Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_movemod` → exit 0 · Ran 7 tests in 25.2s (7 jobs, 16 at a time; slowest: MoveModTest.test_a_failed_import_rolls_the_move_back 9s, MoveModTest.test_a_bare_name_clash_in_a_file_blocks_the_move 5s, MoveModTest.test_apply_mo [ran] [tree ed991656961d] [world 2f1906870a] (2026-11-06T02:41:44Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_movemod` → exit 0 · Ran 7 tests in 21.0s (7 jobs, 16 at a time; slowest: MoveModTest.test_the_proof_names_the_affected_tests 4s, MoveModTest.test_alias_leaves_a_sys_modules_shim_like_the_fm_shims 3s, MoveModTest.test_app [ran] [tree ee583f1adf5c] [world 2f1906870a] (2026-11-06T02:45:29Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_movemod test_docs` → ✗ exit 1 · Ran 122 tests in 98.1s (35 jobs, 16 at a time; slowest: Fences 90s, DocsProof 86s, TaskLifecycle 49s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree ee583f1adf5c] [world 2f1906870a] (2026-11-06T02:47:46Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_movemod test_rename_scan test_docs` → ✗ exit 1 · Ran 131 tests in 139.8s (93 jobs, 16 at a time; slowest: RenameScan 95s, TaskLifecycle 74s, Fences.test_the_documented_runnable_fences_run_green_in_a_temp_home 53s) / FAILED (1 classes: test_docs.Fenc [ran] [tree 0107fed94228] [world 2f1906870a] (2026-11-06T02:50:48Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_movemod test_rename_scan` → exit 0 · Ran 17 tests in 145.8s (17 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 123s, RenameScan.test_user_visible_foreman_only_goes_down 14s, MoveModTest.test_the_proof_names_the_aff [ran] [tree 0107fed94228] [world 2f1906870a] (2026-11-06T02:54:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_movemod test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2349 tests in 1341.7s (801 jobs, 16 at a time; slowest: LeanKindGateSessionLine 394s, LeanKindGateGuardAllow 391s, LeanKindGateHookDelay 383s) / FAILED (1 classes: test_bookkeeping.FinishGaps) [ran] [tree 0107fed94228] [world 2f1906870a] (2026-11-06T03:17:01Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_movemod test_bookkeeping.FinishGaps.test_a_refused_field_naming_a_section_says_how_to_fill_it` → exit 0 · Ran 8 tests in 43.3s (8 jobs, 16 at a time; slowest: FinishGaps 28s, MoveModTest.test_a_failed_import_rolls_the_move_back 5s, MoveModTest.test_dry_run_names_every_site_and_writes_nothing 4s) / OK [ran] [tree a842eb3ee917] [world 2f1906870a] (2026-11-06T03:20:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_movemod test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [72.17s] [ran] [tree a842eb3ee917] [world 2f1906870a] (2026-11-06T03:35:47Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_movemod` → ✗ exit 1 · Ran 11 tests in 4.5s (1 jobs, 2 at a time; slowest: MoveModTest 2s) / FAILED (1 classes: test_movemod.MoveModTest) [ran] [tree 49f66806df5b] [world 2f1906870a] (2026-11-06T04:33:16Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_movemod` → exit 0 · Ran 11 tests in 9.6s (1 jobs, 2 at a time; slowest: MoveModTest 5s) / OK [ran] [tree e22072f25c09] [world 2f1906870a] (2026-11-06T04:34:05Z)
## Log
- 2026-11-06T02:27:49Z created
- 2026-11-06T02:27:55Z set scope=['plugin/lib/sampo/movemod.py', 'plugin/tests/test_movemod.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-11-06T02:27:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3274.builder.md
- 2026-11-06T02:28:31Z focused
- 2026-11-06T02:28:32Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:42:08Z steer: scope widened to plugin/lib/fmmovemod.py, the fm shim a new plugin/lib module needs (standing rule)
- 2026-11-06T02:44:40Z steer: scope widened to docs/map/files-lib-1.md (the map entry for the new fmmovemod shim, beside fmchange, as the brief's docs step asks)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
