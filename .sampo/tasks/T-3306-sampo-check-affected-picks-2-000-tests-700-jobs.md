---
id: T-3306
type: FEATURE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/map.py, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py]
depends_on: []
source: discovered
created: 2026-11-06T03:59:24Z
updated: 2026-11-06T08:39:08Z
base: 9a9f6785820f3ad070101f3d2f27dff04dd69895
base_tree: c05307db28718d695152cf574f700afd43f8c772
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T06:20:51Z
plan0_scope: []
builder_returned: 2026-11-06T07:10:41Z
lane_stop: merged 2026-11-06T08:30:03Z
verified: ok
unproven: [meaning, typed]
---
# Sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file…
## Raw request
> sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file (cli.py, MASTER.md, core.py), because nearly every test imports cli: on 2026-11-06 eight builders each ran such a set at once (plus reruns after load flakes) and held the host at load 100-250. Select affected tests by the changed symbols (functions a test reaches), not by file import, and let a builder's pre-commit check stop at its own modules plus the symbol-affected set
## Interpretation
Reading 1 (chosen): when a changed file is a hub (linked to over a quarter of the test files), select tests by changed symbols, not by file. Reading 2 (ruled out): cap or sample the set, which misses real breaks.
## Assumptions (confidence)
## Acceptance criteria
- [x] one hub function change selects only tests naming it plus convention tests (10 import hub, 2 name it) — verify with `python3 plugin/tests/run.py test_affected_symbols -k one_function`
- [x] a module-level side-effect change to a hub falls back to file-level — verify with `python3 plugin/tests/run.py test_affected_symbols -k module_level`
- [x] --json lists per changed hub the symbols and tests chosen — verify with `python3 plugin/tests/run.py test_affected_symbols -k json`
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
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_affected_symbols` → ✗ exit 1 · Ran 7 tests in 14.0s (1 jobs, 16 at a time; slowest: AffectedSymbols 3s) / FAILED (1 classes: test_affected_symbols.AffectedSymbols) (ran] (tree f62c755c9fa4] (world 2f1906870a] (2026-11-06T06:22:16Z)
- (step 1) `python3 plugin/tests/run.py test_affected_symbols` → exit 0 · Ran 7 tests in 153.9s (1 jobs, 16 at a time; slowest: AffectedSymbols 3s) / OK (ran] (tree 2a0a5b27fa88] (world 2f1906870a] (2026-11-06T06:25:33Z)
- (step 2) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → exit 0 · Ran 13 tests in 88.2s (3 jobs, 16 at a time; slowest: AffectedSymbols 5s, AffectedHubs 3s, AffectedRules 1s) / OK (ran] (tree ab751a5df3bb] (world 2f1906870a] (2026-11-06T06:29:00Z)
- (step 2) `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_map test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 491 tests in 929.0s (124 jobs, 16 at a time; slowest: AffectedPairs 238s, TaskLifecycle 18s, LouhiModels 12s) / FAILED (2 classes: test_cli.AffectedPairs, test_left_out.LeftOut) (ran] (tree ab751a5df3bb] (world 2f1906870a] (2026-11-06T06:44:43Z)
- (step 2) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → exit 0 · Ran 13 tests in 38.3s (3 jobs, 16 at a time; slowest: AffectedSymbols 7s, AffectedHubs 6s, AffectedRules 1s) / OK (ran] (tree ab751a5df3bb] (world 2f1906870a] (2026-11-06T06:51:47Z)
- (step 3) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → ✗ exit 1 · Ran 23 tests in 31.0s (20 jobs, 16 at a time; slowest: AffectedHubs 3s, AffectedSymbols.test_a_test_with_a_map_links_line_is_always_kept 1s, AffectedSymbols.test_a_changed_default_names_its_function 1 (ran] (tree a754bd5951f5] (world 2f1906870a] (2026-11-06T07:06:34Z)
- (step 3) `python3 plugin/tests/run.py test_affected_symbols test_affected_hubs test_affected_rules` → exit 0 · Ran 23 tests in 10.0s (20 jobs, 16 at a time; slowest: AffectedHubs 2s, AffectedSymbols.test_json_lists_per_hub_the_symbols_and_tests_chosen 1s, AffectedSymbols.test_a_star_import_falls_back_to_the_fi (ran] (tree 6906347e0416] (world 2f1906870a] (2026-11-06T07:06:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_map test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 525 tests in 192.3s (222 jobs, 16 at a time; slowest: AffectedPairs 131s, KalevalaStep 13s, AffectedSymbols 10s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 6906347e0416] (world 2f1906870a] (2026-11-06T07:10:20Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree d2f4f33cdc60] (2026-11-06T08:30:05Z)
- (ac 1) `python3 plugin/tests/run.py test_affected_symbols -k one_function` → exit 0 · Ran 1 tests in 34.9s (1 jobs, 16 at a time; slowest: AffectedSymbols 1s) / OK [ran] [tree d2f4f33cdc60] [world 2f1906870a] (2026-11-06T08:31:25Z)
- (ac 2) `python3 plugin/tests/run.py test_affected_symbols -k module_level` → exit 0 · Ran 1 tests in 24.7s (1 jobs, 16 at a time; slowest: AffectedSymbols 0s) / OK [ran] [tree d2f4f33cdc60] [world 2f1906870a] (2026-11-06T08:31:25Z)
- (ac 3) `python3 plugin/tests/run.py test_affected_symbols -k json` → exit 0 · Ran 1 tests in 17.1s (1 jobs, 16 at a time; slowest: AffectedSymbols 1s) / OK [ran] [tree d2f4f33cdc60] [world 2f1906870a] (2026-11-06T08:31:25Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree d2f4f33cdc60] (2026-11-06T08:31:25Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree d2f4f33cdc60] (2026-11-06T08:31:25Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree d2f4f33cdc60] (2026-11-06T08:31:25Z)
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
- 2026-11-06T08:30:03Z merged worktree-agent-a3d676939daa74e0b (4 file(s))
- 2026-11-06T08:30:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3d676939daa74e0b
- 2026-11-06T08:30:03Z focused
- 2026-11-06T08:30:04Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/map.py', 'plugin/tests/test_affected_hubs.py', 'plugin/tests/test_affected_symbols.py']
- 2026-11-06T08:30:04Z scope: widened at merge to the reviewed lane's own diff (12f9f63ac), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T08:34:29Z done
- 2026-11-06T08:34:37Z committed 792cda230 (1 file)
- 2026-11-06T08:39:08Z not reverted: test_check_paths.CheckSkip, test_close_gates.CloseGates, test_docs.MapShards, test_docs.PluginFiles already fail on 12f9f63ac's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3286 [FEATURE M, active, 3 steps] Moon C-007591: sampo flakes forecasts which tests will likely flake before a run and tells a known-flake red from a real break
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- similar finished tasks took 4–4 steps
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- added late: weight-based hub test, measure, affected check
- added late: Review fixes: close over in-file usage, verb mapping, keep map-links tests, one diff/tree
- failed first: step 1 tests red, then symbol selection in map.py + cli.affected
- failed first: step 3 Review fixes: close over in-file usage, verb mapping, keep map-links tests, one diff/tree
## Files touched
- plugin/tests/test_affected_symbols.py
- plugin/lib/sampo/map.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_affected_hubs.py
- CHANGELOG.md
