---
id: T-1743
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmcli.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T04:22:15Z
updated: 2026-10-23T04:25:14Z
base: 02480a2a9f10063b73619bbb4b6191759897f8b1
base_tree: 50d65a65cffdba84afef009bb718d6a2f6d78344
plan0_at: 2026-10-23T04:22:34Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
verified: strong
---
# fm check --affected and --evidence step runs take the machine-wide gate lock, so every builder's affected run waits behind the others
## Raw request
> fm check --affected and --evidence step runs take the machine-wide gate lock, so every builder's affected run waits behind the others
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] only a full fm check run (no --affected, no --repeat) takes the gate lock — verify with `python3 plugin/tests/run.py test_reliability_tools.GateLock`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: cmd_check with --affected doesn't enter gate_lock
2. [x] skip the lock for --affected
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → red as expected (exit 1) · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: GateLock 1s) / FAILED (1 classes) [ran] [tree a82e4e970577] (2026-10-23T04:22:53Z)
- (step 2) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree b635ba1706a5] (2026-10-23T04:23:04Z)
- (step 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 4 tests in 1.5s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree b635ba1706a5] (2026-10-23T04:23:07Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree b635ba1706a5] (2026-10-23T04:23:09Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree 86f56cc2d954] (2026-10-23T04:23:20Z)
- (audit intent) `self: one condition in cmd_check; the test patches gate_lock and _cmd_check and checks --affected, --repeat and a full run` → release checks, the canary and full fm check runs still queue; builders' --affected runs run in parallel again [tree 86f56cc2d954] (2026-10-23T04:23:20Z)
- (audit edge) `self: one condition in cmd_check; the test patches gate_lock and _cmd_check and checks --affected, --repeat and a full run` → fm check --affected --evidence (no full gates) never takes the lock [tree 86f56cc2d954] (2026-10-23T04:23:20Z)
- (audit self) `self: one condition in cmd_check; the test patches gate_lock and _cmd_check and checks --affected, --repeat and a full run` → no findings [tree 86f56cc2d954] (2026-10-23T04:23:20Z)
- `python3 plugin/tests/run.py test_reliability_tools.GateLock` → ✗ exit 1 · Ran 4 tests in 2.4s (1 classes, 16 at a time; slowest: GateLock 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 86f56cc2d954] (2026-10-23T04:24:23Z)
- `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree 86f56cc2d954] (2026-10-23T04:24:23Z)
- (audit intent) `self: one condition in cmd_check; the test patches gate_lock and _cmd_check and checks --affected, --repeat and a full run` → release checks, the canary and full fm check runs still queue; builders' --affected runs run in parallel again [tree 86f56cc2d954] (2026-10-23T04:24:24Z)
- (audit edge) `self: one condition in cmd_check; the test patches gate_lock and _cmd_check and checks --affected, --repeat and a full run` → fm check --affected --evidence (no full gates) never takes the lock [tree 86f56cc2d954] (2026-10-23T04:24:24Z)
- (audit self) `self: one condition in cmd_check; the test patches gate_lock and _cmd_check and checks --affected, --repeat and a full run` → no findings [tree 86f56cc2d954] (2026-10-23T04:24:24Z)
## Log
- 2026-10-23T04:22:15Z created
- 2026-10-23T04:22:23Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_reliability_tools.py', 'CHANGELOG.md'], priority=urgent
- 2026-10-23T04:22:27Z focused
- 2026-10-23T04:25:12Z done
- 2026-10-23T04:25:14Z committed b04585a1 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1668 [FEATURE S, done, 2 steps] One machine-wide gate lock: release checks and the canary queue behind each other — lesson: A pass-through for nested lock holders must…
- T-1731 [FIX M, active, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-22: Round-3 L tasks split into 34 M/S children (T-1618..T-1669, T-1609/T-1610 for T-1513); the parts recon judged speculative went to the inbox as follo…
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
T-1668's tests drove gate_lock directly, never cmd_check's choice of which runs take it
## Lessons
- Test which callers take a new lock, not only the lock
## Files touched
- plugin/tests/test_reliability_tools.py
- plugin/lib/fmcli.py
- CHANGELOG.md
