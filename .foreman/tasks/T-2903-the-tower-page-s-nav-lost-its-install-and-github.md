---
id: T-2903
type: FIX
tier: M
status: planned
priority: normal
scope: [site/build.py, site/pages.py, site/index.html, site/genesis/index.html, plugin/tests/test_site_build.py]
depends_on: []
source: discovered
created: 2026-11-04T06:16:56Z
updated: 2026-11-06T03:53:37Z
---
# One shared nav for the landing, the tower and the section pages, with Install and GitHub back on the tower
## Raw request
> FIX: the tower page's nav lost its Install and GitHub links when it was matched to the landing's; give the landing, the tower and the section pages one shared nav
## Interpretation
Reading 1 (chosen): the site's main nav comes from one list in site/build.py (label, href, and which page marks it current), rendered into the landing (site/index.html), the tower (site/genesis/index.html) and every section page, so Install and GitHub show on all and a new page (Cards, Works) is one entry. Reading 2: patch the tower's two links back; rejected, the three navs drifted once and will again.
## Assumptions (confidence)
## Acceptance criteria
- [ ] every built page's main nav has the same links in the same order, Install and GitHub included, from one NAV list in build.py; the current page is marked — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: build.py's section-page template already renders a nav; lift it into one NAV list and a render function the landing and tower builds call; likely outcome: one place to edit. 2. Do less: add the two links to the tower by hand; fails if: the next page drifts. 3. A client-side nav include in JS; fails if: a static page without JS loses its nav. Choice 1 (85%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: the landing's, the tower's and a section page's main nav links are equal and include Install and GitHub  <- CURRENT
2. [ ] the NAV list and its render in build.py, used by the three builds
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T06:16:56Z created
- 2026-11-05T03:33:45Z planned from capture
- 2026-11-05T03:33:46Z set approved=True
- 2026-11-05T03:33:46Z set scope=['site/build.py', 'site/pages.py', 'site/index.html', 'site/genesis/index.html', 'plugin/tests/test_site_build.py']
- 2026-11-05T03:33:46Z blocked: approved; builder slot after T-3093's merge (site/pages.py); before T-3101, whose Cards page adds one nav entry
- 2026-11-06T03:53:37Z unblocked
## Follow-ups captured
