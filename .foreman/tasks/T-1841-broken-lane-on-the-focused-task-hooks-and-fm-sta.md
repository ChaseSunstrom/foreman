---
id: T-1841
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_lanes.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-28T16:18:05Z
updated: 2026-10-28T16:45:52Z
base: 065208906bd51f459f76ed7eb1e6d23fb8dcc23a
base_tree: 44f7db2472696f7f94cfe6c7c8b6b1205bd631a6
plan0_at: 2026-10-28T16:42:21Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_lanes.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Broken lane on the focused task: hooks and fm status say 'no active task' while the task i
## Raw request
> Broken lane on the focused task: hooks and fm status say 'no active task' while the task is active; name the broken lane instead
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A task active in a lane whose folder is gone is named (with fm lane rm ID) by fm status, fm next and the prompt hook instead of 'no active task' — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_lanes
2. [x] stranded lane named in state, next and the hook
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 34 tests in 20.2s (5 classes, 16 at a time; slowest: Lanes 20s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) [ran] [tree 292385d04deb] (2026-10-28T16:43:23Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_core test_status` → exit 0 · Ran 122 tests in 23.3s (29 classes, 16 at a time; slowest: Lanes 23s, StatuslineUi 3s, BoardLanes 2s) / OK [ran] [tree ba2226f2e0a6] (2026-10-28T16:44:21Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 34 tests in 13.2s (5 classes, 16 at a time; slowest: Lanes 13s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree ba2226f2e0a6] (2026-10-28T16:44:52Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 34 tests in 13.3s (5 classes, 16 at a time; slowest: Lanes 13s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree ba2226f2e0a6] (2026-10-28T16:45:06Z)
- (audit intent) `self: read the diff; stranded() only runs with no active task, one isdir per lane-active brief; next_for reuses the briefs andons loaded` → status, next and the prompt hook name the task, its lane and fm lane rm, tested [tree ba2226f2e0a6] (2026-10-28T16:45:06Z)
- (audit edge) `self: read the diff; stranded() only runs with no active task, one isdir per lane-active brief; next_for reuses the briefs andons loaded` → a lane path from another machine (fm sync) also reads as gone, the same view fm fsck takes [tree ba2226f2e0a6] (2026-10-28T16:45:06Z)
- (audit self) `self: read the diff; stranded() only runs with no active task, one isdir per lane-active brief; next_for reuses the briefs andons loaded` → no findings [tree ba2226f2e0a6] (2026-10-28T16:45:06Z)
## Log
- 2026-10-28T16:18:05Z created
- 2026-10-28T16:42:15Z set tier=S
- 2026-10-28T16:42:16Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-28T16:42:20Z focused
- 2026-10-28T16:45:51Z done
- 2026-10-28T16:45:52Z committed 15586b5f (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- T-1469 [FIX S, done, 2 steps] Drive counts builder lanes as background work
- T-0134 [FEATURE L, done, 5 steps] Lanes: a git worktree is a lane of its project with its own active task — lesson: When a 'single X per project' rule becomes 'per lane'…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- A view filter (lane_view) hides what no view owns: check for orphans whenever a filter decides ownership
## Plan gaps
- failed first: step 1 failing test in test_lanes
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
