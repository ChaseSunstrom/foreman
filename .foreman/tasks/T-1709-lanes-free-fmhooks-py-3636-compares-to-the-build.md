---
id: T-1709
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-23T01:27:12Z
updated: 2026-10-23T01:59:48Z
base: c37cd0a11ccc09acca8f19a8512d1ed84bb742b8
base_tree: 17e7e55b1f3e67d0519f053262ddcceb6fb328b3
plan0_at: 2026-10-23T01:49:08Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmlanes.py, plugin/tests/test_parallel.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
verified: strong
---
# Lane friction: the drive counts the raised lane cap, an unused brief says how to free its slot, a gone worktree says how to merge
## Raw request
> lanes_free (fmhooks.py:3636) compares to the BUILDERS constant (2), not builders_cap(p), so the drive stops offering lanes at 2 when fm lane max is 6; and fm lane brief takes a slot before any launch (fmlanes.py:588) without saying fm lane rm frees it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with fm lane max 6 and 3 builders out, the drive still offers a lane; lane brief's output names fm lane rm for an unused slot; merging a lane whose worktree is gone names fm lane new and --unverified — verify with `python3 plugin/tests/run.py test_lanes.Lanes test_drive_side`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] builders_cap in lanes_free, the two messages
## Resume here
<!-- auto -->
- 2026-10-23T01:49:43Z step 1/2: failing tests
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes -k lane_friction` → red as expected (exit 1) · Ran 23 tests in 68.7s (1 classes, 16 at a time; slowest: Lanes 68s) / FAILED (1 classes) [ran] [tree ca4296448c03] (2026-10-23T01:55:12Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_drive_side` → exit 0 · Ran 37 tests in 13.6s (7 classes, 16 at a time; slowest: Lanes 13s, LaneHeld 3s, DriveSide 3s) / OK [ran] [tree 27cc290df6b7] (2026-10-23T01:56:05Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.Lanes test_drive_side` → exit 0 · Ran 28 tests in 13.0s (3 classes, 16 at a time; slowest: Lanes 13s, LaneHeld 3s, DriveSide 3s) / OK [ran] [tree 27cc290df6b7] (2026-10-23T01:56:19Z)
- `python3 plugin/tests/run.py test_lanes.Lanes` → ✗ exit 1 · Ran 23 tests in 13.0s (1 classes, 16 at a time; slowest: Lanes 12s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 27cc290df6b7] (2026-10-23T01:56:45Z)
- `python3 plugin/tests/run.py test_lanes.Lanes` → exit 0 · Ran 23 tests in 12.8s (1 classes, 16 at a time; slowest: Lanes 13s) / OK [ran] [tree 27cc290df6b7] (2026-10-23T01:56:45Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.Lanes test_drive_side` → exit 0 · Ran 28 tests in 13.3s (3 classes, 16 at a time; slowest: Lanes 13s, LaneHeld 3s, DriveSide 3s) / OK [ran] [tree 27cc290df6b7] (2026-10-23T01:57:07Z)
- (audit intent) `self-review: lanes_free takes the project and uses builders_cap (both drive callers pass p); the two messages name the exact recovery commands; prove red on the start tree, green now` → with fm lane max 6, the drive keeps offering lanes past 2; an unused brief and a gone worktree each say how to recover [tree 27cc290df6b7] (2026-10-23T01:57:07Z)
- (audit edge) `self-review: lanes_free takes the project and uses builders_cap (both drive callers pass p); the two messages name the exact recovery commands; prove red on the start tree, green now` → lanes_free without a project falls back to the default cap; a strained host still takes no lane [tree 27cc290df6b7] (2026-10-23T01:57:07Z)
- (audit self) `self-review: lanes_free takes the project and uses builders_cap (both drive callers pass p); the two messages name the exact recovery commands; prove red on the start tree, green now` → no findings [tree 27cc290df6b7] (2026-10-23T01:57:07Z)
- (audit intent) `self-review: lanes_free takes the project and uses builders_cap (both drive callers pass p); the two messages name the exact recovery commands; prove red on the start tree, green now` → with fm lane max 6, the drive keeps offering lanes past 2; an unused brief and a gone worktree each say how to recover [tree 27cc290df6b7] (2026-10-23T01:58:23Z)
- (audit edge) `self-review: lanes_free takes the project and uses builders_cap (both drive callers pass p); the two messages name the exact recovery commands; prove red on the start tree, green now` → lanes_free without a project falls back to the default cap; a strained host still takes no lane [tree 27cc290df6b7] (2026-10-23T01:58:23Z)
- (audit self) `self-review: lanes_free takes the project and uses builders_cap (both drive callers pass p); the two messages name the exact recovery commands; prove red on the start tree, green now` → no findings [tree 27cc290df6b7] (2026-10-23T01:58:23Z)
## Log
- 2026-10-23T01:27:12Z created
- 2026-10-23T01:48:54Z planned from capture
- 2026-10-23T01:48:56Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmlanes.py', 'plugin/tests/test_parallel.py', 'plugin/tests/test_drive_side.py', 'CHANGELOG.md']
- 2026-10-23T01:49:07Z focused
- 2026-10-23T01:49:45Z paused: focus moved to T-1622
- 2026-10-23T01:53:35Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-23T01:53:35Z focused
- 2026-10-23T01:54:00Z criterion 1 verify: `python3 plugin/tests/run.py test_parallel test_drive_side` → `python3 plugin/tests/run.py test_lanes.Lanes test_drive_side`
- 2026-10-23T01:54:01Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmlanes.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_drive_side.py', 'CHANGELOG.md']
- 2026-10-23T01:58:23Z scope: MASTER.md, fmcli/fmmotion/fmplaybooks/fmsmoke/smoke_web.cjs, playbooks SKILL.md, test_motion_verify.py came from merging T-1622 and T-1627 while T-1709 was checkpointed; those tasks committed them
- 2026-10-23T01:59:46Z done
- 2026-10-23T01:59:48Z committed 177c6ce8 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1028 [FEATURE M, done, 8 steps] Worktree agents resume easily after a session stops: find a stopped builder's worktree and — lesson: A resume that frees a worktree mus…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- T-1710 [FIX S, dropped, 0 steps] Fm lane merge after fm lane rm of an unmerged lane refuses ('worktree is gone', fmlanes.py
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar past tasks were M: consider --tier M
- the similar finished task took 8 steps
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_lanes.py
## Why not caught
no test raised fm lane max and then asked the drive
## Lessons
- A cap with a per-project override must be read through its one accessor everywhere, never the module constant
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmmotion.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- plugin/skills/playbooks/SKILL.md
- plugin/tests/test_motion_verify.py
- plugin/tests/test_playbook_machinery.py
