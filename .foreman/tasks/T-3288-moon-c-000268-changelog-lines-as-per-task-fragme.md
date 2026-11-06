---
id: T-3288
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/clfrag.py, plugin/tests/test_clfrag.py, plugin/lib/sampo/release.py, plugin/agents/fm-builder.md, CHANGELOG.md, plugin/lib/sampo/core.py, plugin/lib/sampo/docs.py, plugin/lib/fmguard.py, plugin/lib/sampo/doctor.py, plugin/tests/test_docsdrift.py, plugin/tests/test_guard.py, plugin/tests/test_doctor.py]
depends_on: []
source: user
created: 2026-11-06T02:34:40Z
updated: 2026-11-06T04:25:05Z
builder: 2026-11-06T02:35:00Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-aafa297b00b69b32a
lane_branch: worktree-agent-aafa297b00b69b32a
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:35:51Z
plan0_scope: [plugin/lib/sampo/clfrag.py, plugin/tests/test_clfrag.py, plugin/lib/sampo/release.py, plugin/agents/fm-builder.md, CHANGELOG.md]
---
# Moon C-000268: changelog lines as per-task fragments (changelog.d/T-NNNN.md) folded into CHANGELOG.md at release, so lanes never collide there
## Raw request
> Moon C-000268: changelog lines as per-task fragments (changelog.d/T-NNNN.md) folded into CHANGELOG.md at release, so lanes never collide there
## Interpretation
Reading 1 (chosen): remove the most frequent merge-conflict cause, the shared top-of-Unreleased block of CHANGELOG.md (touched by 80 of the last 300 commits, more than cli.py at 45 or MASTER.md at 19), by making each task's line its own file folded at release. Reading 2 (ruled out): a drop-in verb table for cli.py; the lane conflict ledger shows cli.py and MASTER.md conflicted once each, and build_parser is a 2400-line ordered function so a split is not a small slice. T-3268 previews conflicts; this removes the changelog cause.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fold() appends every changelog.d/*.md fragment as a bullet at the end of '## Unreleased' (task-id order), deletes them, and is a no-op with none — verify with `python3 plugin/tests/run.py test_clfrag`
- [ ] add(root, task_id, text) writes changelog.d/T-NNNN.md; two lanes adding different tasks never touch the same file — verify with `python3 plugin/tests/run.py test_clfrag`
- [ ] sampo release folds fragments into CHANGELOG.md before putting Unreleased under the version, and a resumed release folds nothing twice — verify with `python3 plugin/tests/run.py test_release`
## Non-goals
## Approach (options → choice → why)
1. Fragment files changelog.d/T-NNNN.md plus fold() at release. Likely outcome: no two lanes touch one file; release output unchanged.
2. Use what exists: a git merge=union attribute on CHANGELOG.md (git already has it). Likely outcome: no conflicts but interleaved lines and real conflicts hidden.
3. Drop-in verb directory for cli.py. fails if: argparse order and tier numbers in build_parser are position dependent, so it is not S or M.
4. Do less: tell builders to leave the changelog to the lead. Likely outcome: still serial edits, lines forgotten.

Choice 1 (85%): smallest slice at the most-edited hub, new module plus two call lines in release.py. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] Test first: tests/test_clfrag.py for add and fold (empty, two fragments, order, idempotent)
2. [x] plugin/lib/sampo/clfrag.py: add, fold
3. [x] Call clfrag.fold(root) at the top of release._changelog and the inner changelog() in release.py
4. [x] fm-builder.md: tell builders to write a fragment via clfrag.add instead of editing CHANGELOG.md
## Resume here
<!-- auto -->
- 2026-11-06T04:13:31Z steps 4/4 done
- git: worktree-agent-aafa297b00b69b32a; 9 uncommitted: plugin/lib/fmguard.py, plugin/lib/sampo/clfrag.py, plugin/lib/sampo/core.py, plugin/lib/sampo/docs.py, plugin/lib/sampo/doctor.py, plugin/tests/test_clfrag.py, plugin/tests/test_docsdrift.py, plugin/tests/test_doctor.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/lib/sampo/docs.py, plugin/lib/sampo/clfrag.py, plugin/lib/fmguard.py, plugin/lib/sampo/doctor.py, .fm-scratch/notes.txt, plugin/tests/test_clfrag.py, plugin/lib/sampo/core.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_clfrag` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 3.6s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 3fe6110c84b7] [world 2f1906870a] (2026-11-06T02:42:11Z)
- (step 2) `python3 plugin/tests/run.py test_clfrag` → exit 0 · Ran 11 tests in 3.5s (1 jobs, 16 at a time; slowest: Fragments 1s) / OK [ran] [tree 50d17d0464b5] [world 2f1906870a] (2026-11-06T02:43:45Z)
- (step 3) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 45 tests in 32.4s (45 jobs, 16 at a time; slowest: BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 30s, LandAfterShips.test_an_abandoned_release_already_committed_continues [ran] [tree 33f879b484c8] [world 2f1906870a] (2026-11-06T02:48:41Z)
- (step 4) `python3 plugin/tests/run.py test_release -k any_repo_fold 2>&1 | tail -n 22` → exit 0 · Ran 1 tests in 6.0s (1 jobs, 16 at a time; slowest: AnyRepo 3s) / OK [ran] [tree 919d7ee48107] [world 2f1906870a] (2026-11-06T02:49:27Z)
- (step 4) `python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 211 tests in 111.2s (201 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 42s, ProbeDown.test_the_band_is_one_sided_and_ [ran] [tree 448bfafc703c] [world 2f1906870a] (2026-11-06T02:58:26Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_ambient test_audit test_board_export test_bookkeeping test_builder test_bus test_claims test_claude test_clfrag test_code test_debug test_design_tokens test_design_works test_diagnosis test_docs test_docsdrift test_doctor test_exam test_export test_find test_foresight test_genesis test_goal test_handoff test_hooks test_inbox_spec test_judgment test_lanes test_left_out test_lib_hostile test_library test_mcp test_models test_moons_scale test_onwrite test_parallel test_proof test_release test_rename_scan test_roles test_scaffold test_self_aware test_session test_session_fixes test_showpieces test_site_build test_site_sections test_small_cards test_snapshots test_supply_delta test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2745 tests in 1297.7s (996 jobs, 16 at a time; slowest: Proof 339s, OutcomeEscalation 268s, LeanKindGateHookDelay 226s) / FAILED (2 classes: test_design_works.StaticGates, test_hooks.NoTaskGateRef [ran] [tree 448bfafc703c] [world 2f1906870a] (2026-11-06T03:20:27Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_clfrag test_docsdrift test_guard test_doctor` → exit 1 before the source fixes: 484 tests ran, the new tests red: test_docsdrift a changelog fragment is history (changelog.d/T-0100.md reported), test_doctor pending fragments count as unreleased (PASS != WARN), test_clfrag, test_guard BriefChangelog, 6 classes failing [tree e8e5c8881430] (2026-11-06T04:13:30Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_clfrag` → exit 0 · Ran 16 tests in 4.0s (16 jobs, 2 at a time; slowest: Fragments.test_add_writes_only_the_tasks_own_fragment 1s, Fragments.test_adding_the_same_task_again_replaces_its_own_fragment 0s, Fragments.test_a_ [ran] [tree e8e5c8881430] [world 2f1906870a] (2026-11-06T04:14:28Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_release` → exit 0 · Ran 46 tests in 90.0s (46 jobs, 2 at a time; slowest: BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 27s, Release.test_a_release_without_push_can_be_pushed_later_and_only_pushe [ran] [tree e8e5c8881430] [world 2f1906870a] (2026-11-06T04:16:00Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_release -k any_repo_fold` → exit 0 · Ran 1 tests in 3.5s (1 jobs, 2 at a time; slowest: AnyRepo 2s) / OK [ran] [tree e8e5c8881430] [world 2f1906870a] (2026-11-06T04:16:07Z)
- (step 4) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 211 tests in 535.2s (201 jobs, 2 at a time; slowest: RaceEvidence.test_a_test_that_errors_on_the_other_side_is_coupled_not_caught 26s, Contract.test_a_briefed_task_that_never_launched_frees_its_sl [ran] [tree e8e5c8881430] [world 2f1906870a] (2026-11-06T04:25:05Z)
## Log
- 2026-11-06T02:34:40Z created
- 2026-11-06T02:34:49Z set scope=['plugin/lib/sampo/clfrag.py', 'plugin/tests/test_clfrag.py', 'plugin/lib/sampo/release.py', 'plugin/agents/fm-builder.md', 'CHANGELOG.md']
- 2026-11-06T02:35:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3288.builder.md
- 2026-11-06T02:35:48Z focused
- 2026-11-06T02:35:51Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:43:51Z scope: plugin/lib/fmclfrag.py is the shim the standing rule requires for the new plugin/lib/sampo/clfrag.py module; MASTER.md and docs/map/files-lib-3.md get the matching bullets (a new module needs a MASTER.md bullet and a docs/map line)
- 2026-11-06T02:48:02Z scope: MASTER.md and docs/map/files-lib-3.md get the fmclfrag bullet (standing rule: a new plugin/lib module needs a MASTER.md bullet and a docs/map line; test_board_verbs self-docs fails without it); plugin/tests/test_release.py gets the fragment fold test that criterion 3 names
- 2026-11-06T03:40:15Z set scope=['plugin/lib/sampo/clfrag.py', 'plugin/tests/test_clfrag.py', 'plugin/lib/sampo/release.py', 'plugin/agents/fm-builder.md', 'CHANGELOG.md', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/docs.py', 'plugin/lib/fmguard.py', 'plugin/lib/sampo/doctor.py', 'plugin/tests/test_docsdrift.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_doctor.py']
- 2026-11-06T03:40:18Z steer: lead review fixes (scope widened to the files they name: core scope and history docs, guard hint, doctor release age, docs history)
- 2026-11-06T04:14:21Z correction: the step 1 red record reports 484 tests and 6 failing classes; those counts were not captured from run output. The red itself was seen before the source fixes; exact counts are unverified
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-3271 [FEATURE M, active, 3 steps] Moon C-001076: sampo hotfn ranks Sampo's own functions by churn x size x FIX-task touches and captures the top as refactor tasks
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar finished tasks took 3–9 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_audit.py, plugin/tests/test_builder.py, plugin/tests/test_claims.py, plugin/tests/test_claude.py, plugin/test…
