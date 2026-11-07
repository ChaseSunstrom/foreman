---
id: T-3572
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T02:24:27Z
updated: 2026-11-07T03:34:05Z
lane: ~/.claude/foreman.lanes/T-3572
base_note: 
lane_branch: foreman/T-3572
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:32:41Z
plan0_scope: []
---
# A new test engine (user 2026-11-06): the suite has ~7,000 call sites that spawn the…
## Raw request
> PERFORMANCE: a new test engine (user 2026-11-06): the suite has ~7,000 call sites that spawn the sampo CLI as a subprocess (python start + import + full state read each); run tests in forked workers that import Sampo once and call the CLI in-process, keep results cached by the files each test actually read (extend T-3502's run-cache), and for Rust: one shared cargo target dir/sccache across lanes so a change rebuilds incrementally in seconds, cargo nextest, and differential tests that run the Python and Rust paths on the same inputs
## Interpretation
Reading 1 (chosen): phase 1 of the new test engine makes the tests' sampo CLI calls cheaper without changing what they test. self.fm() already forks a warm server per test class (forkcli, T-3297); phase 1 measures it on 6 CLI-heavy modules and closes the gaps the numbers show (a server started per class, CPU hidden from rusage, per-call overhead), keeping FOREMAN_FORK_CLI=0 as the fresh-process switch. Reading 2 (ruled out): build a new in-process CLI engine from scratch - forkcli already is one, and a rewrite would re-earn its isolation work (env audit, locale/start checks, timeouts).
## Assumptions (confidence)
## Acceptance criteria
- [ ] one fork server per run.py answers every class's fm calls (a class starts none of its own); a script from another tree or a gone server falls back to the class's own; a killed class's running call dies with it; FOREMAN_FORK_CLI=0 runs fresh and names no server — verify with `nice -n 10 python3 plugin/tests/run.py test_cli_speed`
- [ ] the CLI-heavy modules pass unchanged through the shared server — verify with `nice -n 10 python3 plugin/tests/run.py test_cli test_goal test_loop test_sync test_bookkeeping test_backlog`
## Non-goals
Later phases of T-3572, not this one: results cached by the files each test read (extending T-3502's run-cache); Rust: one shared cargo target dir/sccache across lanes, cargo nextest; differential tests running the Python and Rust paths on the same inputs. No product code changes; the suite slot lock (T-3541) is not touched.
## Approach (options → choice → why)
Found: forkcli (T-3297) already forks a warm server for every self.fm() call (7,400 sites; 63 -> 18 ms a call), but each class process starts its own server (937 classes x ~50 ms), the server's SIG_IGN reaping hides the forked calls' CPU from rusage, and self.hook() (570 sites) still starts a fresh interpreter. 1) use what exists, extend it: one forkcli server per run.py shared by all its classes (socket path in the env), the per-class server as fallback (sandbox, another tree, server gone), per-call trims (ctypes and statistics preloaded, managers reaped so CPU is counted), and hooks through it with the worker's os.getppid() reading as the caller. likely outcome: ~50 ms and one interpreter start saved per class, hooks 2-3x cheaper, honest CPU numbers. 2) hooks stay fresh. fails if: the coordinator's profile: test hooks are ~1/3 of test_hooks' CPU. 3) true in-process calls, no fork. fails if: module globals, cwd, env and os._exit leak between calls. 4) a machine-wide server kept across runs. fails if: it serves stale code after an edit. 5) do less: keep the per-class server, only reap and preload. likely outcome: honest CPU, a few ms a call, the per-class start stays. Choice 1 (85%): the largest remaining fixed costs, a small diff in run.py/forkcli/helpers, FOREMAN_FORK_CLI=0 still runs fresh; hook calls with flags= (a stand-in claude as parent) stay fresh.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a class run by run.py gets its fm calls answered by the run's server, starting none of its own
2. [x] run.py starts one server per run and exports its socket; forkcli uses it, falls back to its own
3. [x] per-call trims: preload ctypes, reap managers so their CPU is counted; measure the 6 modules before/after
4. [x] run every module that calls fm, niced in background batches; report opt-outs
## Resume here
## Docs impact
none: test-runner internals only (forkcli's module docstring and the code comments say how the shared server works); no user-facing doc or map entry names forkcli
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cli_speed -k SharedServer` → ✗ exit 1 · Ran 3 tests in 120.7s (1 jobs, 16 at a time; slowest: SharedServer 0s) / FAILED (1 classes: test_cli_speed.SharedServer) [ran] [tree 504ecee4d57b] [world 2f1906870a] (2026-11-07T02:38:07Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cli_speed -k SharedServer` → exit 0 · Ran 3 tests in 50.0s (1 jobs, 16 at a time; slowest: SharedServer 1s) / OK [ran] [tree 7e0ab2fa4e90] [world 2f1906870a] (2026-11-07T02:41:23Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_cli_speed` → exit 0 · Ran 11 tests in 34.2s (8 jobs, 16 at a time; slowest: ForkServer.test_fm_calls_match_and_cost_a_fraction 3s, ForkServer.test_a_slow_call_times_out_and_is_killed 1s, SharedServer 1s) / OK [ran] [tree 9ef604f83c64] [world 2f1906870a] (2026-11-07T02:41:58Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_cli_speed` → exit 0 · Ran 12 tests in 45.5s (3 jobs, 16 at a time; slowest: ForkServer 4s, SharedServer 2s, ImportAudit 1s) / OK [ran] [tree 17a4751063f8] [world 2f1906870a] (2026-11-07T03:19:58Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_cli_speed test_run test_diff_gates` → exit 0 · Ran 125 tests in 64.9s (90 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 7s, State 7s, PerTestJobs.test_a_k_run_keeps_a_whole_class_time_and_a_full_run_recor [ran] [tree 17a4751063f8] [world 2f1906870a] (2026-11-07T03:21:03Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_hooks test_cli test_goal test_loop test_sync test_bookkeeping test_backlog` → exit 0 · Ran 601 tests in 151.3s (359 jobs, 16 at a time; slowest: Stop 79s, AffectedPairs 11s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_takes_0_4_s 9s) / OK [ran] [tree 17a4751063f8] [world 2f1906870a] (2026-11-07T03:23:35Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_cli_speed` → exit 0 · Ran 12 tests in 2.8s (3 jobs, 16 at a time; slowest: ForkServer 2s, SharedServer 1s, ImportAudit 0s) / OK [ran] [tree 17a4751063f8] [world 2f1906870a] (2026-11-07T03:23:59Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py test_cli test_goal test_loop test_sync test_bookkeeping test_backlog` → exit 0 · Ran 329 tests in 11.7s (227 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 6s, Checks.test_the_suite_gate_deadline_scales_with_load_and_a_timeout_names_both 3s, ForkServer 3s) / OK [ran] [tree 17a4751063f8] [world 2f1906870a] (2026-11-07T03:24:11Z)
- (step 3) `nice -n 15 python3 plugin/tests/run.py -j 4 test_cli_speed test_run test_diff_gates` → exit 0 · Ran 125 tests in 142.0s (76 jobs, 4 at a time; slowest: DiffGates 7s, PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 6s, Hang 5s) / OK [ran] [tree 908e8a7e2ff8] [world 2f1906870a] (2026-11-07T03:34:05Z)
## Log
- 2026-11-07T02:24:27Z created
- 2026-11-07T02:32:08Z planned: it has criteria and steps
- 2026-11-07T02:32:17Z lane: ~/.claude/foreman.lanes/T-3572 on foreman/T-3572
- 2026-11-07T02:32:40Z focused
- 2026-11-07T02:32:41Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T02:46:08Z criterion 1 text: one fork server per run.py answers every class's fm calls (a class starts none of its own); a sandboxed run, a script from another tree or a gone server fall back as before; FOREMAN_FORK_CLI=0 runs fresh → one fork server per run.py answers every class's fm calls (a class starts none of its own); a script from another tree or a gone server falls back to the class's own; a killed class's running call dies with it; FOREMAN_FORK_CLI=0 runs fresh and names no server
- 2026-11-07T02:54:28Z steer (coordinator): route self.hook() through the fork path too; fix test_diff_gates.test_run_py_repeats_p (88 s) if small. Done: the forked worker's os.getppid() reads as the caller (the hook's Claude Code lookup, T-1226, and SessionStart's pids see the test, as fresh); flags= calls stay fresh (a stand-in claude must be the parent); sampo.hooks not preloaded (reads FOREMAN_HOOK_SLACK at import). The 88 s was a CPU-slot wait outside run.py: its nested run now sets SAMPO_SLOTS=0. lane_train/git_repo git calls captured as T-3581.
- 2026-11-07T03:19:22Z numbers (niced, SAMPO_SLOTS=0, --shard 1/1 so every config plans the same jobs; CPU = user+sys of run.py and all it waited for; 'before' = base tree with only the reaping/atexit accounting fix so its forked CPU is visible): 7 modules (test_hooks, test_cli, test_goal, test_loop, test_sync, test_bookkeeping, test_backlog), load 11-39: fresh 116.0 s wall / 469.8 s CPU; before (per-class server) 95.0 / 304.0; after (shared server + forked hooks) 60.4 / 231.2. test_hooks alone: 43.7/203.0 -> 16.6/141.3. Round 1, 6 modules, fm sharing only (load 25-30): 85.2/120.8 -> 75.0/111.5 (fresh 159.5/235.1). Per call: hook PostToolUse 51-54 -> 17 ms, PreToolUse 66-70 -> 31 ms. Sweep: all 325 modules that call fm or hooks, 5 batches, 6,566 tests, OK; no test opted out.
- 2026-11-07T03:19:35Z scope: plugin/tests/forkcli.py, run.py, helpers.py (fork path, hooks), test_cli_speed.py (tests), test_run.py (comment), test_diff_gates.py (coordinator steer: its nested run skips the slot pool)
- 2026-11-07T03:31:42Z review fold-in (coordinator): test_run's in-process run.main() calls run under FOREMAN_FORK_CLI=0 (in_process() helper) so they start no server and leave no FOREMAN_FORK_SERVER; pidfd_open failure falls back to a plain wait; the accept loop survives a failed accept or fork; sweep() removes dead runs' fmfork-<pid>- folders (tested); PYTHONHASHSEED is already in START_ENV via the PYTHON prefix (comment says so). Squashed into 899b04452.
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-07: [costly] T-3571: speed Sampo up with a native Rust fast path for the per-call hot paths (hook dispatch, guard, statusline, ui, next) plus a state in…
- similar past tasks were L: consider --tier L
