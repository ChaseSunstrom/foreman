---
id: T-1899
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T02:55:58Z
updated: 2026-10-29T03:07:33Z
base: 0452a0d420637626152fa75346cbf12e464d86fd
base_tree: b00b31369cdfd718154181118d6f1d209590c0f0
plan0_at: 2026-10-29T02:59:05Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
verified: strong
---
# Drive side work skips a task that waits on any open task, not only on the active one: draf
## Raw request
> Drive side work skips a task that waits on any open task, not only on the active one: drafted work chained by depends_on was offered again each stop (T-1898 offered 4x while it waited for T-1877's tree)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Side work skips a task whose depends_on names any open task — verify with `python3 plugin/tests/run.py test_drive_side`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: waiting on a queued, non-active task is not offered
2. [x] In _side_work, skip a task with any open dependency
3. [x] CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_drive_side` → red as expected (exit 1) · Ran 6 tests in 6.9s (2 classes, 16 at a time; slowest: DriveSide 6s, LaneHeld 4s) / FAILED (1 classes) [ran] [tree bf6fcfeae3bb] (2026-10-29T02:59:18Z)
- (step 2) `python3 plugin/tests/run.py -j 2 test_drive_side test_hooks` → exit 0 · Ran 211 tests in 135.8s (29 classes, 2 at a time; slowest: Stop 69s, NoTaskGate 43s, PreToolUse 40s) / OK [ran] [tree 0d14d19ff4dc] (2026-10-29T03:01:39Z)
- (step 3) `grep -c T-1899 CHANGELOG.md` → exit 0 · 1 [ran] [tree 0d14d19ff4dc] (2026-10-29T03:01:39Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.0    44.5     150  [0] / SessionEnd                  35.2    37.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 0d14d19ff4dc] (2026-10-29T03:06:26Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_side` → exit 0 · Ran 6 tests in 4.3s (2 classes, 16 at a time; slowest: DriveSide 4s, LaneHeld 3s) / OK [ran] [tree 0d14d19ff4dc] (2026-10-29T03:06:45Z)
- (audit intent) `S task: lenses only; the one caller of _side_work checked; a dep missing from the briefs counts as closed` → a task whose depends_on names an open task (active or queued) is never offered as side work [tree 0d14d19ff4dc] (2026-10-29T03:06:45Z)
- (audit edge) `S task: lenses only; the one caller of _side_work checked; a dep missing from the briefs counts as closed` → deferred or blocked deps still count as open, so the waiter stays skipped until the dep closes [tree 0d14d19ff4dc] (2026-10-29T03:06:45Z)
- (audit self) `S task: lenses only; the one caller of _side_work checked; a dep missing from the briefs counts as closed` → no findings [tree 0d14d19ff4dc] (2026-10-29T03:06:45Z)
## Log
- 2026-10-29T02:55:58Z created
- 2026-10-29T02:58:44Z set type=FIX, tier=S, scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_drive_side.py', 'CHANGELOG.md'], status=planned
- 2026-10-29T02:59:04Z focused
- 2026-10-29T03:07:31Z done
- 2026-10-29T03:07:33Z committed 7b3d96de (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1708 [FIX S, done, 2 steps] Drive and fm next skip a queued task whose dependency is still open — lesson: Every picker of 'the next task' must apply the same readiness…
- T-1176 [FIX S, done, 2 steps] Stop drive: (1) offers 'fm lane brief … launch the builder' for RESEARCH and release tasks
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- decision 2026-10-29: Keep the drive offering a new side task each Stop even when one was ignored
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Lessons
- A wait rule that checks only the active task misses chains of queued drafts; check every open dependency
## Files touched
- plugin/tests/test_drive_side.py
- CHANGELOG.md
- plugin/lib/fmhooks.py
