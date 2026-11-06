---
id: T-1615
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmintegrations.py, plugin/lib/fmcli.py, plugin/tests/test_desk.py, plugin/tests/test_site_build.py, plugin/tests/test_docs.py, site/build.py, site/site.js, site/style.css, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T20:54:37Z
updated: 2026-10-23T17:52:25Z
base: 12cc7c1cc8679a1dd3778b9bfc0c6b23715b5663
base_tree: 880fb276fd7b47e3a4bb5b28e46bb687c2b308af
plan0_at: 2026-10-23T17:48:47Z
plan0_scope: [plugin/lib/fmintegrations.py, plugin/lib/fmcli.py, plugin/tests/test_desk.py, plugin/tests/test_site_build.py, site/build.py, site/site.js, site/style.css, CHANGELOG.md, MASTER.md]
verified: strong
---
# Integrations desk card and animated SVG charts (T-1551 step 4): needs a decision on an HTT
## Raw request
> Integrations desk card and animated SVG charts (T-1551 step 4): needs a decision on an HTTP listener, since fmserve has no HTTP routes and fm never opens a port by default
## Interpretation
Two leftovers of T-1551: a desk card (the project's glance drawn for an e-paper panel or an old phone) and animated SVG charts for the bench and stats pages. No HTTP listener: fm desk writes the card as SVG (PNG with rsvg-convert, an HTML copy that refreshes itself), once or every S seconds, for a synced folder the device reads. The site's existing bench and stats charts draw themselves once when scrolled into view, only when the reader allows motion and only with JavaScript (without it they show complete).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm desk writes the glance as a valid SVG card (an HTML copy that refreshes, a PNG with rsvg-convert) and opens no port; the site's charts carry draw classes armed only with motion allowed — verify with `python3 plugin/tests/run.py test_desk test_site_build`
## Non-goals
## Approach (options → choice → why)
Desk: (a) an HTTP listener on the LAN (opens a port, needs auth); (b) push to a device API (one vendor); (c) a file renderer from fm glance, black on white at 800x480 by default (the common 7.5-inch e-paper), with --every to keep it fresh. Chosen (c). Charts: (a) SMIL inside each SVG (plays on load, off-screen, ignores reduced motion); (b) a JS chart library (a dependency); (c) classes on the site's own SVG plus CSS transitions armed by the site's IntersectionObserver under prefers-reduced-motion: no-preference. Chosen (c): no dependency, motion only when it is seen and allowed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] fm desk card
3. [x] animated site charts
4. [x] parser and docs
## Resume here
## Docs impact
MASTER.md (Integrations line: fm desk; site charts), CHANGELOG.md.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_desk test_site_build` → ✗ exit 1 · Ran 10 tests in 1.6s (6 classes, 16 at a time; slowest: TitleCard 1s, Reproducible 1s, Card 0s) / FAILED (2 classes) [ran] [tree 58f2988e1183] (2026-10-23T17:49:09Z)
- (step 1) `python3 plugin/tests/run.py test_desk test_site_build` → exit 0 · Ran 10 tests in 0.9s (6 classes, 16 at a time; slowest: TitleCard 1s, Card 1s, Reproducible 1s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:51:03Z)
- (step 2) `python3 plugin/tests/run.py test_desk test_site_build` → exit 0 · Ran 10 tests in 0.9s (6 classes, 16 at a time; slowest: TitleCard 1s, Card 1s, Reproducible 1s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:51:05Z)
- (step 3) `python3 plugin/tests/run.py test_desk test_site_build` → exit 0 · Ran 10 tests in 0.9s (6 classes, 16 at a time; slowest: TitleCard 1s, Card 1s, Reproducible 1s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:51:06Z)
- (step 4) `python3 plugin/tests/run.py test_cli test_docs test_suite_hygiene test_integrations` → exit 0 · Ran 210 tests in 23.8s (57 classes, 16 at a time; slowest: TaskLifecycle 24s, Fences 9s, StateViews 9s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:51:31Z)
- (ac 1) `python3 plugin/tests/run.py test_desk test_site_build` → exit 0 · Ran 10 tests in 0.8s (6 classes, 16 at a time; slowest: TitleCard 1s, Card 1s, Reproducible 1s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:51:32Z)
- (ac 1) `python3 plugin/tests/run.py test_desk test_site_build` → exit 0 · Ran 10 tests in 0.9s (6 classes, 16 at a time; slowest: TitleCard 1s, Card 1s, Reproducible 1s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:51:58Z)
- (ac 1) `python3 plugin/tests/run.py test_desk test_site_build` → exit 0 · Ran 10 tests in 0.9s (6 classes, 16 at a time; slowest: TitleCard 1s, Card 1s, Reproducible 1s) / OK [ran] [tree cc0dc83b59c5] (2026-10-23T17:52:00Z)
- (audit intent) `self-review of fmintegrations' desk code, the parser and the site motion: the card is black and white only (tested), every string html-escaped, a sensitive project's glance already omits the title, PNG through rsvg-convert with temp files removed, --every floored at 10 s and Ctrl-C ends it, no socket or http.server anywhere (tested); charts are whole without JS or with reduced motion (armed only after site.js's still check, CSS inside prefers-reduced-motion: no-preference); photographed the card` → a desk card for e-paper or an old phone and moving bench and stats charts, with the decision that fm opens no port recorded [tree cc0dc83b59c5] (2026-10-23T17:52:00Z)
- (audit edge) `self-review of fmintegrations' desk code, the parser and the site motion: the card is black and white only (tested), every string html-escaped, a sensitive project's glance already omits the title, PNG through rsvg-convert with temp files removed, --every floored at 10 s and Ctrl-C ends it, no socket or http.server anywhere (tested); charts are whole without JS or with reduced motion (armed only after site.js's still check, CSS inside prefers-reduced-motion: no-preference); photographed the card` → no active task draws 'No active task'; a long title wraps to two lines with an ellipsis; a size outside 120..4000 or not WxH is refused; a glance that fails draws an error card instead of a trace [tree cc0dc83b59c5] (2026-10-23T17:52:00Z)
- (audit adversary) `self-review of fmintegrations' desk code, the parser and the site motion: the card is black and white only (tested), every string html-escaped, a sensitive project's glance already omits the title, PNG through rsvg-convert with temp files removed, --every floored at 10 s and Ctrl-C ends it, no socket or http.server anywhere (tested); charts are whole without JS or with reduced motion (armed only after site.js's still check, CSS inside prefers-reduced-motion: no-preference); photographed the card` → nothing listens: the device reads a file the user's own sync carries; the HTML copy is static with a meta refresh and no script; titles are escaped into the SVG [tree cc0dc83b59c5] (2026-10-23T17:52:00Z)
## Log
- 2026-10-22T20:54:37Z created
- 2026-10-23T17:47:15Z set type=FEATURE, tier=M, scope=['plugin/lib/fmintegrations.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_desk.py', 'plugin/tests/test_site_build.py', 'site/build.py', 'site/site.js', 'site/style.css', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:47:17Z lane: ~/.claude/foreman.lanes/T-1615 on foreman/T-1615
- 2026-10-23T17:48:47Z focused
- 2026-10-23T17:50:31Z set scope=['plugin/lib/fmintegrations.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_desk.py', 'plugin/tests/test_site_build.py', 'plugin/tests/test_docs.py', 'site/build.py', 'site/site.js', 'site/style.css', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:50:31Z scope: test_docs.py: its site check matched class="viz" exactly; charts now carry a motion class too
- 2026-10-23T17:51:46Z merged foreman/T-1615 (10 file(s))
- 2026-10-23T17:51:46Z lane removed: ~/.claude/foreman.lanes/T-1615
- 2026-10-23T17:51:49Z focused
- 2026-10-23T17:52:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1551 [FEATURE M, done, 4 steps] Round 3 (T-1520): Integrations: export runs as Perfetto/OTLP traces, a glance protocol (on — lesson: A stdio server must survive any by…
- decision 2026-10-23: T-1615: the desk card is a file, never a listener
- playbook Scrollytelling: steps the reader controls (fm playbooks show ui/scrollytelling)
- research T-1220-review: Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did no…
- the similar finished task took 4 steps
- start here (files T-1551 touched): plugin/tests/test_integrations.py, plugin/lib/fmintegrations.py, plugin/lib/fmcli.py, MASTER.md, plugin/skills/status/SKILL.md, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_integrations.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmintegrations.py, plugin/tests/test_desk.py, plugin/tests/test_docs.py, plugin/tests/test_site_build.py, site/build.py, site/site.js, site/st…; re-ground the plan against them before editing
## Lessons
- A literal markup check in an older test (class="viz") breaks when markup gains a class: match the stable prefix, not the whole attribute.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmintegrations.py
- plugin/tests/test_desk.py
- plugin/tests/test_docs.py
- plugin/tests/test_site_build.py
- site/build.py
- site/site.js
- site/style.css
