---
id: T-3565
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:57:29Z
updated: 2026-11-07T01:11:52Z
lane: ~/.claude/foreman.lanes/T-3565
lane_branch: foreman/T-3565
base: afca369d5306798d95690ce1a45d2cb7977963e6
base_tree: 26dea69e852fd2d4d59227aa10701119e0110227
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T01:01:52Z
plan0_scope: []
---
# risk.json and genesis-step.json thrash between lane and main processes: risk._counts…
## Raw request
> PERFORMANCE: risk.json and genesis-step.json thrash between lane and main processes: risk._counts keys git on .git/logs/HEAD, None in a worktree (its .git is a file), and rune.health keys on rune.py's own mtime, which differs per lane checkout; so each side rewrites the other's cache on every call (git log / step() each time) and moves the project state folder the pane watches (found in T-3542: fm ui from a lane rewrote both on every run)
## Interpretation
Reading 1 (chosen): both caches live in the shared project state folder but key on per-checkout facts (risk: <root>/.git/logs/HEAD, None in a linked worktree and a different reflog per worktree; rune.health: rune.py's mtime), so a lane and main overwrite each other's file every call; make the keys agree when the inputs agree and write only on change. Reading 2 (ruled out): stop lanes from writing state at all; lanes legitimately need the risk budget and health line, and their own git history differs from main's.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a linked worktree's reflog keys risk's git count, and main and a lane alternating calls stop rewriting risk.json once both are cached — verify with `nice -n 10 python3 plugin/tests/run.py test_risk`
- [ ] rune.health from two checkouts holding the same rune.py shares one genesis-step.json key: no recompute, no rewrite — verify with `nice -n 10 python3 plugin/tests/run.py -k health test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Skip the cache in lanes: likely outcome no thrash, fails if: lanes still run git log and step() (~80 ms) every call. 2) Per-checkout cache files: fails if: N lanes make N files and the pane still sees new files churn. 3) One file, keys fixed: risk resolves the worktree's real git dir for the reflog and keeps one git entry per checkout root ({root: [size, mtime_ns, rev]}); rune.health keys on rune.py's content hash (memoized by stat) instead of its mtime; likely outcome: writes only when an input moves. 4) use what exists: c.git_root and the risk.json cache already exist; lanes.py and doctor read a .git file's gitdir: line the same way; fails if: no shared helper returns a worktree's git dir, so this alone changes nothing. Choice 3 (85%): smallest diff that fixes both root causes and keeps the caches' savings in lanes.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: lane key + alternating no-rewrite for risk, same-content rune.py shares the health key  <- CURRENT
2. [x] fix risk._counts: real git dir for the reflog, per-checkout git entries, write only on change
3. [x] fix rune.health: key on rune.py's content hash
4. [x] measure rewrites/min before and after with 2+ checkouts
5. [x] doctor-cache.json: key on doctor.py's and each SKILL.md's content, not mtimes and the plugin path (coordinator steer)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k 'stop_rewriting_each_others_cache or across_checkouts_of_the_same_code' test_risk test_genesis` → ✗ exit 2 · [names ...] / run.py: error: -k matches a substring of test ids; repeat -k for each pattern (-k test_guard -k test_cli) [ran] [tree 5357cfdb2828] [world 2f1906870a] (2026-11-07T01:02:32Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k stop_rewriting_each_others_cache -k across_checkouts_of_the_same_code test_risk test_genesis` → ✗ exit 1 · Ran 2 tests in 56.4s (2 jobs, 16 at a time; slowest: GenesisHealth 1s, Risk 0s) / FAILED (2 classes: test_genesis.GenesisHealth, test_risk.Risk) [ran] [tree 5357cfdb2828] [world 2f1906870a] (2026-11-07T01:03:32Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_risk` → exit 0 · Ran 13 tests in 7.2s (1 jobs, 16 at a time; slowest: Risk 3s) / OK [ran] [tree f2a6e490164b] [world 2f1906870a] (2026-11-07T01:04:21Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k GenesisHealth test_genesis` → exit 0 · Ran 5 tests in 41.3s (1 jobs, 16 at a time; slowest: GenesisHealth 3s) / OK [ran] [tree f2a6e490164b] [world 2f1906870a] (2026-11-07T01:05:03Z)
- (step 4) `/tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3565/bench.sh ~/.claude/foreman.lanes/T-3565/plugin after 20` → exit 0 · 195 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3565/bench-after/state/projects/proj-4947f8/genesis-step.json / 640 /tmp/claude-1000/-home-~--clau [ran] [tree f2a6e490164b] [world 2f1906870a] (2026-11-07T01:09:16Z)
- (step 5) `nice -n 10 python3 plugin/tests/run.py -k another_checkout_of_the_same_code test_doctor` → ✗ exit 1 · Ran 1 tests in 19.0s (1 jobs, 16 at a time; slowest: ScanCache 0s) / FAILED (1 classes: test_doctor.ScanCache) [ran] [tree c25566879f9a] [world 2f1906870a] (2026-11-07T01:11:13Z)
- (step 5) `nice -n 10 python3 plugin/tests/run.py test_doctor test_risk -k GenesisHealth test_genesis` → ✗ exit 1 · run.py: no test matches test_doctor, test_risk with -k GenesisHealth [ran] [tree c1ca508c9d5c] [world 2f1906870a] (2026-11-07T01:11:41Z)
- (step 5) `nice -n 10 python3 plugin/tests/run.py test_doctor test_risk` → exit 0 · Ran 134 tests in 7.1s (47 jobs, 16 at a time; slowest: ViewsRepair 5s, Risk 4s, LockProbe 4s) / OK [ran] [tree c1ca508c9d5c] [world 2f1906870a] (2026-11-07T01:11:52Z)
## Log
- 2026-11-07T00:57:29Z created
- 2026-11-07T01:01:17Z planned: it has criteria and steps
- 2026-11-07T01:01:33Z criterion 2 verify: `nice -n 10 python3 plugin/tests/run.py test_rune_health` → `nice -n 10 python3 plugin/tests/run.py -k health test_genesis`
- 2026-11-07T01:01:34Z lane: ~/.claude/foreman.lanes/T-3565 on foreman/T-3565
- 2026-11-07T01:01:51Z focused
- 2026-11-07T01:01:52Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T01:10:53Z steer: fold doctor-cache.json (same lane/main pattern) into this lane
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-07: T-3542: fm ui's cache key leaves out derived state files (risk.json, genesis-step.json) that lanes rewrite several times a second, with a 10 s stale…
