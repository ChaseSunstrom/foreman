---
id: T-3577
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T02:34:51Z
updated: 2026-11-07T03:22:19Z
lane: ~/.claude/foreman.lanes/T-3577
base_note: 
lane_branch: foreman/T-3577
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:36:52Z
plan0_scope: []
---
# PERFORMANCE hooks hot path (user 2026-11-06: fast-track the Python CPU fixes): every…
## Raw request
> PERFORMANCE hooks hot path (user 2026-11-06: fast-track the Python CPU fixes): every tool call runs PreToolUse and PostToolUse hooks at ~63 ms CPU each (python itself 9 ms), and the statusline and Stop hooks run often too; with 10-100 agents that is cores of CPU. Profile each hook event, then cut import and state-read cost on the hot paths: lazy imports of heavy modules, no full brief load or ledger parse unless the event needs it, cached reads keyed on file stats; target under 25 ms CPU for a PreToolUse Bash allow and PostToolUse, measured with tests/bench_hooks.py before and after
## Interpretation
Reading 1 (chosen): cut the per-call CPU of the existing hook processes (imports, state reads, subprocesses) so PreToolUse Bash allow and PostToolUse fall under 25 ms median CPU, with the guard's decisions unchanged. Reading 2 (ruled out): change how often hooks fire or drop hook work per agent; the hook set and their outputs are a contract other tasks rely on, and the user asked for the Python CPU fixes.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A PreToolUse Bash allow and a PostToolUse import no heavy module (pinned by a subprocess sys.modules check) — verify with `nice -n 10 python3 plugin/tests/run.py test_bench_hooks`
- [ ] The hook, guard and statusline suites stay green — verify with `nice -n 10 python3 plugin/tests/run.py test_hooks test_guard test_guard_latency test_statusline_ui test_bench_hooks`
## Non-goals
Hook firing frequency and agent count (the 10-100 agents scaling is met by the per-call cut, not by firing fewer hooks); a hook daemon; T-3573's state index (core.load_briefs) and the test engine.
## Approach (options → choice → why)
1) Lazy imports + stat-keyed caches on the hot paths. Likely outcome: 55 -> ~25 ms CPU on PreToolUse/PostToolUse; fails if: the residual cost is python startup itself. 2) use what exists: core._Later stand-ins and the existing state caches, extended to the modules still imported eagerly. Likely outcome: most of the import win for a small diff; fails if: the heavy cost is state reads, not imports. 3) A long-lived hook daemon over a socket. Likely outcome: ~10 ms; fails if: stale code after edits or a dead daemon weakens fail-closed. 4) do less: only lazy-import the top 3 modules by importtime. Likely outcome: ~15 ms saved; fails if: the 25 ms target needs the state-read cuts too. Choice 1+2 (85%): importtime already shows ~25 ms of the ~37 ms floor is sampo.hooks' import tree; measured per event, biggest cost first, reusing _Later; 3 rejected for the fail-closed risk.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a PreToolUse Bash allow and a PostToolUse load none of the heavy modules
2. [x] Profile each event (bench_hooks, importtime, cProfile) and cut import and state-read cost on the hot paths
3. [x] Hook suites green; bench before/after per event
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_bench_hooks` → ✗ exit 1 · Ran 6 tests in 17.2s (6 jobs, 16 at a time; slowest: HotPathImports 14s, Modules.test_a_hook_run_records_the_plugin_files_its_process_imported 13s, Modules.test_the_hook_writes_only_under_the_temp_dir [ran] [tree 054fe75fdfd1] [world 2f1906870a] (2026-11-07T02:45:21Z)
- (step 2) `nice -n 10 python3 plugin/tests/bench_hooks.py --runs 10` → exit 0 · SessionEnd                  27.8    33.7     150  [0] / machine busy (load 2.0 per core): judged by each hook's CPU time, not wall time (T-0805) [ran] [tree 37ad63bd185a] [world 2f1906870a] (2026-11-07T03:12:30Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_bench_hooks` → exit 0 · Ran 8 tests in 57.2s (8 jobs, 16 at a time; slowest: HotPathImports.test_the_hot_events_load_no_heavy_module 5s, Modules.test_a_hook_run_records_the_plugin_files_its_process_imported 4s, ActiveMemo 1s [ran] [tree 37ad63bd185a] [world 2f1906870a] (2026-11-07T03:13:43Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_hooks test_guard test_guard_latency test_guard_cases test_guard_evasions test_statusline_ui test_bench_hooks test_tool_taint test_core test_fixes test_map test_recall test_ambient test_bus test_anergy test_library test_lib_hostile test_ledger_chain test_ledger_index test_state_volatile test_docs` → exit 0 · Ran 1147 tests in 80.2s (627 jobs, 16 at a time; slowest: Mutation 17s, SessionStart.test_budget_holds_with_large_queue 11s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_py [ran] [tree 37ad63bd185a] [world 2f1906870a] (2026-11-07T03:13:54Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_tool_taint test_hooks test_bench_hooks test_statusline_ui test_guard_latency test_core` → exit 0 · Ran 450 tests in 114.6s (298 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 11s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_tak [ran] [tree 6426f7d7d96d] [world 2f1906870a] (2026-11-07T03:22:19Z)
## Log
- 2026-11-07T02:34:51Z created
- 2026-11-07T02:36:01Z set type=PERFORMANCE
- 2026-11-07T02:36:25Z planned: it has criteria and steps
- 2026-11-07T02:36:26Z lane: ~/.claude/foreman.lanes/T-3577 on foreman/T-3577
- 2026-11-07T02:36:50Z focused
- 2026-11-07T02:36:52Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3352 [PERFORMANCE S, done, 2 steps] Measure the hook handler: hook_ms events carry the tool name and the guard's own ms, so the PreToolUse handler's 32 → 90 ms p50 ris…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-07: [costly] T-3571: speed Sampo up with a native Rust fast path for the per-call hot paths (hook dispatch, guard, statusline, ui, next) plus a state in…
