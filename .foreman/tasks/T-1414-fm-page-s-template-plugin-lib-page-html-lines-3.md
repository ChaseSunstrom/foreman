---
id: T-1414
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T17:52:42Z
updated: 2026-10-21T19:51:18Z
base: 43bd088105c657d993238caaa916e271b85d78eb
base_tree: 94961b2d2f4a56f500893bb258cb0de8f153b2a6
plan0_at: 2026-10-21T19:48:26Z
plan0_scope: []
verified: strong
---
# fm page loads nothing from another host: drop the Google Fonts links from its template
## Raw request
> fm page's template (plugin/lib/page.html lines 3-4) loads Google Fonts, so every page fm page makes contacts another host; use the same system font stacks as the site (T-1411)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a page fm page writes has no link, script or @import to another host, and its fonts fall back to local faces — verify with `python3 plugin/tests/run.py test_page`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_page: the written page.html has no <link …https://> or fonts.googleapis; then delete page.html's two font lines (its --display and --body stacks already end in system faces)
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_page` → ✗ exit 1 · Ran 12 tests in 5.2s (4 classes, 16 at a time; slowest: PageHardening 5s, Page 4s, BoardSurfaces 1s) / FAILED (1 classes) [ran] [tree bcd3978b8098] (2026-10-21T19:48:42Z)
- (step 1) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 12 tests in 5.5s (4 classes, 16 at a time; slowest: PageHardening 5s, Page 4s, BoardSurfaces 1s) / OK [ran] [tree 4dc3d0c05fe0] (2026-10-21T19:48:56Z)
- (ac 1) `python3 plugin/tests/run.py test_page` → exit 0 · Ran 12 tests in 5.1s (4 classes, 16 at a time; slowest: PageHardening 5s, Page 4s, BoardSurfaces 1s) / OK [ran] [tree 4e954045e110] (2026-10-21T19:49:11Z)
- (audit intent) `self: deleted the two font lines; --display/--body/--mono already end in system faces; the test scans the written page for any link or script with an absolute or protocol-relative URL` → a page fm page writes loads nothing from another host (test_page) [tree 4e954045e110] (2026-10-21T19:49:11Z)
- (audit edge) `self: deleted the two font lines; --display/--body/--mono already end in system faces; the test scans the written page for any link or script with an absolute or protocol-relative URL` → the page's own inline data and styles are untouched; the scan covers protocol-relative //host URLs too [tree 4e954045e110] (2026-10-21T19:49:11Z)
- (audit self) `self: deleted the two font lines; --display/--body/--mono already end in system faces; the test scans the written page for any link or script with an absolute or protocol-relative URL` → no findings [tree 4e954045e110] (2026-10-21T19:49:11Z)
## Log
- 2026-10-21T17:52:42Z created
- 2026-10-21T18:33:43Z planned from capture
- 2026-10-21T19:48:25Z focused
- 2026-10-21T19:51:16Z done
- 2026-10-21T19:51:18Z committed 7f6098f3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1411 [FIX S, done, 2 steps] The website loads nothing from third parties: fonts self-hosted, and the site build fails on any outside host — lesson: A no-third-party ru…
- T-1385 [FEATURE M, dropped, 0 steps] Site/build.py:196-198` pulls Google Fonts, against the project's stance that nothing leave
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- similar finished tasks took 2–3 steps
## Regression test
test_page: the written page has no link/script loading another host and no @import; red before (step 1 evidence exit 1), green after
## Why not caught
T-1411's site build check covers site/ only; fm page has its own template
## Lessons
- A no-third-party rule needs a test on every page generator, not only the website
## Plan gaps
- failed first: step 1 failing test in test_page: the written page.html has no <link …https://> or fonts.googleapis; then …
## Files touched
- plugin/tests/test_page.py
- plugin/lib/page.html
- CHANGELOG.md
