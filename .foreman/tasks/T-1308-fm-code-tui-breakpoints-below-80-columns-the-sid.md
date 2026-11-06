---
id: T-1308
type: FEATURE
tier: M
status: dropped
priority: normal
scope: [plugin/lib/fmcodetui.py]
depends_on: []
source: followup
created: 2026-10-21T00:22:57Z
updated: 2026-10-23T09:52:21Z
---
# Fm code tui breakpoints: below 80 columns the side panels stack under Activity, below 50 o
## Raw request
> fm code tui breakpoints: below 80 columns the side panels stack under Activity, below 50 or when piped a one-line live status (C16)
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
- 2026-10-21T00:22:57Z created
- 2026-10-21T03:48:22Z steer (catalogue U11): bare fm code with stdout not a terminal prints one state sentence ('foreman: T-1330 step 2/5, 4m · 2 projects need you') and exits 0
- 2026-10-23T09:52:21Z dropped: already built in the app: below narrow_below (80) the side panels stack under Activity, below 60 Activity shows alone, and a piped run prints plain lines (fm code tui --plain), which a pipe reads better than a status line rewritten in place
## Follow-ups captured
