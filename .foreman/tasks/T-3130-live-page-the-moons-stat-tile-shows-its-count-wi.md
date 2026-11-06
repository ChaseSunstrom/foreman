---
id: T-3130
type: FIX
tier: S
status: blocked
priority: normal
scope: []
depends_on: [T-3092]
source: discovered
created: 2026-11-05T03:43:05Z
updated: 2026-11-05T03:43:13Z
group: live page polish and charts
---
# The live page's Moons stat tile gets a sparkline of kept moons like the other tiles
## Raw request
> live page: the Moons stat tile shows its count with no sparkline beside it (the other five tiles have one); give it the kept-moons series
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the Moons tile draws a sparkline of the kept-moons count over the page's history beside its number, from the same chart kit, in both themes — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: the Moons tile has a sparkline svg with an aria-label  <- CURRENT
2. [ ] the series and the sparkline
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:43:05Z created
- 2026-11-05T03:43:13Z planned from capture
- 2026-11-05T03:43:13Z set approved=True
- 2026-11-05T03:43:13Z set depends_on=['T-3092']
- 2026-11-05T03:43:13Z blocked: after T-3092 merges (same files)
## Follow-ups captured
