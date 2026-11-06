---
id: T-3081
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py, plugin/lib/fmkalevala.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/louhi.py, MASTER.md, docs/map/files-lib-2.md, plugin/tests/test_moons_scale.py, plugin/tests/test_louhi_models.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/budget.py, CHANGELOG.md]
depends_on: [T-3053]
source: user
created: 2026-11-05T00:33:50Z
updated: 2026-11-05T17:51:30Z
builder_model: haiku
base: 397e14bea9c20443e1f4c429d37afd82edd860af
base_tree: 1e42c126f43baa43b8131b2901c69c64f0b040c8
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T13:24:02Z
plan0_scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py]
builder_returned: 2026-11-05T14:57:39Z
lane_stop: merged 2026-11-05T17:37:48Z
verified: strong
unproven: [docs]
lane_verified: daf01510546ddd3ea60f906d1f2365a876d4485f
---
# Kalevala part 2: the towers per aspect, seeded and sealed, run at once as jobs; Kalevala's own generations and the capability registry (T-3050)
## Raw request
> Kalevala part 2: the towers per aspect, seeded and sealed, run at once as jobs; Kalevala's own generations and the capability registry (T-3050)
## Interpretation
Reading 1 (taken): the orchestrator half of Kalevala (T-3050): choose aspects from data, make and seal each tower's gen-0, run the towers' genesis steps at once as jobs, give Kalevala generations of its own selected by the towers' exams, and register every behaviour change so each new generation builds on the last. Reading 2 (ruled out): one long-running daemon process: Sampo runs work as verbs and night jobs; a daemon adds a second process model.
## Assumptions (confidence)
## Acceptance criteria
- [x] Many aspects, not a few: sampo kalevala start opens a tower for each aspect with open coverage (every coverage.md area plus problem solving, memory and efficiency, read from data), each with a gen-0 made from the root's gen-0 plus its aspect, sealed; sampo kalevala status lists them — verify with `python3 plugin/tests/run.py test_kalevala`
- [x] Simultaneous: sampo kalevala step advances every tower's next genesis step as background jobs, at most K at once (K from the local slots and the budget), each tower's step one at a time, results in Kalevala's manifest — verify with `python3 plugin/tests/run.py test_kalevala`
- [x] Genesis of genesis: Kalevala keeps its own generations (research/genesis/kalevala/gen-N): each picks the tower set and their setup, selected by the towers' combined exam results, with its own lineage — verify with `python3 plugin/tests/run.py test_kalevala`
- [x] Building on built things: each closed task that changes how Sampo behaves (ideas, thinking, review, planning, memory) is registered as a capability, and the next Kalevala generation writes it into every tower's next seed and records whether it helped there — verify with `python3 plugin/tests/run.py test_kalevala`
- [x] A hard spend ceiling: a Kalevala round has its own budget feature and a daily share; it refuses to start past it; at most K towers active, the rest queued thinnest first — verify with `python3 plugin/tests/run.py test_kalevala`
- [x] Towers share safely: moons writes under the store lock, exam scenarios read-only, two concurrent steps writing one file refused — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
1) use what exists: a new kalevala.py over part 1's --tower verbs (subprocess sampo genesis --tower X step), night.py's job runner for the background, coverage.md for aspects, lineage.md's format for Kalevala's own lineage, task_done ledger rows (type, title, files under plugin/skills, prompts, the ideas and review paths) for the capability registry: likely outcome: a thin layer over proven parts. 2) threads in one process driving rune functions directly: fails if: rune's process-wide tower switch (part 1) races between threads. 3) a cron per tower: fails if: no one place sees all towers or holds the slot count. 4) do less: start towers but step them by hand: fails if: nothing runs at once, the ask. Choice 1 (80%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/test_cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/tests/test_lanes.py; past FIXes T-2814, T-2836, T-2993, T-3014, T-3049.
## Execution prompt
Read T-3050's brief (state/projects/foreman-4a056f/tasks/T-3050-is-it-possible-to-have-orchestrators-of-orcehstr.md) and part 1's code (rune.home/root/set_tower, sampo genesis --tower, sampo genesis towers; merged from T-3053). Build plugin/lib/sampo/kalevala.py and the sampo kalevala verb (start, status, step, gen) test-first in plugin/tests/test_kalevala.py. A tower's gen-0: the root gen-0's MUST and NEVER lines verbatim plus an aspect section; sealed with rune's init. Jobs: background subprocesses with a slot cap and a per-tower lock; never two steps of one tower at once. Capability registry: research/genesis/kalevala/capabilities.jsonl, one row per closed task whose change touches how Sampo behaves, with the task id and a one-line what; the seeding writes them into each tower's next seed through the tower's steer file. Never write to the live tower state from tests.
## Steps
1. [x] aspects, tower gen-0s, start and status (tests first)
2. [x] step: towers' steps as parallel jobs with slots (tests first)
3. [x] Kalevala's generations, lineage and selection (tests first)
4. [x] the capability registry and its seeding (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T14:35:50Z steps 4/4 done
- git: worktree-agent-aac052eb335d8a688; 6 uncommitted: plugin/lib/sampo/budget.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/kalevala.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/tests/test_kalevala.py
- touched since last checkpoint: plugin/lib/sampo/kalevala.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/budget.py, plugin/lib/sampo/cli.py
## Docs impact
CHANGELOG line; MASTER.md Kalevala row names the verbs
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -15` → ✗ exit 1 · Ran 14 tests in 4.1s (3 jobs, 16 at a time; slowest: Kalevala 4s, KalevalaStart 1s, KalevalaNoRootGen0 0s) / FAILED (2 classes: test_kalevala.KalevalaStart, test_kalevala.KalevalaNoRootGen0) [ran] [tree c8883cb9a698] [world 2f1906870a] (2026-11-05T13:28:15Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -15` → ✗ exit 1 · Ran 14 tests in 4.1s (3 jobs, 16 at a time; slowest: Kalevala 4s, KalevalaStart 1s, KalevalaNoRootGen0 0s) / FAILED (2 classes: test_kalevala.KalevalaStart, test_kalevala.KalevalaNoRootGen0) [ran] [tree c8883cb9a698] [world 2f1906870a] (2026-11-05T13:28:15Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -15` → ✗ exit 1 · Ran 14 tests in 4.1s (3 jobs, 16 at a time; slowest: Kalevala 4s, KalevalaStart 1s, KalevalaNoRootGen0 0s) / FAILED (2 classes: test_kalevala.KalevalaStart, test_kalevala.KalevalaNoRootGen0) [ran] [tree c8883cb9a698] [world 2f1906870a] (2026-11-05T13:28:15Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -15` → ✗ exit 1 · Ran 14 tests in 4.1s (3 jobs, 16 at a time; slowest: Kalevala 4s, KalevalaStart 1s, KalevalaNoRootGen0 0s) / FAILED (2 classes: test_kalevala.KalevalaStart, test_kalevala.KalevalaNoRootGen0) [ran] [tree c8883cb9a698] [world 2f1906870a] (2026-11-05T13:28:15Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -15` → ✗ exit 1 · Ran 14 tests in 4.1s (3 jobs, 16 at a time; slowest: Kalevala 4s, KalevalaStart 1s, KalevalaNoRootGen0 0s) / FAILED (2 classes: test_kalevala.KalevalaStart, test_kalevala.KalevalaNoRootGen0) [ran] [tree c8883cb9a698] [world 2f1906870a] (2026-11-05T13:28:15Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -15` → ✗ exit 1 · Ran 14 tests in 4.1s (3 jobs, 16 at a time; slowest: Kalevala 4s, KalevalaStart 1s, KalevalaNoRootGen0 0s) / FAILED (2 classes: test_kalevala.KalevalaStart, test_kalevala.KalevalaNoRootGen0) [ran] [tree c8883cb9a698] [world 2f1906870a] (2026-11-05T13:28:15Z)
- (step 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 14 tests in 3.3s (3 jobs, 16 at a time; slowest: Kalevala 3s, KalevalaStart 2s, KalevalaNoRootGen0 0s) / OK [ran] [tree c98a21544730] [world 2f1906870a] (2026-11-05T13:29:07Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -30` → ✗ exit 1 · Ran 26 tests in 15.3s (4 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 13s, KalevalaStart 7s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 72a122e5b1d9] [world 2f1906870a] (2026-11-05T13:35:51Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -30` → ✗ exit 1 · Ran 26 tests in 15.3s (4 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 13s, KalevalaStart 7s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 72a122e5b1d9] [world 2f1906870a] (2026-11-05T13:35:51Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -30` → ✗ exit 1 · Ran 26 tests in 15.3s (4 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 13s, KalevalaStart 7s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 72a122e5b1d9] [world 2f1906870a] (2026-11-05T13:35:51Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -30` → ✗ exit 1 · Ran 26 tests in 15.3s (4 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 13s, KalevalaStart 7s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 72a122e5b1d9] [world 2f1906870a] (2026-11-05T13:35:51Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -30` → ✗ exit 1 · Ran 26 tests in 15.3s (4 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 13s, KalevalaStart 7s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 72a122e5b1d9] [world 2f1906870a] (2026-11-05T13:35:51Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -30` → ✗ exit 1 · Ran 26 tests in 15.3s (4 jobs, 16 at a time; slowest: KalevalaStep 14s, Kalevala 13s, KalevalaStart 7s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 72a122e5b1d9] [world 2f1906870a] (2026-11-05T13:35:51Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 26 tests in 7.2s (4 jobs, 16 at a time; slowest: KalevalaStep 7s, Kalevala 5s, KalevalaStart 3s) / OK [ran] [tree 37e5baaa229d] [world 2f1906870a] (2026-11-05T13:41:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_doctor test_exam test_kalevala test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 829 tests in 148.1s (237 jobs, 16 at a time; slowest: LeanKindGateHookDelay 86s, JudgmentKinds 84s, LeanKindGateGuardAllow 72s) / FAILED (3 classes: test_doctor.Checks, test_moons_scale.Catalogue, [ran] [tree 9af3d56bde48] [world 2f1906870a] (2026-11-05T13:43:52Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 15` → ✗ exit 1 · Ran 34 tests in 16.6s (5 jobs, 16 at a time; slowest: KalevalaStep 15s, Kalevala 15s, KalevalaGen 11s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 70662ddcfec5] [world 2f1906870a] (2026-11-05T13:47:39Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 15` → ✗ exit 1 · Ran 34 tests in 16.6s (5 jobs, 16 at a time; slowest: KalevalaStep 15s, Kalevala 15s, KalevalaGen 11s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 70662ddcfec5] [world 2f1906870a] (2026-11-05T13:47:39Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 15` → ✗ exit 1 · Ran 34 tests in 16.6s (5 jobs, 16 at a time; slowest: KalevalaStep 15s, Kalevala 15s, KalevalaGen 11s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 70662ddcfec5] [world 2f1906870a] (2026-11-05T13:47:39Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 15` → ✗ exit 1 · Ran 34 tests in 16.6s (5 jobs, 16 at a time; slowest: KalevalaStep 15s, Kalevala 15s, KalevalaGen 11s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 70662ddcfec5] [world 2f1906870a] (2026-11-05T13:47:39Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 15` → ✗ exit 1 · Ran 34 tests in 16.6s (5 jobs, 16 at a time; slowest: KalevalaStep 15s, Kalevala 15s, KalevalaGen 11s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 70662ddcfec5] [world 2f1906870a] (2026-11-05T13:47:39Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 15` → ✗ exit 1 · Ran 34 tests in 16.6s (5 jobs, 16 at a time; slowest: KalevalaStep 15s, Kalevala 15s, KalevalaGen 11s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 70662ddcfec5] [world 2f1906870a] (2026-11-05T13:47:39Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 30` → ✗ exit 1 · Ran 34 tests in 12.6s (5 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 8s, KalevalaGen 7s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 41883d071214] [world 2f1906870a] (2026-11-05T13:48:30Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 30` → ✗ exit 1 · Ran 34 tests in 12.6s (5 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 8s, KalevalaGen 7s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 41883d071214] [world 2f1906870a] (2026-11-05T13:48:30Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 30` → ✗ exit 1 · Ran 34 tests in 12.6s (5 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 8s, KalevalaGen 7s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 41883d071214] [world 2f1906870a] (2026-11-05T13:48:30Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 30` → ✗ exit 1 · Ran 34 tests in 12.6s (5 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 8s, KalevalaGen 7s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 41883d071214] [world 2f1906870a] (2026-11-05T13:48:30Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 30` → ✗ exit 1 · Ran 34 tests in 12.6s (5 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 8s, KalevalaGen 7s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 41883d071214] [world 2f1906870a] (2026-11-05T13:48:30Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 30` → ✗ exit 1 · Ran 34 tests in 12.6s (5 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 8s, KalevalaGen 7s) / FAILED (1 classes: test_kalevala.KalevalaGen) [ran] [tree 41883d071214] [world 2f1906870a] (2026-11-05T13:48:30Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 25` → exit 0 · Ran 34 tests in 11.0s (5 jobs, 16 at a time; slowest: KalevalaStep 10s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:06Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 34 tests in 11.6s (5 jobs, 16 at a time; slowest: KalevalaStep 11s, Kalevala 8s, KalevalaGen 7s) / OK [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:21Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2419 tests in 288.2s (929 jobs, 16 at a time; slowest: LeanKindGateHookDelay 138s, LeanKindGateSessionLine 122s, LeanKindGateGuardAllow 117s) / FAILED (1 classes: test_louhi_models.ModelBenchVisib [ran] [tree 1d7986bf6131] [world 2f1906870a] (2026-11-05T13:49:34Z)
- (step 4) `python3 plugin/tests/run.py test_louhi_models 2>&1 | tail -n 4` → exit 0 · Ran 27 tests in 5.5s (10 jobs, 16 at a time; slowest: ModelBenchVisible 5s, LouhiModels.test_no_endpoint_is_named_in_the_code 4s, LouhiModels.test_the_generation_arm_writes_yield_and_pass_rate_one_end [ran] [tree f00c8922139f] [world 2f1906870a] (2026-11-05T13:49:59Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 9.1s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:04Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 9.1s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:04Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 9.1s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:04Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 9.1s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:04Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 9.1s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:04Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 9.1s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:04Z)
- (step 4) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 40 tests in 8.7s (6 jobs, 16 at a time; slowest: KalevalaStep 8s, Kalevala 7s, KalevalaGen 5s) / OK [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:16Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2427 tests in 199.9s (1453 jobs, 16 at a time; slowest: LeanKindGateHookDelay 104s, LeanKindGateGuardAllow 87s, LeanKindGateSessionLine 87s) / FAILED (3 classes: test_exam.ExamGen.test_runs_lists_ [ran] [tree 7af1b02a0cd9] [world 2f1906870a] (2026-11-05T13:54:21Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2433 tests in 258.6s (1299 jobs, 16 at a time; slowest: LeanKindGateHookDelay 131s, LeanKindGateSessionLine 113s, LeanKindGateGuardAllow 112s) / FAILED (1 classes: test_left_out.LeftOut) [ran] [tree 9a3a0008abd7] [world 2f1906870a] (2026-11-05T14:02:24Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [33.37s] [ran] [tree 1fcfdd5242ec] [world 2f1906870a] (2026-11-05T14:08:34Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 150` → ✗ exit 1 · Ran 51 tests in 18.2s (7 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 8s, KalevalaGen 6s) / FAILED (3 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaCapabilities, test_kalevala. [ran] [tree 56a4db90feca] [world 2f1906870a] (2026-11-05T14:30:52Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 150` → ✗ exit 1 · Ran 51 tests in 18.2s (7 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 8s, KalevalaGen 6s) / FAILED (3 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaCapabilities, test_kalevala. [ran] [tree 56a4db90feca] [world 2f1906870a] (2026-11-05T14:30:52Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 150` → ✗ exit 1 · Ran 51 tests in 18.2s (7 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 8s, KalevalaGen 6s) / FAILED (3 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaCapabilities, test_kalevala. [ran] [tree 56a4db90feca] [world 2f1906870a] (2026-11-05T14:30:52Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 150` → ✗ exit 1 · Ran 51 tests in 18.2s (7 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 8s, KalevalaGen 6s) / FAILED (3 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaCapabilities, test_kalevala. [ran] [tree 56a4db90feca] [world 2f1906870a] (2026-11-05T14:30:52Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 150` → ✗ exit 1 · Ran 51 tests in 18.2s (7 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 8s, KalevalaGen 6s) / FAILED (3 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaCapabilities, test_kalevala. [ran] [tree 56a4db90feca] [world 2f1906870a] (2026-11-05T14:30:52Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -n 150` → ✗ exit 1 · Ran 51 tests in 18.2s (7 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 8s, KalevalaGen 6s) / FAILED (3 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaCapabilities, test_kalevala. [ran] [tree 56a4db90feca] [world 2f1906870a] (2026-11-05T14:30:52Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 30.1s (7 jobs, 16 at a time; slowest: KalevalaStep 29s, Kalevala 10s, KalevalaGen 8s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree af46bccc5e25] [world 2f1906870a] (2026-11-05T14:35:03Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 30.1s (7 jobs, 16 at a time; slowest: KalevalaStep 29s, Kalevala 10s, KalevalaGen 8s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree af46bccc5e25] [world 2f1906870a] (2026-11-05T14:35:03Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 30.1s (7 jobs, 16 at a time; slowest: KalevalaStep 29s, Kalevala 10s, KalevalaGen 8s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree af46bccc5e25] [world 2f1906870a] (2026-11-05T14:35:03Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 30.1s (7 jobs, 16 at a time; slowest: KalevalaStep 29s, Kalevala 10s, KalevalaGen 8s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree af46bccc5e25] [world 2f1906870a] (2026-11-05T14:35:03Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 30.1s (7 jobs, 16 at a time; slowest: KalevalaStep 29s, Kalevala 10s, KalevalaGen 8s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree af46bccc5e25] [world 2f1906870a] (2026-11-05T14:35:03Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 30.1s (7 jobs, 16 at a time; slowest: KalevalaStep 29s, Kalevala 10s, KalevalaGen 8s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree af46bccc5e25] [world 2f1906870a] (2026-11-05T14:35:03Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -60` → exit 0 · Ran 51 tests in 22.2s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 11s, KalevalaGen 10s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:37:38Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -60` → exit 0 · Ran 51 tests in 22.2s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 11s, KalevalaGen 10s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:37:38Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -60` → exit 0 · Ran 51 tests in 22.2s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 11s, KalevalaGen 10s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:37:38Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -60` → exit 0 · Ran 51 tests in 22.2s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 11s, KalevalaGen 10s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:37:38Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -60` → exit 0 · Ran 51 tests in 22.2s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 11s, KalevalaGen 10s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:37:38Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -60` → exit 0 · Ran 51 tests in 22.2s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 11s, KalevalaGen 10s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:37:38Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 51 tests in 19.6s (7 jobs, 16 at a time; slowest: KalevalaStep 19s, Kalevala 4s, KalevalaGen 3s) / OK [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:38:25Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 113 tests in 11.8s (79 jobs, 16 at a time; slowest: KeepGrow.test_a_model_whose_rows_all_fail_admit_stalls_with_no_max_calls 9s, Yield.test_a_repair_that_the_kill_judge_refuses_is_never_repaired_a [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:38:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_budget test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2456 tests in 436.0s (1455 jobs, 16 at a time; slowest: LeanKindGateHookDelay 174s, LeanKindGateGuardAllow 151s, LeanKindGateSessionLine 149s) / FAILED (1 classes: test_rename_scan.RenameScan.test [ran] [tree 28adac268950] [world 2f1906870a] (2026-11-05T14:45:58Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_kalevala` → exit 0 · Ran 61 tests in 27.7s (17 jobs, 16 at a time; slowest: KalevalaStep 26s, Kalevala 7s, RenameScan.test_no_fm_only_command_regex 7s) / OK [ran] [tree b09611126ebd] [world 2f1906870a] (2026-11-05T14:47:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_budget test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [48.97s] [ran] [tree b09611126ebd] [world 2f1906870a] (2026-11-05T14:57:06Z)
- `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 51 tests in 18.3s (7 jobs, 16 at a time; slowest: KalevalaStep 16s, Kalevala 9s, KalevalaGen 6s) / FAILED (5 classes: test_kalevala.KalevalaStep, test_kalevala.KalevalaGen, test_kalevala.KalevalaC (start tree + this task's tests) [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:42Z)
- `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 51 tests in 21.4s (7 jobs, 16 at a time; slowest: KalevalaStep 21s, Kalevala 9s, KalevalaGen 7s) / OK [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:42Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:40:42Z [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:56Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:40:42Z [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:56Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:40:42Z [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:56Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:40:42Z [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:56Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:40:42Z [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:56Z)
- (ac 6) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T17:40:42Z [ran] [tree 934b19ea56ee] [world 2f1906870a] (2026-11-05T17:40:56Z)
- (audit intent) `builder lane reviewed before merge (one fm-reviewer pass on the lane diff); merged by the queue with post-merge verify green` → start opens a tower per open-coverage aspect, step runs them as K-capped jobs, gens select by combined exam, capabilities registry seeds the next gen [tree 934b19ea56ee] (2026-11-05T17:40:56Z)
- (audit adversary) `builder lane reviewed before merge (one fm-reviewer pass on the lane diff); merged by the queue with post-merge verify green` → past the daily share start refuses; two concurrent steps writing one file are refused [tree 934b19ea56ee] (2026-11-05T17:40:56Z)
- (audit edge) `builder lane reviewed before merge (one fm-reviewer pass on the lane diff); merged by the queue with post-merge verify green` → no open coverage opens only the three read-from-data aspects; K=0 queues all thinnest first [tree 934b19ea56ee] (2026-11-05T17:40:56Z)
- (audit intent) `builder lane reviewed before merge (one fm-reviewer pass on the lane diff); merged by the queue with post-merge verify green` → start opens a tower per open-coverage aspect, step runs them as K-capped jobs, gens select by combined exam, capabilities registry seeds the next gen [tree 934b19ea56ee] (2026-11-05T17:41:32Z)
- (audit adversary) `builder lane reviewed before merge (one fm-reviewer pass on the lane diff); merged by the queue with post-merge verify green` → past the daily share start refuses; two concurrent steps writing one file are refused [tree 934b19ea56ee] (2026-11-05T17:41:32Z)
- (audit edge) `builder lane reviewed before merge (one fm-reviewer pass on the lane diff); merged by the queue with post-merge verify green` → no open coverage opens only the three read-from-data aspects; K=0 queues all thinnest first [tree 934b19ea56ee] (2026-11-05T17:41:32Z)
## Log
- 2026-11-05T00:33:50Z created
- 2026-11-05T00:33:51Z set approved=True
- 2026-11-05T13:23:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3081.builder.md
- 2026-11-05T13:24:00Z focused
- 2026-11-05T13:24:02Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T13:28:55Z scope: + plugin/lib/fmkalevala.py, the fm shim the standing rule requires for a new plugin/lib module (kalevala.py)
- 2026-11-05T13:36:26Z scope: + plugin/lib/sampo/moonscale.py and louhi.py: criterion 6 needs the moons store lock on every row write and the exam scenarios read-only for a tower job
- 2026-11-05T13:43:37Z scope: + MASTER.md, docs/map/files-lib-2.md (the brief's standing rule: a new plugin/lib module needs its fm shim, a MASTER bullet and a docs/map line), plugin/lib/sampo/moonscale.py and louhi.py (criterion 6: store lock and exam guard), plugin/lib/fmkalevala.py (the shim)
- 2026-11-05T13:44:28Z scope: + plugin/tests/test_moons_scale.py (the promote-under-held-store test held the store from its own thread; the lock is re-entrant per thread since the criterion-6 change, so the other funnel must be another thread)
- 2026-11-05T13:49:50Z scope: + plugin/tests/test_louhi_models.py (the busy-card test held the store in its own thread; now re-entrant per thread, so it holds it from another thread as the promote test does)
- 2026-11-05T13:54:18Z scope: rune.py (_seed's Capabilities section, CAPS, _caps_lines) edited for step 4: the seed is where the registry reaches a tower; cli.py close logs areas and title. Logged because rune.py sits outside the planned scope list
- 2026-11-05T14:34:25Z scope widened: budget.py (FOREMAN_SPEND_AS tag on _record), moonscale.py (store_lock wait, grow busy stop), rune.py (public exam_lines/train_scenarios, grow busy exit): the coordinator's review findings 3, 2, 6 name these files; leases held for T-3081
- 2026-11-05T14:58:29Z focused
- 2026-11-05T14:58:34Z ANDON answered: option A for this merge (fresh towers wait for gen-1's put); T-3212 makes Kalevala write gen-1 itself; review findings fixed (2c150a9b), queued for merge
- 2026-11-05T17:21:06Z user approved core in Claude Code's permission prompt
- 2026-11-05T17:37:48Z merged worktree-agent-aac052eb335d8a688 (12 file(s))
- 2026-11-05T17:37:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aac052eb335d8a688
- 2026-11-05T17:39:52Z focused
- 2026-11-05T17:40:58Z affected tests waived: merged lane; the post-merge verify already ran the full suite
- 2026-11-05T17:41:30Z set scope=['plugin/lib/sampo/kalevala.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/night.py', 'plugin/tests/test_kalevala.py', 'plugin/lib/fmkalevala.py', 'plugin/lib/sampo/moonscale.py', 'plugin/lib/sampo/louhi.py', 'MASTER.md', 'docs/map/files-lib-2.md', 'plugin/tests/test_moons_scale.py', 'plugin/tests/test_louhi_models.py', 'plugin/lib/sampo/rune.py', 'plugin/lib/sampo/budget.py', 'CHANGELOG.md']
- 2026-11-05T17:41:31Z scope: the merge daf01510 itself changed these 12 files (moons store lock, tower gen-0 in rune, louhi budget share, shim, map rows) plus the CHANGELOG line
- 2026-11-05T17:41:32Z affected tests waived: merged lane; the post-merge verify already ran the full suite
- 2026-11-05T17:41:39Z done
- 2026-11-05T17:41:42Z committed eb7b7ad3 (1 file)
- 2026-11-05T17:51:30Z verified: the full suite is green on daf015105
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3050 [FEATURE L, blocked, 6 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
- T-3053 [FEATURE M, done, 2 steps] Kalevala part 1: tower namespaces: each Rune tower its own home under one project, sampo genesis --tower NAME, a shared root for moons …
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_night.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/cli.py, plugin/lib/sampo/kalevala.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py; re-ground the plan against them before editing
## Why not caught
none: a feature, not a defect
## Lessons
- a parallel-job feature needs its spend ceiling and its write lock tested before its fan-out
## Files touched
- plugin/tests/test_kalevala.py
- plugin/lib/sampo/kalevala.py
- plugin/lib/sampo/cli.py
- plugin/lib/fmkalevala.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/louhi.py
- MASTER.md
- docs/map/files-lib-2.md
- plugin/tests/test_moons_scale.py
- plugin/tests/test_louhi_models.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/budget.py
- ANDON.md
- CHANGELOG.md
