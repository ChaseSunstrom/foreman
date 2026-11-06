---
id: T-1477
type: FIX
tier: S
status: blocked
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T16:33:46Z
updated: 2026-10-22T16:38:03Z
---
# Model tables: the default openai model is the bare alias gpt-4.1-mini, but the deprecation
## Raw request
> Model tables: the default openai model is the bare alias gpt-4.1-mini, but the deprecation page lists only the dated gpt-4.1-mini-2025-04-14 retiring 2027-01-14, so the alias isn't covered; and claude-haiku-4-5-20251001 shows 'not sooner than October 15, 2026' with no date yet while it is the replacement in several rows — recheck both on the next table refresh (research T-1433-deprecations)
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
- 2026-10-22T16:33:46Z created
- 2026-10-22T16:38:03Z blocked: needs the providers to announce: the gpt-4.1-mini alias's fate and claude-haiku-4-5's date aren't on the pages yet (research T-1433-deprecations); recheck on the next table refresh
## Follow-ups captured
