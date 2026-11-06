---
id: T-1726
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_roles.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T03:31:55Z
updated: 2026-10-23T06:00:15Z
base: fa17e2f597e61a0933ec9ce6de0425bc998012b6
base_tree: a1a366d5ee6e8c80762b52f0e4da470524844cea
plan0_at: 2026-10-23T05:58:30Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_roles.py, CHANGELOG.md]
verified: strong
---
# Fm research --from-agent: a Noticed line close to an open task is logged onto that task in
## Raw request
> fm research --from-agent: a Noticed line close to an open task is logged onto that task instead of becoming a new one
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a Noticed line close to an open task (same rule as fm capture's near-duplicate check) is logged onto that task, and the report says so; others are captured as before — verify with `python3 plugin/tests/run.py test_roles.Noticed`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] near_tasks in the noticed loop
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_roles.Noticed` → red as expected (exit 1) · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Noticed 1s) / FAILED (1 classes) [ran] [tree 7a0109db05aa] (2026-10-23T05:58:40Z)
- (step 2) `python3 plugin/tests/run.py test_roles test_backlog 2>&1 | grep -E "AssertionError|Error:|^OK" | head -3` → exit 0 · OK [ran] [tree 58bad1fe6596] (2026-10-23T05:59:07Z)
- (step 1) `python3 plugin/tests/run.py test_roles.Noticed` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Noticed 1s) / OK [ran] [tree 6ba244f76c55] (2026-10-23T05:59:18Z)
- (step 2) `python3 plugin/tests/run.py test_roles test_backlog test_research` → exit 0 · Ran 48 tests in 9.1s (18 classes, 16 at a time; slowest: Reverify 9s, Capture 5s, DriveSide 3s) / OK [ran] [tree 6ba244f76c55] (2026-10-23T05:59:28Z)
- (ac 1) `python3 plugin/tests/run.py test_roles.Noticed` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: Noticed 1s) / OK [ran] [tree 6ba244f76c55] (2026-10-23T05:59:30Z)
- (ac 1) `python3 plugin/tests/run.py test_roles.Noticed` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Noticed 1s) / OK [ran] [tree 6ba244f76c55] (2026-10-23T05:59:33Z)
- (audit intent) `self: the noticed loop asks fmrecall.near_tasks (T-1662's rule: shared title tokens, names and numbers kept whole, scopes) for an open task of either type; a hit gets a log line naming the research note and the item, under the lock already held (no nested mutate), and the output lists the tasks it logged onto; misses are captured as before` → builders' Noticed lines stop piling duplicate tasks onto the inbox [tree 6ba244f76c55] (2026-10-23T05:59:33Z)
- (audit edge) `self: the noticed loop asks fmrecall.near_tasks (T-1662's rule: shared title tokens, names and numbers kept whole, scopes) for an open task of either type; a hit gets a log line naming the research note and the item, under the lock already held (no nested mutate), and the output lists the tasks it logged onto; misses are captured as before` → a done task's near match isn't used (only open ones); the same task hit twice is named once [tree 6ba244f76c55] (2026-10-23T05:59:33Z)
- (audit self) `self: the noticed loop asks fmrecall.near_tasks (T-1662's rule: shared title tokens, names and numbers kept whole, scopes) for an open task of either type; a hit gets a log line naming the research note and the item, under the lock already held (no nested mutate), and the output lists the tasks it logged onto; misses are captured as before` → no findings [tree 6ba244f76c55] (2026-10-23T05:59:33Z)
## Log
- 2026-10-23T03:31:55Z created
- 2026-10-23T05:58:28Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_roles.py', 'CHANGELOG.md']
- 2026-10-23T05:58:29Z focused
- 2026-10-23T06:00:13Z done
- 2026-10-23T06:00:15Z committed 1e03ed54 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-09: T-0672 L self-approved: every member only adds checks or logging; replay at close proves nothing is newly allowed
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- Reuse one similarity rule for every place that might create a duplicate
## Files touched
- plugin/tests/test_roles.py
- plugin/lib/fmcli.py
- CHANGELOG.md
