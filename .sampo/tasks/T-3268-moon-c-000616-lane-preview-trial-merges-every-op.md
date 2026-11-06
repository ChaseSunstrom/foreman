---
id: T-3268
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/lane_preview.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/cli.py, plugin/tests/test_lane_preview.py, plugin/lib/fmlane_preview.py, MASTER.md, docs/map/files-lib-2.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:17Z
updated: 2026-11-06T04:52:27Z
builder: 2026-11-06T02:27:29Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a924b708954d48496
lane_branch: worktree-agent-a924b708954d48496
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:21Z
plan0_scope: [plugin/lib/sampo/lane_preview.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lane_preview.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:52:27Z
---
# Moon C-000616: lane_preview trial-merges every open lane branch against main and each other (git merge-tree) and lane list names the conflicting files
## Raw request
> Moon C-000616: lane_preview trial-merges every open lane branch against main and each other (git merge-tree) and lane list names the conflicting files
## Interpretation
Reading 1 (chosen): a read-only trial merge of every open foreman/* lane branch against main and against each other, surfaced in lane list, so conflicts show before lane merge. Reading 2 (ruled out): a nightly scheduled job with suggested resolutions, because the early warning is the valuable part, resolutions need a model, and lane list already runs on demand and in the drive line later.
## Assumptions (confidence)
## Acceptance criteria
- [ ] lane_preview.clashes(main, branches) returns {(a,b): [files]} for conflicting pairs, with main as 'main', using git merge-tree --write-tree --name-only and no checkout; clean pairs omitted — verify with `python3 plugin/tests/run.py test_lane_preview`
- [ ] fm lane list prints a 'Will conflict:' line per clashing pair of open lane branches (<=10 pairs, files capped) and adds a 'conflicts' key to its json; nothing printed when clean — verify with `python3 plugin/tests/run.py test_lane_preview`
- [ ] pairs are capped (<=12 branches, n^2 merge-tree calls with a timeout) and a git failure yields no clash, never an exception in lane list — verify with `python3 plugin/tests/run.py test_lane_preview`
## Non-goals
## Approach (options → choice → why)
1. New module lane_preview.py using git merge-tree --write-tree --name-only per pair, called from lane list. Likely outcome: no checkout, no collision with other lanes, small diff in lanes.py.
2. Use what exists: lanes._conflict_brief and the lane_conflict ledger (hot_files) only report after a failed lane merge, and merge() aborts a real merge. Likely outcome: reuse _git and the files-list format, but they cannot predict, so only the helpers are reused.
3. Real throwaway worktree merges per pair. Likely outcome: works but slow and leaves worktrees behind.
4. Predict from changed-file overlap only. fails if: both lanes touch different hunks of one file, giving false alarms.
5. Do less: main-vs-lane only. Likely outcome: misses lane-vs-lane clashes, the late ones.

Choice 1 (88%): merge-tree is exact, object-only and available (git 2.56). Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] write failing test_lane_preview.py on a temp git repo: two branches editing same line, one clean branch, one clashing with main
2. [x] write plugin/lib/sampo/lane_preview.py clashes() parsing merge-tree --write-tree --name-only (exit 1 = conflicts; file list after the tree line up to blank line)
3. [x] register in cmd_lane list branch of lanes.py: call clashes on the foreman/* branches, append lines and json key
4. [x] CHANGELOG.md entry; run test_lane_preview and test_lanes
## Resume here
<!-- auto -->
- 2026-11-06T04:31:19Z steps 4/4 done
- git: worktree-agent-a924b708954d48496; 2 uncommitted: plugin/lib/sampo/lane_preview.py, plugin/tests/test_lane_preview.py
- touched since last checkpoint: plugin/lib/sampo/lane_preview.py, plugin/tests/test_lane_preview.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_preview` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 1.5s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 04ef38134f83] [world 2f1906870a] (2026-11-06T02:30:37Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_lane_preview` → exit 0 · Ran 9 tests in 1.6s (2 jobs, 16 at a time; slowest: LaneListPreview 1s, Clashes 0s) / OK [ran] [tree 09a8547ef35e] [world 2f1906870a] (2026-11-06T02:32:21Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_lane_preview` → exit 0 · Ran 9 tests in 2.0s (2 jobs, 16 at a time; slowest: LaneListPreview 2s, Clashes 0s) / OK [ran] [tree 09a8547ef35e] [world 2f1906870a] (2026-11-06T02:32:24Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_preview test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [68.54s] [ran] [tree 17357afe89d0] [world 2f1906870a] (2026-11-06T02:47:17Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_preview test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [142.27s] [ran] [tree 17357afe89d0] [world 2f1906870a] (2026-11-06T03:06:13Z)
- (step 4) `sampo check --affected --evidence T-3268` → exit 0 · ✓ affected tests only (34): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find t [ran] [tree 17357afe89d0] [world 2f1906870a] (2026-11-06T03:06:15Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_preview` → exit 0 · Ran 18 tests in 25.7s (18 jobs, 2 at a time; slowest: LaneListPreview.test_more_than_twelve_branches_says_the_preview_is_incomplete 8s, LaneListPreview.test_ten_pairs_and_three_files_at_most_in_text 5 [ran] [tree 23b2f8c859a7] [world 2f1906870a] (2026-11-06T04:10:08Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_preview` → exit 0 · Ran 18 tests in 33.6s (18 jobs, 2 at a time; slowest: LaneListPreview.test_more_than_twelve_branches_says_the_preview_is_incomplete 9s, LaneListPreview.test_no_preview_skips_the_trial_merges 7s, LaneL [ran] [tree 23b2f8c859a7] [world 2f1906870a] (2026-11-06T04:10:46Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_preview test_docs test_rename_aliases test_lanes` → exit 0 · Ran 326 tests in 386.2s (287 jobs, 2 at a time; slowest: Lanes.test_tidy_sweeps_stale_lanes 25s, Lanes.test_an_audit_on_the_current_tree_beats_an_older_pre_merge_one 24s, ProbeProvisional.test_revert_ [ran] [tree 23b2f8c859a7] [world 2f1906870a] (2026-11-06T04:17:16Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_preview test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [33.27s] [ran] [tree 23b2f8c859a7] [world 2f1906870a] (2026-11-06T04:24:12Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_preview test_lanes` → exit 0 · Ran 202 tests in 506.1s (179 jobs, 2 at a time; slowest: Lanes.test_another_lanes_merge_is_not_this_tasks_scope_or_stale_audit 37s, Lanes.test_finish_after_two_other_merges_has_no_audit_gap 35s, RaceE [ran] [tree 23b2f8c859a7] [world 2f1906870a] (2026-11-06T04:25:47Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_preview` → exit 0 · Ran 21 tests in 20.8s (9 jobs, 2 at a time; slowest: Clashes 8s, LaneListPreview.test_more_than_twelve_branches_says_the_preview_is_incomplete 7s, LaneListPreview.test_ten_pairs_and_three_files_at_mos [ran] [tree 8ba6e3c8bd69] [world 2f1906870a] (2026-11-06T04:33:02Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lane_preview` → exit 0 · Ran 21 tests in 14.8s (21 jobs, 2 at a time; slowest: LaneListPreview.test_clashes_are_named_in_text_and_json 4s, LaneListPreview.test_more_than_twelve_branches_says_the_preview_is_incomplete 3s, Lane [ran] [tree 8ba6e3c8bd69] [world 2f1906870a] (2026-11-06T04:33:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_preview test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [59.45s] [ran] [tree 8ba6e3c8bd69] [world 2f1906870a] (2026-11-06T04:45:14Z)
## Log
- 2026-11-06T02:27:17Z created
- 2026-11-06T02:27:23Z set scope=['plugin/lib/sampo/lane_preview.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lane_preview.py', 'CHANGELOG.md']
- 2026-11-06T02:27:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3268.builder.md
- 2026-11-06T02:28:20Z focused
- 2026-11-06T02:28:21Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:31:43Z scope widened: plugin/lib/fmlane_preview.py (the fm shim), MASTER.md and docs/map/files-lib-2.md (the standing rule: a new plugin/lib module needs its fm shim, a MASTER.md bullet and a docs/map line)
- 2026-11-06T02:34:45Z set scope=['plugin/lib/sampo/lane_preview.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lane_preview.py', 'plugin/lib/fmlane_preview.py', 'MASTER.md', 'docs/map/files-lib-2.md', 'CHANGELOG.md']
- 2026-11-06T03:41:16Z set scope=['plugin/lib/sampo/lane_preview.py', 'plugin/lib/sampo/lanes.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_lane_preview.py', 'plugin/lib/fmlane_preview.py', 'MASTER.md', 'docs/map/files-lib-2.md', 'CHANGELOG.md']
- 2026-11-06T03:41:18Z scope widened: plugin/lib/sampo/cli.py gets the one --no-preview argument line in the lane parser (review fixes, T-3268)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- T-3249 [FEATURE M, planned, 2 steps] Drive's Stop-hook continuation runs Kalevala rounds too (T-3082 criterion 3's drive…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py
