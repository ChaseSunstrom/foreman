---
id: T-3197
type: PERFORMANCE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T11:33:20Z
updated: 2026-11-05T11:33:20Z
inferred_deps: [T-3104, T-3110]
inferred_why: T-3104: named in its request; T-3110: named in its request
---
# Works dedupe compares each new work with every kept one (O(n^2)); index the 24x24 thumbs…
## Raw request
> works dedupe compares each new work with every kept one (O(n^2)); index the 24x24 thumbs (bucket by a coarse hash) before the design-works fill reaches thousands (T-3104/T-3110)
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
- 2026-11-05T11:33:20Z created
## Follow-ups captured
