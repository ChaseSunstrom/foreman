---
id: T-1296
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:43:10Z
updated: 2026-10-21T00:43:07Z
base: 3ee15e04e1ccbd687ed27055d9e90f0772d573ce
base_tree: a6740739650336423d56ee2eaacc918e89e61a47
plan0_at: 2026-10-20T23:28:38Z
plan0_scope: []
verified: strong
---
# fm audit prep's diff includes every changed file of the task, committed or not, so a reviewer never sees only the CHANGELOG hunk
## Raw request
> fm audit prep's diff (audits/<id>.diff) left out modified but uncommitted .py files and held only the CHANGELOG hunk (T-1294), so the reviewer saw the wrong diff; it should include every changed tracked file of the task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a task's code changes uncommitted (a .py edit plus a CHANGELOG line), audits/<id>.diff holds the .py hunks too — verify with `python3 plugin/tests/run.py test_audit_run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test reproducing T-1294's case (uncommitted .py + CHANGELOG)
2. [x] Fix how fm audit prep collects the task's files for the diff
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_audit_run 2>&1 | tail -15` → ✗ exit 1 · Ran 5 tests in 15.8s (1 classes, 16 at a time; slowest: AuditRun 14s) / FAILED (1 classes) [ran] [tree 815ac7fdf4bd] (2026-10-20T23:29:40Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_run 2>&1 | grep -v "^ File" | tail -12` → ✗ exit 1 · Ran 5 tests in 12.9s (1 classes, 16 at a time; slowest: AuditRun 12s) / FAILED (1 classes) [ran] [tree 641d6f73d4a9] (2026-10-20T23:30:05Z)
- (step 1) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 5 tests in 10.9s (1 classes, 16 at a time; slowest: AuditRun 11s) / OK [ran] [tree 8419124a0e83] (2026-10-20T23:30:50Z)
- (step 2) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 5 tests in 12.0s (1 classes, 16 at a time; slowest: AuditRun 12s) / OK [ran] [tree 8419124a0e83] (2026-10-20T23:31:03Z)
- (step 2) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 5 tests in 13.2s (1 classes, 16 at a time; slowest: AuditRun 13s) / OK [ran] [tree 31e7f09ea3df] (2026-10-21T00:40:26Z)
- `python3 plugin/tests/run.py test_audit_run` → ✗ exit 1 · Ran 5 tests in 14.1s (1 classes, 16 at a time; slowest: AuditRun 12s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 31e7f09ea3df] (2026-10-21T00:41:03Z)
- `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 5 tests in 12.4s (1 classes, 16 at a time; slowest: AuditRun 12s) / OK [ran] [tree 31e7f09ea3df] (2026-10-21T00:41:03Z)
- (ac 1) `python3 plugin/tests/run.py test_audit_run` → exit 0 · Ran 5 tests in 12.7s (1 classes, 16 at a time; slowest: AuditRun 12s) / OK [ran] [tree 31e7f09ea3df] (2026-10-21T00:41:30Z)
- (audit edge) `self: read the diff; for a lane branch the checkout's uncommitted edits (HEAD → worktree tree) are appended to the branch diff. Like the no-branch case it includes every uncommitted file in the checkout, not only the task's — same scope as before, noted` → no uncommitted edits → worktree_tree equals HEAD, the second diff is empty; a timeout or git error names which diff [tree 31e7f09ea3df] (2026-10-21T00:41:30Z)
- (audit self) `self: read the diff; for a lane branch the checkout's uncommitted edits (HEAD → worktree tree) are appended to the branch diff. Like the no-branch case it includes every uncommitted file in the checkout, not only the task's — same scope as before, noted` → no findings [tree 31e7f09ea3df] (2026-10-21T00:41:30Z)
## Log
- 2026-10-20T21:43:10Z created
- 2026-10-20T23:28:17Z planned from capture
- 2026-10-20T23:28:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1296.builder.md
- 2026-10-20T23:28:38Z focused
- 2026-10-21T00:40:02Z merged worktree-agent-aeb702776e8d4de24 (2 file(s))
- 2026-10-21T00:40:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aeb702776e8d4de24
- 2026-10-21T00:40:07Z focused
- 2026-10-21T00:43:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0722 [FIX S, done, 3 steps] Close-out friction: audit prep reads a builder's branch; a refused commit can be retried
- T-1297 [FEATURE M, dropped, 0 steps] ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1294.diff` omitted the
- T-0078 [FEATURE L, done, 4 steps] A task's own changes: diff from a working-tree snapshot taken at focus, not the last commit — lesson: A check that reads a diff must te…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 3–4 steps
- start here (files T-0722 touched): plugin/tests/test_builder.py, plugin/tests/test_secrets.py, plugin/lib/fmcli.py, CHANGELOG.md
## Files touched
- plugin/tests/test_audit_run.py.add
- plugin/tests/test_audit_run.py
- plugin/lib/fmcli.py
