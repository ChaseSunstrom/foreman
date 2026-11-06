---
id: T-2082
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T02:53:46Z
updated: 2026-11-05T04:43:29Z
explore: true
confirm: true
---
# Can you add pages for ALL of the different features of foreman? with more graphs, and…
## Raw request
> can you add pages for ALL of the different features of foreman? with more graphs, and everything?
> (fm second session: can you add pages for ALL of the different features of foreman? with more graphs, and everything? — no open work item covers feature pages, and nothing later shows it was finished.)
## Interpretation
The user's words from an old session (a child surfaced them, so the user confirms before work starts): a page for every Foreman feature, with more graphs. Grounding: site/pages.py already builds 19 feature pages (planning, proof, guard, permissions, review, lanes, drive, cards, panel, speed, learning, …) from real data. The gap is coverage: no check ties pages to MASTER.md's user-facing areas, so newer capabilities (Genesis exam and scorecard, fm find/prove, fm goal, the cold read) may have no page and no chart.
## Assumptions (confidence)
## Acceptance criteria
- [ ] every user-facing area in MASTER.md maps to a site page (or a recorded n/a) and a site test fails when one doesn't; each new page carries a chart from real data — verify with `python3 plugin/tests/run.py test_site`
## Non-goals
## Approach (options → choice → why)
Options: (1) a coverage check: each user-facing area MASTER.md names maps to a PAGES entry or a recorded n/a, plus pages for the uncovered ones, each with a chart from stats.py's real data; (2) one page per module (hundreds; noise); (3) one long features page (no graphs per feature). Choice 1: the check keeps 'ALL' true as Foreman grows, and each new page reuses pages.py's data-driven entries and the site's no-outside-hosts rule.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test: the area→page map check over MASTER.md  <- CURRENT
2. [ ] pages and charts for the uncovered areas (data from stats.py), site rebuilt, shots checked
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-30T02:53:46Z created
- 2026-10-31T00:20:28Z planned: it has criteria and steps
- 2026-10-31T00:20:28Z set tier=M
- 2026-10-31T00:20:29Z planned; held for the user's confirm (a child found it in an old session): fm ask T-2082 confirm goes in the final report
- 2026-10-31T00:20:38Z blocked: waits on the user's confirm: a child surfaced this request from an old session, and Foreman starts such work only on the user's yes; the plan is ready, and fm ask T-2082 confirm goes in the final report
- 2026-11-05T04:43:29Z dropped: done by commit 1bba1e37 (T-1220, archived: feature pages with charts from Foreman's own history); today's build has 29 feature pages under features/; this was the same ask resurfaced from an old session
## Follow-ups captured
