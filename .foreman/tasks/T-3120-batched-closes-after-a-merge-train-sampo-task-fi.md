---
id: T-3120
type: PERFORMANCE
tier: S
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T03:13:13Z
updated: 2026-11-06T03:53:26Z
inferred_deps: [T-3119]
inferred_why: T-3119: batched closes follow merge train design
group: fast merges and merge trains
---
# sampo task finish reuses a full-gates pass on the same tree from any task when the only change since is CHANGELOG.md lines, rerunning only the tests that read the changelog
## Raw request
> batched closes after a merge train: sampo task finish reuses a full gate run on the same tree when the only change since is CHANGELOG or docs lines (each close's own changelog line today changes the tree and forces a fresh 5-minute suite per task)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] after a green sampo check on tree X, a finish on tree X plus CHANGELOG.md line additions (from any task) reuses that full-gates pass and reruns only the changelog's affected tests, saying so; any other file changed, a red pass, or a different world (models, tool versions) runs the full gates as today — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: reuse across tasks on a changelog-only change; refuse on any other change or a red pass  <- CURRENT
2. [ ] a tree id that ignores CHANGELOG.md added lines, the cross-task pass record, the affected rerun
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:13:13Z created
- 2026-11-05T03:23:16Z planned from capture
- 2026-11-05T03:23:17Z set approved=True
- 2026-11-05T03:23:17Z blocked: after T-3087's merge (cli.py); then a builder slot
- 2026-11-06T03:53:26Z unblocked
## Follow-ups captured
