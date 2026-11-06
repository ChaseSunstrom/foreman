---
id: T-0166
type: CLEAN
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-03T08:34:29Z
updated: 2026-10-03T08:34:54Z
---
# Foreman-ui: move the band and pane out of register.tsx (needs their stateful helpers behin
## Raw request
> foreman-ui: move the band and pane out of register.tsx (needs their stateful helpers behind functions declared in the same file, or element-table parameters like rows.tsx); T-0130 found the engine rules
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
- 2026-10-03T08:34:29Z created
- 2026-10-03T08:34:54Z deferred: the band and pane read atoms through $, the clock and panes, and wire buttons to stateful helpers; under the engine's rules moving them is a data-passing rewrite; do it when one next needs a structural change
## Follow-ups captured
