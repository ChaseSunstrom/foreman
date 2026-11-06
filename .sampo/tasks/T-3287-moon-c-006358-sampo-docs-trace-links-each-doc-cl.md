---
id: T-3287
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/doctrace.py, plugin/tests/test_doctrace.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:34:27Z
updated: 2026-11-06T06:06:24Z
builder: 2026-11-06T02:34:38Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a36bf2516cf24b349
lane_branch: worktree-agent-a36bf2516cf24b349
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:43:38Z
plan0_scope: [plugin/lib/sampo/doctrace.py, plugin/tests/test_doctrace.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T05:57:31Z
---
# Moon C-006358: sampo docs --trace links each doc claim to the code lines that back it, and --since REF flags claims whose backing changed
## Raw request
> Moon C-006358: sampo docs --trace links each doc claim to the code lines that back it, and --since REF flags claims whose backing changed
## Interpretation
Reading 1 (chosen): a doc-claim-to-code trace for Sampo's own docs (MASTER.md, README, docs/) built on the existing docs.claims verdicts, adding the backing file:line and a stale flag when the backing changed since a git ref. Reading 2 (ruled out): hover UI over rendered docs, because the edit-time need is a CLI/gate list and docs.claims already proves existence (docs.py:327), only the line link and change tracking are missing.
## Assumptions (confidence)
## Acceptance criteria
- [ ] doctrace.trace(root) returns, per claim from docs.claims, the doc line and backing file:line list (path: the file; flag/subcommand: lines in code files defining it; failed claim: empty backing) — verify with `python3 plugin/tests/run.py test_doctrace`
- [ ] doctrace.trace(root, since=REF) marks a proven claim stale when a backing file is in git diff REF..worktree, and leaves others fresh — verify with `python3 plugin/tests/run.py test_doctrace`
- [ ] sampo docs --trace [--since REF] prints 'doc:line kind detail -> file:line|UNBACKED|STALE' and --json output carries the same rows — verify with `python3 plugin/tests/run.py test_doctrace`
## Non-goals
## Approach (options → choice → why)
1. New doctrace.py wrapping docs.claims: find doc line by text match, grep backing lines in non-doc files, git diff --name-only REF for stale. Likely outcome: small, new file, no collision with docs.py.
2. Extend docs.claims itself to emit line and backing fields. Likely outcome: one source of truth but touches a hot function used by prove.py and task_docs, risking regressions.
3. Index every claim into a persistent store updated on commit. fails if: the index goes stale between commits, which is the problem being solved.
4. Do less: only print backing file:line, no --since. Likely outcome: answers the proof question but misses the stale-in-a-diff half.

Choice 1 (85%): isolated module reusing claims; cli registration is a two-line flag add. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] Write failing test_doctrace on a tmp repo (README with a path, a flag, a gone path; code defining the flag; a commit then edit of the backing file)  <- CURRENT
2. [x] Add plugin/lib/sampo/doctrace.py reusing docs.claims, docs._tree_files and git diff --name-only
3. [x] Register --trace/--since on the docs verb in cli.py (tiny edit) and add a CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T06:06:24Z step 1/3: Write failing test_doctrace on a tmp repo (README with a path, a flag, a gone path; code defining the flag; a commit then edit of the backing file)
- git: worktree-agent-a36bf2516cf24b349; 2 uncommitted: plugin/lib/sampo/doctrace.py, plugin/tests/test_doctrace.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctrace` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 7.4s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 11a29a684f4a] [world 2f1906870a] (2026-11-06T02:46:28Z)
- (ac 1) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -40` → ✗ exit 1 · Ran 3 tests in 6.3s (1 jobs, 16 at a time; slowest: DocTrace 2s) / FAILED (1 classes: test_doctrace.DocTrace) [ran] [tree ea574c83bbb5] [world 2f1906870a] (2026-11-06T02:51:13Z)
- (ac 2) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -40` → ✗ exit 1 · Ran 3 tests in 6.3s (1 jobs, 16 at a time; slowest: DocTrace 2s) / FAILED (1 classes: test_doctrace.DocTrace) [ran] [tree ea574c83bbb5] [world 2f1906870a] (2026-11-06T02:51:13Z)
- (ac 3) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -40` → ✗ exit 1 · Ran 3 tests in 6.3s (1 jobs, 16 at a time; slowest: DocTrace 2s) / FAILED (1 classes: test_doctrace.DocTrace) [ran] [tree ea574c83bbb5] [world 2f1906870a] (2026-11-06T02:51:13Z)
- (step 2) `python3 plugin/tests/run.py test_doctrace.DocTrace.test_trace_links_each_claim_to_the_lines_that_back_it test_doctrace.DocTrace.test_trace_since_marks_only_the_claims_whose_backing_changed 2>&1 | tail -5` → exit 0 · Ran 2 tests in 5.5s (1 jobs, 16 at a time; slowest: DocTrace 2s) / OK [ran] [tree ea574c83bbb5] [world 2f1906870a] (2026-11-06T02:51:29Z)
- (step 2) `python3 plugin/tests/run.py test_doctrace.DocTrace.test_trace_links_each_claim_to_the_lines_that_back_it test_doctrace.DocTrace.test_trace_since_marks_only_the_claims_whose_backing_changed` → exit 0 · Ran 2 tests in 3.0s (1 jobs, 16 at a time; slowest: DocTrace 1s) / OK [ran] [tree ea574c83bbb5] [world 2f1906870a] (2026-11-06T02:51:41Z)
- (ac 1) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -4` → exit 0 · Ran 3 tests in 5.3s (1 jobs, 16 at a time; slowest: DocTrace 3s) / OK [ran] [tree 11ecab1bbca3] [world 2f1906870a] (2026-11-06T02:53:56Z)
- (ac 2) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -4` → exit 0 · Ran 3 tests in 5.3s (1 jobs, 16 at a time; slowest: DocTrace 3s) / OK [ran] [tree 11ecab1bbca3] [world 2f1906870a] (2026-11-06T02:53:56Z)
- (ac 3) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -4` → exit 0 · Ran 3 tests in 5.3s (1 jobs, 16 at a time; slowest: DocTrace 3s) / OK [ran] [tree 11ecab1bbca3] [world 2f1906870a] (2026-11-06T02:53:56Z)
- (step 3) `python3 plugin/tests/run.py test_doctrace 2>&1 | tail -4` → exit 0 · Ran 3 tests in 5.3s (1 jobs, 16 at a time; slowest: DocTrace 3s) / OK [ran] [tree 11ecab1bbca3] [world 2f1906870a] (2026-11-06T02:53:56Z)
- (step 3) `python3 plugin/tests/run.py test_doctrace` → exit 0 · Ran 3 tests in 5.5s (1 jobs, 16 at a time; slowest: DocTrace 2s) / OK [ran] [tree 11ecab1bbca3] [world 2f1906870a] (2026-11-06T02:54:14Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_doctrace test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2345 tests in 1350.4s (693 jobs, 16 at a time; slowest: LeanKindGateHookDelay 441s, LeanKindGateGuardAllow 412s, LeanKindGateSessionLine 406s) / FAILED (4 classes: test_genesis.GenesisCheck, test_ [ran] [tree 11ecab1bbca3] [world 2f1906870a] (2026-11-06T03:16:55Z)
- (step 3) `python3 plugin/tests/run.py test_doctrace test_docs test_genesis.GenesisCheck` → exit 0 · Ran 133 tests in 111.6s (72 jobs, 16 at a time; slowest: GenesisCheck 108s, TaskLifecycle 15s, Fences.test_the_documented_runnable_fences_run_green_in_a_temp_home 13s) / OK [ran] [tree 12e62694e709] [world 2f1906870a] (2026-11-06T03:23:24Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_doctrace test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [77.99s] [ran] [tree 12e62694e709] [world 2f1906870a] (2026-11-06T03:37:45Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_doctrace` → ✗ exit 1 · Ran 8 tests in 7.7s (1 jobs, 2 at a time; slowest: DocTrace 4s) / FAILED (1 classes: test_doctrace.DocTrace) [ran] [tree b037a4fe7c3f] [world 2f1906870a] (2026-11-06T04:32:11Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_doctrace test_docs test_genesis.GenesisCheck` → ✗ exit 1 · Ran 138 tests in 119.2s (72 jobs, 2 at a time; slowest: GenesisCheck 90s, TaskLifecycle 8s, Fences.test_the_documented_runnable_fences_run_green_in_a_temp_home 7s) / FAILED (1 classes: test_doctrace.D [ran] [tree 01e30afcbbd4] [world 2f1906870a] (2026-11-06T04:34:56Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_doctrace test_docs test_genesis.GenesisCheck` → exit 0 · Ran 138 tests in 310.5s (88 jobs, 2 at a time; slowest: GenesisCheck 219s, Fences.test_the_documented_runnable_fences_run_green_in_a_temp_home 29s, Fences.test_fm_new_lists_copies_and_never_overwrites [ran] [tree 0b100e49d558] [world 2f1906870a] (2026-11-06T04:41:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_doctrace test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_race test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2353 tests in 4291.5s (1561 jobs, 2 at a time; slowest: LeanKindGateSessionLine 483s, LeanKindGateHookDelay 483s, LeanKindGateGuardAllow 454s) / FAILED (3 classes: test_exam.LeanKindGateHookDelay, [ran] [tree 0b100e49d558] [world 2f1906870a] (2026-11-06T05:53:33Z)
## Log
- 2026-11-06T02:34:27Z created
- 2026-11-06T02:34:33Z set scope=['plugin/lib/sampo/doctrace.py', 'plugin/tests/test_doctrace.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:34:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3287.builder.md
- 2026-11-06T02:43:34Z focused
- 2026-11-06T02:43:38Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:53:17Z scope widened: plugin/lib/fmdoctrace.py (the fm shim), MASTER.md and docs/map/files-lib-1.md: brief line 45 requires a shim, a MASTER.md bullet and a docs/map line for a new plugin/lib module
- 2026-11-06T04:31:35Z scope widened: docs.py:466-468 (cmd_docs hands --trace and --since to doctrace.cmd_trace, so the docs verb keeps reach through sampo.docs; the reach test needs it)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
