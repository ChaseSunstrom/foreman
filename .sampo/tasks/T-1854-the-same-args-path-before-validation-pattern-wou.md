---
id: T-1854
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T18:01:22Z
updated: 2026-10-28T18:01:29Z
---
# The same `args.path`-before-validation pattern would hit any future action that reads `arg
## Raw request
> the same `args.path`-before-validation pattern would hit any future action that reads `args.path` ahead of the FILE check
> (noticed by an agent; research T-1848-review)
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
- 2026-10-28T18:01:22Z created
- 2026-10-28T18:01:29Z dropped: covered in T-1848: the FILE check now sits at the top of cmd_scene, before any action reads args.path
## Follow-ups captured
