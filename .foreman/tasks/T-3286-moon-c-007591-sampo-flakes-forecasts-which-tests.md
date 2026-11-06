---
id: T-3286
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/flake_forecast.py, plugin/tests/test_flake_forecast.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:34:16Z
updated: 2026-11-06T04:00:55Z
builder: 2026-11-06T02:34:29Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-ad7f14ad9f7a9a506
lane_branch: worktree-agent-ad7f14ad9f7a9a506
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:43:23Z
plan0_scope: [plugin/lib/sampo/flake_forecast.py, plugin/tests/test_flake_forecast.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:00:55Z
---
# Moon C-007591: sampo flakes forecasts which tests will likely flake before a run and tells a known-flake red from a real break
## Raw request
> Moon C-007591: sampo flakes forecasts which tests will likely flake before a run and tells a known-flake red from a real break
## Interpretation
Reading 1 (chosen): flake ledger flakes.json already records fails/passes per test (core.note_flakes, doctor.check_flaky_rates warns after the fact); the missing part is a pre-run forecast naming likely flakes and their trigger (load vs chance), plus telling a red run's known flakes from new failures. Reading 2 (ruled out): an ML model predicting flakes from code, because the ledger has 51 entries and no features worth training on.
## Assumptions (confidence)
## Acceptance criteria
- [ ] forecast() ranks flakes.json entries by fail rate and tags each trigger (load for timing/deadline/timeout text, else chance), weighted up when loadavg per cpu is high — verify with `python3 plugin/tests/run.py test_flake_forecast`
- [ ] sampo flakes prints the ranked forecast and, given failing test names (--red NAME ...), says which are known flakes (with trigger and a rerun hint) and which are new, so a possibly real break — verify with `python3 plugin/tests/run.py test_flake_forecast`
- [ ] a missing, empty or damaged flakes.json prints a plain 'no flake history' line and exits 0 — verify with `python3 plugin/tests/run.py test_flake_forecast`
## Non-goals
## Approach (options → choice → why)
1. New module flake_forecast.py reading flakes.json: rank by fail rate, trigger tag from the stored why text (timeout, deadline, timing words mean load), scale by loadavg per cpu; verb sampo flakes with --red NAMES to split known from new. Likely outcome: works with existing data, small diff, one registration in cli.py.
2. Extend doctor.check_flaky_rates to print the forecast. Likely outcome: no new verb but doctor is slow and not run before test runs.
3. Parse past run.py outputs and git history for flips to learn triggers. fails if: outputs are not kept per run, so the data is missing.
4. Do less: print the existing top-3 doctor line from a new verb. Likely outcome: no trigger tag and no red classification, so little new.

Choice 1 (85%): uses the existing ledger, adds trigger and red-vs-flake split. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] write failing tests in plugin/tests/test_flake_forecast.py with a fake flakes.json  <- CURRENT
2. [x] add plugin/lib/sampo/flake_forecast.py (forecast, classify_red; reuse the ledger shape from core.note_flakes and the rate logic of doctor.check_flaky_rates)
3. [x] register the flakes verb in cli.py with a small dispatch, add a CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T04:00:00Z step 1/3: write failing tests in plugin/tests/test_flake_forecast.py with a fake flakes.json
- git: worktree-agent-ad7f14ad9f7a9a506; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_flake_forecast.py, plugin/lib/sampo/flake_forecast.py, plugin/lib/sampo/doctor.py, plugin/lib/sampo/cli.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_flake_forecast` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 8.5s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 3f5db5fcf394] [world 2f1906870a] (2026-11-06T02:47:09Z)
- (ac 1) `python3 plugin/tests/run.py test_flake_forecast 2>&1 | tail -6` → exit 0 · Ran 4 tests in 11.8s (4 jobs, 16 at a time; slowest: FlakeForecast.test_a_missing_empty_or_damaged_ledger_says_no_flake_history_and_exits_zero 8s, FlakeForecast.test_sampo_flakes_prints_the_forecast_a [ran] [tree 05d43dc9c580] [world 2f1906870a] (2026-11-06T02:49:12Z)
- (ac 2) `python3 plugin/tests/run.py test_flake_forecast 2>&1 | tail -6` → exit 0 · Ran 4 tests in 11.8s (4 jobs, 16 at a time; slowest: FlakeForecast.test_a_missing_empty_or_damaged_ledger_says_no_flake_history_and_exits_zero 8s, FlakeForecast.test_sampo_flakes_prints_the_forecast_a [ran] [tree 05d43dc9c580] [world 2f1906870a] (2026-11-06T02:49:12Z)
- (ac 3) `python3 plugin/tests/run.py test_flake_forecast 2>&1 | tail -6` → exit 0 · Ran 4 tests in 11.8s (4 jobs, 16 at a time; slowest: FlakeForecast.test_a_missing_empty_or_damaged_ledger_says_no_flake_history_and_exits_zero 8s, FlakeForecast.test_sampo_flakes_prints_the_forecast_a [ran] [tree 05d43dc9c580] [world 2f1906870a] (2026-11-06T02:49:12Z)
- (step 3) `python3 plugin/tests/run.py test_flake_forecast 2>&1 | tail -6` → exit 0 · Ran 4 tests in 11.8s (4 jobs, 16 at a time; slowest: FlakeForecast.test_a_missing_empty_or_damaged_ledger_says_no_flake_history_and_exits_zero 8s, FlakeForecast.test_sampo_flakes_prints_the_forecast_a [ran] [tree 05d43dc9c580] [world 2f1906870a] (2026-11-06T02:49:12Z)
- (step 2) `python3 plugin/tests/run.py test_flake_forecast` → exit 0 · Ran 4 tests in 7.4s (4 jobs, 16 at a time; slowest: FlakeForecast.test_a_missing_empty_or_damaged_ledger_says_no_flake_history_and_exits_zero 5s, FlakeForecast.test_sampo_flakes_prints_the_forecast_an [ran] [tree 05d43dc9c580] [world 2f1906870a] (2026-11-06T02:49:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_flake_forecast test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 488 tests in 215.6s (125 jobs, 16 at a time; slowest: TaskLifecycle 212s, LouhiModels 148s, CaptureAndIntake 119s) / FAILED (1 classes: test_doctor.Checks) [ran] [tree a8460fb2828d] [world 2f1906870a] (2026-11-06T02:53:10Z)
- (step 3) `python3 plugin/tests/run.py test_rename_aliases test_docs test_flake_forecast` → exit 0 · Ran 128 tests in 49.2s (84 jobs, 16 at a time; slowest: RenameAliases.test_nothing_but_the_shims_names_an_old_module 44s, TaskLifecycle 19s, RenameAliases.test_completion_and_help_teach_the_sampo_name [ran] [tree 75d3d0aed6da] [world 2f1906870a] (2026-11-06T02:59:17Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_flake_forecast test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2346 tests in 1268.9s (940 jobs, 16 at a time; slowest: Proof 327s, LeanKindGateHookDelay 309s, LeanKindGateGuardAllow 298s) / FAILED (2 classes: test_hooks.NoTaskGateQueue, test_hooks.NoTaskGateM [ran] [tree 75d3d0aed6da] [world 2f1906870a] (2026-11-06T03:19:22Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_doctor` → exit 0 · Ran 372 tests in 191.9s (308 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 136s, SessionStart.test_the_whole_note_fits_one_budget_with_a_long_mandate 52s, Stop.test_a_te [ran] [tree 75d3d0aed6da] [world 2f1906870a] (2026-11-06T03:27:46Z)
- (step 2) `python3 plugin/tests/run.py test_flake_forecast` → exit 0 · Ran 7 tests in 7.0s (7 jobs, 16 at a time; slowest: FlakeForecast.test_a_missing_empty_or_damaged_ledger_says_no_flake_history_and_exits_zero 5s, FlakeForecast.test_sampo_flakes_prints_the_forecast_an [ran] [tree d65954ed3cc3] [world 2f1906870a] (2026-11-06T03:42:17Z)
- (step 3) `python3 plugin/tests/run.py test_doctor test_flake_forecast` → exit 0 · Ran 121 tests in 13.7s (97 jobs, 16 at a time; slowest: ViewsRepair 12s, LockProbe 8s, NightTimers 8s) / OK [ran] [tree d65954ed3cc3] [world 2f1906870a] (2026-11-06T03:48:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_flake_forecast test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [89.92s] [ran] [tree d65954ed3cc3] [world 2f1906870a] (2026-11-06T03:59:39Z)
## Log
- 2026-11-06T02:34:16Z created
- 2026-11-06T02:34:24Z set scope=['plugin/lib/sampo/flake_forecast.py', 'plugin/tests/test_flake_forecast.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:34:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3286.builder.md
- 2026-11-06T02:43:19Z focused
- 2026-11-06T02:43:23Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:48:08Z scope: plugin/lib/fmflake_forecast.py is the fm shim the standing rule requires for every new plugin/lib/sampo module (test_rename_aliases checks it); also a docs/map line and a MASTER.md bullet for the new verb
- 2026-11-06T02:53:01Z scope widened: docs/map/files-lib-2.md and MASTER.md take one index line and one shard line each for the new fmflake_forecast module, as the standing docs rule requires (every plugin/lib module is listed)
- 2026-11-06T03:40:44Z scope widened for review fixes: doctor.py check_flaky_rates takes the shared flake_forecast.counts rule (the review asked for it); its percent display and rank are unchanged here
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
