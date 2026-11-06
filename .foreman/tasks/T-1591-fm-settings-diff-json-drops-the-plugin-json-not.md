---
id: T-1591
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T19:25:27Z
updated: 2026-10-22T20:29:17Z
---
# - `fm settings diff --json` drops the "plugin.json not found" problem (fmsettings.py:494-4
## Raw request
> - `fm settings diff --json` drops the "plugin.json not found" problem (fmsettings.py:494-496). The plugin rows are not misreported as dead, but the warning is lost in JSON mode, and no test covers a …
> (noticed by an agent; research T-1510-review)
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
- 2026-10-22T19:25:27Z created
- 2026-10-22T20:29:17Z dropped: done in T-1510: diff --json keeps the plugin.json problem
## Follow-ups captured
