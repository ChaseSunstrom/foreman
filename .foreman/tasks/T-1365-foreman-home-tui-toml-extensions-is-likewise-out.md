---
id: T-1365
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T05:25:48Z
updated: 2026-10-21T13:37:43Z
---
# $FOREMAN_HOME/tui.toml` (extensions) is likewise outside the guard's protected paths. `fm
## Raw request
> $FOREMAN_HOME/tui.toml` (extensions) is likewise outside the guard's protected paths. `fm code --use` and `--here` can be written to the wrong place when the project's meta is missing, which I did no…
> (noticed by an agent; research T-1328-review)
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
- 2026-10-21T05:25:48Z created
- 2026-10-21T13:37:43Z dropped: done in T-1328: code.toml, tui.toml, tui/ and models.json are guard-protected; --use --here resolves (and creates) the project first, so meta is never missing
## Follow-ups captured
