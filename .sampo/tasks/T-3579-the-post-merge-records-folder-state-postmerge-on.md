---
id: T-3579
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T02:45:46Z
updated: 2026-11-07T02:45:46Z
---
# The post-merge records folder (state postmerge/, one JSON per merge ever made) is never…
## Raw request
> The post-merge records folder (state postmerge/, one JSON per merge ever made) is never pruned and pm_records globs and parses all of it; a 'running' record has no age cutoff, so a reused pid suppresses the sentinel and the pm claim indefinitely (T-3576 review): prune records older than N days once verified, iterate newest-first, and treat a running record older than ~1 h as dead
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
- 2026-11-07T02:45:46Z created
## Follow-ups captured
