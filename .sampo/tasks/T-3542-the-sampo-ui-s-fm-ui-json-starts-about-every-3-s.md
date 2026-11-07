---
id: T-3542
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T22:04:58Z
updated: 2026-11-07T01:11:28Z
group: hook, doctor and UI speed
lane: ~/.claude/foreman.lanes/T-3542
lane_branch: foreman/T-3542
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:38:21Z
plan0_scope: []
---
# The Sampo UI's fm ui --json starts about every 3 s and uses most of a core each time…
## Raw request
> PERFORMANCE: the Sampo UI's fm ui --json starts about every 3 s and uses most of a core each time (78% CPU in a 16:25 sample): cache its JSON by the state files' mtimes and refresh only what changed; measure its CPU per minute before and after
## Interpretation
Reading 1 (chosen): fm ui --json (the foreman-ui mod's poll, every ~2-3 s while any tool call runs: each tool.complete marks it dirty) rebuilds the whole view (~0.74 s CPU) even when no project input moved; a repeat run with unchanged inputs should return the stored JSON so CPU per minute drops, output staying what a fresh build prints. Reading 2 (ruled out): make every build incremental part by part so even a changed ledger rebuilds cheaply — the cost is spread over ~12 parts whose inputs (ledger, briefs, meta) move together, so it is a rewrite of the view for a partial gain.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a second fm ui --json with unchanged inputs is served from the cache, and a touched state file or brief makes it rebuild — verify with `nice -n 10 python3 plugin/tests/run.py test_ui_cache`
- [ ] the existing fm ui view and band-signal tests still pass — verify with `nice -n 10 python3 plugin/tests/run.py test_ui test_ui_signals`
## Non-goals
- A gated CPU-per-minute check: it depends on host load, so it is measured by hand before and after (N=10 consecutive runs and a 60 s run at the mod's 2 s cadence) and reported in the Numbers, not asserted by a test.
## Approach (options → choice → why)
1) Whole-view cache keyed by the stat of every top-level project-state entry, the view's own watch paths and git HEAD, with a 10 s TTL bounding clocks and unkeyed globals (events.jsonl, bus, lane commits); stored under the project's cache/ subfolder so its write never moves the watched folder. Likely outcome: hits on every poll a read-only tool call or a second session causes; ~0.74 s → ~0.1 s CPU on a hit. Fails if: a view input changes in place without moving any stat (an in-place rewrite in the same tick) — bounded by the TTL. 2) Per-part caches keyed per input. Fails if: ledger/briefs/meta move together, so the parts miss together; many keys to get right. 3) use what exists: the mod already skips fm when its watch paths are still (marks) and watch._kept keeps slow lines 120 s; extend that keyed idea to the whole view (this is option 1's base). Likely outcome: same as 1 if extended; fails if: kept as is, since the mod is dirtied by every tool call anyway. 4) do less: drop the mod's isDirty on every tool.complete. Fails if: a change outside the watch paths (lane commit, trust) waits 30 s; one session only. Choice 1 (80%): biggest cut per run for the least code; also move the _kept files into cache/ so fm ui stops waking its own poll. Tests disable the cache by env unless they test it.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing test: test_ui_cache (hit on unchanged inputs, miss on a touched state file, a saved brief, and an expired TTL)  <- CURRENT
2. [x] Cache the view in watch.cmd_ui keyed by state stats + HEAD with a TTL; move _kept files under cache/
3. [x] Measure N=10 runs and a 60 s mod-cadence run before/after; run the ui tests
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_ui_cache` → ✗ exit 1 · Ran 3 tests in 28.2s (1 jobs, 16 at a time; slowest: UiCache 2s) / FAILED (1 classes: test_ui_cache.UiCache) [ran] [tree e97eaef876fa] [world 2f1906870a] (2026-11-07T00:39:52Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui test_ui_signals` → exit 0 · Ran 61 tests in 40.8s (18 jobs, 16 at a time; slowest: UiView 21s, CloseOut 2s, UiCache 2s) / OK [ran] [tree 82e101e4b8fa] [world 2f1906870a] (2026-11-07T00:44:17Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui test_ui_signals test_design_surfaces test_verbs_nopipe` → exit 0 · Ran 91 tests in 7.5s (45 jobs, 16 at a time; slowest: ClosedPipe 7s, Xray 4s, UiView.test_today_done_counts_tasks_closed_today 2s) / OK [ran] [tree df4c6b230cdc] [world 2f1906870a] (2026-11-07T00:56:56Z)
- (step 3) `python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/bench_ui.py ~/.claude/foreman.lanes/T-3542/plugin/bin/fm ~/.claude/foreman 10 0` → exit 0 · N=10 gap=0.0s span=3.3s wall/run=333ms cpu/run=329ms cpu total=3.29s [ran] [tree df4c6b230cdc] [world 2f1906870a] (2026-11-07T00:57:17Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_ui_cache` → exit 0 · Ran 3 tests in 1.1s (1 jobs, 16 at a time; slowest: UiCache 1s) / OK [ran] [tree df4c6b230cdc] [world 2f1906870a] (2026-11-07T00:57:18Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py test_ui test_ui_signals` → exit 0 · Ran 61 tests in 3.7s (35 jobs, 16 at a time; slowest: UiView.test_today_done_counts_tasks_closed_today 3s, UiView.test_cards_get_queue_progress_inbox_age_latency_and_the_last_check 2s, GoalSignal 2s) [ran] [tree df4c6b230cdc] [world 2f1906870a] (2026-11-07T00:57:22Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui test_ui_signals` → exit 0 · Ran 62 tests in 25.2s (38 jobs, 16 at a time; slowest: UiView.test_today_done_counts_tasks_closed_today 2s, GoalSignal 2s, UiView.test_unproven_count_and_top_kind_ride_in_the_view_model 1s) / OK [ran] [tree 969a884fc790] [world 2f1906870a] (2026-11-07T01:09:06Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_ui_cache` → exit 0 · Ran 4 tests in 25.2s (1 jobs, 16 at a time; slowest: UiCache 2s) / OK [ran] [tree 969a884fc790] [world 2f1906870a] (2026-11-07T01:09:32Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py test_ui test_ui_signals` → exit 0 · Ran 62 tests in 68.8s (35 jobs, 16 at a time; slowest: UiView.test_today_done_counts_tasks_closed_today 3s, UiView.test_the_view_carries_budget_bench_research_and_the_tasks_ledger 3s, UiCache 2s) / OK [ran] [tree 969a884fc790] [world 2f1906870a] (2026-11-07T01:10:41Z)
- (step 2) `nice -n 10 claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 177 tests across 6 files. [46.20s] [ran] [tree 969a884fc790] [world 2f1906870a] (2026-11-07T01:11:28Z)
## Log
- 2026-11-06T22:04:58Z created
- 2026-11-07T00:37:46Z planned: it has criteria and steps
- 2026-11-07T00:37:49Z lane: ~/.claude/foreman.lanes/T-3542 on foreman/T-3542
- 2026-11-07T00:38:19Z focused
- 2026-11-07T00:38:21Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T00:57:41Z numbers: 10 back-to-back fm ui --json: 814-1163 ms CPU/run → 168-221 ms (two alternating rounds, same checkout path, load ~30-37 on 16 cores); 30 runs at the pane's 2 s cadence beside 40+ active lanes: 1244 → 917 ms CPU/run (15 of 29 kept; misses were ledger/meta/tasks moves); a kept run ~0.11 s profiled. Discovered T-3565 (risk.json/genesis-step.json lane-vs-main thrash).
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
