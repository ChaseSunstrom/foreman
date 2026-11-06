---
id: T-3306
type: FEATURE
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T03:59:24Z
updated: 2026-11-06T07:10:41Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a3d676939daa74e0b
lane_branch: worktree-agent-a3d676939daa74e0b
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:20:51Z
plan0_scope: []
builder_returned: 2026-11-06T07:10:41Z
---
# Sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file…
## Raw request
> sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file (cli.py, MASTER.md, core.py), because nearly every test imports cli: on 2026-11-06 eight builders each ran such a set at once (plus reruns after load flakes) and held the host at load 100-250. Select affected tests by the changed symbols (functions a test reaches), not by file import, and let a builder's pre-commit check stop at its own modules plus the symbol-affected set
## Interpretation
Reading 1 (chosen): when a changed file is a hub (linked to over a quarter of the test files), select tests by changed symbols, not by file. Reading 2 (ruled out): cap or sample the set, which misses real breaks.
## Assumptions (confidence)
## Acceptance criteria
- [ ] one hub function change selects only tests naming it plus convention tests (10 import hub, 2 name it) — verify with `python3 plugin/tests/run.py test_affected_symbols -k one_function`
- [ ] a module-level side-effect change to a hub falls back to file-level — verify with `python3 plugin/tests/run.py test_affected_symbols -k module_level`
- [ ] --json lists per changed hub the symbols and tests chosen — verify with `python3 plugin/tests/run.py test_affected_symbols -k json`
## Non-goals
## Approach (options → choice → why)
1) Symbol-level selection from old/new ast+difflib; likely outcome: ~2000 tests drop to tens; fails if a test reaches the symbol without naming it. 2) Per-test coverage map; fails: stale, needs a traced run. 3) Cap/sample; fails: misses breaks. 4) Split cli.py; fails: large, not core.py. 5) use what exists: map.tests_for links and git show of base; likely outcome: no new state. 6) do less: file-level only (today); likely outcome: 70-minute runs. Choice 1 (80%): cheap, no state, falls back to file-level on doubt.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red, then symbol selection in map.py + cli.affected
2. [x] weight-based hub test, measure, affected check
3. [x] Review fixes: close over in-file usage, verb mapping, keep map-links tests, one diff/tree
## Resume here
<!-- auto -->
- 2026-11-06T07:03:46Z step 3/3: Review fixes: close over in-file usage, verb mapping, keep map-links tests, one diff/tree
- git: worktree-agent-a3d676939daa74e0b; 3 uncommitted: plugin/lib/sampo/map.py, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py
- touched since last checkpoint: plugin/tests/test_affected_symbols.py, plugin/tests/test_affected_hubs.py, plugin/lib/sampo/map.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_affected_symbols` → ✗ exit 1 · Ran 7 tests in 14.0s (1 jobs, 16 at a time; slowest: AffectedSymbols 3s) / FAILED (1 classes: test_affected_symbols.AffectedSymbols) (ran] (tree f62c755c9fa4] (world 2f1906870a] (2026-11-06T06:22:16Z)
- (step 1) `python3 plugin/tests/run.py test_affected_symbols` → exit 0 · Ran 7 tests in 153.9s (1 jobs, 16 at a time; slowest: AffectedSymbols 3s) / OK (ran] (tree 2a0a5b27fa88] (world 2f1906870a] (2026-11-06T06:25:33Z)
- (step 2) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → exit 0 · Ran 13 tests in 88.2s (3 jobs, 16 at a time; slowest: AffectedSymbols 5s, AffectedHubs 3s, AffectedRules 1s) / OK (ran] (tree ab751a5df3bb] (world 2f1906870a] (2026-11-06T06:29:00Z)
- (step 2) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_map test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 491 tests in 929.0s (124 jobs, 16 at a time; slowest: AffectedPairs 238s, TaskLifecycle 18s, LouhiModels 12s) / FAILED (2 classes: test_cli.AffectedPairs, test_left_out.LeftOut) (ran] (tree ab751a5df3bb] (world 2f1906870a] (2026-11-06T06:44:43Z)
- (step 2) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → exit 0 · Ran 13 tests in 38.3s (3 jobs, 16 at a time; slowest: AffectedSymbols 7s, AffectedHubs 6s, AffectedRules 1s) / OK (ran] (tree ab751a5df3bb] (world 2f1906870a] (2026-11-06T06:51:47Z)
- (step 3) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → ✗ exit 1 · Ran 23 tests in 31.0s (20 jobs, 16 at a time; slowest: AffectedHubs 3s, AffectedSymbols.test_a_test_with_a_map_links_line_is_always_kept 1s, AffectedSymbols.test_a_changed_default_names_its_function 1 (ran] (tree a754bd5951f5] (world 2f1906870a] (2026-11-06T07:06:34Z)
- (step 3) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → exit 0 · Ran 23 tests in 10.0s (20 jobs, 16 at a time; slowest: AffectedHubs 2s, AffectedSymbols.test_json_lists_per_hub_the_symbols_and_tests_chosen 1s, AffectedSymbols.test_a_star_import_falls_back_to_the_fi (ran] (tree 6906347e0416] (world 2f1906870a] (2026-11-06T07:06:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_map test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 525 tests in 192.3s (222 jobs, 16 at a time; slowest: AffectedPairs 131s, KalevalaStep 13s, AffectedSymbols 10s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 6906347e0416] (world 2f1906870a] (2026-11-06T07:10:20Z)
## Log
- 2026-11-06T03:59:24Z created
- 2026-11-06T06:20:39Z planned: it has criteria and steps
- 2026-11-06T06:20:50Z focused
- 2026-11-06T06:20:51Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T06:26:37Z focused
- 2026-11-06T06:27:11Z focused
- 2026-11-06T06:49:44Z focused
- 2026-11-06T06:59:55Z focused
- 2026-11-06T07:02:12Z focused
- 2026-11-06T07:03:25Z focused
- 2026-11-06T07:06:37Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3286 [FEATURE M, active, 3 steps] Moon C-007591: sampo flakes forecasts which tests will likely flake before a run and tells a known-flake red from a real break
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- similar finished tasks took 4–4 steps
