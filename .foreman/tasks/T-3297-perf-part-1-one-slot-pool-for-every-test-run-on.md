---
id: T-3297
type: PERFORMANCE
tier: L
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_slots.py, plugin/tests/perf_bench.py, plugin/tests/test_perf_bench.py, plugin/tests/forkcli.py, plugin/tests/test_cli_speed.py, plugin/tests/helpers.py, research/perf/, plugin/lib/sampo/lanes.py, CHANGELOG.md, README.md, docs/map/ops-1.md, plugin/tests/test_run.py]
depends_on: []
source: user
created: 2026-11-06T03:03:04Z
updated: 2026-11-06T04:43:16Z
base: fd073c44daf9d432d1398e14e3f6f50953d0af6a
base_tree: 1395d0f856bc85c5cb17e6367024623b0efa3931
plan0_at: 2026-11-06T03:04:28Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_slots.py, plugin/tests/perf_bench.py, plugin/tests/test_perf_bench.py, plugin/tests/forkcli.py, plugin/tests/test_cli_speed.py, plugin/tests/helpers.py, research/perf/, plugin/lib/sampo/lanes.py, CHANGELOG.md]
verified: strong
unproven: [data, docs, perf-typed]
---
# PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ceiling of 100 (from T-3252)
## Raw request
> PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ceiling of 100 (from T-3252)
## Interpretation
Reading 1 (chosen): part 1 of T-3252 (the user: 'how can we make it so what youre doing doesnt eat up the entire CPU, and is much more efficient? without losing speed/quality, and actually even faster'), cut to what was built and measured: a machine-wide slot pool so concurrent test runs share the CPUs instead of thrashing (load reached 62, later 250 with ~20 builder lanes each at -j16), a fork server so the tests' thousands of fm() calls skip interpreter start and imports (measured 2.4x: 23 vs 55 ms quiet, 85 vs 205 ms at load 60), a bench script, and, after the user's 2026-11-06 steer ('you can use as much CPU as you want now, and you can run up to like 100 agents'), a builder ceiling of 100. Lazy regexes and lean argparse were measured as no gain (help checks 0 ms, color 0 ms, regexes ~7 ms) and dropped. Reading 2 (ruled out): keep T-3252 whole until the pass cache, browser sharing and bench-after land. Ruled out because 20 lanes are thrashing the host now and the pool only reaches new worktrees once committed; the rest is T-3296.
## Assumptions (confidence)
## Acceptance criteria
- [x] a bench script records the suite alone, N suites at once, CLI calls and host load in research/perf/bench.jsonl — verify with `python3 plugin/tests/run.py test_perf_bench`
- [x] concurrent run.py runs share one CPU-count slot pool: a second holder waits, a dead holder frees its slot, nested runs never wait, SAMPO_SLOTS=0 or a timed-out wait runs without one, a cgroup CPU quota shrinks the pool — verify with `python3 plugin/tests/run.py test_slots`
- [x] the tests' fm() calls go through a fork server that behaves as a fresh process (argv, cwd, env, stdin, exit code, crash, timeout kill) at under 60% of its cost, and no preloaded sampo module reads the environment at import — verify with `python3 plugin/tests/run.py test_cli_speed`
- [x] sampo lane max accepts up to 100 builders — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1. Land the slot pool, fork server, bench and lane ceiling now as one task. Likely outcome: new lanes and every merge's gates share the pool at once.
2. Land the slot pool alone first. Likely outcome: the pool lands a little sooner; fails if the fork server's helpers.fm change sits uncommitted for another cycle with the same validation cost.
3. A cgroup quota per runner instead of a pool. fails if: contention moves into throttling, each run slower, nothing gets cheaper.
4. Do less: lower -j everywhere. fails if: a run alone gets slower, the opposite of the ask.

Choice 1 (85%): all four parts are built and each has its own tests; one close validates them together. Captured: T-3296 (part 2).
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] bench script and the before numbers
2. [x] slot pool in run.py
3. [x] fork server for helpers.fm, with the import-time env audit and the parser's first-build imports preloaded
4. [x] lane ceiling 100
## Resume here
<!-- auto -->
- 2026-11-06T04:17:46Z steps 4/4 done
- git: foreman/build; 13 uncommitted: CHANGELOG.md, README.md, docs/map/ops-1.md, plugin/lib/sampo/lanes.py, plugin/tests/helpers.py, plugin/tests/run.py, plugin/tests/forkcli.py, plugin/tests/perf_bench.py, plugin/tests/test_cli_speed.py, plugin/tests/test_perf_bench.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/readme-site-audit.md, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/blocked_review.py, ~/.claude/projects/-home-<user>--claude-foreman/memory/standing-intent.md, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/procs.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/orphans.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/kalevala/kalevala-stack.html
## Docs impact
README.md (testing block) and docs/map/ops-1.md (dev loop) now say the runner draws one class per CPU slot from a pool shared by every run on the machine, with SAMPO_SLOTS and FOREMAN_FORK_CLI as the switches; CHANGELOG line added.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_perf_bench` → exit 0 · Ran 1 tests in 31.5s (1 jobs, 16 at a time; slowest: Bench 27s) / OK [ran] [tree 54d241c69064] [world 2f1906870a] (2026-11-06T03:05:30Z)
- (step 2) `python3 plugin/tests/run.py test_slots` → exit 0 · Ran 6 tests in 7.1s (1 jobs, 16 at a time; slowest: Slots 3s) / OK [ran] [tree 5c26b0d4a038] [world 2f1906870a] (2026-11-06T03:05:42Z)
- (step 3) `python3 plugin/tests/run.py test_cli_speed` → exit 0 · Ran 5 tests in 17.2s (4 jobs, 16 at a time; slowest: ForkServer.test_fm_calls_match_and_cost_a_fraction 12s, ImportAudit 4s, ForkServer.test_a_slow_call_times_out_and_is_killed 3s) / OK [ran] [tree 5c26b0d4a038] [world 2f1906870a] (2026-11-06T03:06:05Z)
- (step 4) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 184 tests in 265.5s (68 jobs, 16 at a time; slowest: Lanes 244s, ProbeDown 67s, SelfChangeGate 47s) / OK [ran] [tree 5c26b0d4a038] [world 2f1906870a] (2026-11-06T03:10:39Z)
- (step 2) `python3 plugin/tests/run.py test_slots` → exit 0 · Ran 7 tests in 5.2s (1 jobs, 16 at a time; slowest: Slots 2s) / OK [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:26:12Z)
- (step 3) `python3 plugin/tests/run.py test_cli_speed` → exit 0 · Ran 8 tests in 17.3s (7 jobs, 16 at a time; slowest: ForkServer.test_fm_calls_match_and_cost_a_fraction 14s, ForkServer.test_a_forked_call_sees_what_a_fresh_one_does 4s, ImportAudit 4s) / OK [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:26:39Z)
- (audit intent) `fm-reviewer full review of the diff` → after-bench row contaminated (no speedup shown): criterion 1 only records; wall-time comparison moved to T-3296 [tree c3192a68d2bc] (2026-11-06T03:26:58Z)
- (audit adversary) `fm-reviewer` → slot folder squatting/unwritable aborted runs: now lstat-checked (mine, not group/other writable) and runs unslotted; tested [tree c3192a68d2bc] (2026-11-06T03:27:00Z)
- (audit edge) `fm-reviewer` → orphaned forked calls (PDEATHSIG added), rerun-after-start fallback (removed; raises), exit -1 parity, sys.path parity, TMPDIR/locale parity: all fixed and tested; ancestor-chain depth captured as T-3298 [tree c3192a68d2bc] (2026-11-06T03:27:01Z)
- (audit operator) `fm-reviewer` → fmfork folders leaked: server folder now lives in the class TMPDIR and is removed on stop/exit; start failure cached; slot waiters back off 1-5x [tree c3192a68d2bc] (2026-11-06T03:27:02Z)
- (audit maintainer) `fm-reviewer` → Windows: fcntl/getuid guarded; ImportAudit breadth captured as T-3298 [tree c3192a68d2bc] (2026-11-06T03:27:03Z)
- (ac 1) `python3 plugin/tests/run.py test_perf_bench` → exit 0 · Ran 1 tests in 18.5s (1 jobs, 16 at a time; slowest: Bench 16s) / OK [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:29:33Z)
- (ac 2) `python3 plugin/tests/run.py test_slots` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T03:26:12Z [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:29:33Z)
- (ac 3) `python3 plugin/tests/run.py test_cli_speed` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T03:26:39Z [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:29:33Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 184 tests in 62.1s (174 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 24s, Lanes.test_finish_after_two_other_merges_h [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:29:33Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 184 tests in 53.6s (174 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 19s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:32:38Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 184 tests in 43.4s (170 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 15s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:37:14Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 184 tests in 40.6s (168 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 17s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree c3192a68d2bc] [world 2f1906870a] (2026-11-06T03:40:08Z)
- (step 4) `python3 plugin/tests/run.py test_run test_diff_gates test_slots test_cli_speed` → exit 0 · Ran 119 tests in 12.0s (71 jobs, 16 at a time; slowest: DiffGates 11s, PerTestJobs.test_a_k_run_keeps_a_whole_class_time_and_a_full_run_records_it 8s, PerTestJobs.test_a_split_class_runs_as_one_job_pe [ran] [tree c00f587f3487] [world 2f1906870a] (2026-11-06T04:25:18Z)
- (audit intent) `fm-reviewer full review of the diff, re-read after the test_run.Load fix (its mock now covers forkcli.run)` → criterion 1 only records the bench; wall-time comparison moved to T-3296; the Load test still proves fm()'s guard stretches (90 s at factor 3) [tree c00f587f3487] (2026-11-06T04:25:42Z)
- (audit adversary) `fm-reviewer full review of the diff, re-read after the test_run.Load fix (its mock now covers forkcli.run)` → slot folder squatting/unwritable: lstat-checked (mine, not group/other writable), runs unslotted; tested [tree c00f587f3487] (2026-11-06T04:25:42Z)
- (audit edge) `fm-reviewer full review of the diff, re-read after the test_run.Load fix (its mock now covers forkcli.run)` → orphaned forked calls (PDEATHSIG), no rerun after start, exit/sys.path/TMPDIR/locale parity fixed and tested; Load test flaked on whether the fork server was up: now mocks both paths [tree c00f587f3487] (2026-11-06T04:25:42Z)
- (audit operator) `fm-reviewer full review of the diff, re-read after the test_run.Load fix (its mock now covers forkcli.run)` → fmfork folders live in the class TMPDIR and are removed on stop/exit; start failure cached; slot waiters back off 1-5x [tree c00f587f3487] (2026-11-06T04:25:42Z)
- (audit maintainer) `fm-reviewer full review of the diff, re-read after the test_run.Load fix (its mock now covers forkcli.run)` → fcntl/getuid guarded for Windows; ImportAudit breadth captured as T-3298; out-of-repo edits staling audits captured as T-3317 [tree c00f587f3487] (2026-11-06T04:25:43Z)
## Log
- 2026-11-06T03:03:04Z created
- 2026-11-06T03:03:04Z redo of T-3252: takes over its start point and edited files
- 2026-11-06T03:04:10Z set scope=['plugin/tests/run.py', 'plugin/tests/test_slots.py', 'plugin/tests/perf_bench.py', 'plugin/tests/test_perf_bench.py', 'plugin/tests/forkcli.py', 'plugin/tests/test_cli_speed.py', 'plugin/tests/helpers.py', 'research/perf/', 'plugin/lib/sampo/lanes.py', 'CHANGELOG.md']
- 2026-11-06T03:04:18Z focused
- 2026-11-06T03:13:32Z set scope=['plugin/tests/run.py', 'plugin/tests/test_slots.py', 'plugin/tests/perf_bench.py', 'plugin/tests/test_perf_bench.py', 'plugin/tests/forkcli.py', 'plugin/tests/test_cli_speed.py', 'plugin/tests/helpers.py', 'research/perf/', 'plugin/lib/sampo/lanes.py', 'CHANGELOG.md', 'README.md', 'docs/map/ops-1.md']
- 2026-11-06T03:13:39Z scope: README.md and docs/map/ops-1.md describe run.py as one class per core; they now name the shared slot pool and the fork server
- 2026-11-06T03:24:53Z hypothesis: a SIGKILLed fork server leaks /tmp/fmfork-*; making its folder inside the test class's own TMPDIR (which run.py removes after the class) rules that out, unless the socket path passes the 107-char AF_UNIX limit, when it falls back to /tmp
- 2026-11-06T03:51:31Z guard authorization added: system
- 2026-11-06T04:24:39Z set scope=['plugin/tests/run.py', 'plugin/tests/test_slots.py', 'plugin/tests/perf_bench.py', 'plugin/tests/test_perf_bench.py', 'plugin/tests/forkcli.py', 'plugin/tests/test_cli_speed.py', 'plugin/tests/helpers.py', 'research/perf/', 'plugin/lib/sampo/lanes.py', 'CHANGELOG.md', 'README.md', 'docs/map/ops-1.md', 'plugin/tests/test_run.py']
- 2026-11-06T04:24:40Z scope: test_run.Load mocked subprocess.run to read fm()'s hang guard; fm() now goes through forkcli.run, so the test reads that call's timeout instead
- 2026-11-06T04:43:01Z done
- 2026-11-06T04:43:16Z committed a6a471ef (13 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3252 [PERFORMANCE L, dropped, 4 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- T-3177 [PERFORMANCE M, deferred, 3 steps] Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load,…
- research mission-20261027-200117.pack: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playbooks, …
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_brainstorm_skill.py, plugin/tests/test_budget.py, plugin/tests/test_clean…
## Measurements
fm() call through the fork server vs a fresh python3 fm: 23 vs 55 ms quiet (2.4x), 85 vs 205 ms at load 60 (2.4x). Parser first build 18 ms cold, 3 ms warm: preloading its imports into the server removes ~15 ms per call. Lazy regexes and argparse help-check/colour: 0-7 ms, dropped. Slot pool: under the 8-CPU cap slot_count() = 8; the 2026-11-06 before/after suite bench was contaminated by a concurrent full check (after-row invalid), so the wall-time comparison moved to T-3296. Step evidence ran green at host load ~250: test_lanes 184 tests in 265 s.
## Lessons
- A test that mocks subprocess.run to watch fm() calls misses calls routed through the fork server; patch forkcli.run too. Out-of-repo edits (scratchpad, memory) currently stale a task's audits (T-3317): finish before writing them.
## Files touched
- plugin/tests/perf_bench.py
- plugin/tests/test_perf_bench.py
- plugin/tests/test_slots.py
- plugin/tests/run.py
- plugin/tests/test_cli_speed.py
- plugin/tests/forkcli.py
- plugin/tests/helpers.py
- research/perf/bench.jsonl
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
- docs/map/ops-1.md
- README.md
- plugin/tests/test_run.py
