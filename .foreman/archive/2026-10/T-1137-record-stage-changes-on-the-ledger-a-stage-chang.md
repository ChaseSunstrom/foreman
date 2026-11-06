---
id: T-1137
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmwatch.py, plugin/tests/test_splits.py, plugin/tests/test_core.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-16T09:20:53Z
updated: 2026-10-16T09:36:38Z
base: 10c15d62b3c01939154fdb6790bbf09a90e37120
base_tree: a9f895ee71a45a297b79e242829a1f1295e385f1
plan0_at: 2026-10-16T09:22:51Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmwatch.py, plugin/tests/test_splits.py, plugin/tests/test_core.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Record stage changes on the ledger (a stage_change event when fm's stage() moves), so pane
## Raw request
> Record stage changes on the ledger (a stage_change event when fm's stage() moves), so pane splits (T-1078) measure real stage times instead of proxy events
## Interpretation
Stages are derived (c.stage) and never recorded, so splits use proxy events. Log a 'stage' ledger event whenever a brief's derived stage changes, and have fmwatch.splits prefer those events, falling back to the proxies for older tasks.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task moving planning → executing → verifying logs one stage event per transition, and splits uses them when present — verify with `python3 plugin/tests/run.py test_splits test_core`
## Non-goals
## Approach (options → choice → why)
In the one brief-write path (fmcli.mutate, or c.save_brief if every writer goes through it), compute stage before and after, and log stage {from, to} when it differs. splits() reads stage events first. It's one event per transition, so the cost is negligible. Options considered: a stage field on the brief (state duplication), or keep the proxies (inexact).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: transitions logged once each; splits from stage events; old tasks still use proxies
2. [x] Log in the brief-write path; read in fmwatch.splits
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_splits` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: Splits 1s) / FAILED (1 classes) [ran] [tree 4af32cd13bc4] (2026-10-16T09:23:23Z)
- (step 2) `python3 plugin/tests/run.py test_splits test_core test_cli` → exit 0 · Ran 172 tests in 24.3s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 11s, AuditPrep 9s) / OK [ran] [tree d9e1bbceeb15] (2026-10-16T09:30:52Z)
- (step 1) `python3 plugin/tests/run.py test_splits test_core test_cli` → exit 0 · Ran 173 tests in 20.9s (45 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 8s, AuditPrep 7s) / OK [ran] [tree daf71db6972f] (2026-10-16T09:35:35Z)
- (ac 1) `python3 plugin/tests/run.py test_splits test_core` → exit 0 · Ran 71 tests in 1.8s (17 classes, 16 at a time; slowest: WritesAndLocks 2s, Splits 1s, PreToolUse 1s) / OK [ran] [tree a405f90368e0] (2026-10-16T09:35:46Z)
- `python3 plugin/tests/run.py test_splits` → exit 0 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: Splits 1s) / OK [ran] [tree a405f90368e0] (2026-10-16T09:35:46Z)
- (audit intent) `self review: stage computed from the in-memory brief before and after each mutate and in focus (no extra loads; fm task log measured 228 ms avg after, no slowdown seen); splits prefer stage events and fall back to proxies; the focus gap the builder noticed is closed and tested` → real stage times for the splits [tree a405f90368e0] (2026-10-16T09:35:46Z)
- (audit edge) `self review: stage computed from the in-memory brief before and after each mutate and in focus (no extra loads; fm task log measured 228 ms avg after, no slowdown seen); splits prefer stage events and fall back to proxies; the focus gap the builder noticed is closed and tested` → tasks from before this have no stage events and use proxies [tree a405f90368e0] (2026-10-16T09:35:46Z)
- (audit self) `self review: stage computed from the in-memory brief before and after each mutate and in focus (no extra loads; fm task log measured 228 ms avg after, no slowdown seen); splits prefer stage events and fall back to proxies; the focus gap the builder noticed is closed and tested` → no findings [tree a405f90368e0] (2026-10-16T09:35:46Z)
## Log
- 2026-10-16T09:20:53Z created
- 2026-10-16T09:22:40Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmwatch.py', 'plugin/tests/test_splits.py', 'plugin/tests/test_core.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:22:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1137.builder.md
- 2026-10-16T09:22:51Z focused
- 2026-10-16T09:23:36Z bench base
- 2026-10-16T09:23:37Z bench base
- 2026-10-16T09:23:37Z bench base
- 2026-10-16T09:23:37Z bench base
- 2026-10-16T09:23:37Z bench base
- 2026-10-16T09:29:31Z bench after
- 2026-10-16T09:29:31Z bench after
- 2026-10-16T09:29:32Z bench after
- 2026-10-16T09:29:32Z bench after
- 2026-10-16T09:29:32Z bench after
- 2026-10-16T09:34:40Z merged worktree-agent-a7aaefc5e93c30305 (3 file(s))
- 2026-10-16T09:34:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7aaefc5e93c30305
- 2026-10-16T09:35:01Z focused
- 2026-10-16T09:35:14Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmwatch.py', 'plugin/tests/test_splits.py', 'plugin/tests/test_core.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:35:42Z scope: CHANGELOG.md, MASTER.md — docs; fmcli.cmd_focus logs its stage move
- 2026-10-16T09:36:37Z done
- 2026-10-16T09:36:38Z committed 25bc528 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Lessons
- When a log hooks the main write path, check every writer that bypasses it
## Plan gaps
- failed first: step 1 Failing tests: transitions logged once each; splits from stage events; old tasks still use proxies
## Files touched
- plugin/tests/test_splits.py
- plugin/lib/fmwatch.py
- ANDON.md
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
