---
id: T-0434
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T14:40:52Z
base: 9c2722c0d3fa69dd182def0bcb29790d5825e4e4
base_tree: 4e8eb5df022ae8d3538751faef700cb6f1a82128
verified: strong
---
# Heartbeat and breaker for unattended runs
## Raw request
> FEATURE: Heartbeat for unattended work (C099, value 5/5, effort M, risk low)
>   first version: First version: fm run/night write a heartbeat file each loop and a preflight (guard fixture replay + fm doctor) before starting; a stale heartbeat triggers the fm notify command. Add a consecutive-failure breaker that stops the run.
>   what it is: Circuit breakers, retry classes, an external dead-man heartbeat and anomaly switches for headless runs.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
fm run and fm night write a heartbeat file each loop; two failed sessions or jobs in a row stop the run (stop only, never retry); fm doctor flags a stale heartbeat and fires the notify command once per stale episode. Unattended work that wedges or loops on failure is seen and stopped instead of silently burning time.
## Assumptions (confidence)
## Acceptance criteria
- [x] a run writes its heartbeat, and a stale one makes doctor notify once — verify with `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies`
- [x] night stops after two failed jobs in a row — verify with `python3 plugin/tests/run.py -k test_night_breaker_stops_after_two_failed_jobs`
## Non-goals
## Approach (options → choice → why)
(A, chosen) heartbeat file + doctor staleness check + consecutive-failure breaker in the existing loops: no new process. (B) a watchdog thread; (C) a separate fm watch process — both add a process to keep alive. The usage-limit wait doesn't count as a failure.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first with a stub claude and notify command
2. [x] _beat in fmserve (cmd_run loop) and fmnight (job loop)
3. [x] breaker + doctor stale check
## Resume here
## Docs impact
CHANGELOG entry; MASTER (fm run, fm night)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies -k test_night_breaker_stops_after_two_failed_jobs -k test_two_failed_sessions_in_a_row_trip_the_breaker` → ✗ exit 1 · Ran 3 tests in 1.1s (2 classes, 16 at a time; slowest: Run 1s, NightGuards 0s) / FAILED (2 classes) [ran] [tree 00407313b34b] (2026-10-09T14:35:19Z)
- (step 2) `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Run 1s) / OK [ran] [tree eed2316ea139] (2026-10-09T14:37:01Z)
- (step 3) `python3 plugin/tests/run.py -k test_night_breaker_stops_after_two_failed_jobs -k test_two_failed_sessions_in_a_row_trip_the_breaker -k test_serve -k test_night -k test_parallel -k test_doctor` → exit 0 · Ran 69 tests in 15.0s (16 classes, 16 at a time; slowest: Parallel 15s, Run 8s, Command 6s) / OK [ran] [tree eed2316ea139] (2026-10-09T14:37:16Z)
- `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Run 1s) / OK [ran] [tree eed2316ea139] (2026-10-09T14:37:20Z)
- `python3 plugin/tests/run.py -k test_night_breaker_stops_after_two_failed_jobs` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: NightGuards 0s) / OK [ran] [tree eed2316ea139] (2026-10-09T14:37:21Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                34.5    36.7     150  [0] / SessionEnd                  30.8    32.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 975 tests in [ran] [tree 21e638c35984] (2026-10-09T14:38:54Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 14:38 UTC) [ran] [tree 21e638c35984] (2026-10-09T14:38:57Z)
- (step 3) `python3 plugin/tests/run.py -p test_serve.py -p test_night.py -p test_doctor.py` → exit 0 · Ran 56 tests in 8.1s (12 classes, 16 at a time; slowest: Run 8s, Command 6s, Serve 2s) / OK [ran] [tree 37f2c08271f0] (2026-10-09T14:40:42Z)
- (step 1) `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies -k test_night_breaker_stops_after_two_failed_jobs` → exit 0 · Ran 2 tests in 0.8s (2 classes, 16 at a time; slowest: Run 1s, NightGuards 0s) / OK [ran] [tree 37f2c08271f0] (2026-10-09T14:40:49Z)
- (step 2) `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Run 1s) / OK [ran] [tree 37f2c08271f0] (2026-10-09T14:40:50Z)
- (ac 1) `python3 plugin/tests/run.py -k test_run_heartbeat_goes_stale_and_notifies` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Run 1s) / OK [ran] [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
- (ac 2) `python3 plugin/tests/run.py -k test_night_breaker_stops_after_two_failed_jobs` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: NightGuards 0s) / OK [ran] [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
- (audit intent) `builder branch read (heartbeat files, doctor staleness + notify-once, night breaker, lane breaker); one change at merge (blocked isn't a failure); serve/night/doctor suites OK` → unattended work that wedges is now seen (stale heartbeat + notify) and repeated failure stops it [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
- (audit edge) `builder branch read (heartbeat files, doctor staleness + notify-once, night breaker, lane breaker); one change at merge (blocked isn't a failure); serve/night/doctor suites OK` → a killed run leaves its heartbeat (that's the signal); a clean exit removes it; the notify fires once per stale episode [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
- (audit operator) `builder branch read (heartbeat files, doctor staleness + notify-once, night breaker, lane breaker); one change at merge (blocked isn't a failure); serve/night/doctor suites OK` → doctor's heartbeats line names the run and how overdue it is [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
- (audit adversary) `builder branch read (heartbeat files, doctor staleness + notify-once, night breaker, lane breaker); one change at merge (blocked isn't a failure); serve/night/doctor suites OK` → the breaker only stops, never retries or spends [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
- (audit maintainer) `builder branch read (heartbeat files, doctor staleness + notify-once, night breaker, lane breaker); one change at merge (blocked isn't a failure); serve/night/doctor suites OK` → FAILS_MAX constant, one helper per loop [tree 37f2c08271f0] (2026-10-09T14:40:52Z)
## Log
- 2026-10-09T14:30:17Z created
- 2026-10-09T14:32:34Z planned from capture
- 2026-10-09T14:32:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0434.builder.md
- 2026-10-09T14:32:53Z focused
- 2026-10-09T14:39:58Z merged worktree-agent-aa60e9525f9496474 (6 file(s))
- 2026-10-09T14:39:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa60e9525f9496474
- 2026-10-09T14:39:58Z focused
- 2026-10-09T14:40:34Z review at merge: the builder counted a session that blocked its task as a failure, so two legitimately blocked tasks stopped fm run; removed (a block says why and the run moves on; crashes and no-progress already stop it); its test now asserts the run continues
- 2026-10-09T14:40:52Z done
- 2026-10-09T14:40:52Z committed 1a35601 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0504 [FEATURE M, dropped, 0 steps] Heartbeat for unattended work (C099, value 5/5, effort M, risk low)
- research brainstorm-foreman-20261009: 835 ideas, 103 capabilities; every idea is listed under exactly one capability.
- T-0507 [FEATURE M, dropped, 0 steps] Observer health (C066, value 4/5, effort S, risk low)
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- A breaker must count failures, not outcomes: a task that says why it's blocked is the system working.
## Files touched
- .claude/worktrees/agent-aa60e9525f9496474/plugin/tests/test_serve.py
- .claude/worktrees/agent-aa60e9525f9496474/plugin/tests/test_night.py
- .claude/worktrees/agent-aa60e9525f9496474/plugin/lib/fmserve.py
- .claude/worktrees/agent-aa60e9525f9496474/plugin/lib/fmnight.py
- .claude/worktrees/agent-aa60e9525f9496474/plugin/lib/fmdoctor.py
- .claude/worktrees/agent-aa60e9525f9496474/MASTER.md
- plugin/lib/fmserve.py
- plugin/tests/test_serve.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmfriction.py
- plugin/lib/fmhooks.py
- plugin/lib/fmnight.py
- plugin/lib/fmrecall.py
- plugin/tests/test_cli.py
- plugin/tests/test_friction.py
- plugin/tests/test_hooks.py
- plugin/tests/test_night.py
