---
id: T-3380
type: FEATURE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, MASTER.md, docs/map/files-lib-3.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/train.py, plugin/tests/test_lane_train.py]
depends_on: []
source: user
created: 2026-11-06T06:23:45Z
updated: 2026-11-06T08:07:06Z
base: ef1480837c3030543e9401c689169ee50ad704e3
base_tree: faa67f80514afd54c6ebde0eb1300167e1e56242
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:24:24Z
plan0_scope: []
builder_returned: 2026-11-06T07:26:46Z
lane_stop: merged 2026-11-06T07:49:17Z
verified: ok
unproven: [docs, typed]
---
# Merge train: sampo lane train merges N reviewed lanes in a scratch integration worktree, runs the full gates once, bisects a red set to the culprit lanes, fast-forwards foreman/build, and lets each task's finish reuse that gate pass
## Raw request
> Merge train: sampo lane train merges N reviewed lanes in a scratch integration worktree, runs the full gates once, bisects a red set to the culprit lanes, fast-forwards foreman/build, and lets each task's finish reuse that gate pass
## Interpretation
Reading 1: a new verb sampo lane train that merges N lanes in a scratch worktree and gates once (chosen). Reading 2: only loosen the gate cache to ignore CHANGELOG/mirror; ruled out: still one gate per lane.
## Assumptions (confidence)
## Acceptance criteria
- [x] four lanes, one of which breaks a test, train-merge as three with the breaker named and left unmerged, and the full gates ran at most 1+ceil(log2 4) times — verify with `python3 plugin/tests/run.py test_lane_train`
- [x] after a green train, sampo task finish for each merged task reuses the train's gate pass when the code tree since differs only in CHANGELOG.md and the sync mirror, and re-runs the gates otherwise — verify with `python3 plugin/tests/run.py test_lane_train`
- [x] a lane that conflicts with an earlier one in the train is skipped with its files named, the main checkout is never written except the final fast-forward — verify with `python3 plugin/tests/run.py test_lane_train`
## Non-goals
## Approach (options → choice → why)
1) integration worktree + one gate + bisect + finish reuses pass by code tree; likely outcome: N lanes cost 1 gate run. 2) only make gate cache ignore CHANGELOG/mirror; fails if: still one gate per lane. 3) octopus merge; fails if: no per-lane conflict isolation. 4) do less: skip gates at close; fails if: unsafe, red lands. Choice 1 (80%): N lanes cost 1 gate plus bisect on red.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1473, T-1579, T-1588, T-1589.
## Execution prompt
## Steps
1. [x] failing tests in test_lane_train.py
2. [x] lane train: integration worktree, ordered merges, conflict skip
3. [x] one gate run, bisect on red, fast-forward
4. [x] finish reuses the train gate pass (code tree excludes CHANGELOG and mirror)
## Resume here
<!-- auto -->
- 2026-11-06T08:02:08Z steps 4/4 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/sampo/core.py, scripts/
- touched since last checkpoint: plugin/lib/sampo/core.py
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lane_train` → ✗ exit 1 · Ran 4 tests in 241.5s (1 jobs, 16 at a time; slowest: Train 5s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:31:46Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_train 2>&1 | tail -40` → ✗ exit 1 · Ran 4 tests in 127.7s (1 jobs, 16 at a time; slowest: Train 7s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:34:02Z)
- (ac 2) `python3 plugin/tests/run.py test_lane_train 2>&1 | tail -40` → ✗ exit 1 · Ran 4 tests in 127.7s (1 jobs, 16 at a time; slowest: Train 7s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:34:02Z)
- (ac 3) `python3 plugin/tests/run.py test_lane_train 2>&1 | tail -40` → ✗ exit 1 · Ran 4 tests in 127.7s (1 jobs, 16 at a time; slowest: Train 7s) / FAILED (1 classes: test_lane_train.Train) (ran] (tree 5e83bf2263db] (world 2f1906870a] (2026-11-06T06:34:02Z)
- (step 2) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 4 tests in 149.8s (1 jobs, 16 at a time; slowest: Train 7s) / OK (ran] (tree cbbb9fbb55c1] (world 2f1906870a] (2026-11-06T06:39:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_train test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2716 tests in 757.8s (749 jobs, 16 at a time; slowest: AffectedPairs 165s, LeanKindGateHookDelay 91s, JudgmentKinds 70s) / FAILED (14 classes: test_lanes.Lanes, test_doctor.Checks, test_lanes.Lane (ran] (tree cbbb9fbb55c1] (world 2f1906870a] (2026-11-06T06:52:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_lane_train test_lane_twins test_lanes test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2716 tests in 406.9s (1363 jobs, 16 at a time; slowest: LeanKindGateHookDelay 63s, AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 53s, AffectedPairs.test_an_affected_run_with_e (ran] (tree 31e78c0bc07d] (world 2f1906870a] (2026-11-06T07:01:28Z)
- (step 4) `python3 plugin/tests/run.py test_lane_train test_lanes test_docs test_doctor` → exit 0 · Ran 416 tests in 189.1s (204 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, SelfChangeGate 7s, PostMergeVerify 6s) / OK (ran] (tree b7ea283d4ed9] (world 2f1906870a] (2026-11-06T07:10:13Z)
- (step 4) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 8 tests in 81.1s (8 jobs, 16 at a time; slowest: Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget 1s, Train.test_a_middle_culprit_costs_one_regate_more 1s, Train.test_a_conf [ran] [tree 909df63d745c] [world 2f1906870a] (2026-11-06T07:26:32Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 75c4c18c0dfb] (2026-11-06T07:49:19Z)
- (step 3) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 8 tests in 27.7s (1 jobs, 16 at a time; slowest: Train 4s) / OK [ran] [tree 75c4c18c0dfb] [world 2f1906870a] (2026-11-06T07:50:00Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 75c4c18c0dfb] (2026-11-06T07:50:10Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_train` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T07:50:00Z [ran] [tree 75c4c18c0dfb] [world 2f1906870a] (2026-11-06T07:50:12Z)
- (ac 2) `python3 plugin/tests/run.py test_lane_train` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T07:50:00Z [ran] [tree 75c4c18c0dfb] [world 2f1906870a] (2026-11-06T07:50:12Z)
- (ac 3) `python3 plugin/tests/run.py test_lane_train` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T07:50:00Z [ran] [tree 75c4c18c0dfb] [world 2f1906870a] (2026-11-06T07:50:12Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 75c4c18c0dfb] (2026-11-06T07:50:12Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 75c4c18c0dfb] (2026-11-06T07:50:12Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 75c4c18c0dfb] (2026-11-06T07:50:12Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree ef233f48fea6] (2026-11-06T08:04:15Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree ef233f48fea6] (2026-11-06T08:04:16Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree ef233f48fea6] (2026-11-06T08:04:16Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree ef233f48fea6] (2026-11-06T08:04:16Z)
## Log
- 2026-11-06T06:23:45Z created
- 2026-11-06T06:24:23Z focused
- 2026-11-06T06:24:24Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:27:18Z focused
- 2026-11-06T06:52:45Z focused
- 2026-11-06T07:01:44Z focused
- 2026-11-06T07:06:01Z focused
- 2026-11-06T07:19:11Z focused
- 2026-11-06T07:49:17Z merged worktree-agent-a40aba0c9902d36d6 (7 file(s))
- 2026-11-06T07:49:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a40aba0c9902d36d6
- 2026-11-06T07:49:17Z focused
- 2026-11-06T07:49:18Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'MASTER.md', 'docs/map/files-lib-3.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/lanes.py', 'plugin/lib/sampo/train.py', 'plugin/tests/test_lane_train.py']
- 2026-11-06T07:49:19Z scope: widened at merge to the reviewed lane's own diff (d93df53c7), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T07:50:07Z focused
- 2026-11-06T08:02:10Z paused: focus moved to T-3404
- 2026-11-06T08:04:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T08:04:12Z focused
- 2026-11-06T08:04:14Z post-merge fix: core.CODE_TREE_SKIP reads core.MIRRORS instead of naming .foreman/.sampo (T-3342's hardcode test); test_rename_scan and test_lane_train pass
- 2026-11-06T08:04:14Z focused
- 2026-11-06T08:07:04Z done
- 2026-11-06T08:07:06Z committed 15ffb1b36 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3119 [PERFORMANCE M, planned, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-05: fast-merge build order (plan review): T-3139 runtime hook map, T-3141 land-then-verify with revert (the safety net before the cache), T-3140 content…
## Preflight
Changed in scope since this was planned (2026-11-06): .sampo/decisions.md, .sampo/research/brainstorm-20261106-000946/ideas.md, .sampo/research/brainstorm-20261106-000946/r1-01-user-value.md, .sampo/research/brainstorm-20261106-000946/r1-02-unspoken-nee…; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing tests in test_lane_train.py
## Files touched
- plugin/tests/test_lane_train.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/train.py
- plugin/lib/sampo/lanes.py
- docs/map/files-lib-3.md
- MASTER.md
- .fm-scratch/edit.json
- CHANGELOG.md
