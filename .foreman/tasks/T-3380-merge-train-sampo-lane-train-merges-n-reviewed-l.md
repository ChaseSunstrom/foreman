---
id: T-3380
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T06:23:45Z
updated: 2026-11-06T07:10:33Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a40aba0c9902d36d6
lane_branch: worktree-agent-a40aba0c9902d36d6
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:24:24Z
plan0_scope: []
builder_returned: 2026-11-06T07:10:33Z
---
# Merge train: sampo lane train merges N reviewed lanes in a scratch integration worktree, runs the full gates once, bisects a red set to the culprit lanes, fast-forwards foreman/build, and lets each task's finish reuse that gate pass
## Raw request
> Merge train: sampo lane train merges N reviewed lanes in a scratch integration worktree, runs the full gates once, bisects a red set to the culprit lanes, fast-forwards foreman/build, and lets each task's finish reuse that gate pass
## Interpretation
Reading 1: a new verb sampo lane train that merges N lanes in a scratch worktree and gates once (chosen). Reading 2: only loosen the gate cache to ignore CHANGELOG/mirror; ruled out: still one gate per lane.
## Assumptions (confidence)
## Acceptance criteria
- [ ] four lanes, one of which breaks a test, train-merge as three with the breaker named and left unmerged, and the full gates ran at most 1+ceil(log2 4) times — verify with `python3 plugin/tests/run.py test_lane_train`
- [ ] after a green train, sampo task finish for each merged task reuses the train's gate pass when the code tree since differs only in CHANGELOG.md and the sync mirror, and re-runs the gates otherwise — verify with `python3 plugin/tests/run.py test_lane_train`
- [ ] a lane that conflicts with an earlier one in the train is skipped with its files named, the main checkout is never written except the final fast-forward — verify with `python3 plugin/tests/run.py test_lane_train`
## Non-goals
## Approach (options → choice → why)
1) integration worktree + one gate + bisect + finish reuses pass by code tree; likely outcome: N lanes cost 1 gate run. 2) only make gate cache ignore CHANGELOG/mirror; fails if: still one gate per lane. 3) octopus merge; fails if: no per-lane conflict isolation. 4) do less: skip gates at close; fails if: unsafe, red lands. Choice 1 (80%): N lanes cost 1 gate plus bisect on red.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests in test_lane_train.py  <- CURRENT
2. [x] lane train: integration worktree, ordered merges, conflict skip
3. [ ] one gate run, bisect on red, fast-forward
4. [x] finish reuses the train gate pass (code tree excludes CHANGELOG and mirror)
## Resume here
<!-- auto -->
- 2026-11-06T06:31:05Z step 1/4: failing tests in test_lane_train.py
- git: worktree-agent-a40aba0c9902d36d6; 5 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/train.py, plugin/tests/test_lane_train.py
- touched since last checkpoint: plugin/tests/test_lane_train.py, plugin/lib/sampo/core.py, plugin/lib/sampo/train.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/cli.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lane_train` → ✗ exit 1 · Ran 4 tests in 241.5s (1 jobs, 16 at a time; slowest: Train 5s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:31:46Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_train 2>&1 | tail -40` → ✗ exit 1 · Ran 4 tests in 127.7s (1 jobs, 16 at a time; slowest: Train 7s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:34:02Z)
- (ac 2) `python3 plugin/tests/run.py test_lane_train 2>&1 | tail -40` → ✗ exit 1 · Ran 4 tests in 127.7s (1 jobs, 16 at a time; slowest: Train 7s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:34:02Z)
- (ac 3) `python3 plugin/tests/run.py test_lane_train 2>&1 | tail -40` → ✗ exit 1 · Ran 4 tests in 127.7s (1 jobs, 16 at a time; slowest: Train 7s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:34:02Z)
- (step 2) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 4 tests in 149.8s (1 jobs, 16 at a time; slowest: Train 7s) / OK (ran] (tree cbbb9fbb55c1] (world 2f1906870a] (2026-11-06T06:39:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_train test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2716 tests in 757.8s (749 jobs, 16 at a time; slowest: AffectedPairs 165s, LeanKindGateHookDelay 91s, JudgmentKinds 70s) / FAILED (14 classes: test_lanes.Lanes, test_doctor.Checks, test_lanes.Lane (ran] (tree cbbb9fbb55c1] (world 2f1906870a] (2026-11-06T06:52:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_train test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2716 tests in 406.9s (1363 jobs, 16 at a time; slowest: LeanKindGateHookDelay 63s, AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 53s, AffectedPairs.test_an_affected_run_with_e (ran] (tree 31e78c0bc07d] (world 2f1906870a] (2026-11-06T07:01:28Z)
- (step 4) `python3 plugin/tests/run.py test_lane_train test_lanes test_docs test_doctor` → exit 0 · Ran 416 tests in 189.1s (204 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, SelfChangeGate 7s, PostMergeVerify 6s) / OK (ran] (tree b7ea283d4ed9] (world 2f1906870a] (2026-11-06T07:10:13Z)
## Log
- 2026-11-06T06:23:45Z created
- 2026-11-06T06:24:23Z focused
- 2026-11-06T06:24:24Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:27:18Z focused
- 2026-11-06T06:52:45Z focused
- 2026-11-06T07:01:44Z focused
- 2026-11-06T07:06:01Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3119 [PERFORMANCE M, planned, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-05: fast-merge build order (plan review): T-3139 runtime hook map, T-3141 land-then-verify with revert (the safety net before the cache), T-3140 content…
