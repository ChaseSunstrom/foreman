---
id: T-3280
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/racemetrics.py, plugin/lib/sampo/lanes.py, plugin/lib/fmracemetrics.py, plugin/tests/test_racemetrics.py, CHANGELOG.md, MASTER.md, docs/map/files-lib-3.md]
depends_on: []
source: user
created: 2026-11-06T02:28:16Z
updated: 2026-11-06T05:35:42Z
builder: 2026-11-06T02:28:39Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a47e54653eb561ec3
lane_branch: worktree-agent-a47e54653eb561ec3
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:29:05Z
plan0_scope: [plugin/lib/sampo/racemetrics.py, plugin/lib/sampo/lanes.py, plugin/tests/test_racemetrics.py, CHANGELOG.md, MASTER.md, docs/map.md]
builder_returned: 2026-11-06T05:35:42Z
---
# Moon C-000115: race --score also reports each rival branch import time
## Raw request
> Moon C-000115: race --score also reports each rival's import time and reviewer findings, so the strongest refactor is picked on more evidence
## Interpretation
Reading 1 (chosen): lane race/score/pick already exist (lanes.py race/score/pick, _side at ~1023) and rank rival builders on checks, cross-tests, lines, scope, taste, recording why on pick; the missing measurable is import time (no mutation or reviewer column exists), so add import ms per side. Reading 2 (ruled out): a new 'lane compare A B' command, because race --score already compares sides and a second verb would duplicate it.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a racemetrics module measures a branch's import time for its changed plugin/lib python modules and returns it in ms — verify with `python3 plugin/tests/run.py test_racemetrics`
- [ ] fm lane race ID --score prints import ms per side and lists it in the sides JSON, never changing the ranking order — verify with `python3 plugin/tests/run.py test_racemetrics`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: lanes._side already runs per-side measurements and mutate.py/lanes.race hold scoring; add a small racemetrics.py with import_ms(path, files), called from _side, shown in the score line and sides JSON, ranking unchanged. Likely outcome: small diff, one touch in lanes.py.
2. Also add import time to the ranking after lines. Likely outcome: noisy timings flip winners; fails if a loaded machine skews medians.
3. Also add mutation survivors via mutate.run. Fails if runtime per side is minutes, blowing the race budget.
4. Do less: document that import time can be measured by hand. Likely outcome: nothing measured in the score.

Choice 1 (85%): informational evidence first, ranking stays deterministic. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] failing test: import_ms of a tmp module with a sleep at import beats a trivial one; score row has import_ms  <- CURRENT
2. [x] write plugin/lib/sampo/racemetrics.py (import_ms(path, files) via python -X importtime or timed subprocess import, median of 3)
3. [x] call it from lanes._side and add the clause to the score line; CHANGELOG, MASTER bullet, docs/map line
## Resume here
<!-- auto -->
- 2026-11-06T04:30:43Z step 1/3: failing test: import_ms of a tmp module with a sleep at import beats a trivial one; score row has import_ms
- git: worktree-agent-a47e54653eb561ec3; 2 uncommitted: plugin/lib/sampo/racemetrics.py, plugin/tests/test_racemetrics.py
- touched since last checkpoint: plugin/tests/test_racemetrics.py, plugin/lib/sampo/racemetrics.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_racemetrics` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 1.4s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree f2d0e346ef63] [world 2f1906870a] (2026-11-06T02:30:39Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k measures test_racemetrics` → exit 0 · Ran 3 tests in 1.4s (1 jobs, 16 at a time; slowest: RaceMetrics 1s) / OK [ran] [tree 1a9ef2dd69fe] [world 2f1906870a] (2026-11-06T02:31:26Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k prints_each test_racemetrics` → ✗ exit 1 · Ran 1 tests in 1.0s (1 jobs, 16 at a time; slowest: RaceMetrics 1s) / FAILED (1 classes: test_racemetrics.RaceMetrics) [ran] [tree 1a9ef2dd69fe] [world 2f1906870a] (2026-11-06T02:31:36Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_race test_racemetrics` → exit 0 · Ran 9 tests in 12.7s (9 jobs, 16 at a time; slowest: Race.test_review_fixes_lines_snapshot_brief_and_no_half_start 10s, RaceMetrics.test_race_score_prints_each_sides_import_ms_and_the_ranking_keeps_it [ran] [tree 97eba3fd32c0] [world 2f1906870a] (2026-11-06T02:33:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_racemetrics test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 1940.5s) · timed out after 1940.5s [ran] [tree 88763a246115] [world 2f1906870a] (2026-11-06T03:05:45Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_racemetrics test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2221 tests in 2080.2s (835 jobs, 16 at a time; slowest: Lanes 485s, Proof 484s, OutcomeEscalation 481s) / FAILED (16 classes: test_lanes.Lanes, test_proof.Proof, test_lanes.LaneRecovery, test_desi [ran] [tree 88763a246115] [world 2f1906870a] (2026-11-06T04:09:51Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_racemetrics` → exit 0 · Ran 4 tests in 23.0s (4 jobs, 16 at a time; slowest: RaceMetrics.test_race_score_prints_each_sides_import_ms_and_the_ranking_keeps_its_order 19s, RaceMetrics.test_a_module_that_sleeps_at_import_measur [ran] [tree 88763a246115] [world 2f1906870a] (2026-11-06T04:10:52Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k test_cross_examination_ranks_the_side_whose_test_catches_the_other_first test_lanes` → exit 0 · Ran 1 tests in 21.0s (1 jobs, 16 at a time; slowest: RaceEvidence 16s) / OK [ran] [tree 88763a246115] [world 2f1906870a] (2026-11-06T04:11:20Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_racemetrics` → exit 0 · Ran 8 tests in 69.0s (8 jobs, 2 at a time; slowest: RaceMetrics.test_race_score_prints_each_sides_import_time_and_module_count_and_the_ranking_keeps_its_order 44s, RaceMetrics.test_a_side_with_too_man [ran] [tree 21f2ece0de66] [world 2f1906870a] (2026-11-06T05:08:36Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py --timeout 1800 test_lanes test_race test_racemetrics` → exit 0 · Ran 197 tests in 991.2s (194 jobs, 2 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 83s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree 21f2ece0de66] [world 2f1906870a] (2026-11-06T05:21:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lane_twins test_lanes test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_racemetrics test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [22.81s] [ran] [tree 21f2ece0de66] [world 2f1906870a] (2026-11-06T05:35:25Z)
## Log
- 2026-11-06T02:28:16Z created
- 2026-11-06T02:28:23Z set title=Moon C-000115: race --score also reports each rival branch import time
- 2026-11-06T02:28:24Z set scope=['plugin/lib/sampo/racemetrics.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_racemetrics.py', 'CHANGELOG.md', 'MASTER.md', 'docs/map.md']
- 2026-11-06T02:28:39Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3280.builder.md
- 2026-11-06T02:29:05Z focused
- 2026-11-06T02:29:05Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:31:18Z set scope=['plugin/lib/sampo/racemetrics.py', 'plugin/lib/sampo/lanes.py', 'plugin/lib/fmracemetrics.py', 'plugin/tests/test_racemetrics.py', 'CHANGELOG.md', 'MASTER.md', 'docs/map/files-lib-3.md']
- 2026-11-06T02:31:18Z scope widened: plugin/lib/fmracemetrics.py (the fm shim a new lib module needs, standing rule) and docs/map/files-lib-3.md (the map shard; docs/map.md does not exist)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2339 [FEATURE M, done, 4 steps] Race at plan time, chosen by evidence (Mission 5, #2): fm lane race takes up to 3 sides from the Approach's options, refuses checks tha…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
