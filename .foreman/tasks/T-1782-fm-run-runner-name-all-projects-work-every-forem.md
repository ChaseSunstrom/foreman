---
id: T-1782
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_serve.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T11:51:30Z
updated: 2026-10-23T12:14:52Z
base: ac9b9701f87d4e681dedf875759e065c511880c2
base_tree: 4d856e08762655318ef889d0f6a9483c4f168e31
plan0_at: 2026-10-23T12:13:02Z
plan0_scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_serve.py, CHANGELOG.md]
verified: strong
---
# Fm run --runner NAME --all-projects: work every Foreman project's queue in turn through fm
## Raw request
> fm run --runner NAME --all-projects: work every Foreman project's queue in turn through fm code --task (the rest of T-1773/T-1779), one project lock at a time
## Interpretation
fm run --all-projects runs fm run -p SLUG in each registered project that has queued work, one after another, with the options as typed (--runner NAME included); each takes its own run lock; projects with nothing queued are skipped; a summary says how many were worked and how many stopped early.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm run --all-projects works each project's queue, skips idle ones, and refuses -p — verify with `python3 plugin/tests/run.py test_serve.Run`
## Non-goals
## Approach (options → choice → why)
Options: (1) a loop that re-invokes fm run per project with the typed options (chosen: every fm run behaviour, lock and log stays per project); (2) one fm run process switching projects inside its loop (rejected: its lock, log and state are per project throughout); (3) leave it to cron per project (rejected: the request asks for one command).
## Risks and rollback
## Execution prompt
## Steps
1. [x] the per-project loop, test first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_serve.Run` → ✗ exit 1 · Ran 15 tests in 15.4s (1 classes, 16 at a time; slowest: Run 15s) / FAILED (1 classes) [ran] [tree 3a5f8993f965] (2026-10-23T12:13:20Z)
- (step 1) `python3 plugin/tests/run.py test_serve test_cli` → exit 0 · Ran 151 tests in 23.1s (41 classes, 16 at a time; slowest: TaskLifecycle 23s, Run 18s, AuditPrep 8s) / OK [ran] [tree 289317d2c86e] (2026-10-23T12:13:44Z)
- (ac 1) `python3 plugin/tests/run.py test_serve.Run` → exit 0 · Ran 15 tests in 17.0s (1 classes, 16 at a time; slowest: Run 17s) / OK [ran] [tree 289317d2c86e] (2026-10-23T12:14:07Z)
- (ac 1) `python3 plugin/tests/run.py test_serve.Run` → exit 0 · Ran 15 tests in 16.9s (1 classes, 16 at a time; slowest: Run 17s) / OK [ran] [tree 289317d2c86e] (2026-10-23T12:14:25Z)
- (audit edge) `self: fm run --all-projects re-invokes fm run -p SLUG per project with the options as typed, in that project's root, so locks, logs, sandbox and runner checks stay per project; -p is refused with it` → a project whose folder is gone or whose briefs can't be read is skipped; one with nothing queued is skipped and not named; a project already being run fails its own lock and counts as stopped early while the next goes on; nothing queued anywhere says so with exit 0 [tree 289317d2c86e] (2026-10-23T12:14:25Z)
- (audit adversary) `self: fm run --all-projects re-invokes fm run -p SLUG per project with the options as typed, in that project's root, so locks, logs, sandbox and runner checks stay per project; -p is refused with it` → the child argv is the typed options plus -p SLUG from the registry, as a list, never a shell string; each child runs every check fm run makes [tree 289317d2c86e] (2026-10-23T12:14:25Z)
- (audit self) `self: fm run --all-projects re-invokes fm run -p SLUG per project with the options as typed, in that project's root, so locks, logs, sandbox and runner checks stay per project; -p is refused with it` → no findings [tree 289317d2c86e] (2026-10-23T12:14:25Z)
## Log
- 2026-10-23T11:51:30Z created
- 2026-10-23T12:07:38Z set tier=S, scope=['plugin/lib/fmserve.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_serve.py', 'CHANGELOG.md']
- 2026-10-23T12:13:02Z focused
- 2026-10-23T12:14:50Z done
- 2026-10-23T12:14:52Z committed 1fc938a9 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1773 [FEATURE M, done, 1 steps] Fm code works the queue unattended, the rest of T-1342: fm run --runner NAME [--all-projec — lesson: Give a loop one seam for what it r…
- T-1342 [FEATURE M, done, 1 steps] Fm code works the queue unattended (R17+U20): a per-project run lock (a second run says wh — lesson: Worktrees share a project's state …
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar past tasks were M: consider --tier M
- similar finished tasks took 1–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_serve.py
## Lessons
- To run a per-project command over many projects, re-invoke it per project rather than teaching its loop to switch projects
## Plan gaps
- failed first: step 1 the per-project loop, test first
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmserve.py
- plugin/tests/test_serve.py
