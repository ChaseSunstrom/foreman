---
id: T-1335
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code_worker.py, plugin/tests/test_code_tui.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:21Z
updated: 2026-10-23T07:09:24Z
group: runner checks, routing and config
base: e0163ccc4f32693b037e5578a3e7374695752d31
base_tree: a1700d68616e15ee4c8697a8751bcbee8eab107b
plan0_at: 2026-10-23T07:04:26Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code_worker.py, plugin/tests/test_code_tui.py, README.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code runner pings: fm code runners --ping [NAME] asks each runner one tiny read-only question and sorts the answer (ok, not logged in, usage limit, flag refused, endpoint down, no answer) with latency and version; the app's runners screen shows each one's lamp and p pings the selected
## Raw request
> fm code preflight and runner lamps (R5+U16, after T-1328): fm code runners --check runs a tiny bounded prompt through each runner and sorts it into ok / not logged in / flag refused / endpoint down / no answer, with latency and CLI version; the app's runner picker shows a status lamp per row and p pings the selected one
## Interpretation
Before an unattended run, the user wants to know which runners will actually answer: signed in, flags accepted, endpoint up, and how fast, from the CLI and at a glance in the app.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code runners --ping asks each installed runner with a read-only plan command one tiny question in a scratch folder, bounded, and shows its state, latency and version; a runner with no plan command is only asked --version — verify with `python3 plugin/tests/run.py test_code_worker.Ping`
- [x] a ping's answer is sorted into ok, not logged in, usage limit, flag refused, endpoint down, no answer or failed — verify with `python3 plugin/tests/run.py test_code_worker.Ping`
- [x] the app's runners screen shows each runner's last ping as a lamp and p pings the selected one on a thread — verify with `python3 plugin/tests/run.py test_code_tui.RunnerPing`
## Non-goals
## Approach (options → choice → why)
Complete version: ping_runner(name) builds the runner's read-only plan command with a fixed tiny prompt, runs it with run_bounded in a scratch folder with a worker environment (60 s), times it, and sorts the reply with ping_state (failure_kind plus flag-refused and endpoint-down patterns); fm code runners --ping [NAME] prints state, latency and version and writes state/code-runners-ping.json; the app's runners screen draws a lamp per row from that file and p pings the selected runner on a thread (Enter still tests --version). Options: (1) --ping as its own flag (chosen: it spends a few tokens per runner, which --check, today a free version and retirement check, never did); (2) fold it into --check (silent spend for anyone using --check); (3) only --version (says the CLI starts, not that it is signed in). Only plan (read-only) commands are pinged: a work command could change files.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: ping states, the --ping table, the app's lamp and p
2. [x] fmcode: ping_runner, ping_state, --ping in fm code runners, the ping cache
3. [x] app: lamps from the cache, p pings on a thread
4. [x] docs: README, CHANGELOG, MASTER
## Resume here
## Docs impact
README fm code section, CHANGELOG, MASTER; fm code --help gains --ping
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker.Ping test_code_tui.RunnerPing` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: Ping 0s, RunnerPing 0s) / OK [ran] [tree a1514a3dcabe] (2026-10-23T07:07:35Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker.Ping` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Ping 0s) / OK [ran] [tree a1514a3dcabe] (2026-10-23T07:07:36Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui.RunnerPing test_code_tui.Editors` → exit 0 · Ran 13 tests in 0.9s (2 classes, 16 at a time; slowest: Editors 1s, RunnerPing 0s) / OK [ran] [tree a1514a3dcabe] (2026-10-23T07:07:38Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 68 tests in 8.6s (16 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree bcc3eadabd7c] (2026-10-23T07:07:47Z)
- (audit intent) `self: request re-read` → pass: --ping sorts each runner's answer with latency and version, the app shows lamps and p pings; one decision recorded (--ping, not --check) [tree bcc3eadabd7c] (2026-10-23T07:07:54Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker.Ping` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Ping 0s) / OK [ran] [tree bcc3eadabd7c] (2026-10-23T07:07:56Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker.Ping` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: Ping 0s) / OK [ran] [tree bcc3eadabd7c] (2026-10-23T07:07:56Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui.RunnerPing` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: RunnerPing 0s) / OK [ran] [tree bcc3eadabd7c] (2026-10-23T07:07:56Z)
- (audit intent) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → all criteria met; --ping kept apart from --check (decision recorded) [tree bcc3eadabd7c] (2026-10-23T07:07:56Z)
- (audit adversary) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → only registry and code.toml runners are pinged (test_runner refuses any other name, never running it); only read-only plan commands get the prompt, a work command never does; the run is in a temp folder with the worker environment (no model keys), bounded at 60 s, its group killed and registered [tree bcc3eadabd7c] (2026-10-23T07:07:56Z)
- (audit edge) `self review (subagents paused at 76% weekly usage): intent, adversary, edge` → an is_error stream result with exit 0 counts as a failure; an empty answer is no answer; a corrupt ping file reads as empty; a ping thread shares the test's one-at-a-time slot and its quit-time stop [tree bcc3eadabd7c] (2026-10-23T07:07:56Z)
## Log
- 2026-10-21T03:47:21Z created
- 2026-10-23T07:04:15Z planned from capture
- 2026-10-23T07:04:24Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code_worker.py', 'plugin/tests/test_code_tui.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:04:25Z focused
- 2026-10-23T07:09:22Z done
- 2026-10-23T07:09:24Z committed f9d13124 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- T-1356 [FEATURE M, done, 3 steps] fm code limits and failover: a worker turn's failure is sorted (usage limit with its reset, sign-in, crash, timeout); a limit within th…
- research T-1320-review: Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards. [stale: plugin/lib/fmcl…
- decision 2026-10-23: fm code runners --ping is its own flag, not part of --check
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, plugin/tests/test_code_worker.py; re-ground the plan against them before editing
## Lessons
- When a CLI check could spend money or change files, give it its own flag and only feed prompts to read-only commands
## Files touched
- plugin/tests/test_code_tui.py
- plugin/tests/test_code_worker.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- MASTER.md
- README.md
