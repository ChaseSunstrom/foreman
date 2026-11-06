---
id: T-1149
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T10:11:06Z
updated: 2026-10-16T10:38:50Z
base: d17015b22e643db7b73ca90760f15c074a570e4f
base_tree: 8499f7206c3dd27fc55def0cc9d5e53deddd58f7
plan0_at: 2026-10-16T10:22:19Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
verified: strong
---
# Fm check says 'the gates changed the working tree' when the session edited files during a
## Raw request
> fm check says 'the gates changed the working tree' when the session edited files during a long gate run (README edits during the 1.2.32 gates): compare only files the gates' own processes wrote, or say the change may be the session's
## Interpretation
fm check compares the worktree id before and after its gates. A difference reads as 'one of them writes files', even when the session edited files during a long run (README edits during the 1.2.32 gates).
## Assumptions (confidence)
## Acceptance criteria
- [x] a file changed during fm check is named in the warning, which says it may be the session's edit; no change, no warning — verify with `python3 plugin/tests/run.py test_round_f test_cli`
## Non-goals
## Approach (options → choice → why)
Record git status --porcelain (with mtimes) before the gates and diff it after, so the warning names the changed files and says honestly that a gate wrote them or the session edited them meanwhile. JSON keeps wrote and adds the paths. Options considered: blame no one (loses the formatter case), or watch the gates' own processes (needs fanotify, out of reach).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test: a gate that writes a file (named), then no change (no warning)
2. [x] Snapshot status before/after in cmd_check; name the paths
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_round_f` → ✗ exit 1 · Ran 11 tests in 3.2s (1 classes, 16 at a time; slowest: RoundF 3s) / FAILED (1 classes) [ran] [tree b7c0ef365998] (2026-10-16T10:22:43Z)
- (step 2) `python3 plugin/tests/run.py -k test_round_f -k test_cli` → exit 0 · Ran 113 tests in 25.6s (29 classes, 16 at a time; slowest: TaskLifecycle 25s, StateViews 10s, AuditPrep 8s) / OK [ran] [tree 7f59da9d31cd] (2026-10-16T10:23:23Z)
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 11 tests in 7.9s (1 classes, 16 at a time; slowest: RoundF 7s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1ac716f40386] (2026-10-16T10:34:50Z)
- `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 11 tests in 6.7s (1 classes, 16 at a time; slowest: RoundF 7s) / OK [ran] [tree 1ac716f40386] (2026-10-16T10:34:50Z)
- (ac 1) `python3 plugin/tests/run.py test_round_f test_cli` → exit 0 · Ran 113 tests in 45.3s (29 classes, 16 at a time; slowest: TaskLifecycle 45s, StateViews 20s, Checks 17s) / OK [ran] [tree 1ac716f40386] (2026-10-16T10:35:36Z)
- (ac 1) `python3 plugin/tests/run.py test_round_f test_cli` → exit 0 · Ran 113 tests in 90.9s (29 classes, 16 at a time; slowest: TaskLifecycle 90s, StateViews 38s, Checks 31s) / OK [ran] [tree e94cf88bb825] (2026-10-16T10:37:29Z)
- (step 1) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 11 tests in 9.4s (1 classes, 16 at a time; slowest: RoundF 9s) / OK [ran] [tree e94cf88bb825] (2026-10-16T10:37:29Z)
- (audit edge) `self: reviewed merged diff; names come from git diff of the two worktree tree ids, capped at 8 with a count; JSON gains wrote_paths; no-change run prints nothing` → a failed git diff returns no names and the warning falls back to 'files' [tree e94cf88bb825] (2026-10-16T10:37:29Z)
- (audit self) `self: reviewed merged diff; names come from git diff of the two worktree tree ids, capped at 8 with a count; JSON gains wrote_paths; no-change run prints nothing` → no findings [tree e94cf88bb825] (2026-10-16T10:37:29Z)
## Log
- 2026-10-16T10:11:06Z created
- 2026-10-16T10:13:55Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-10-16T10:22:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1149.builder.md
- 2026-10-16T10:22:19Z focused
- 2026-10-16T10:34:18Z merged worktree-agent-a5a192c0fa764fa34 (2 file(s))
- 2026-10-16T10:34:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5a192c0fa764fa34
- 2026-10-16T10:34:22Z focused
- 2026-10-16T10:34:34Z criterion 1 verify: `python3 plugin/tests/run.py test_cli` → `python3 plugin/tests/run.py test_round_f test_cli`
- 2026-10-16T10:35:42Z scope: test lives in test_round_f.py (where the wrote-warning test was); CHANGELOG.md line
- 2026-10-16T10:38:50Z done
- 2026-10-16T10:38:50Z committed 86e3640 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- research T-0224-review-2: HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit. [stale: plugin/lib/fmevolve.py, plugin/lib/fmguard.…
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_cli.py
## Plan gaps
- failed first: step 1 Test: a gate that writes a file (named), then no change (no warning)
## Files touched
- plugin/tests/test_round_f.py
- plugin/lib/fmcli.py
- CHANGELOG.md
