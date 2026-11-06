---
id: T-1773
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_serve.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T10:18:29Z
updated: 2026-10-23T11:36:29Z
base: a1e62b905a2863e798b8a028ec45ac5eeae39d2e
base_tree: 4c7bc078e6cc8dfd142b38330f1d67450aaf55cd
plan0_at: 2026-10-23T11:34:33Z
plan0_scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_serve.py, CHANGELOG.md]
verified: strong
---
# Fm code works the queue unattended, the rest of T-1342: fm run --runner NAME [--all-projec
## Raw request
> fm code works the queue unattended, the rest of T-1342: fm run --runner NAME [--all-projects] through fm code --task, the app's g works the queue until empty, a task blocks twice or a stop line, and a while-you-were-away digest on return
## Interpretation
First part: fm run --runner NAME works each queued task with fm code --task ID on that runner instead of a claude -p session, inside fm run's own loop (lanes, blocked tasks skipped, no progress stops it). The app's g to work the queue, the while-you-were-away digest and --all-projects are captured as their own item.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm run --runner NAME starts fm code --task ID --worker NAME per task and refuses an unknown runner before anything runs — verify with `python3 plugin/tests/run.py test_serve`
## Non-goals
## Approach (options → choice → why)
Options: (1) one seam, _session_cmd, picks claude -p or fm code --task --worker NAME, so every fm run feature around the session keeps working (chosen); (2) a separate fm code queue loop (rejected: a second copy of fm run's stall, lane and limit handling); (3) fm code --queue inside fm code (rejected: same duplication, and fm run already owns the queue). NAME is checked against fm code's runners before anything runs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] the session seam and --runner, test first
## Resume here
## Docs impact
CHANGELOG line; fm run -h documents --runner. MASTER's fmserve bullet says fm run works the queue in claude -p sessions; the flag is an option on it, not a new module.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_serve.Run` → ✗ exit 1 · Ran 14 tests in 14.8s (1 classes, 16 at a time; slowest: Run 15s) / FAILED (1 classes) [ran] [tree d7106762e1c4] (2026-10-23T11:34:54Z)
- (step 1) `python3 plugin/tests/run.py test_serve test_parallel test_cli` → exit 0 · Ran 164 tests in 23.6s (43 classes, 16 at a time; slowest: Parallel 23s, TaskLifecycle 23s, Run 16s) / OK [ran] [tree ad7a791e7a2b] (2026-10-23T11:35:18Z)
- (ac 1) `python3 plugin/tests/run.py test_serve` → exit 0 · Ran 30 tests in 14.9s (5 classes, 16 at a time; slowest: Run 15s, Serve 3s, BoardRun 2s) / OK [ran] [tree ad7a791e7a2b] (2026-10-23T11:35:40Z)
- (ac 1) `python3 plugin/tests/run.py test_serve` → exit 0 · Ran 30 tests in 14.9s (5 classes, 16 at a time; slowest: Run 15s, Serve 3s, BoardRun 2s) / OK [ran] [tree ad7a791e7a2b] (2026-10-23T11:36:02Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): one seam replaces both session call sites (single task and lanes), the runner is checked against fm code's registry before the run lock, and the failure message names what exited` → fm run --runner NAME works the queue through fm code --task on that runner, keeping fm run's lanes, block handling, no-progress stop and notify around it [tree ad7a791e7a2b] (2026-10-23T11:36:02Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): one seam replaces both session call sites (single task and lanes), the runner is checked against fm code's registry before the run lock, and the failure message names what exited` → an unknown runner stops before the run lock or any task starts; a runner whose CLI is missing fails inside fm code at once (worker_argv), which fm run reports as that runner exiting; without --runner every path builds the same claude -p argv as before [tree ad7a791e7a2b] (2026-10-23T11:36:02Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): one seam replaces both session call sites (single task and lanes), the runner is checked against fm code's registry before the run lock, and the failure message names what exited` → the runner name reaches argv as one list element after --worker, never a shell string, and only names fm code's registry or code.toml define pass; the fm path is Foreman's own plugin/bin/fm under this interpreter [tree ad7a791e7a2b] (2026-10-23T11:36:02Z)
## Log
- 2026-10-23T10:18:29Z created
- 2026-10-23T11:34:28Z set tier=M, scope=['plugin/lib/fmserve.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_serve.py', 'CHANGELOG.md']
- 2026-10-23T11:34:33Z focused
- 2026-10-23T11:36:28Z done
- 2026-10-23T11:36:29Z committed 5594486c (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1342 [FEATURE M, done, 1 steps] Fm code works the queue unattended (R17+U20): a per-project run lock (a second run says wh — lesson: Worktrees share a project's state …
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research mission-20261016-071058: Request: forever loop round 4: improve past everything shipped [stale: demo/live.mp4, demo/live.svg, plugin/tests/bench_hooks.py change…
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_serve.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- Give a loop one seam for what it runs per item: both call sites (single and lanes) changed by changing one function
## Plan gaps
- failed first: step 1 the session seam and --runner, test first
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmserve.py
- plugin/tests/test_serve.py
