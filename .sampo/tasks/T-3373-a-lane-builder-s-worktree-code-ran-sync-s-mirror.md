---
id: T-3373
type: SECURITY
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:21:32Z
updated: 2026-11-06T06:21:32Z
---
# A lane builder's worktree code ran sync's mirror move against the MAIN checkout and…
## Raw request
> SECURITY: a lane builder's worktree code ran sync's mirror move against the MAIN checkout and committed 63f19d902 (6189 files) on foreman/build at 00:13 2026-11-06 (T-3342 lane): any git commit/mv a sampo command makes must act only on the cwd's own toplevel, and a lane worktree never writes another checkout
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
- 2026-11-06T06:21:32Z created
## Follow-ups captured
