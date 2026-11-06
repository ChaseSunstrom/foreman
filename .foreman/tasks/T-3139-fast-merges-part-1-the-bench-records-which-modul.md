---
id: T-3139
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T04:53:33Z
updated: 2026-11-05T09:47:52Z
builder_model: haiku
base: a2ec3766250dd0a0a481e5c633a337e30187c5f2
base_tree: 532c9dc81da299465c06756deba8b19de9d50f3f
plan0_at: 2026-11-05T04:55:57Z
plan0_scope: []
lane_stop: merged 2026-11-05T09:37:07Z
verified: strong
unproven: [perf-typed]
---
# Fast merges part 1: the bench records which modules each hook really imports, and the self-change gate times hooks only when a diff touches one (T-3138)
## Raw request
> Fast merges part 1: the bench records which modules each hook really imports, and the self-change gate times hooks only when a diff touches one (T-3138)
## Interpretation
Reading 1 (chosen): bench_hooks dumps sys.modules' plugin files after each hook fixture run (in the hook's own process, written to a file the bench reads), the base's map is cached per main commit, and selfgate times only when the diff touches a mapped file, a hook entry, hooks.json or a data file a hook reads; the guard replay, footprint and verbs checks always run. Reading 2: the static import closure; rejected, measured 131 of 132 modules reachable statically.
## Assumptions (confidence)
## Acceptance criteria
- [x] a bench run writes, per hook fixture, the plugin files that hook's process imported; the gate skips timing (saying so) when the diff touches none of them and no hook entry or data file, and times as today otherwise — verify with `python3 plugin/tests/run.py test_selfgate test_bench_hooks`
- [x] the hook module map is the union over runs per fixture, refreshed whenever a hook entry, hooks.json or a mapped module changes; an empty or stale map means time as today — verify with `python3 plugin/tests/run.py test_selfgate test_bench_hooks`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the bench already runs every hook fixture; add a modules dump env flag the hook entry honours; likely outcome: most lanes skip the bench. 2. Do less: a hand list of hook modules; fails if: it drifts. 3. Trace imports with an audit hook in every hook run always; fails if: it costs every real hook call. Choice 1 (80%)
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/test_live_page.py, plugin/web/live/index.html, plugin/web/live/live.css, plugin/tests/fixtures/live/machine.json, plugin/lib/sampo/live.py.
## Execution prompt
## Steps
1. [x] failing tests: a diff touching only plugin/web/live/live.js skips timing; one touching hooks.py times
2. [x] the dump, the map cache, the skip
## Resume here
## Docs impact
CHANGELOG line added; the self-change gate's docstring names the module map
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → ✗ exit 1 · Ran 23 tests in 1.3s (8 classes, 16 at a time; slowest: MedianCpu 0s, WhichDiffsAreTimed 0s, Interleaved 0s) / FAILED (2 classes: test_selfgate.WhichDiffsAreTimed, test_bench_hooks.Modules) [ran] [tree e9b8b2d15ea9] [world 2f1906870a] (2026-11-05T04:56:47Z)
- (step 1) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 23 tests in 10.3s (8 classes, 16 at a time; slowest: Modules 10s, WhichDiffsAreTimed 0s, Interleaved 0s) / OK [ran] [tree d5e0db6a503c] [world 2f1906870a] (2026-11-05T04:57:39Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 23 tests in 3.9s (8 classes, 16 at a time; slowest: Modules 3s, WhichDiffsAreTimed 0s, MedianCpu 0s) / OK [ran] [tree d5e0db6a503c] [world 2f1906870a] (2026-11-05T04:58:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_agents test_bench test_bench_hooks test_board_posture test_board_surfaces test_bus test_cli test_cloned_config test_code_tui test_code_worker test_compact test_design_surfaces test_docs test_doctor test_evolve test_firewall test_guard_hardening test_hooks test_hunks test_left_out test_library test_models test_onwrite test_plugins test_rename_scan test_resilience test_safety test_scout test_selfgate test_settings test_setup test_ship test_statusline_ui test_supply_delta test_tool_injection test_ui_replay test_visibility && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [39.88s] [ran] [tree d5e0db6a503c] [world 2f1906870a] (2026-11-05T05:02:58Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 28 tests in 3.6s (9 classes, 16 at a time; slowest: Modules 3s, GateEndToEnd 0s, Interleaved 0s) / OK [ran] [tree 00e28f2c2e89] [world 2f1906870a] (2026-11-05T05:11:51Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_agents test_bench test_bench_hooks test_board_posture test_board_surfaces test_bus test_cli test_cloned_config test_code_tui test_code_worker test_compact test_design_surfaces test_docs test_doctor test_evolve test_firewall test_guard_hardening test_hooks test_hunks test_left_out test_library test_models test_onwrite test_plugins test_rename_scan test_resilience test_safety test_scout test_selfgate test_settings test_setup test_ship test_statusline_ui test_supply_delta test_tool_injection test_ui_replay test_visibility && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [25.89s] [ran] [tree 00e28f2c2e89] [world 2f1906870a] (2026-11-05T05:14:53Z)
- `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 28 tests in 4.2s (9 classes, 16 at a time; slowest: Modules 4s, GateEndToEnd 0s, AaFixtures 0s) / OK [ran] [tree 448626a957e2] [world 2f1906870a] (2026-11-05T09:37:32Z)
- `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → ✗ exit 1 · Ran 28 tests in 2.3s (9 classes, 16 at a time; slowest: Modules 0s, GateEndToEnd 0s, LoadedWallCheck 0s) / FAILED (3 classes: test_selfgate.WhichDiffsAreTimed, test_bench_hooks.Modules, test_selfgate. (start tree + this task's tests) [ran] [tree 448626a957e2] [world 2f1906870a] (2026-11-05T09:37:39Z)
- `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 28 tests in 4.1s (9 classes, 16 at a time; slowest: Modules 4s, GateEndToEnd 0s, Interleaved 0s) / OK [ran] [tree 448626a957e2] [world 2f1906870a] (2026-11-05T09:37:39Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → ✗ exit 1 · Ran 28 tests in 7.3s (9 classes, 16 at a time; slowest: Modules 7s, GateEndToEnd 0s, MedianCpu 0s) / FAILED (1 classes: test_bench_hooks.Modules) [ran] [tree 64c1651d6901] [world 2f1906870a] (2026-11-05T09:38:22Z)
- (ac 2) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → ✗ exit 1 · Ran 28 tests in 7.3s (9 classes, 16 at a time; slowest: Modules 7s, GateEndToEnd 0s, MedianCpu 0s) / FAILED (1 classes: test_bench_hooks.Modules) [ran] [tree 64c1651d6901] [world 2f1906870a] (2026-11-05T09:38:22Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 28 tests in 13.1s (9 classes, 16 at a time; slowest: Modules 12s, GateEndToEnd 1s, WhichDiffsAreTimed 1s) / OK [ran] [tree 64c1651d6901] [world 2f1906870a] (2026-11-05T09:44:30Z)
- (ac 2) `python3 plugin/tests/run.py test_selfgate test_bench_hooks` → exit 0 · Ran 28 tests in 13.1s (9 classes, 16 at a time; slowest: Modules 12s, GateEndToEnd 1s, WhichDiffsAreTimed 1s) / OK [ran] [tree 64c1651d6901] [world 2f1906870a] (2026-11-05T09:44:30Z)
- (audit edge) `builder lane reviewed (fixed after review) and merged; criteria re-run on main green (28 tests, 3 reruns OK after one flaky failure under load, captured)` → a hook whose module map is missing or stale benches as before; a change touching any mapped module still benches [tree 64c1651d6901] (2026-11-05T09:44:30Z)
- (audit intent) `builder lane reviewed (fixed after review) and merged; criteria re-run on main green (28 tests, 3 reruns OK after one flaky failure under load, captured)` → fast merges part 1: the self-change gate's bench only runs when a change reaches modules the hooks load [tree 64c1651d6901] (2026-11-05T09:44:30Z)
## Log
- 2026-11-05T04:53:33Z created
- 2026-11-05T04:53:47Z set approved=True
- 2026-11-05T04:55:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3139.builder.md
- 2026-11-05T04:55:56Z focused
- 2026-11-05T09:37:07Z merged worktree-agent-a4f47c992e4c5af98 (5 file(s))
- 2026-11-05T09:37:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4f47c992e4c5af98
- 2026-11-05T09:37:21Z focused
- 2026-11-05T09:37:39Z scope: files outside its globs came from other tasks' merges and closes landing between its merge and this close
- 2026-11-05T09:47:49Z done
- 2026-11-05T09:47:52Z committed 44a312cd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3138 [PERFORMANCE L, planned, 4 steps] Fast merges: seconds-to-minutes instead of an hour, still proven: a runtime map of what each hook loads, content-hashed test res…
- T-3140 [PERFORMANCE M, planned, 2 steps] Fast merges part 2: test results cached by a hash of every file each test imports, so a merge reruns only tests whose inputs cha…
- T-3118 [PERFORMANCE M, dropped, 0 steps] Merge speed: the self-change gate's paired timing bench (selfgate._benched: any plugin/…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Measurements
none: the saving shows only on merges that skip the bench; T-3176 (base bench cache) and T-3119 (trains) are measured with it
## Lessons
- Merge time hides in repeated work on unchanged inputs: record what a check reads, then skip it when none of that changed
## Plan gaps
- failed first: step 1 failing tests: a diff touching only plugin/web/live/live.js skips timing; one touching hooks.py tim…
## Files touched
- plugin/tests/test_selfgate.py
- plugin/tests/test_bench_hooks.py
- plugin/hooks/hook
- plugin/tests/bench_hooks.py
- plugin/lib/sampo/selfgate.py
- CHANGELOG.md
