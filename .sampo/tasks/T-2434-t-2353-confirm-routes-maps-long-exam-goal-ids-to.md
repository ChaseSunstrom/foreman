---
id: T-2434
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T18:01:40Z
updated: 2026-11-02T01:39:24Z
---
# T-2353 confirm_routes maps long-exam goal ids to task briefs to find a promotion's tier,…
## Raw request
> T-2353 confirm_routes maps long-exam goal ids to task briefs to find a promotion's tier, but fm exam long goals are scenario ids, so a provisional route may never confirm: stamp each long goal with its tier
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
- 2026-10-31T18:01:40Z created
- 2026-11-02T01:39:24Z dropped: premise doesn't hold: fm exam long's goals are task ids mined from history (fmlong: key id = w['task']; the last foreman long run's goals are T-1878, T-1759, T-2269, T-2217, T-1834, T-2216), and each has a brief with its tier (S, S, M, L, M, L), so confirm_routes' tier lookup finds them; a run on another repo's history would miss, but that run isn't foreman's own project and confirm_routes judges only this project's runs
## Follow-ups captured
