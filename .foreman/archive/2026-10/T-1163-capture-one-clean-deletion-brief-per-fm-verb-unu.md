---
id: T-1163
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:47:35Z
---
# Capture one CLEAN deletion brief per `fm` verb unused for 60 days from `fm tidy --apply`,
## Raw request
> FEATURE: Capture one CLEAN deletion brief per `fm` verb unused for 60 days from `fm tidy --apply`, at most three open at a time.
> DONE-WHEN: a test with usage data showing two stale verbs captures two CLEAN briefs, a second run captures no duplicates, and a fourth stale verb stays uncaptured while three are open
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
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:47:35Z dropped: fm usage --prune already lists commands not run in N days and prints the capture line; auto-capturing deletions would target commands days old (release-check, risk, round were built this week, so 'unused 60 days' means 'new'), and the user asked for more capability, not trimming
## Follow-ups captured
