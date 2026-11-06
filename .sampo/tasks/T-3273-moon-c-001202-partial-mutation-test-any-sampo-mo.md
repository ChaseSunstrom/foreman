---
id: T-3273
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/modmutate.py, plugin/tests/test_modmutate.py, plugin/lib/sampo/replay.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:42Z
updated: 2026-11-06T03:59:42Z
builder: 2026-11-06T02:27:49Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a69ac4d481749d9c2
lane_branch: worktree-agent-a69ac4d481749d9c2
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:30Z
plan0_scope: [plugin/lib/sampo/modmutate.py, plugin/tests/test_modmutate.py, plugin/lib/sampo/replay.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T03:59:42Z
---
# Moon C-001202 (partial): mutation-test any Sampo module: bench guard --mutate --module X --flip --func F flips comparisons/constants in any function, runs only the tests importing X at idle priority, lists survivors
## Raw request
> Moon C-001202 (partial): mutation-test any Sampo module: bench guard --mutate --module X --flip --func F flips comparisons/constants in any function, runs only the tests importing X at idle priority, lists survivors
## Interpretation
Reading 1 (chosen): the moon's 'file's own tests evolve so it never goes lazy' becomes a survivor report for a Sampo module: mutate one comparison or constant at a time, run only that module's tests, list the lines no test notices. Reading 2 (ruled out): auto-generating new tests that evolve over time, because it needs a model loop and the survivor list is the part that makes a change safer now. Partial: sampo/mutate.py:run and 'bench guard --mutate' (replay.py:255) already mutate, but only fmguard rule sites and flips only inside check* functions (mutate.py:89), with the guard's tests.
## Assumptions (confidence)
## Acceptance criteria
- [ ] modmutate.mutants(src, func=None) returns ast-made compare/constant/boolop flips for every function (not only check*), each parseable and distinct from the source — verify with `python3 plugin/tests/run.py test_modmutate`
- [ ] modmutate.tests_for(module) returns the test files that import that module, and run() reports a planted untested comparison as a survivor and a tested one as killed in a tmp fixture — verify with `python3 plugin/tests/run.py test_modmutate`
- [ ] sampo bench guard --mutate --module <non-guard file> --flip --func NAME uses them (default tests = tests_for, niced, capped by --max/--timeout) and exits 1 on survivors — verify with `python3 plugin/tests/run.py test_modmutate`
## Non-goals
## Approach (options → choice → why)
1. New module modmutate.py (mutants for any function via ast, tests_for by import scan) reusing mutate._sh and sample, wired into the existing bench guard --mutate --module path. Likely outcome: small diff, survivors for any module, one more flag.
2. Generalise mutate.flips with a function-name regex argument. Likely outcome: fewer files but edits a module the guard work depends on, and its text-replace flips can hit strings.
3. A new top-level sampo verb. fails if: cli.py is a hot file and parallel lanes collide on registration.
4. Do less: only pass --tests by hand to the existing command. Likely outcome: still no flips outside check*, and the user must know which tests apply.

Choice 1 (85%): ast-based mutants are exact and new code lives in a new file; registration reuses the existing command. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] Failing tests first: fixture module with one tested and one untested comparison; mutants/tests_for/run assertions  <- CURRENT
2. [x] Write plugin/lib/sampo/modmutate.py (ast NodeTransformer-free: ast.walk compare op swaps, int/bool constant flips, and/or swap; reuse mutate._sh, sample)
3. [x] Wire into replay.cmd_mutate when --module is not fmguard and --flip; add --func arg in cli.py; nice the test command
4. [x] CHANGELOG line; run test_modmutate and test_replay
## Resume here
<!-- auto -->
- 2026-11-06T02:43:40Z step 1/4: Failing tests first: fixture module with one tested and one untested comparison; mutants/tests_for/run assertions
- git: worktree-agent-a69ac4d481749d9c2; 9 uncommitted: MASTER.md, docs/map/files-lib-3.md, docs/map/ops-2.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/mutate.py, plugin/lib/sampo/replay.py, plugin/lib/fmmodmutate.py, plugin/lib/sampo/modmutate.py, plugin/tests/test_modmutate.py
- touched since last checkpoint: plugin/lib/sampo/cli.py, plugin/lib/fmmodmutate.py, MASTER.md, docs/map/files-lib-3.md, docs/map/ops-2.md, plugin/lib/sampo/modmutate.py, plugin/lib/sampo/replay.py, plugin/tests/test_modmutate.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_modmutate` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.4s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 59fd94c000df] [world 2f1906870a] (2026-11-06T02:31:26Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_modmutate -k Flips -k Importers` → exit 0 · Ran 7 tests in 4.1s (2 jobs, 16 at a time; slowest: Importers 3s, Flips 0s) / OK [ran] [tree ef867eaa5b5f] [world 2f1906870a] (2026-11-06T02:33:52Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_modmutate test_replay` → exit 0 · Ran 21 tests in 27.1s (17 jobs, 16 at a time; slowest: Replay.test_replay_reports_changed_verdicts_until_accepted 16s, Importers.test_run_reports_an_untested_comparison_as_a_survivor_and_a_tested_one_ [ran] [tree 7ad6dd3364df] [world 2f1906870a] (2026-11-06T02:35:43Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_modmutate test_replay` → exit 0 · Ran 22 tests in 30.2s (18 jobs, 16 at a time; slowest: Importers.test_run_reports_an_untested_comparison_as_a_survivor_and_a_tested_one_as_killed 18s, Bench.test_flip_module_runs_the_importing_tests_a [ran] [tree dc7c23cfbe4a] [world 2f1906870a] (2026-11-06T02:39:11Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_modmutate test_moons_scale test_parallel test_proof test_rename_scan test_replay test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2201 tests in 3667.9s (718 jobs, 16 at a time; slowest: GoalReview 485s, LouhiModels 485s, TaskLifecycle 484s) / FAILED (43 classes: test_cli.TaskLifecycle, test_proof.Proof, test_design_works.Sta [ran] [tree dc7c23cfbe4a] [world 2f1906870a] (2026-11-06T03:40:37Z)
## Log
- 2026-11-06T02:27:42Z created
- 2026-11-06T02:27:48Z set scope=['plugin/lib/sampo/modmutate.py', 'plugin/tests/test_modmutate.py', 'plugin/lib/sampo/replay.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:27:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3273.builder.md
- 2026-11-06T02:28:30Z focused
- 2026-11-06T02:28:30Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_replay.py, plugin/tests/test_verify_alias.py
