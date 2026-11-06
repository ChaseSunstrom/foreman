---
id: T-1753
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-23T05:13:17Z
updated: 2026-10-23T05:15:09Z
base: 536968c11c0c7d9a0da9453b83d674a1a3c9fd2b
base_tree: da6b41bf9284b041bd54f6bc7d457f7732283a8e
plan0_at: 2026-10-23T05:13:22Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
verified: strong
---
# Gate lock: a full fm check waits at most 15 minutes for another run (a hung check in another project held it for over 40), then runs beside it and says so
## Raw request
> Gate lock: a full fm check waits at most 15 minutes for another run (a hung check in another project held it for over 40), then runs beside it and says so
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm check waits on the gate lock at most FOREMAN_GATE_WAIT seconds (default 900), then runs without it and names the holder — verify with `python3 plugin/tests/run.py test_reliability_tools.GateLock`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a held lock and a short wait run the check anyway with a note
2. [x] bounded wait in cmd_check
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → red as expected (exit 1) · Ran 5 tests in 11.0s (1 classes, 16 at a time; slowest: GateLock 11s) / FAILED (1 classes) [ran] [tree a357fd6f9bf7] (2026-10-23T05:14:11Z)
- (step 2) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree a946e9ba462b] (2026-10-23T05:14:24Z)
- (step 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree a946e9ba462b] (2026-10-23T05:14:26Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree a946e9ba462b] (2026-10-23T05:14:28Z)
- `python3 plugin/tests/run.py test_reliability_tools.GateLock` → ✗ exit 1 · Ran 5 tests in 11.7s (1 classes, 16 at a time; slowest: GateLock 11s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a946e9ba462b] (2026-10-23T05:14:41Z)
- `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree a946e9ba462b] (2026-10-23T05:14:41Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 5 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree a946e9ba462b] (2026-10-23T05:14:43Z)
- (audit intent) `self: the wait is bounded (FOREMAN_GATE_WAIT, default 900 s, a bad value falls back to 900); a timeout while acquiring runs the check beside the holder with a note naming the wait; a LockTimeout raised by the check itself (its project lock) is re-raised, not mistaken for the gate's, and that is tested` → a hung or very long check in one project no longer blocks every other project's gates for hours [tree a946e9ba462b] (2026-10-23T05:14:43Z)
- (audit edge) `self: the wait is bounded (FOREMAN_GATE_WAIT, default 900 s, a bad value falls back to 900); a timeout while acquiring runs the check beside the holder with a note naming the wait; a LockTimeout raised by the check itself (its project lock) is re-raised, not mistaken for the gate's, and that is tested` → FOREMAN_GATE_WAIT=0 runs at once beside any holder; the canary still waits without a bound (detached, nobody waiting on it) [tree a946e9ba462b] (2026-10-23T05:14:43Z)
- (audit self) `self: the wait is bounded (FOREMAN_GATE_WAIT, default 900 s, a bad value falls back to 900); a timeout while acquiring runs the check beside the holder with a note naming the wait; a LockTimeout raised by the check itself (its project lock) is re-raised, not mistaken for the gate's, and that is tested` → no findings [tree a946e9ba462b] (2026-10-23T05:14:43Z)
## Log
- 2026-10-23T05:13:17Z created
- 2026-10-23T05:13:20Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_reliability_tools.py', 'CHANGELOG.md'], priority=urgent
- 2026-10-23T05:13:21Z focused
- 2026-10-23T05:15:07Z done
- 2026-10-23T05:15:09Z committed 01aa0a17 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- T-1668 [FEATURE S, done, 2 steps] One machine-wide gate lock: release checks and the canary queue behind each other — lesson: A pass-through for nested lock holders must…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Why not caught
T-1668's tests covered queueing and pass-through, not a holder that never finishes
## Lessons
- A machine-wide lock across projects needs a bounded wait: one hung holder must not stop everyone
## Files touched
- plugin/tests/test_reliability_tools.py
- plugin/lib/fmcli.py
- CHANGELOG.md
