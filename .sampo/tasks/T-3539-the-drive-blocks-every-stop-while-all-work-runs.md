---
id: T-3539
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, plugin/lib/sampo/hooks.py, plugin/tests/test_drive_wait.py, plugin/tests/test_hooks.py]
depends_on: []
source: user
created: 2026-11-06T21:57:19Z
updated: 2026-11-07T02:19:34Z
base: afca369d5306798d95690ce1a45d2cb7977963e6
base_tree: 26dea69e852fd2d4d59227aa10701119e0110227
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T22:16:27Z
plan0_scope: []
inferred_deps: [T-1331]
inferred_why: T-1331: named in its request
lane_stop: merged 2026-11-07T02:10:19Z
lane_verified: 87141c83670a7d7ac43c5ac3673cca85ad91a2d9
verified: strong
---
# The drive blocks every Stop while all work runs in the background and no task is active in the main checkout: 361 identical 'T-1331 step 6/6 is open; N more queued' blocks in one session, each shown to the user as a Stop hook error
## Raw request
> The drive blocks every Stop while all work runs in the background and no task is active in the main checkout: 361 identical 'T-1331 step 6/6 is open; N more queued' blocks in one session, each shown to the user as a Stop hook error
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with no active task and background work running (subagents or background shells), a Stop is not blocked: it says once per running set that the drive waits and returns no block, as the active-task path already does; and a block whose reason matches the previous Stop's (same work, same queue head, nothing landed or changed since) is not repeated — verify with `python3 plugin/tests/run.py test_drive_wait`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the no-active-task wait and the repeat suppression, test-first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_drive_wait` → ✗ exit 1 · Ran 4 tests in 3.1s (2 jobs, 16 at a time; slowest: DriveWait 1s, Stop 1s) / FAILED (1 classes: test_drive_wait.DriveWait) [ran] [tree e835e4a9cca1] [world 2f1906870a] (2026-11-06T22:16:45Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_drive_wait` → exit 0 · Ran 4 tests in 9.2s (4 jobs, 16 at a time; slowest: DriveWait.test_the_same_drive_block_twice_is_said_once 2s, DriveWait.test_no_active_task_and_a_running_subagent_never_blocks 2s, Stop 1s) / OK [ran] [tree 6f2120680715] [world 2f1906870a] (2026-11-06T22:25:43Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cost_forecast` → ✗ exit 1 · Ran 11 tests in 1.4s (10 jobs, 16 at a time; slowest: TaskCostCap.test_a_cap_hit_asks_for_a_checkpoint_and_no_cap_changes_nothing 1s, TaskCostCap.test_the_brief_readers_show_the_cost_line 1s, TaskCost [ran] [tree c7848a0a45c6] [world 2f1906870a] (2026-11-07T00:10:20Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_drive_wait test_cost_forecast` → exit 0 · Ran 15 tests in 21.3s (14 jobs, 16 at a time; slowest: TaskCostCap.test_a_cap_hit_asks_for_a_checkpoint_and_no_cap_changes_nothing 2s, DriveWait.test_the_same_drive_block_twice_is_said_once 2s, Stop 2 [ran] [tree cbdc0255253f] [world 2f1906870a] (2026-11-07T00:21:01Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c927a46b7d94] (2026-11-07T02:17:57Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_wait` → exit 0 · Ran 4 tests in 2.1s (2 jobs, 16 at a time; slowest: DriveWait 2s, Stop 1s) / OK [ran] [tree c927a46b7d94] [world 2f1906870a] (2026-11-07T02:18:02Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c927a46b7d94] (2026-11-07T02:18:02Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c927a46b7d94] (2026-11-07T02:18:02Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c927a46b7d94] (2026-11-07T02:18:02Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree c927a46b7d94] (2026-11-07T02:18:02Z)
## Log
- 2026-11-06T21:57:19Z created
- 2026-11-06T22:16:20Z lane: ~/.claude/foreman.lanes/T-3539 on foreman/T-3539
- 2026-11-06T22:16:25Z focused
- 2026-11-06T22:16:27Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T02:10:19Z merged foreman/T-3539 in merge train
- 2026-11-07T02:17:57Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_drive_wait.py', 'plugin/tests/test_hooks.py']
- 2026-11-07T02:17:57Z scope: widened at merge to the reviewed lane's own diff (87141c836), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T02:18:07Z verified: the full suite is green on 9b743b958, which contains 87141c836
- 2026-11-07T02:19:27Z done
- 2026-11-07T02:19:30Z committed c21c5820d (1 file)
- 2026-11-07T02:19:34Z lane removed: ~/.claude/foreman.lanes/T-3539; dropped: merged and closed
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2790 [FIX M, done, 2 steps] The Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a… — lesson: Background work has three starts (run_i…
- T-1469 [FIX S, done, 2 steps] Drive counts builder lanes as background work
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- decision 2026-11-03: [revisited: keep going with everything else] [cites: user steer 2026-11-03: make sure to keep going with everything else when done] [check: python3 …
- similar finished tasks took 2–3 steps
- start here (files T-2790 touched): plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py
## Measurements
drive blocks while waiting on background work: 361 in session 46d2c60e on 2026-11-06 → 0 (test_drive_wait: 0 blocks over 3 Stops)
## Lessons
- A message said once per X needs a key that stays stable while nothing changes, backed by a check that its text changed.
## Plan gaps
- failed first: step 1 the no-active-task wait and the repeat suppression, test-first
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/hooks.py
- plugin/tests/test_drive_wait.py
- plugin/tests/test_hooks.py
