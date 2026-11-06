---
id: T-3275
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/shape.py, plugin/tests/test_shape.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:51Z
updated: 2026-11-06T04:41:37Z
builder: 2026-11-06T02:28:00Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a2289859d06ade9df
lane_branch: worktree-agent-a2289859d06ade9df
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:33Z
plan0_scope: [plugin/lib/sampo/shape.py, plugin/tests/test_shape.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:41:37Z
---
# Moon C-000723: sampo shape FILE drafts the companions a new file is owed (test, alias, MASTER line) learned from how past files were added
## Raw request
> Moon C-000723: sampo shape FILE drafts the companions a new file is owed (test, alias, MASTER line) learned from how past files were added
## Interpretation
Reading 1 (chosen): given a new or partly written file, learn from git history which companions earlier same-shaped files were added with (test module, plugin/lib fm alias, MASTER.md line) and print drafted stubs. Reading 2 (ruled out): extend loop.lag/map.drift to draft stubs; they answer 'which existing files are owed an update' in aggregate (map.py:158, loop.py:59) and have no notion of a new file's stem, so templated companions need their own module. Partial: drift/_co_change exist; this adds the per-new-file stem templating and drafts.
## Assumptions (confidence)
## Acceptance criteria
- [ ] shape.owed(root, new_file) returns companions learned from past add-commits of same-shaped files, with stem templates (tests/test_<stem>.py) and a count/share per companion, on a fixture repo — verify with `python3 plugin/tests/run.py test_shape`
- [ ] shape.draft() returns a stub for each templated companion that is missing (copied from the newest existing sibling with the stem swapped) and the last-added-line format for shared append files (MASTER.md, CHANGELOG.md); nothing is written without --write — verify with `python3 plugin/tests/run.py test_shape`
- [ ] sampo shape plugin/lib/sampo/x.py runs via the CLI and prints one line per owed file, and says nothing owed when history gives no pattern — verify with `python3 plugin/tests/run.py test_shape`
## Non-goals
## Approach (options → choice → why)
1. New module shape.py: scan git log --diff-filter=A for files in the same directory and extension, find co-added files, generalise their names by replacing the stem with a placeholder, keep templates seen in at least 3 commits and 50 percent of them. Likely outcome: finds test and alias files with no hardcoded list; no big-file collision.
2. Extend map.drift to take a file argument. Likely outcome: reuses code but map.py is shared and drift is aggregate, so the stem logic bloats it.
3. Hardcode a table of owed files per folder. fails if: a new convention appears, and the user rejected hardcoded lists.
4. Do less: only report owed templates, no stubs. Likely outcome: cheap but leaves the writing to the user, which is the moon's point.

Choice 1 (85%): own module learned from add-commits, stubs drafted read-only unless --write. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] Failing test: fixture git repo where 4 past commits each add src/NAME.py with tests/test_NAME.py and a MASTER.md line; assert owed + draft for a new src/foo.py  <- CURRENT
2. [x] Implement plugin/lib/sampo/shape.py: owed(), draft(), cmd_shape (reuse map._git / map._co_change style git log)
3. [x] Register verb 'shape' in cli.py via lazy(), run test_shape and test_map
## Resume here
<!-- auto -->
- 2026-11-06T04:40:42Z step 1/3: Failing test: fixture git repo where 4 past commits each add src/NAME.py with tests/test_NAME.py and a MASTER.md line; assert owed + draft for a new src/foo.py
- git: worktree-agent-a2289859d06ade9df; 6 uncommitted: MASTER.md, docs/map/files-lib-3.md, plugin/lib/sampo/cli.py, plugin/lib/fmshape.py, plugin/lib/sampo/shape.py, plugin/tests/test_shape.py
- touched since last checkpoint: plugin/tests/test_shape.py, plugin/lib/sampo/shape.py, docs/map/files-lib-3.md
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_shape` → ✗ exit 1 (never ran: no tests ran) · Ran 1 tests in 2.3s (2 jobs, 16 at a time; slowest: Format 0s, loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (ran] (tree 4b92a706460f] (world 2f1906870a] (2026-11-06T02:31:08Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k test_owed_learns -k test_no_same_shaped -k test_draft_copies -k test_a_stem_that test_shape` → exit 0 · Ran 4 tests in 20.7s (4 jobs, 16 at a time; slowest: Shape.test_no_same_shaped_history_owes_nothing 6s, Shape.test_a_stem_that_is_not_a_plain_name_owes_nothing_and_writes_nothing 4s, Shape.test_draft_ (ran] (tree 9c132af4ae59] (world 2f1906870a] (2026-11-06T02:36:49Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_shape test_map test_docs test_rename_scan` → exit 0 · Ran 143 tests in 93.1s (119 jobs, 16 at a time; slowest: RenameScan.test_no_fm_only_command_regex 51s, Fences.test_fm_new_lists_copies_and_never_overwrites 50s, Fences.test_the_documented_runnable_fen (ran] (tree dccdc26dc845] (world 2f1906870a] (2026-11-06T02:45:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_shape test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2383 tests in 1101.9s (808 jobs, 16 at a time; slowest: LeanKindGateHookDelay 484s, LeanKindGateSessionLine 464s, LeanKindGateGuardAllow 453s) / FAILED (2 classes: test_hooks.NoTaskGateRefusals, t (ran] (tree dccdc26dc845] (world 2f1906870a] (2026-11-06T03:03:58Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_shape` → exit 0 · Ran 13 tests in 29.0s (13 jobs, 2 at a time; slowest: Shape.test_an_absolute_path_names_the_same_file_as_a_repo_relative_one 9s, Shape.test_the_cli_prints_one_line_per_owed_file_and_says_nothing_owed_ (ran] (tree 4f613b8485c3] (world 2f1906870a] (2026-11-06T04:35:43Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_shape test_map test_docs test_rename_scan` → exit 0 · Ran 148 tests in 291.5s (112 jobs, 2 at a time; slowest: RenameScan.test_no_fm_only_command_regex 24s, Fences.test_fm_new_lists_copies_and_never_overwrites 23s, Fences.test_the_documented_runnable_fen (ran] (tree 83b10aebe071] (world 2f1906870a] (2026-11-06T04:40:39Z)
## Log
- 2026-11-06T02:27:51Z created
- 2026-11-06T02:27:59Z set scope=['plugin/lib/sampo/shape.py', 'plugin/tests/test_shape.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:28:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3275.builder.md
- 2026-11-06T02:28:32Z focused
- 2026-11-06T02:28:33Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:35:06Z scope: plugin/lib/fmshape.py added: the fm shim every new plugin/lib module needs (standing rule, brief)
- 2026-11-06T02:37:53Z scope: MASTER.md bullet and docs/map/files-lib-3.md entry added: the new plugin/lib module's docs line (standing rule, brief)
- 2026-11-06T04:39:18Z scope widened to docs/map/files-lib-3.md: the fmshape entry describes the review's pure-append and adapt rules (review fixes 1-3)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-05: Recommendation: keep the notes as the cold read for these files; the fm*.py aliases point at plugin/lib/sampo, so a session reading them should open…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
