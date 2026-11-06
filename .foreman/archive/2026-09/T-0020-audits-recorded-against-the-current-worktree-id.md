---
id: T-0020
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-09-26T14:37:34Z
updated: 2026-09-26T15:47:34Z
---
# Audits that match the current worktree id stay fresh after evidence-only updates
## Raw request
> Audits recorded against the current worktree id shouldn't go stale when only step evidence (no file change) is recorded afterwards: T-0009 had to re-record 5 audits after recording merge/push evidence with the tree unchanged
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] An audit recorded with tree X counts as fresh while the tree is still X, even if step or criterion evidence was recorded after it; a changed tree, or later evidence outside git, still makes it stale — verify with python3 -m unittest test_core test_cli
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] TDD: failing test in test_core (Brief.audit_blockers with a matching tree after later evidence), then fix audit_blockers
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -m unittest test_cli.TaskLifecycle (new test with a 1.1 s gap); full suite` → RED: 'recorded audits predate the last change' reproduced; fix in Brief.audit_blockers; then OK; full suite OK (a19c34f) (2026-09-26T15:47:34Z)
- (ac 1) `python3 -m unittest test_core test_cli` → OK: evidence after an audit with the same tree id → done allowed; a real edit after it → 're-audit' (2026-09-26T15:47:34Z)
- (audit self) `S checklist: root cause in audit_blockers (not callers), regression test reproduces with a 1.1 s gap, non-git path unchanged, suite green` → no findings; display-vs-gate limit logged [tree 8836eea5461b] (2026-09-26T15:47:34Z)
## Log
- 2026-09-26T14:37:34Z created
- 2026-09-26T14:38:09Z planned from capture
- 2026-09-26T15:28:27Z user approved core in Claude Code's permission prompt
- 2026-09-26T15:45:22Z focused
- 2026-09-26T15:47:34Z known limit: stage()/fm next still use the timestamp rule (no worktree id in hooks, too slow), so the drive text may say 'audit missing' where fm task done would pass
- 2026-09-26T15:47:34Z done
## Follow-ups captured
