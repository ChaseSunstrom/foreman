---
id: T-1038
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T03:21:17Z
updated: 2026-10-16T04:59:31Z
---
# The 120000 ms tree window is duplicated at `register.tsx:929` and `rows.tsx:546`; extract
## Raw request
> the 120000 ms tree window is duplicated at `register.tsx:929` and `rows.tsx:546`; extract a constant in `state.ts
> (noticed by an agent; research T-1033-review)
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
- 2026-10-16T03:21:17Z created
- 2026-10-16T04:59:31Z dropped: done: TREE_MS lives in state.ts and both files import it
## Follow-ups captured
