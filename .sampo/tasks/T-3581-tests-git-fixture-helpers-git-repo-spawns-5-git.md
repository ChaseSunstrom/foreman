---
id: T-3581
type: PERFORMANCE
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T02:49:34Z
updated: 2026-11-07T04:50:51Z
lane: ~/.claude/foreman.lanes/T-3581
lane_branch: foreman/T-3581
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-07T04:25:33Z
plan0_scope: []
---
# Tests' git fixture: helpers.git_repo spawns 5 git processes per test (init, 2x config,…
## Raw request
> PERFORMANCE: tests' git fixture: helpers.git_repo spawns 5 git processes per test (init, 2x config, add, commit; ~35,000 per suite) and test_lane_train.Train makes ~124 git calls a test. A per-process template repo copied per test needs one 'git update-index -q --refresh' after the copy (measured: a copied index reads dirty to diff-files/diff-index until refreshed), and every test in a process then shares one init commit hash and time; sweep the suite before trusting it (from T-3572)
## Interpretation
Every SampoTestCase setUp (and each direct helpers.git_repo call) spawns 5 git processes: init, 2x config, add, commit. Cut that per test without changing what a test sees (same files, identity, branch, one fresh init commit made now).
## Assumptions (confidence)
## Acceptance criteria
- [ ] helpers.git_repo spawns one git process per repo after a process's first, and the copied repo reads clean with its own commit made at call time — verify with `nice -n 10 python3 plugin/tests/run.py test_helpers_env`
- [ ] every module that calls git_repo directly stays green — verify with `nice -n 10 python3 plugin/tests/run.py test_helpers_env test_projects test_ecosystem test_code_hardening test_serve test_repeats test_recall test_knowledge test_friction test_foresight test_find test_mint test_reliability_tools test_subdir_matrix test_doctor test_guard test_ci_watch`
## Non-goals
## Approach (options → choice → why)
Options: (a) per-process template repo with the commit already made, copied per test + one 'git update-index --refresh' (1 git/test, but every test shares one commit hash and an old commit time: lanes/rune/recall read commit times); (b) git init + identity written straight into .git/config + add + commit (3 git/test); (c) per-process template holding init + identity + the added README (no commit), copied per test, then only 'git commit' (1 git/test; commit refreshes the copied index itself, and the commit is made now, so hash and time match today's). Choice: (c): fewest processes and nothing a test can see changes. The template's identity is appended to .git/config as the exact text git config writes (2 fewer processes per class).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing test in test_helpers_env: one git process per repo after the first, clean copy, commit made at call time  <- CURRENT
2. [x] helpers.git_repo copies a per-process template (init, identity, added README) and only runs git commit
3. [x] Run every direct git_repo caller module; measure git processes and wall/CPU before and after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_helpers_env` → ✗ exit 1 · Ran 5 tests in 1.9s (3 jobs, 16 at a time; slowest: GitEnvIsolation 0s, ScratchRepoCost 0s, GateKeyIsolation 0s) / FAILED (1 classes: test_helpers_env.ScratchRepoCost) [ran] [tree f89b7fb41f02] [world 2f1906870a] (2026-11-07T04:26:59Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_helpers_env` → exit 0 · Ran 5 tests in 1.1s (3 jobs, 16 at a time; slowest: GitEnvIsolation 0s, ScratchRepoCost 0s, GateKeyIsolation 0s) / OK [ran] [tree 45d50547f299] [world 2f1906870a] (2026-11-07T04:27:39Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_helpers_env test_projects test_ecosystem test_code_hardening test_serve test_repeats test_recall test_knowledge test_friction test_foresight test_find test_mint test_reliability_tools test_subdir_matrix test_doctor test_guard test_ci_watch` → exit 0 · Ran 856 tests in 472.6s (306 jobs, 16 at a time; slowest: FindRenders 39s, GuardAgainstBash 39s, Mutation 32s) / OK [ran] [tree 45d50547f299] [world 2f1906870a] (2026-11-07T04:50:51Z)
## Log
- 2026-11-07T02:49:34Z created
- 2026-11-07T04:25:11Z set tier=S
- 2026-11-07T04:25:24Z planned: it has criteria and steps
- 2026-11-07T04:25:28Z lane: ~/.claude/foreman.lanes/T-3581 on foreman/T-3581
- 2026-11-07T04:25:33Z focused
- 2026-11-07T04:25:33Z predicted from its closes: 5 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- T-3585 [PERFORMANCE M, active, 3 steps] finished_lanes (core.py) re-runs 3 git calls per lane (~250 git processes at 83 lanes,…
- decision 2026-11-04: [confidence: 90%] Snapshot before a one-way step: ground (done by recon: mods/foreman-ui kit.ts/register.tsx/rows.tsx, smithtui.py, tokens.json, pan…
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
