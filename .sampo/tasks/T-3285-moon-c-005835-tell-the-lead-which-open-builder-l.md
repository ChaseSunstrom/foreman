---
id: T-3285
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/lane_overlap.py plugin/lib/fmlane_overlap.py plugin/lib/sampo/lanes.py plugin/tests/test_lane_overlap.py MASTER.md docs/map/files-lib-2.md CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:34:16Z
updated: 2026-11-06T06:12:03Z
builder: 2026-11-06T02:34:32Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-afb7472a42a09803e
lane_branch: worktree-agent-afb7472a42a09803e
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:43:11Z
plan0_scope: [plugin/lib/sampo/lane_overlap.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lane_overlap.py, CHANGELOG.md]
builder_returned: 2026-11-06T06:12:03Z
---
# Moon C-005835: tell the lead which open builder lanes overlap (same files or same new function) so one can be merged or stopped
## Raw request
> Moon C-005835: tell the lead which open builder lanes overlap (same files or same new function) so one can be merged or stopped
## Interpretation
Reading 1 (chosen): detect overlap between open lanes from their branch diffs (shared new function names, shared touched files) and show it in fm lane list so the lead merges or stops one. Reading 2 (ruled out): comparing brief text by similarity, because titles are short and give false hits; diffs are the ground truth. lanes.twins (post-merge string literals) and louhi lanes_dup (recovered lanes) are different things and stay.
## Assumptions (confidence)
## Acceptance criteria
- [ ] overlap() flags two lanes that add the same function name or touch the same file, and ignores unrelated lanes — verify with `python3 plugin/tests/run.py test_lane_overlap`
- [ ] fm lane list prints an OVERLAP line for a flagged pair naming both task ids and the shared symbols/files, and none otherwise — verify with `python3 plugin/tests/run.py test_lane_overlap`
- [ ] existing lane tests still pass — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1. New module lane_overlap.py: per open lane, files and added defs from git diff base...branch; pair lanes sharing a def or file; list prints OVERLAP lines. Likely outcome: small, no collisions with big files, catches same-helper and same-file cases.
2. Token-similarity of brief texts. Likely outcome: noisy, misses lanes that have not described the same thing alike.
3. Check at merge time only via twins. fails if: the lead wants to stop a duplicate before it finishes, merge-time is too late.
4. Do less: same-file only, no function names. Likely outcome: floods with false hits on hot files like cli.py.
5) use what exists: lanes.functions_changed and _SIGNED_DEF already parse a diff into {file: [functions]}, and lane list already enumerates lanes with branches; reuse both, no new diff parser. Likely outcome: least new code.

Choice 1 (85%): diffs are cheap and exact; reuses option 5's parser; shared new defs rank above shared files. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] Write failing test_lane_overlap.py: pure overlap() over lane facts, then a git-repo case with two branches  <- CURRENT
2. [x] Add plugin/lib/sampo/lane_overlap.py: facts(main, branch) = files and added defs from git diff base...branch (reuse lanes.functions_changed/_SIGNED_DEF); overlap(facts) pairs with shared defs or files, ranked, with a merge-or-stop advice line
3. [x] Register in lanes.py cmd_lane list: one OVERLAP line per pair and an overlaps key in the JSON
4. [x] CHANGELOG entry
## Resume here
<!-- auto -->
- 2026-11-06T06:11:04Z step 1/4: Write failing test_lane_overlap.py: pure overlap() over lane facts, then a git-repo case with two branches
- git: worktree-agent-afb7472a42a09803e; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lane_overlap` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 3.8s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 7a0ec79f56fe] [world 2f1906870a] (2026-11-06T02:46:00Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -40` → ✗ exit 1 · Ran 7 tests in 13.7s (3 jobs, 16 at a time; slowest: LaneList 11s, Facts 1s, Overlap 0s) / FAILED (1 classes: test_lane_overlap.LaneList) [ran] [tree 27f3f55b5486] [world 2f1906870a] (2026-11-06T02:48:20Z)
- (ac 2) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -40` → ✗ exit 1 · Ran 7 tests in 13.7s (3 jobs, 16 at a time; slowest: LaneList 11s, Facts 1s, Overlap 0s) / FAILED (1 classes: test_lane_overlap.LaneList) [ran] [tree 27f3f55b5486] [world 2f1906870a] (2026-11-06T02:48:20Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -30` → exit 0 · Ran 7 tests in 10.9s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 8s, LaneList.test_fm_lane_list_prints_no_ [ran] [tree f9fe4f709e34] [world 2f1906870a] (2026-11-06T02:48:52Z)
- (ac 2) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -30` → exit 0 · Ran 7 tests in 10.9s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 8s, LaneList.test_fm_lane_list_prints_no_ [ran] [tree f9fe4f709e34] [world 2f1906870a] (2026-11-06T02:48:52Z)
- (step 3) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -30` → exit 0 · Ran 7 tests in 10.9s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 8s, LaneList.test_fm_lane_list_prints_no_ [ran] [tree f9fe4f709e34] [world 2f1906870a] (2026-11-06T02:48:52Z)
- (step 2) `python3 plugin/tests/run.py test_lane_overlap` → exit 0 · Ran 7 tests in 18.6s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 16s, LaneList.test_fm_lane_list_prints_no [ran] [tree f9fe4f709e34] [world 2f1906870a] (2026-11-06T02:49:18Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_lane_twins test_lane_overlap` → exit 0 · Ran 193 tests in 341.4s (20 jobs, 16 at a time; slowest: Lanes 338s, LaneRecovery 180s, RaceEvidence 130s) / OK [ran] [tree 6299518747de] [world 2f1906870a] (2026-11-06T02:55:15Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -n 15` → exit 0 · Ran 8 tests in 16.7s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 12s, LaneList.test_fm_lane_list_prints_no [ran] [tree 0894d5b56108] [world 2f1906870a] (2026-11-06T02:57:13Z)
- (ac 2) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -n 15` → exit 0 · Ran 8 tests in 16.7s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 12s, LaneList.test_fm_lane_list_prints_no [ran] [tree 0894d5b56108] [world 2f1906870a] (2026-11-06T02:57:13Z)
- (step 4) `python3 plugin/tests/run.py test_lane_overlap 2>&1 | tail -n 15` → exit 0 · Ran 8 tests in 16.7s (4 jobs, 16 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 12s, LaneList.test_fm_lane_list_prints_no [ran] [tree 0894d5b56108] [world 2f1906870a] (2026-11-06T02:57:13Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_lane_twins test_lane_overlap` → exit 0 · Ran 194 tests in 106.0s (179 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 41s, Lanes.test_another_lanes_merge_of_a_prove [ran] [tree 0894d5b56108] [world 2f1906870a] (2026-11-06T02:59:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_overlap test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2278 tests in 1196.7s (820 jobs, 16 at a time; slowest: Proof 314s, OutcomeEscalation 276s, LeanKindGateHookDelay 254s) / FAILED (3 classes: test_rename_scan.RenameScan, test_docs.PluginFiles, tes [ran] [tree 0894d5b56108] [world 2f1906870a] (2026-11-06T03:19:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_overlap test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2278 tests in 799.7s (1758 jobs, 16 at a time; slowest: LeanKindGateHookDelay 364s, LeanKindGateSessionLine 358s, LeanKindGateGuardAllow 352s) / FAILED (1 classes: test_site_build.CardsPage) [ran] [tree 623003e65b13] [world 2f1906870a] (2026-11-06T03:35:42Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_overlap test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [47.89s] [ran] [tree 623003e65b13] [world 2f1906870a] (2026-11-06T03:46:08Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_overlap` → ✗ exit 1 · Ran 22 tests in 11.8s (7 jobs, 2 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 6s, LaneList.test_uncommitted_lanes_overl [ran] [tree 0bd63bfe41dc] [world 2f1906870a] (2026-11-06T04:33:20Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_overlap` → exit 0 · Ran 23 tests in 63.5s (17 jobs, 2 at a time; slowest: LaneList.test_fm_lane_list_prints_an_overlap_line_for_a_pair_sharing_a_def_and_none_for_an_unrelated_lane 25s, LaneList.test_fm_lane_list_prints_n [ran] [tree 6207368b3314] [world 2f1906870a] (2026-11-06T04:39:53Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lanes test_lane_twins test_lane_overlap` → exit 0 · Ran 209 tests in 411.7s (192 jobs, 2 at a time; slowest: Lanes.test_a_merged_file_this_task_also_touched_still_stales_the_audit 41s, ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pau [ran] [tree 935b57b7a7df] [world 2f1906870a] (2026-11-06T05:36:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_overlap test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2292 tests in 4539.6s (1600 jobs, 2 at a time; slowest: LeanKindGateSessionLine 486s, LeanKindGateHookDelay 470s, LeanKindGateGuardAllow 437s) / FAILED (2 classes: test_exam.LeanKindGateSessionLin [ran] [tree 935b57b7a7df] [world 2f1906870a] (2026-11-06T06:10:46Z)
## Log
- 2026-11-06T02:34:16Z created
- 2026-11-06T02:34:24Z set scope=['plugin/lib/sampo/lane_overlap.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lane_overlap.py', 'CHANGELOG.md']
- 2026-11-06T02:34:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3285.builder.md
- 2026-11-06T02:43:07Z focused
- 2026-11-06T02:43:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:47:31Z set scope=['plugin/lib/sampo/lane_overlap.py plugin/lib/fmlane_overlap.py plugin/lib/sampo/lanes.py plugin/tests/test_lane_overlap.py MASTER.md docs/map/files-lib-2.md CHANGELOG.md']
- 2026-11-06T02:47:33Z steer: scope widened to the fm shim, MASTER.md and docs/map/files-lib-2.md: the brief's standing rule needs a shim, a MASTER bullet and a map line for a new lib module (T-3285 step 2)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-3268 [FEATURE M, active, 4 steps] Moon C-000616: lane_preview trial-merges every open lane branch against main and each other (git merge-tree) and lane list names the …
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py
