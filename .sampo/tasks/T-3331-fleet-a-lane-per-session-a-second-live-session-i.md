---
id: T-3331
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py]
depends_on: []
source: followup
created: 2026-11-06T04:31:59Z
updated: 2026-11-06T07:10:52Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a824caa9aad2c966a
lane_branch: worktree-agent-a824caa9aad2c966a
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:27:17Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py]
---
# Fleet: a lane per session: a second live session in the same checkout gets its own lane worktree, so its edits are its own task's
## Raw request
> Fleet: a lane per session: a second live session in the same checkout gets its own lane worktree, so its edits are its own task's
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] when a session starts while another live session holds the main checkout's focus, it is told to work in a new lane (sampo lane new + EnterWorktree) and its edits there are credited to its lane's task, never the other session's — verify with `python3 plugin/tests/run.py test_lanes`
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
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_second_live` → exit 0 · Ran 1 tests in 46.8s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:32:47Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_second_live` → exit 0 · Ran 1 tests in 35.3s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:34:58Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.Lanes.test_a_second_live` → exit 0 · Ran 1 tests in 173.6s (1 jobs, 16 at a time; slowest: Lanes 1s) / OK (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:35:42Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_hooks test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 802 tests in 833.9s (254 jobs, 16 at a time; slowest: Lanes 80s, LaneRecovery 30s, Approvals 20s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 2f571e8052c9] (world 2f1906870a] (2026-11-06T06:48:03Z)
## Log
- 2026-11-06T04:31:59Z created
- 2026-11-06T06:27:14Z focused
- 2026-11-06T06:27:17Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T07:01:04Z focused
- 2026-11-06T07:08:16Z focused
- 2026-11-06T07:10:52Z focused
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
