---
id: T-1738
type: FIX
tier: S
status: done
priority: normal
scope: [site/**, plugin/lib/fmpage.py, plugin/lib/graph.html, plugin/tests/test_site*.py, plugin/tests/test_showpieces.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T04:12:23Z
updated: 2026-10-23T05:22:06Z
batch: [T-1683, T-1735]
base: 01aa0a172d69996c23b770bbaff8c1789a2aafd7
base_tree: a946e9ba462b126fd5e04948952d617aae98b76a
plan0_at: 2026-10-23T05:15:32Z
plan0_scope: [site/**, plugin/lib/fmpage.py, plugin/lib/graph.html, plugin/tests/test_site*.py, plugin/tests/test_showpieces.py, CHANGELOG.md]
verified: strong
---
# Layout collisions: site header at 320 px, graph poster labels in dense clusters
## Raw request
> T-1683: Site header at 320 px: the Foreman brand overlaps the Install link (seen in T-1609's phone screenshots)
> T-1735: fm page graph: poster labels in dense blocked clusters overlap (T-0352 and T-0337); space them or drop colliding ones
## Interpretation
Do T-1683, T-1735 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1738. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1683: at 320 px wide the site header's brand and Install link don't overlap (bounding boxes measured in a real browser, skipped with a reason when none) — verify with `python3 plugin/tests/run.py test_site`
- [x] T-1735: graph poster labels never overlap: colliding labels are nudged or dropped, and a dense blocked cluster test asserts no two label boxes intersect — verify with `python3 plugin/tests/run.py test_showpieces.Graph`
## Non-goals
## Approach (options → choice → why)
T-1683: fix the header with CSS (wrap or shrink the brand below a breakpoint, no JS); measure with fm shot or the existing site browser test at 320x640. T-1735: in fmpage's poster, place labels greedily in priority order (active, then blocked) and skip any whose estimated box (chars x 0.6em by 1.2em) intersects a placed one; say how many were dropped in the poster's title text.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1683: Site header at 320 px: the Foreman brand overlaps the Install link (seen in T-1609's phone
2. [x] T-1735: Fm page graph: poster labels in dense blocked clusters overlap (T-0352 and T-0337); space
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_site test_showpieces.Graph` → ✗ exit 1 · Ran 41 tests in 13.5s (5 classes, 16 at a time; slowest: Scene 13s, GraphBrowser 12s, Header 3s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 6ff29e4c98d6] (2026-10-23T05:20:31Z)
- `python3 plugin/tests/run.py test_site test_showpieces.Graph` → exit 0 · Ran 41 tests in 12.8s (5 classes, 16 at a time; slowest: Scene 13s, GraphBrowser 12s, Header 3s) / OK [ran] [tree 6ff29e4c98d6] (2026-10-23T05:20:31Z)
- (ac 1) `python3 plugin/tests/run.py test_site.Header` → exit 0 · Ran 1 tests in 2.7s (1 classes, 16 at a time; slowest: Header 3s) / OK [ran] [tree bda435ac628a] (2026-10-23T05:20:45Z)
- (ac 2) `python3 plugin/tests/run.py test_showpieces.Graph` → exit 0 · Ran 27 tests in 12.4s (2 classes, 16 at a time; slowest: GraphBrowser 12s, Graph 2s) / OK [ran] [tree bda435ac628a] (2026-10-23T05:20:58Z)
- (step 1) `python3 plugin/tests/run.py test_site.Header test_showpieces.Graph` → exit 0 · Ran 28 tests in 12.3s (3 classes, 16 at a time; slowest: GraphBrowser 12s, Header 3s, Graph 1s) / OK [ran] [tree bda435ac628a] (2026-10-23T05:21:11Z)
- (step 2) `python3 plugin/tests/run.py test_site.Header test_showpieces.Graph` → exit 0 · Ran 28 tests in 12.3s (3 classes, 16 at a time; slowest: GraphBrowser 12s, Header 3s, Graph 1s) / OK [ran] [tree bda435ac628a] (2026-10-23T05:21:24Z)
- (ac 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 14 tests in 11.7s (3 classes, 16 at a time; slowest: Scene 12s, Header 3s, Hero 1s) / OK [ran] [tree bda435ac628a] (2026-10-23T05:21:49Z)
- (ac 2) `python3 plugin/tests/run.py test_showpieces.Graph` → exit 0 · Ran 27 tests in 12.3s (2 classes, 16 at a time; slowest: GraphBrowser 12s, Graph 1s) / OK [ran] [tree bda435ac628a] (2026-10-23T05:21:49Z)
- (audit intent) `self: the header fix is CSS only (gaps 10/14 px and a 1.3rem brand below 360 px), measured by a new test in headless Chromium at 320, 360 and 390 px (no overlap, nothing off screen, no sideways scroll); poster labels are placed greedily in priority order (active, then blocked) and one whose box would intersect a placed one is dropped` → the landing page header no longer overlaps at 320 px; dense blocked clusters on the graph poster stay readable [tree bda435ac628a] (2026-10-23T05:21:49Z)
- (audit design) `self: the header fix is CSS only (gaps 10/14 px and a 1.3rem brand below 360 px), measured by a new test in headless Chromium at 320, 360 and 390 px (no overlap, nothing off screen, no sideways scroll); poster labels are placed greedily in priority order (active, then blocked) and one whose box would intersect a placed one is dropped` → the brand shrinks only below 360 px; on the poster the first label of a cluster wins and the text twin still names every task [tree bda435ac628a] (2026-10-23T05:21:49Z)
- (audit edge) `self: the header fix is CSS only (gaps 10/14 px and a 1.3rem brand below 360 px), measured by a new test in headless Chromium at 320, 360 and 390 px (no overlap, nothing off screen, no sideways scroll); poster labels are placed greedily in priority order (active, then blocked) and one whose box would intersect a placed one is dropped` → the label box is estimated from the mono font (0.3 per character, 0.6 tall); the header test skips with a reason when there is no Chromium [tree bda435ac628a] (2026-10-23T05:21:49Z)
- (audit self) `self: the header fix is CSS only (gaps 10/14 px and a 1.3rem brand below 360 px), measured by a new test in headless Chromium at 320, 360 and 390 px (no overlap, nothing off screen, no sideways scroll); poster labels are placed greedily in priority order (active, then blocked) and one whose box would intersect a placed one is dropped` → no findings [tree bda435ac628a] (2026-10-23T05:21:49Z)
## Log
- 2026-10-23T04:12:23Z created
- 2026-10-23T04:13:05Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_site`
- 2026-10-23T04:13:05Z criterion 1 text: T-1683: Site header at 320 px: the Foreman brand overlaps the Install link (seen in T-1609's phone works → T-1683: at 320 px wide the site header's brand and Install link don't overlap (bounding boxes measured in a real browser, skipped with a reason when none)
- 2026-10-23T04:13:06Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_showpieces.Graph`
- 2026-10-23T04:13:06Z criterion 2 text: T-1735: Fm page graph: poster labels in dense blocked clusters overlap (T-0352 and T-0337); space works → T-1735: graph poster labels never overlap: colliding labels are nudged or dropped, and a dense blocked cluster test asserts no two label boxes intersect
- 2026-10-23T04:13:07Z set scope=['site/**', 'plugin/lib/fmpage.py', 'plugin/lib/graph.html', 'plugin/tests/test_site*.py', 'plugin/tests/test_showpieces.py', 'CHANGELOG.md']
- 2026-10-23T04:17:11Z grounding: site/style.css:63-73 — .top .wrap gap 20px, .brand 1.6rem condensed + 28px img, .nav gap 22px with Install, GitHub and a 38px theme button visible below 760px; estimated ~340px + wrap padding at 320 px, so it overflows. Plan: a max-width ~400px rule (smaller gaps, brand 1.3rem) and, if still over, GitHub as an icon-only link with an aria-label below 360px; measure the boxes in a real browser at 320x640 (fm shot or the site browser test). Graph labels: fmpage _graph_poster places <text class=tag> ids; add greedy placement skipping intersecting boxes.
- 2026-10-23T05:15:31Z focused
- 2026-10-23T05:21:24Z scope: plugin/tests/test_site.py (new: header layout at phone widths in a real browser), plugin/tests/test_showpieces.py, CHANGELOG.md; done in a scratch worktree while the full gates ran on main, then copied (main's copies were unchanged since its base)
- 2026-10-23T05:22:04Z done
- 2026-10-23T05:22:06Z committed d63d2058 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1737 [FEATURE S, done, 2 steps] fm shot presets: --profile tv|eink|car|wrist and --reduced-motion, also in fm stories — lesson: Emulate media features before the first…
- T-1730 [FIX M, done, 3 steps] Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil… — lesson: Judge an…
- T-1742 [FEATURE M, planned, 3 steps] fm code TUI: theme gallery, a diff view with line-by-line reveal and intra-line highlights, a third column at 160+ colu…
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_page.py, plugin/tests/test_safety.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/tests/test_showpieces.py, plugin/tests/test_site_hero.py; re-ground the plan against them before editing
## Why not caught
no test measured the header at phone widths, and the graph's label test counted labels without checking overlap
## Lessons
- Layout claims need a measurement in a real browser at the narrowest supported width
## Files touched
- plugin/lib/fmpage.py
- plugin/tests/test_showpieces.py
- site/style.css
- plugin/tests/test_site.py
- CHANGELOG.md
