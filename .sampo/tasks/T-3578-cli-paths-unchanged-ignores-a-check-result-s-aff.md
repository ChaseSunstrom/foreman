---
id: T-3578
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T02:44:46Z
updated: 2026-11-07T02:44:46Z
---
# cli._paths_unchanged ignores a check result's 'affected' list, so a hand-run fm check…
## Raw request
> cli._paths_unchanged ignores a check result's 'affected' list, so a hand-run fm check can reuse a merge train's affected-only suite pass as if it were the full suite and log a run that later checks treat as a full pass (T-3576 builder): only reuse an affected-only row for a check whose own selection is a subset, else run
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
- 2026-11-07T02:44:46Z created
## Follow-ups captured
