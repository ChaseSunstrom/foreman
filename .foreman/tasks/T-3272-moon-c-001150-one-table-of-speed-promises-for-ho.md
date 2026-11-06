---
id: T-3272
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/tests/speed_promises.py, plugin/tests/test_speed_promises.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:39Z
updated: 2026-11-06T03:54:27Z
builder: 2026-11-06T02:27:50Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a1a2726e175b8ebba
lane_branch: worktree-agent-a1a2726e175b8ebba
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:29Z
plan0_scope: [plugin/tests/speed_promises.py, plugin/tests/test_speed_promises.py, CHANGELOG.md]
builder_returned: 2026-11-06T03:54:27Z
---
# Moon C-001150: one table of speed promises for hot CLI verbs and hook imports, enforced by a robust test
## Raw request
> Moon C-001150: one table of speed promises for hot CLI verbs and hook imports, enforced by a robust test
## Interpretation
Reading 1 (chosen): a single PROMISES table in a new test-side module states, per hot path (sampo next, task show, state, which), a max multiple of bare python start; a test measures medians and fails over a promise, building on bench_hooks (hook budgets already live in BUDGET_MS, reused) and T-3252's perf_bench idea of a scratch project. Reading 2 (ruled out): per-file promises declared in source headers for every module, because Sampo has hundreds of files and no consumer-dependency graph to warn downstream; the hot paths are what multiplies across sessions.
## Assumptions (confidence)
## Acceptance criteria
- [ ] PROMISES in plugin/tests/speed_promises.py names each hot path (sampo next, task show, state, which) with a max ratio to bare python start, and the hook budgets are read from bench_hooks.BUDGET_MS, not copied — verify with `python3 plugin/tests/run.py test_speed_promises`
- [ ] check() takes the median of N calls per path against a same-run bare python median, and a path whose ratio is over its promise is reported with its numbers; a stubbed slow verb fails and a fast one passes — verify with `python3 plugin/tests/run.py test_speed_promises`
- [ ] the real verbs keep their promises in a scratch project (ratio, not wall ms, so a busy machine does not flake) — verify with `python3 plugin/tests/run.py test_speed_promises`
## Non-goals
## Approach (options → choice → why)
1. New speed_promises.py with a PROMISES table plus check(), live test in test_speed_promises.py using bench_hooks._scratch_project. Likely outcome: one place to read and edit budgets, robust because ratio to same-run python median; no big file touched.
2. Add the verbs to perf_bench.VERBS and assert there. Likely outcome: works but perf_bench is uncommitted T-3252 work with an open diff, so lanes collide; and it is a bench not a gate.
3. Absolute millisecond limits per verb. fails if: the machine is busy, the test flakes and gets disabled.
4. Do less: only add a ratio assert for sampo next. Likely outcome: covers one path, no table to grow.
5) use what exists: bench_hooks.BUDGET_MS and within() already hold hook budgets (reuse, do not copy); bench_hooks._scratch_project builds the scratch project; perf_bench.cli_ms shows the median-vs-python measurement. Likely outcome: new module is thin glue over these.

Choice 1 (85%): separate module avoids collisions and gives the single table; ratio plus median is flake-proof. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] failing test: check() on injected timings (fast ok, slow flagged, bare python scales both)  <- CURRENT
2. [x] write speed_promises.py: PROMISES table, median-vs-python check(), scratch project from bench_hooks._scratch_project
3. [x] measure real ratios on this machine 3 times, set each promise at ~2x the worst, add the live test, CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T03:11:25Z step 1/3: failing test: check() on injected timings (fast ok, slow flagged, bare python scales both)
- git: worktree-agent-a1a2726e175b8ebba; 1 uncommitted: plugin/tests/test_speed_promises.py
- touched since last checkpoint: plugin/tests/test_speed_promises.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_speed_promises` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 1.5s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree f96c719f89dc] [world 2f1906870a] (2026-11-06T02:29:34Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_speed_promises` → exit 0 · Ran 6 tests in 0.5s (2 jobs, 16 at a time; slowest: Table 0s, Check 0s) / OK [ran] [tree c603a25c0172] [world 2f1906870a] (2026-11-06T02:30:02Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_speed_promises` → exit 0 · Ran 8 tests in 7.6s (3 jobs, 16 at a time; slowest: Live 7s, Check 0s, Table 0s) / OK [ran] [tree dcbf65446282] [world 2f1906870a] (2026-11-06T02:30:44Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_speed_promises && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [14.09s] [ran] [tree 8e2ff6b5759d] [world 2f1906870a] (2026-11-06T02:31:23Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_speed_promises` → ✗ exit 1 · Ran 15 tests in 54.6s (5 jobs, 2 at a time; slowest: Check 11s, Live 8s, Table 7s) / FAILED (5 classes: test_speed_promises.Live, test_speed_promises.Settle, test_speed_promises.Cpu, test_speed_promis [ran] [tree 6dcfe7fd7bcc] [world 2f1906870a] (2026-11-06T03:15:36Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_speed_promises` → exit 0 · Ran 18 tests in 300.4s (13 jobs, 2 at a time; slowest: Live 290s, Cpu 7s, Check.test_the_first_round_is_warmup_and_is_discarded 6s) / OK [ran] [tree 9e246c3e338e] [world 2f1906870a] (2026-11-06T03:22:14Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_speed_promises` → exit 0 · Ran 18 tests in 204.8s (10 jobs, 2 at a time; slowest: Live 198s, Cpu 8s, Check.test_a_fast_path_passes_and_a_slow_one_is_flagged_with_its_numbers 3s) / OK [ran] [tree 4c60e922256b] [world 2f1906870a] (2026-11-06T03:44:56Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_speed_promises && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 234 tests in 438.9s (80 jobs, 2 at a time; slowest: Live 153s, Timing.test_json_and_verbose_carry_the_timings 64s, ViewsRepair 57s) / FAILED (1 classes: test_doctor.Checks) [ran] [tree 4c60e922256b] [world 2f1906870a] (2026-11-06T03:52:50Z)
## Log
- 2026-11-06T02:27:39Z created
- 2026-11-06T02:27:45Z set scope=['plugin/tests/speed_promises.py', 'plugin/tests/test_speed_promises.py', 'CHANGELOG.md']
- 2026-11-06T02:27:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3272.builder.md
- 2026-11-06T02:28:28Z focused
- 2026-11-06T02:28:29Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
