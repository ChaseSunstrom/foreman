---
id: T-3482
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/selfcheck.py, plugin/tests/test_selfcheck.py, plugin/lib/sampo/hooks.py, CHANGELOG.md, docs/map/**, MASTER.md, plugin/lib/sampo/release.py]
depends_on: []
source: user
created: 2026-11-06T18:34:00Z
updated: 2026-11-07T00:57:19Z
lane: ~/.claude/foreman.lanes/T-3482
lane_branch: foreman/T-3482
base: 16d73c11bf482298c46f1f5eb9cc680208d7ff33
base_tree: 9c030b3b39af80f8d3a45a0b8ea52d0df6ba29b0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T18:44:58Z
plan0_scope: [plugin/lib/sampo/selfcheck.py, plugin/tests/test_selfcheck.py, plugin/lib/sampo/hooks.py, CHANGELOG.md, docs/map/**, MASTER.md, plugin/lib/sampo/release.py]
lane_passed: {"tree": "2d8b3df6ffce1999dcf4d9bdb2f4564b01c5be0f", "cmds": ["python3 plugin/tests/run.py test_selfcheck"]}
---
# Be aware of everything, not only merge lanes: self-checks over every process and my own…
## Raw request
> Be aware of everything, not only merge lanes: self-checks over every process and my own behaviour, learned from data rather than a fixed list (user 2026-11-06: 'this stuff shouldnt just apply to the merge lanes, but everything, you need to be aware of everything and all of your behavior'): any job or background process running past 1.5x its typical time (typicals from the ledger's own history per kind), any step repeated (the same command 3+ times in an hour, 5 gate runs for one batch), idle capacity (GPU or CPU idle while work waits, agent slots idle while ready tasks wait), the user's asks not yet visible, and my own turns (N wait-only replies in a row: name the slow job and its elapsed vs typical); every user steer becomes a new class automatically
## Interpretation
Reading 1 (chosen): part 1 = three selfcheck checks from data Sampo already records, quiet when nothing to say: slow_jobs (a live meta marker — gates_running, ship_testing — past 1.5x the median of its last 20 passing runs in the ledger), repeats (the same normalized command failing 3+ times in the last hour per evidence events: a retry storm), wait_turns (N short wait-only Stop replies in a row, counted by the Stop hook in the session's gate state). Reading 2 (ruled out): time every process on the host and every command run 3+ times — no typical exists for arbitrary processes, and plain 3+ reruns are normal TDD (fires in 77% of 10-minute windows of the real ledger).
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo next names, with numbers, any Sampo job running past 1.5x its typical time (typicals learned from the ledger's own history per kind), any command repeated 3+ times in an hour, and N wait-only Stop turns in a row with the slow job's elapsed vs typical; each quiet once resolved; cached — verify with `python3 plugin/tests/run.py test_selfcheck`
## Non-goals
Not in part 1: idle capacity (GPU/CPU/agent slots) and 'every user steer becomes a new class automatically' — later parts of this task; the lane train (it marks no live start) and passing-only loops.
## Approach (options → choice → why)
1) scan /proc for any process and time it — likely outcome: names jobs with no typical; fails if: the brief's 'no arbitrary processes' rule. 2) use what exists: read each live meta marker with c.gates_live, its typical from the ledger event that records its finished runs (check_run results' seconds; one new ship_test event, since sampo ship's test run records no duration) — likely outcome: gates history works today; fails if: a marker has <3 recorded runs (then quiet). 3) a uniform job_done event from every marker owner — likely outcome: cleaner, but gates blind until new runs; fails if: today's report needs history. 4) do less: only repeats and wait_turns — fails if: the slow push the user asked about stays unnamed. Choice 2 (80%): history today, one tiny writer. Repeats count failing reruns only (9-16% of windows fire). wait_turns: a counter in gate.json's per-session drive dict, O(1), read uncached by selfcheck.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1671, T-1674, T-1678, T-1707.
## Execution prompt
## Steps
1. [x] part 1: failing tests, then slow_jobs, repeats and wait_turns in selfcheck.py from data Sampo already records
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_selfcheck` → ✗ exit 1 · Ran 10 tests in 1.6s (2 jobs, 16 at a time; slowest: SelfCheck 1s, SelfCheckBehaviour 0s) / FAILED (1 classes: test_selfcheck.SelfCheckBehaviour) [ran] [tree 087f7675de10] [world 2f1906870a] (2026-11-06T18:45:50Z)
- (step 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 10 tests in 3.5s (2 jobs, 16 at a time; slowest: SelfCheck 2s, SelfCheckBehaviour 1s) / OK [ran] [tree 2d8b3df6ffce] [world 2f1906870a] (2026-11-06T18:50:37Z)
## Log
- 2026-11-06T18:34:00Z created
- 2026-11-06T18:35:11Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/tests/test_selfcheck.py', 'plugin/lib/sampo/hooks.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md']
- 2026-11-06T18:35:12Z planned: it has criteria and steps
- 2026-11-06T18:35:12Z lane: ~/.claude/foreman.lanes/T-3482 on foreman/T-3482
- 2026-11-06T18:44:41Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/tests/test_selfcheck.py', 'plugin/lib/sampo/hooks.py', 'CHANGELOG.md', 'docs/map/**', 'MASTER.md', 'plugin/lib/sampo/release.py']
- 2026-11-06T18:44:56Z focused
- 2026-11-06T18:44:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T18:45:53Z focused
- 2026-11-06T18:48:39Z focused
- 2026-11-06T18:50:41Z focused
- 2026-11-07T00:57:19Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3127 [FEATURE M, planned, 3 steps] Self-awareness part 2: turn-end self-checks, one per miss class, that fire with numbers before the user would ask (T-3123)
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar finished tasks took 4–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, docs/map/files-lib-3.md, plugin/lib/sampo/hooks.py, plugin/lib/sampo/release.py, plugin/lib/sampo/selfcheck.py, plugin/tests/test_selfcheck.py; re-ground the plan against them before editing
