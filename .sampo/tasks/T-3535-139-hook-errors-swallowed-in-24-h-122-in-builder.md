---
id: T-3535
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T21:55:00Z
updated: 2026-11-07T01:01:59Z
group: hook lock contention and error logging
lane: ~/.claude/foreman.lanes/T-3535
lane_branch: foreman/T-3535
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-07T00:38:26Z
plan0_scope: []
---
# 139 hook errors swallowed in 24 h (122 in builders), the latest a LockTimeout on the…
## Raw request
> FIX: 139 hook errors swallowed in 24 h (122 in builders), the latest a LockTimeout on the project dir: hooks give up after 1, 3 or 5 s on the project lock every mutate shares (hooks.py:732-734, core.py:1267-1279); find who holds it long, count a busy lock as one rolled-up line, and retry the Stop and heartbeat writes once
## Interpretation
Reading 1 (chosen): all 139 swallowed hook errors in 24 h are LockTimeouts on the project lock (builder mark 122, PostToolUse auto-evidence 8, SessionStart 6, PreCompact 3); find the long holders, shrink the one that holds across slow work, roll busy-lock skips into one counted friction line (no traceback, no breaker strike), and retry the Stop counters and SessionStart heartbeat lock once. Reading 2 (ruled out): a gate run or lane merge holds the project lock for minutes; ruled out by reading the code: sampo check holds gate.lock, lane merge and train lock postmerge/ and train/, never the project lock.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a busy lock in a hook is one rolled-up count (no hooks.log traceback, no breaker strike) and friction shows it as one line; the builder mark takes no lock when no lane matches — verify with `nice -n 10 python3 plugin/tests/run.py -k LockBusy test_hooks`
- [ ] Stop counters and SessionStart heartbeat retry the lock once and still save after one busy wait — verify with `nice -n 10 python3 plugin/tests/run.py -k LockRetry test_hooks`
- [ ] builder marks still work (T-3145) — verify with `nice -n 10 python3 plugin/tests/run.py -k builders_own_stop test_lanes`
## Non-goals
## Approach (options → choice → why)
Holders found: the busiest is _mark_builder itself: every fm-builder SubagentStart/Stop (365 in one hour) takes the project lock and re-reads all 2,345 briefs under it, usually to match nothing; next, every CLI mutate holds it across regen_views (0.3 s idle, 0.3-1.3 s sampled from /proc/locks under builder load). 1) raise every hook wait: likely outcome fewer errors; fails if: the holder keeps growing with the brief count, hides it. 2) use what exists: move regen_views out of mutate's lock under its own lock: fails if: sync off's mirror removal (sync.py, under the project lock) races an export, and view writes reorder; captured as a follow-up. 3) do less at the holder: _mark_builder scans unlocked and locks only on a match for one read+save; async hooks (SubagentStart/Stop, PostToolUse) wait LOCK_SLOW; log_error rolls a LockTimeout into logs/lock-busy.json (one friction line); run() gives it no breaker strike; Stop and SessionStart retry the lock once. Likely outcome: the 122 builder-mark errors go, the rest become one counted line; fails if: a write still loses after two waits (then it is counted, not silent). Choice 3 (80%): smallest change at the top holder and in the hooks.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: LockBusy roll-up and LockRetry in test_hooks
2. [x] Fix: log_error roll-up, run() no breaker on LockTimeout, _mark_builder unlocked scan, async waits, Stop/SessionStart retry, friction line
3. [x] Targeted suites green (test_hooks, test_lanes builder mark)
## Resume here
## Docs impact
docs/map/ops-3.md: busy project lock roll-up, holder naming, retries and waits; docs/map/files-1.md: state/logs/lock-busy.json row.
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k Lock test_hooks` → ✗ exit 1 · Ran 5 tests in 70.2s (2 jobs, 16 at a time; slowest: LockBusy 3s, LockRetry 1s) / FAILED (2 classes: test_hooks.LockBusy, test_hooks.LockRetry) [ran] [tree f1d8cbba62c0] [world 2f1906870a] (2026-11-07T00:40:37Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k Lock test_hooks` → exit 0 · Ran 6 tests in 4.6s (2 jobs, 16 at a time; slowest: LockBusy 2s, LockRetry 1s) / OK [ran] [tree 306d1d71e454] [world 2f1906870a] (2026-11-07T00:44:47Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py -k LockBusy test_hooks` → exit 0 · Ran 4 tests in 11.7s (1 jobs, 16 at a time; slowest: LockBusy 3s) / OK [ran] [tree 306d1d71e454] [world 2f1906870a] (2026-11-07T00:46:24Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py -k LockRetry test_hooks` → exit 0 · Ran 2 tests in 5.6s (1 jobs, 16 at a time; slowest: LockRetry 2s) / OK [ran] [tree 306d1d71e454] [world 2f1906870a] (2026-11-07T00:46:31Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_hooks test_breaker test_friction test_core test_exit_next test_reliability_tools test_inbox_more test_lanes test_live` → exit 0 · Ran 823 tests in 135.7s (412 jobs, 16 at a time; slowest: Lanes 58s, LaneRecovery 39s, Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 30s) / OK [ran] [tree 306d1d71e454] [world 2f1906870a] (2026-11-07T00:47:07Z)
- (ac 3) `nice -n 10 python3 plugin/tests/run.py -k builders_own_stop test_lanes` → exit 0 · Ran 1 tests in 36.8s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 306d1d71e454] [world 2f1906870a] (2026-11-07T00:47:09Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_hooks test_doctor test_breaker test_friction test_core test_exit_next test_reliability_tools test_inbox_more test_lanes test_live` → exit 0 · Ran 941 tests in 74.8s (642 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 30s, Page.test_the_charts_are_drawn_from_one_kit_labelle [ran] [tree 543b598f97b3] [world 2f1906870a] (2026-11-07T01:01:48Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py -k LockBusy test_hooks` → exit 0 · Ran 5 tests in 1.5s (1 jobs, 16 at a time; slowest: LockBusy 1s) / OK [ran] [tree 543b598f97b3] [world 2f1906870a] (2026-11-07T01:01:58Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py -k LockRetry test_hooks` → exit 0 · Ran 2 tests in 0.6s (1 jobs, 16 at a time; slowest: LockRetry 0s) / OK [ran] [tree 543b598f97b3] [world 2f1906870a] (2026-11-07T01:01:59Z)
## Log
- 2026-11-06T21:55:00Z created
- 2026-11-07T00:32:13Z recon: hooks.log shows 139 LockTimeouts in 24h: builder mark 122, PostToolUse auto evidence 8, SessionStart 6, PreCompact 3
- 2026-11-07T00:35:20Z recon: sampling /proc/locks: plain sampo task set/ac/step hold the project lock 0.3-1.3 s under builder load
- 2026-11-07T00:38:04Z planned: it has criteria and steps
- 2026-11-07T00:38:08Z lane: ~/.claude/foreman.lanes/T-3535 on foreman/T-3535
- 2026-11-07T00:38:24Z focused
- 2026-11-07T00:38:26Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-07T00:39:16Z steer: recon (friction pass) — the LockTimeout at core.py:1277-1278 records only the path; also record the holder's pid, command and age so the 122 builder timeouts are diagnosable
- 2026-11-07T00:39:44Z steer: LockTimeout names the holder: pid, command and how long it has held the lock (written into the .lock file on acquire)
- 2026-11-07T00:43:29Z focused
- 2026-11-07T00:47:57Z found: holders sampled from /proc/locks for 30 min while 8+ lanes ran: sampo focus 12 holds avg 2.8 s max 7.3 s (git snapshots, load_briefs, recall and regen_views under the lock); task evidence 32 holds avg 0.5 s; plain mutates 0.3-1.3 s, mostly regen_views (state_dict: rune.health ledger read 0.4 s + load_briefs of 2,345 briefs). sampo check holds gate.lock and lane merge/train postmerge/ and train/, never the project lock. _mark_builder took the lock on each of 365 builder start/stops an hour and read every brief under it; now it scans unlocked. Follow-ups T-3556 (mutate regen out of the lock), T-3557 (SessionStart keeps its context on a busy lock), T-3558 (focus's slow work under the lock).
- 2026-11-07T01:00:33Z steer: review (MERGE) asks: redact_local on holder text, 'last known holder' wording, poll backoff 20→100 ms after 200 ms, doctor warns on a hold over 60 s or 50+ skips in 24 h naming the holder, a test for the _mark_builder scan/save race
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-3350 [FIX S, active, 1 steps] State writes give up after 5 s with 'lock busy' (core.py:1181 timeout, cli.py:8782-8786…
- T-1453 [FIX S, done, 2 steps] Stop hook still judges the turn when the project lock is busy
- decision 2026-10-31: Narrow the code freeze during the long-tier runs: lanes off the session path (T-2294 builder doc, T-2156 ci-watch, T-2279 doctor, T-2296 friction di…
- similar finished tasks took 2–2 steps
- start here (files T-2763 touched): plugin/tests/test_friction.py, plugin/lib/sampo/friction.py, plugin/lib/sampo/cli.py
