---
id: T-1668
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:59:15Z
updated: 2026-10-23T03:56:17Z
base: d3e85e9dcf3d30fa115c4b3630e7888aae253bae
base_tree: cfee64fa639fe0bd4c2b002ea5d5df928048a4a8
plan0_at: 2026-10-23T03:32:23Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_reliability_tools.py, CHANGELOG.md]
verified: strong
---
# One machine-wide gate lock: release checks and the canary queue behind each other
## Raw request
> One machine-wide gate lock: release checks and the canary queue behind each other
## Interpretation
One machine-wide gate lock (a flock file in Foreman's home) makes release checks, the canary and full fm check runs queue behind each other instead of overloading the machine; a second run waits, saying who holds the lock.
## Assumptions (confidence)
## Acceptance criteria
- [x] a second gate run waits while the first holds the lock — verify with `python3 plugin/tests/run.py test_reliability_tools.GateLock`
## Non-goals
## Approach (options → choice → why)
Options: per-project locks (two projects still collide); a machine-wide flock; a scheduler daemon. Choice: the flock: stdlib, released if a process dies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with two threads
2. [x] flock file in the Foreman home
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree d1c8002851de] (2026-10-23T03:33:30Z)
- (step 2) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree d1c8002851de] (2026-10-23T03:33:32Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock 2>&1 | tail -6` → ✗ exit 1 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: GateLock 1s) / FAILED (1 classes) [ran] [tree c83344913600] (2026-10-23T03:35:33Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock 2>&1 | tail -4` → exit 0 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree 9f08872b337c] (2026-10-23T03:35:55Z)
- (step 2) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 3 tests in 4.0s (1 classes, 16 at a time; slowest: GateLock 2s) / OK [ran] [tree a1573c3d0605] (2026-10-23T03:36:15Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock 2>&1 | tail -3` → exit 0 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: GateLock 2s) / OK [ran] [tree a1573c3d0605] (2026-10-23T03:38:22Z)
- (step 2) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 3 tests in 2.7s (1 classes, 16 at a time; slowest: GateLock 2s) / OK [ran] [tree a1573c3d0605] (2026-10-23T03:38:32Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:54:41Z)
- (ac 1) `python3 plugin/tests/run.py test_reliability_tools.GateLock` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: GateLock 1s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:54:44Z)
- (audit intent) `self review of the diff found the pass-through let any FOREMAN_GATE_HELD value skip the lock; fixed test-first (LOCK_NB first: a free lock is taken whatever the variable says; a busy one passes only when the lock file names that pid); the yield moved out of suppress(OSError); the ordering test waits on the waiter's message, not a sleep` → release checks, the canary and full fm check runs queue behind each other instead of overloading the machine [tree 4d7ae0069c4a] (2026-10-23T03:54:44Z)
- (audit edge) `self review of the diff found the pass-through let any FOREMAN_GATE_HELD value skip the lock; fixed test-first (LOCK_NB first: a free lock is taken whatever the variable says; a busy one passes only when the lock file names that pid); the yield moved out of suppress(OSError); the ordering test waits on the waiter's message, not a sleep` → a dead holder releases the flock itself; a child of the holder passes; fm check --affected and --repeat don't take it; the default wait has no timeout (Ctrl-C ends it) [tree 4d7ae0069c4a] (2026-10-23T03:54:44Z)
- (audit adversary) `self review of the diff found the pass-through let any FOREMAN_GATE_HELD value skip the lock; fixed test-first (LOCK_NB first: a free lock is taken whatever the variable says; a busy one passes only when the lock file names that pid); the yield moved out of suppress(OSError); the ordering test waits on the waiter's message, not a sleep` → a stray FOREMAN_GATE_HELD value can't skip the lock; the lock file is 0600 in Foreman's state [tree 4d7ae0069c4a] (2026-10-23T03:54:44Z)
- (audit self) `self review of the diff found the pass-through let any FOREMAN_GATE_HELD value skip the lock; fixed test-first (LOCK_NB first: a free lock is taken whatever the variable says; a busy one passes only when the lock file names that pid); the yield moved out of suppress(OSError); the ordering test waits on the waiter's message, not a sleep` → no findings [tree 4d7ae0069c4a] (2026-10-23T03:54:44Z)
## Log
- 2026-10-22T20:59:15Z created
- 2026-10-22T20:59:16Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_reliability_tools.py', 'CHANGELOG.md']
- 2026-10-22T20:59:17Z split from T-1552 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:05Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_reliability_tools.GateLock`
- 2026-10-22T21:30:28Z criterion 1 text: a second gate run waits while the first holds the lock — verify with python3 plugin/tests/run.py test_reliability_tools.GateLock → a second gate run waits while the first holds the lock
- 2026-10-23T03:32:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1668.builder.md
- 2026-10-23T03:32:22Z focused
- 2026-10-23T03:51:42Z merged worktree-agent-a6fe4d120ab7909fe (4 file(s))
- 2026-10-23T03:51:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6fe4d120ab7909fe
- 2026-10-23T03:54:31Z focused
- 2026-10-23T03:54:42Z scope: plugin/lib/fmrelease.py (the canary worker takes the lock), CHANGELOG.md
- 2026-10-23T03:56:15Z done
- 2026-10-23T03:56:17Z committed a0619ce6 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1552 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Reliability tooling: one machine-wide gate lock for release checks and t
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1099 [FIX S, done, 3 steps] Ledger roll takes the ledger lock and keeps time order: _roll_ledger keeps unparseable-ts — lesson: Rewriting a file other processes append…
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
- similar finished tasks took 3–4 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_reliability_tools.py; re-ground the plan against them before editing
## Lessons
- A pass-through for nested lock holders must check the lock is really held by that pid now
## Files touched
- plugin/tests/test_reliability_tools.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmfixes.py
- plugin/lib/fmpage.py
- plugin/lib/fmrecall.py
- plugin/lib/graph.html
- plugin/tests/test_backlog.py
- plugin/tests/test_showpieces.py
