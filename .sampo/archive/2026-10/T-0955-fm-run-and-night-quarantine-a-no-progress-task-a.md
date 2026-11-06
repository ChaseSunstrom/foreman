---
id: T-0955
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:40Z
updated: 2026-10-15T21:57:19Z
base: 297fd94e3b4c156c8841128c015cd1a1d7bed022
base_tree: bdc76b8af8e31cbd34c3e282e7a8d2ae4871550f
verified: strong
---
# fm run and night: quarantine a no-progress task across runs, keep the machine awake, print a timer line
## Raw request
> fm run and night: quarantine a no-progress task across runs, keep the machine awake, print a timer line
## Interpretation
Board clusters resilience (crash-loop quarantine: fmserve.py:645 keeps skip in memory, so the next fm run re-picks the task; block it via mutate where fail() exits at ~748/752), r4-away-queue (re-exec fm run under systemd-inhibit --what=sleep:idle when on PATH, env guard against recursion) and cloud-scheduling (fm night --print-timer: a systemd user timer+service and a crontab line; fmnight.py:6 says scheduling is the user's).
## Assumptions (confidence)
## Acceptance criteria
- [x] After fm run gives up on a task for no progress, the task is blocked with that reason and the next fm run takes the next task — verify with `python3 plugin/tests/run.py -k BoardRun`
- [x] fm run re-execs itself under systemd-inhibit --what=sleep:idle when systemd-inhibit is on PATH, once (an env guard stops recursion) — verify with `python3 plugin/tests/run.py -k BoardRun`
- [x] fm night --print-timer prints a systemd user timer and service and a crontab line that run fm night, and changes nothing — verify with `python3 plugin/tests/run.py -k BoardRun`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardRun class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
MASTER, README, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardRun` → ✗ exit 1 · Ran 13 tests in 10.3s (1 classes, 16 at a time; slowest: BoardRun 10s) / FAILED (1 classes) [ran] [tree 2dd511088849] (2026-10-15T21:40:54Z)
- (step 1) `python3 plugin/tests/run.py -k BoardRun` → ✗ exit 1 · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: BoardRun 1s) / FAILED (1 classes) [ran] [tree 3f6efe6453db] (2026-10-15T21:41:13Z)
- (step 2) `python3 plugin/tests/run.py -k BoardRun` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: BoardRun 2s) / OK [ran] [tree dd7345c6a749] (2026-10-15T21:42:10Z)
- (step 3) `python3 plugin/tests/run.py -k BoardRun` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: BoardRun 1s) / OK [ran] [tree b8efead8633a] (2026-10-15T21:43:02Z)
- (step 2) `python3 plugin/tests/run.py test_serve test_night` → exit 0 · Ran 40 tests in 14.0s (12 classes, 16 at a time; slowest: Run 14s, Serve 4s, NightGuards 2s) / OK [ran] [tree ce34ffe5c4fb] (2026-10-15T21:57:14Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardRun` → exit 0 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: BoardRun 2s) / OK [ran] [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardRun` → exit 0 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: BoardRun 2s) / OK [ran] [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardRun` → exit 0 · Ran 3 tests in 2.6s (1 classes, 16 at a time; slowest: BoardRun 2s) / OK [ran] [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
- (audit intent) `one fm-reviewer pass (sonnet): 1 medium, 2 low; 2 fixed test-first, the parallel-lanes quarantine captured as T-0968` → a stuck task is blocked with its reason and the next run moves on; the machine stays awake; night gets a printed schedule [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
- (audit edge) `one fm-reviewer pass (sonnet): 1 medium, 2 low; 2 fixed test-first, the parallel-lanes quarantine captured as T-0968` → no systemd-inhibit or a broken logind runs uninhibited; FOREMAN_INHIBITED stops recursion; a failed block never hides the stop [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
- (audit operator) `one fm-reviewer pass (sonnet): 1 medium, 2 low; 2 fixed test-first, the parallel-lanes quarantine captured as T-0968` → units carry FOREMAN_HOME and PATH; nothing is installed [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
- (audit maintainer) `one fm-reviewer pass (sonnet): 1 medium, 2 low; 2 fixed test-first, the parallel-lanes quarantine captured as T-0968` → the quarantine is fm task block itself, one code path for blocks [tree ce34ffe5c4fb] (2026-10-15T21:57:17Z)
## Log
- 2026-10-15T21:12:40Z created
- 2026-10-15T21:30:22Z grounding: fmserve.cmd_run (~line 748) calls fail('no progress in a fresh session; stopping') and at SESSIONS_PER_TASK; plan: block the task with that reason (the same call fm task block uses) before stopping, so _next_runnable skips it next run. AC2: at cmd_run start, when shutil.which('systemd-inhibit') and FOREMAN_INHIBITED unset, os.execvpe systemd-inhibit --what=sleep:idle --why='fm run' sys.executable bin/fm argv with FOREMAN_INHIBITED=1; test with a fake systemd-inhibit on PATH that records argv. AC3: fmnight cmd_night --print-timer prints foreman-night.service/.timer (OnCalendar=*-*-* 02:30, Persistent=true) and a crontab line using bin/fm's absolute path, writes nothing. Lane-able (fmserve, fmnight, fmcli parser only).
- 2026-10-15T21:38:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0955.builder.md
- 2026-10-15T21:38:53Z focused
- 2026-10-15T21:50:22Z merged worktree-agent-a2b645f79da74f464 (7 file(s))
- 2026-10-15T21:50:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2b645f79da74f464
- 2026-10-15T21:55:47Z focused
- 2026-10-15T21:57:18Z done
- 2026-10-15T21:57:19Z committed 02e1d07 (4 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- playbook Loop Design + Review (skills/playbooks/references/evals/loop-design-check.md)
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 3 steps
## Lessons
- A side door that sets a status by hand skips what the front door does (snapshots, eval cases): call the verb
## Plan gaps
- failed first: step 1 Failing tests in a BoardRun class
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_serve.py
- plugin/lib/fmserve.py
- plugin/lib/fmnight.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/tests/test_board_hooks.py
- plugin/tests/test_execution.py
- plugin/tests/test_verification.py
