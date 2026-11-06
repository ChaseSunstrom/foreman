---
id: T-3306
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T03:59:24Z
updated: 2026-11-06T03:59:24Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a3d676939daa74e0b
lane_branch: worktree-agent-a3d676939daa74e0b
---
# Sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file…
## Raw request
> sampo check --affected picks ~2,000 tests (700 jobs) for any change to a hub file (cli.py, MASTER.md, core.py), because nearly every test imports cli: on 2026-11-06 eight builders each ran such a set at once (plus reruns after load flakes) and held the host at load 100-250. Select affected tests by the changed symbols (functions a test reaches), not by file import, and let a builder's pre-commit check stop at its own modules plus the symbol-affected set
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T03:59:24Z created
## Follow-ups captured
