---
id: T-3276
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/objections.py, plugin/tests/test_objections.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:28:01Z
updated: 2026-11-06T04:07:02Z
builder: 2026-11-06T02:28:40Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a8fc8b949d737001d
lane_branch: worktree-agent-a8fc8b949d737001d
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:53Z
plan0_scope: [plugin/lib/sampo/objections.py, plugin/tests/test_objections.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:07:02Z
---
# Moon C-000717: 'sampo audit ahead ID' lists the objections reviewers most likely raise on this diff, before the review
## Raw request
> Moon C-000717: 'sampo audit ahead ID' lists the objections reviewers most likely raise on this diff, before the review
## Interpretation
Reading 1 (chosen): before the review, the author runs one command and sees the objections past reviewers raised on this kind of change: same files, sibling files, and defect classes whose cue words appear in the diff. Partial: cli._past_nits (cli.py:1583) already feeds exact-file nits to the reviewer brief only (audit prep, cli.py:6001), and lanes.defect_classes (lanes.py:1452) counts classes globally; this adds the author-facing, diff-matched view. Reading 2 (ruled out): mining task finish refusals; they are not logged as events (only closeout_flags, close_score), so there is no data to mine yet.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a new objections module ranks past reviewer findings (ledger finding events, rejected ones dropped) for a diff's files: exact-file matches first, then same-directory matches, then the defect classes (lanes.DEFECT_CLASSES) whose cue words appear in the diff's added lines — verify with `python3 plugin/tests/run.py test_objections`
- [ ] sampo audit ahead ID prints at most 8 ranked objections, each with file, text, lens and source task, and prints one 'none on record' line when nothing matches; it reuses cli._past_nits for the exact-file part instead of duplicating it — verify with `python3 plugin/tests/run.py test_objections`
- [ ] sampo audit prep ID output ends with a hint to run sampo audit ahead before it, and the CHANGELOG has an entry — verify with `python3 plugin/tests/run.py test_objections`
## Non-goals
## Approach (options → choice → why)
1. New module objections.py ranking ledger findings by exact file, then same directory, then DEFECT_CLASSES cues found in the diff's added lines; exposed as sampo audit ahead ID. Likely outcome: author sees a short ranked list before audit prep, fewer repeat findings.
2. Only extend audit prep to print the existing nits to the author. Likely outcome: tiny, but no sibling-file or class matching, so new files get nothing.
3. Embed an LLM to predict objections from the diff. fails if: it costs tokens per close and has no grounding in recorded findings.
4. Do less: add one hint line to audit prep pointing at the existing nits. Likely outcome: little new signal.

Choice 1 (85%): grounded in recorded findings, cheap, a new module avoids collisions in cli.py. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] write test_objections first: seeded findings on an edited file, a sibling file and a cue word in the diff; assert ranking, rejected dropped, cap of 8, empty case  <- CURRENT
2. [ ] write plugin/lib/sampo/objections.py: likely(p, files, added_text, tid) returning ranked rows
3. [x] register 'ahead' in cmd_audit in cli.py (small branch) and add the prep hint line
4. [x] CHANGELOG entry; run test_objections and test_receipts
## Resume here
<!-- auto -->
- 2026-11-06T02:32:10Z step 2/4: write plugin/lib/sampo/objections.py: likely(p, files, added_text, tid) returning ranked rows
- git: worktree-agent-a8fc8b949d737001d; 2 uncommitted: plugin/lib/sampo/objections.py, plugin/tests/test_objections.py
- touched since last checkpoint: plugin/tests/test_objections.py, plugin/lib/sampo/objections.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_objections` → ✗ exit 1 (never ran: no tests ran) · Ran 1 tests in 1.5s (2 jobs, 16 at a time; slowest: Dissent 1s, loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree b0a9dd1b6b4b] [world 2f1906870a] (2026-11-06T02:31:17Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_objections` → ✗ exit 1 · Ran 9 tests in 4.0s (3 jobs, 16 at a time; slowest: AheadCommand 3s, Dissent 2s, Objections 1s) / FAILED (1 classes: test_objections.AheadCommand) [ran] [tree 942e3dae7506] [world 2f1906870a] (2026-11-06T02:32:07Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_objections` → exit 0 · Ran 9 tests in 10.8s (9 jobs, 16 at a time; slowest: Dissent 10s, AheadCommand.test_audit_prep_ends_with_a_hint_to_run_ahead_first 3s, AheadCommand.test_ahead_lists_the_objections_on_the_diffs_files_a [ran] [tree b0cdcb33d927] [world 2f1906870a] (2026-11-06T02:34:44Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_objections test_receipts test_audit test_defect_classes test_affected_rules` → exit 0 · Ran 59 tests in 69.6s (51 jobs, 16 at a time; slowest: ImportCards.test_audit_prep_of_an_l_task_that_used_a_card_runs 47s, AuditRun.test_refuses_when_the_budget_is_spent 34s, AuditRun.test_one_verdict [ran] [tree b0cdcb33d927] [world 2f1906870a] (2026-11-06T02:36:03Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_objections` → exit 0 · Ran 9 tests in 42.1s (9 jobs, 16 at a time; slowest: Dissent 35s, AheadCommand.test_ahead_lists_the_objections_on_the_diffs_files_and_one_line_each 17s, AheadCommand.test_audit_prep_ends_with_a_hint_t [ran] [tree 57f974c2a6b9] [world 2f1906870a] (2026-11-06T02:40:05Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_objections test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [94.08s] [ran] [tree 57f974c2a6b9] [world 2f1906870a] (2026-11-06T02:49:20Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_objections test_receipts test_audit test_audit_run test_defect_classes test_affected_rules` → exit 0 · Ran 62 tests in 555.7s (61 jobs, 2 at a time; slowest: ImportCards.test_audit_prep_of_an_l_task_that_used_a_card_runs 91s, DesignLens.test_prep_names_the_design_lens_for_a_ui_diff_with_its_screenshots [ran] [tree 5787112adc05] [world 2f1906870a] (2026-11-06T03:58:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_objections test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [37.29s] [ran] [tree 5787112adc05] [world 2f1906870a] (2026-11-06T04:06:41Z)
## Log
- 2026-11-06T02:28:01Z created
- 2026-11-06T02:28:08Z set scope=['plugin/lib/sampo/objections.py', 'plugin/tests/test_objections.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:28:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3276.builder.md
- 2026-11-06T02:28:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3276.builder.md
- 2026-11-06T02:28:52Z focused
- 2026-11-06T02:28:53Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:33:24Z scope widened: plugin/lib/fmobjections.py shim, MASTER.md and docs/map/files-lib-1.md bullets are required by the standing rule that every new plugin/lib module has a shim, a MASTER bullet and a map line (RULE_TESTS)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3278 [FEATURE M, planned, 3 steps] Moon C-010008: sampo gatemap FILES predicts which gates a self-change will hit, from past refusals, with the smallest fix
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar finished tasks took 2–9 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
