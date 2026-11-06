---
id: T-3252
type: PERFORMANCE
tier: L
status: dropped
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_slots.py, plugin/tests/perf_bench.py, plugin/tests/test_perf_bench.py, plugin/tests/forkcli.py, plugin/tests/test_cli_speed.py, plugin/tests/helpers.py, research/perf/, plugin/lib/sampo/lanes.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T00:07:13Z
updated: 2026-11-06T03:02:17Z
base_note: 
rival_at: 2026-11-06T00:20:22Z
rival_split: true
base: fd073c44daf9d432d1398e14e3f6f50953d0af6a
base_tree: 1395d0f856bc85c5cb17e6367024623b0efa3931
plan0_at: 2026-11-06T00:38:55Z
plan0_scope: []
---
# PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
## Raw request
> PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured 2026-11-05: load 62 on 16 CPUs; test-spawned sampo CLI calls take 427% CPU (190 ms each under load vs 20 ms bare python; 6,700 call sites in the tests); each test runner takes -j cpu_count, so 4 runners (mine, 3 builders) put 64 workers on 16 CPUs; the same test classes re-run across evidence, task finish, check --affected, ship's scratch tree, post-merge verify and every builder; 19 chromium processes from per-check browser launches; llama-server uses 200% CPU for GPU-resident models. Parts: (1) one machine-wide slot pool (a make-style jobserver, flock tokens = CPUs) that every run.py, sampo check, ship and lane gate draws from; (2) a content-addressed pass cache per test class (hash of the test file, every sampo module it imports, python version) shared across worktrees, so an unchanged class never re-runs; (3) a fork server for the tests' fm()/sampo calls: import sampo once, fork per call; (4) one shared headless browser per run for works and page tests; (5) background generators on SCHED_IDLE by default and model servers' CPU threads capped when the model is fully on the GPU. Bar: the full suite and a builder's gates no slower than today when alone, and faster when 4 run at once; host load at or under CPUs while 3 builders work
## Interpretation
Reading 1 (chosen): cut the CPU Sampo's own work burns (tests, gates, CLI calls, renders, background generators) so the host stays near its CPU count with 3 builders out, and runs finish sooner, not later. Measured 2026-11-05: load 62 on 16 CPUs; test-spawned sampo calls 427% CPU; a verb costs 140-270 ms under load against 24 ms for bare python (97 regex compiles ~45 ms, Python 3.14 argparse colour and help checks ~40 ms, imports the rest); 4 runners x -j 16 = 64 workers. Reading 2: only cap CPU (nice/cgroup quotas); rejected: the user asked for faster, and a cap alone makes each run slower.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a bench script records the suite alone, 4 suites at once, a CLI call and host load, before and after, in research/perf/ — verify with `python3 plugin/tests/run.py test_perf_bench`
- [ ] concurrent runners share one CPU-count slot pool (a second holder waits, a dead holder frees its slot, nested runs never wait, SAMPO_SLOTS=0 or a timed-out wait runs without); the wall-time comparison moves to T-3296's ABAB bench (the 2026-11-06 after-row was contaminated by a concurrent full check) — verify with `python3 plugin/tests/run.py test_slots`
- [ ] a CLI verb costs at most half today's time cold (lazy regexes, lean argparse), and a test's fm() call at most 15 ms through the fork server, with no sampo module reading the environment at import — verify with `python3 plugin/tests/run.py test_cli_speed`
- [x] an unchanged test class is not re-run by check --affected or evidence runs across worktrees, while ship and post-merge gates always run in full — verify with `python3 plugin/tests/run.py test_pass_cache`
- [x] works and page tests share one browser per run; moons, cards and night run SCHED_IDLE by default — verify with `python3 plugin/tests/run.py test_slots test_design_works`
- [x] sampo cpu cap 50 keeps every Sampo session's scope (Claude, builders, tests, generators) at half the CPUs, applied at SessionStart; off lifts it — verify with `python3 plugin/tests/run.py test_slots`
- [ ] the tests' 6,700 fm call sites go through the fork server, each call at most 15 ms — verify with `python3 plugin/tests/run.py test_cli_speed`
- [x] chromium: one browser per run instead of per-check launches, so a run holds at most one browser's processes — verify with `python3 plugin/tests/run.py test_design_works`
- [x] llama-server and Ollama models fully on the GPU run with their CPU threads capped (measured: 200% CPU before) — verify with `python3 plugin/tests/run.py test_slots`
## Non-goals
## Approach (options → choice → why)
1) use what exists, attack the waste at each layer. Slot pool: flock token files, one per CPU, in XDG_RUNTIME_DIR, drawn by every run.py (sampo check, the ship and post-merge verify all run it), so 4 runners share 16 slots instead of 64 thrashing workers. Cheaper CLI calls: lazy regexes, argparse with color off and no per-argument help check, then a fork server for the tests' fm() calls with module-level env reads audited. Pass cache: per test class, keyed on the files the class and its subprocess calls imported plus non-Python inputs, for check --affected and evidence runs only, never the final gates. One headless browser per run. Generators on SCHED_IDLE, model servers' CPU threads capped. sampo cpu cap PCT kept on every session's scope. likely outcome: same or better wall time alone, much better with 4 at once, load near CPUs.
2) cgroup CPU quotas per runner only. fails if: contention moves into throttling, each run slower, nothing gets cheaper.
3) lower -j everywhere. fails if: a run alone gets slower, the opposite of the ask.
4) do less: nice and SCHED_IDLE everything. fails if: equal-priority runners still thrash; it helps only the generators.
Choice 1 (80%): each part is measured alone against the bench and kept only if it wins; the pass cache is the riskiest (a stale pass) so it never feeds the final gates.
## Risks and rollback
A stale cached pass hides a red: the cache serves only iteration runs, the ship and post-merge verify always run in full, and the key includes every imported file's hash plus a global hash of non-Python inputs; FOREMAN_NO_PASS_CACHE=1 turns it off. A forked CLI keeps a parent's module state (env read at import): the fork server is opt-in per test helper, an audit test asserts no sampo module reads FOREMAN_HOME or HOME at import, and any mismatch falls back to a fresh process. A slot pool deadlock or leak: flock releases on process death; a waiter times out to running without a slot and logs it. Each part is its own commit; revert one without the rest.
## Execution prompt
## Steps
1. [x] bench first: measure today's numbers (suite alone, 4 at once, CLI call, load)
2. [x] slot pool in run.py, sampo check and the ship's scratch run
3. [ ] lazy regexes and lean argparse in the CLI  <- CURRENT
4. [ ] fork server for the tests' fm() calls, with the import-time env audit
## Resume here
<!-- auto -->
- 2026-11-06T02:11:34Z step 4/8: fork server for the tests' fm() calls, with the import-time env audit
- git: foreman/build; 8 uncommitted: plugin/tests/helpers.py, plugin/tests/run.py, plugin/tests/forkcli.py, plugin/tests/perf_bench.py, plugin/tests/test_cli_speed.py, plugin/tests/test_perf_bench.py, plugin/tests/test_slots.py, scripts/
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_perf_bench` → ✗ exit 1 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: Bench 0s) / FAILED (1 classes: test_perf_bench.Bench) [ran] [tree 261df9234972] [world 2f1906870a] (2026-11-06T00:39:06Z)
- (step 1) `python3 plugin/tests/run.py test_perf_bench` → exit 0 · Ran 1 tests in 2.9s (1 jobs, 16 at a time; slowest: Bench 2s) / OK [ran] [tree c2a5caf84ecb] [world 2f1906870a] (2026-11-06T00:39:09Z)
- (step 2) `python3 plugin/tests/run.py test_slots` → ✗ exit 1 · Ran 5 tests in 0.5s (1 jobs, 16 at a time; slowest: Slots 0s) / FAILED (1 classes: test_slots.Slots) [ran] [tree 6c46376b61e1] [world 2f1906870a] (2026-11-06T00:39:18Z)
- (step 2) `python3 plugin/tests/run.py test_slots test_run` → exit 0 · Ran 97 tests in 11.3s (56 jobs, 16 at a time; slowest: PerTestJobs 9s, DiffGates 8s, Hang 7s) / OK [ran] [tree b602634b89f5] [world 2f1906870a] (2026-11-06T00:40:09Z)
- (step 4) `python3 plugin/tests/run.py test_cli_speed` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 1.2s (1 jobs, 8 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 87af9ab1faf5] [world 2f1906870a] (2026-11-06T00:43:35Z)
- (ac 3) `python3 plugin/tests/run.py test_cli_speed 2>&1 | grep -E 'Error|assert|FAIL|OK|forked' | head -12` → ✗ exit 1 · FAILED (failures=1) / FAILED (2 classes: test_cli_speed.ForkServer, test_cli_speed.ImportAudit) [ran] [tree feb6db828a94] [world 2f1906870a] (2026-11-06T00:45:01Z)
- (ac 7) `python3 plugin/tests/run.py test_cli_speed 2>&1 | grep -E 'Error|assert|FAIL|OK|forked' | head -12` → ✗ exit 1 · FAILED (failures=1) / FAILED (2 classes: test_cli_speed.ForkServer, test_cli_speed.ImportAudit) [ran] [tree feb6db828a94] [world 2f1906870a] (2026-11-06T00:45:01Z)
- (step 3) `python3 plugin/tests/run.py test_cli_speed` → ✗ exit 1 · Ran 5 tests in 20.6s (2 jobs, 16 at a time; slowest: ForkServer 16s, ImportAudit 4s) / FAILED (1 classes: test_cli_speed.ForkServer) [ran] [tree 54d241c69064] [world 2f1906870a] (2026-11-06T02:36:23Z)
- (ac 4) `sampo task show T-3296` → moved to T-3296 (PERF part 2) on 2026-11-06 (2026-11-06T02:56:55Z)
- (ac 5) `sampo task show T-3296` → moved to T-3296 (PERF part 2) on 2026-11-06 (2026-11-06T02:56:57Z)
- (ac 8) `sampo task show T-3296` → moved to T-3296 (PERF part 2) on 2026-11-06 (2026-11-06T02:57:00Z)
- (ac 9) `sampo task show T-3296` → moved to T-3296 (PERF part 2) on 2026-11-06 (2026-11-06T02:57:07Z)
- (ac 6) `sampo task show T-3252` → dropped: the user lifted the CPU limit on 2026-11-06 ('you can use as much CPU as you want now'); runtime cap removed (2026-11-06T02:57:10Z)
## Log
- 2026-11-06T00:07:13Z created
- 2026-11-06T00:19:34Z planned: it has criteria and steps
- 2026-11-06T00:20:34Z set approved=True
- 2026-11-06T00:38:54Z focused
- 2026-11-06T02:08:56Z guard authorization added: system
- 2026-11-06T02:11:00Z paused: focus moved to T-3179
- 2026-11-06T02:11:16Z focused
- 2026-11-06T02:11:21Z paused: focus moved to T-3179
- 2026-11-06T02:11:29Z focused
- 2026-11-06T02:21:57Z steer: after-bench row (02:2xZ) is contaminated: Sampo's sentinel started a full fm check at 20:11 that held pool slots during it; re-run both arms back to back (ABAB). Fills now run as idle-class transient user units (sampo-moons/cards/jeff); step 8 should make them persistent units so a reboot doesn't stop them
- 2026-11-06T02:32:58Z steer (user 2026-11-06): 'you can use as much CPU as you want now, and you can run up to like 100 agents, i literally do not care'. Runtime cap lifted (kitty scope CPUQuota removed). Step 8 (sampo cpu cap) becomes opt-in, off by default; the slot pool keeps parallel runs from thrashing rather than capping them. Lane ceiling raised 16 -> 100 (lanes.BUILDERS_MAX)
- 2026-11-06T02:32:58Z set scope=['plugin/tests/run.py', 'plugin/tests/test_slots.py', 'plugin/tests/perf_bench.py', 'plugin/tests/test_perf_bench.py', 'plugin/tests/forkcli.py', 'plugin/tests/test_cli_speed.py', 'plugin/tests/helpers.py', 'research/perf/', 'plugin/lib/sampo/lanes.py', 'CHANGELOG.md']
- 2026-11-06T02:32:58Z scope: plugin/lib/sampo/lanes.py for BUILDERS_MAX 16 -> 100, the user's run-up-to-100-agents steer on this CPU/parallelism task
- 2026-11-06T02:56:53Z criterion 2 text: 4 concurrent runners share one CPU-count slot pool: host load stays at or under 1.25 x CPUs and their total wall time beats today's → concurrent runners share one CPU-count slot pool (a second holder waits, a dead holder frees its slot, nested runs never wait, SAMPO_SLOTS=0 or a timed-out wait runs without); the wall-time comparison moves to T-3296's ABAB bench (the 2026-11-06 after-row was contaminated by a concurrent full check)
- 2026-11-06T02:57:12Z step 5 removed: pass cache for iteration runs only
- 2026-11-06T02:57:13Z step 5 removed: one browser per run; SCHED_IDLE generators; model thread caps
- 2026-11-06T02:57:15Z step 5 removed: bench after: record before and after, keep only what won
- 2026-11-06T02:57:17Z step 5 removed: a cap that keeps: sampo cpu cap PCT (default 50) sets CPUQuota on the session's own scope at every SessionStart, sampo cpu shows it, off removes it
- 2026-11-06T02:57:18Z steer: split — steps 5-7 (pass cache, browser/SCHED_IDLE/model threads, ABAB bench) moved to T-3296; step 8 (cpu cap) dropped by the user's 2026-11-06 steer; criteria 4,5,8,9 moved, 6 dropped
- 2026-11-06T03:02:17Z dropped: split: part 1 (bench, slot pool, fork server, lane ceiling) recreated with --redo and criteria matching what was measured; part 2 is T-3296; the CPU cap step was dropped by the user's 2026-11-06 steer
- 2026-11-06T03:02:17Z work at drop saved: 67fadc4ce113 (restore: git -C ~/.claude/foreman restore --source=67fadc4ce113 --worktree -- :/)
## Follow-ups captured
## Build vs reuse
Reuse: run.py's ThreadPoolExecutor and busy_factor, lanes' host_strain gate, cli.py's per-verb parser (T-2016), check's identical-tree reuse (T-2644), shot.find_browser, sandbox's job_env. New: a slots module (flock pool, ~60 lines), a pass cache (~150), a fork server (~120). No dependency.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: implement all five parts as a coherent resource-governance layer. The jobserver (`plugin/tests/run.py` plus `sampo check`, ship, lane gate) is the core, and parts 2–5 reduce the work that draws tokens. The bar is measurable: alone no slower, 4 concurrent faster, load ≤ 16 with 3 builders.
- Narrower: only parts 1 and 5 (throttling and priority), accepting repeated work. This meets the "load ≤ CPUs" bar but not "faster when 4 run at once", since duplicated test classes still run.
- Narrower: only parts 2 and 3 (cache plus fork server), which cut CPU per call and per class but leave `-j cpu_count` oversubscription across 4 runners untouched.
- Diagnostic-first: add a measurement harness (load, per-call CPU, chromium count) and pick fixes from the data. The request already lists the measurements, so this is likely a deliverable for the bar, not the whole task.
Approaches:
- Jobserver as a small module under `plugin/lib/sampo/` (flock token files in a machine-wide dir, e.g. under `/run/user/<uid>`, tokens = `os.cpu_count()`). `run.py` replaces its `-j cpu_count` pool with token acquisition per worker. Nested callers (`sampo check` → run.py → test-spawned CLI) inherit t…
- Pass cache keyed by sha256 of the test file, the transitive sampo imports (resolved statically via `ast` from `plugin/lib/sampo/*.py` and `plugin/lib/fm*.py`), and the python version. Store it in a git-common-dir or user-level shared path so worktrees hit it. Record only passes. Wire it into `run.p…
- Fork server: a long-lived process that imports `plugin/lib/sampo/cli.py` once and forks per request over a unix socket, with a stdin/stdout/exit-code passthrough. Tests' `fm()`/sampo helpers talk to it, with fallback to subprocess when it is absent. Alternative of lower risk: an in-process call of …
- Browser and priority: one headless chromium launched by `run.py` and shared through a CDP endpoint env var, with per-test contexts instead of per-check launches. Background generators get `os.sched_setscheduler(SCHED_IDLE)` at their launch point. Model server launch args get `--threads` reduced whe…
Failure modes:
- Token deadlock or leak: a worker holding a token spawns a child that also blocks on the pool. Crashed holders must release it, so use flock on fds (auto-released at death), not token files that must be deleted. Missed env inheritance in `plugin/bin/sampo` or `fm` re-exec breaks it.
- Stale or false cache hits: the hash misses dynamic imports, fixtures (`plugin/tests/fixtures/`), data files, `plugin/bin/` scripts or env-dependent behaviour, so a broken class is skipped as passing. Recording flaky or partially-run results as passes is the other path to the same failure.
- Fork server hazards: state leaking between calls (cwd, env, `sys.modules` mutated, open sqlite handles, threads before fork). A server started with an older module version serves stale code after edits unless it is keyed on the source hash. Exit codes and stderr ordering also change, which tests th…
- Alone-case regression: token acquisition, hashing the import closure, socket round trips and the shared browser add latency when the machine is idle. The bar "no slower alone" is violated if the hash is recomputed per class instead of once per run, or if the shared browser serialises page tests tha…
## Dissent
- [x] rival reading: Likeliest: implement all five parts as a coherent resource-governance layer. The jobserver (`plugin/tests/run.py` plus `sampo check`, ship, lane gate) is the core, and parts 2–5 reduce the work that draws tokens. The bar is measurable: alone no slower, 4 concurrent faster, load ≤ 16 with 3 builders. — answered: Agreed, it is the chosen reading: the slot pool is the core and the other parts cut the work that draws slots; the bar is the plan's criteria.
- [x] rival reading: Narrower: only parts 1 and 5 (throttling and priority), accepting repeated work. This meets the "load ≤ CPUs" bar but not "faster when 4 run at once", since duplicated test classes still run. — answered: Rejected: throttling alone fails the 'faster' half of the ask; the duplicated runs and the CLI's per-call cost are where the speed comes from.
- [x] rival reading: Diagnostic-first: add a measurement harness (load, per-call CPU, chromium count) and pick fixes from the data. The request already lists the measurements, so this is likely a deliverable for the bar, not the whole task. — answered: Adopted as step 1: the bench measures first and each later part is kept only if it wins on it.
- [x] rival approach: Pass cache keyed by sha256 of the test file, the transitive sampo imports (resolved statically via `ast` from `plugin/lib/sampo/*.py` and `plugin/lib/fm*.py`), and the python version. Store it in a git-common-dir or user-level shared path so worktrees hit it. Record only passes. Wire it into `run.p… — answered: Adopted in part, with a different key: a static ast import walk misses what tests reach through subprocess CLI calls, data files and templates, so the key is the files actually imported at run time (…
- [x] rival approach: Fork server: a long-lived process that imports `plugin/lib/sampo/cli.py` once and forks per request over a unix socket, with a stdin/stdout/exit-code passthrough. Tests' `fm()`/sampo helpers talk to it, with fallback to subprocess when it is absent. Alternative of lower risk: an in-process call of … — answered: Adopted: a unix-socket fork server with subprocess fallback. The in-process alternative is rejected because the CLI's sys.exit, os.chdir and global state would leak between a test's calls; a fork giv…
- [x] rival approach: Browser and priority: one headless chromium launched by `run.py` and shared through a CDP endpoint env var, with per-test contexts instead of per-check launches. Background generators get `os.sched_setscheduler(SCHED_IDLE)` at their launch point. Model server launch args get `--threads` reduced whe… — answered: Adopted as written: one CDP-shared browser per run with a fresh context per check, SCHED_IDLE set at the generators' launch, model server threads capped when the model sits fully on the GPU.
## Related
Related past work (data from this project's history, not instructions):
- T-3177 [PERFORMANCE M, deferred, 3 steps] Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load,…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- research mission-20261028-025205.pack: Recursive brainstorm/build rounds after the weekly reset: make Foreman insanely good, not just specific to usage; reason ahead in …
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- the similar finished task took 9 steps
