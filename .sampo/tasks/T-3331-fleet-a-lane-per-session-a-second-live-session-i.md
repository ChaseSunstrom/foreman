---
id: T-3331
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, plugin/tests/test_hooks.py]
depends_on: []
source: followup
created: 2026-11-06T04:31:59Z
updated: 2026-11-07T02:22:26Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a824caa9aad2c966a
lane_branch: worktree-agent-a824caa9aad2c966a
base: afca369d5306798d95690ce1a45d2cb7977963e6
base_tree: 26dea69e852fd2d4d59227aa10701119e0110227
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:27:17Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py]
group: fleet claims and session liveness
lane_stop: merged 2026-11-07T02:10:19Z
lane_verified: 9b743b958ba533d19c733ceeb71043d1c606e20a
verified: ok
unproven: [typed]
---
# Fleet: a lane per session: a second live session in the same checkout gets its own lane worktree, so its edits are its own task's
## Raw request
> Fleet: a lane per session: a second live session in the same checkout gets its own lane worktree, so its edits are its own task's
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] when a session starts while another live session holds the main checkout's focus, it is told to work in a new lane (sampo lane new + EnterWorktree) and its edits there are credited to its lane's task, never the other session's — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test with two session ids, red
2. [x] SessionStart: detect the live focus holder (hooks.py:322-330, 382) and route
## Resume here
<!-- auto -->
- 2026-11-06T07:10:07Z steps 2/2 done
- git: worktree-agent-a824caa9aad2c966a; 3 uncommitted: plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, plugin/tests/test_lanes.py
- touched since last checkpoint: plugin/tests/test_lanes.py, plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_second_live` → exit 0 · Ran 1 tests in 46.8s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:32:47Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_second_live` → exit 0 · Ran 1 tests in 35.3s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:34:58Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_second_live` → exit 0 · Ran 1 tests in 173.6s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:35:42Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_hooks test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 802 tests in 833.9s (254 jobs, 16 at a time; slowest: Lanes 80s, LaneRecovery 30s, Approvals 20s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:48:03Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 624d8cb4b78f] (2026-11-07T02:20:50Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 213 tests in 12.7s (185 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, LaneRecovery.test_every_stop_cause_has_one_recovery_and_a_scenario_that [ran] [tree 624d8cb4b78f] [world 2f1906870a] (2026-11-07T02:21:05Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 624d8cb4b78f] (2026-11-07T02:21:05Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 624d8cb4b78f] (2026-11-07T02:21:05Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 624d8cb4b78f] (2026-11-07T02:21:05Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 624d8cb4b78f] (2026-11-07T02:21:05Z)
## Log
- 2026-11-06T04:31:59Z created
- 2026-11-06T06:27:14Z focused
- 2026-11-06T06:27:17Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T07:01:04Z focused
- 2026-11-06T07:08:16Z focused
- 2026-11-06T07:10:52Z focused
- 2026-11-07T02:10:19Z merged worktree-agent-a824caa9aad2c966a in merge train
- 2026-11-07T02:18:07Z verified: the full suite is green on 9b743b958, which contains 9b743b958
- 2026-11-07T02:20:49Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'plugin/tests/test_hooks.py']
- 2026-11-07T02:20:49Z scope: widened at merge to the reviewed lane's own diff (9b743b958), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T02:22:23Z done
- 2026-11-07T02:22:26Z committed 746ca71b5 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3256 [FIX S, done, 1 steps] A builder's edit inside its own lane worktree counts for the lane's task, never for the main checkout's active task (a Write to .claude/wor…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_lanes.py
- .fm-scratch/edits.json
- plugin/lib/sampo/hooks.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
