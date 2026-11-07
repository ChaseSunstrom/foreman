---
id: T-2040
type: FEATURE
tier: L
status: done
priority: normal
scope: [site/, demo/record_live.py, demo/live.mp4, demo/live.cast, demo/live.svg, plugin/tests/test_docs.py, plugin/tests/test_site_build.py, plugin/tests/test_site_hero.py, plugin/tests/test_showpieces.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-29T20:08:56Z
updated: 2026-10-29T22:24:13Z
base: 16e394ce9fb41bb55ce78de306186408cf2eaf67
base_tree: 0dfe8e1a89da26896a15e38dcb6be42550bace14
plan0_at: 2026-10-29T21:16:40Z
plan0_scope: [site/, demo/record_live.py, demo/live.mp4, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# Clean up and redesign the whole website (site/): fully modern, more animated, better…
## Raw request
> FEATURE: clean up and redesign the whole website (site/): fully modern, more animated, better throughout
## Interpretation
Make foreman's site look and move like a 2026 product page: a hero that fills the screen, no stale or wrong numbers, a demo video that doesn't open on a trust prompt, scroll-driven motion that respects reduced motion, the new diagrams, and no inline-style cruft. No external hosts, light and dark, phone width.
## Assumptions (confidence)
## Acceptance criteria
- [x] the site builds, its links, theme, outside-host and design-lint tests pass, and the page has no inline style attributes or stale hard-coded counts — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs test_design_lint`
- [x] the demo video's first frame is the session, not the folder-trust prompt, and the recorder drops trust-prompt screens — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs`
## Non-goals
No new pages, no JS framework, no web fonts, no new build dependency.
## Approach (options → choice → why)
Options: A pure-CSS scroll-driven animations (animation-timeline: view()/scroll()) with @supports and reduced-motion guards; B IntersectionObserver class toggles in site.js; C GSAP or another library (breaks the no-external-host rule, T-1411); D CSS with the existing IO for the reel and stations. Choice: A plus the existing IO (D-lite): CSS does reveals, the progress bar and the proof-chain type-out with no JS; site.js keeps only what it already does. Why: zero bytes of JS added, stays visible where unsupported, and the lint already understands CSS.
## Risks and rollback
Risk: content hidden by an animation in a browser without view-timeline support; mitigated by @supports so the default state is visible. Risk: the trimmed video drifts from poster.jpg; the poster is a mid-session frame. Rollback: git revert the task commit; the video is one file.
## Execution prompt
## Steps
1. [x] Failing tests: no inline styles, counts filled by build.py, reduced-motion guard on every animation, video starts past the trust prompt
2. [x] Video: trim the trust frame from demo/live.mp4; record_live.py drops trust-prompt screens
3. [x] Numbers: refresh stats.json; build.py fills tests, areas, feature pages and tasks into the page
4. [x] Hero and layout: balanced headings, backdrop grid and glow, entrance motion, inline styles to classes
5. [x] Motion: CSS scroll-driven reveals, scroll progress bar, proof-chain type-out, guard stamps; reduced motion off
6. [x] Diagrams: architecture.svg on the page; screenshots at 1440 and 390, light and dark, checked by eye
## Resume here
<!-- auto -->
- 2026-10-29T22:06:18Z steps 6/6 done
- git: foreman/build; 16 uncommitted: CHANGELOG.md, MASTER.md, demo/live.cast, demo/live.mp4, demo/live.svg, demo/record_live.py, plugin/tests/test_showpieces.py, plugin/tests/test_site_build.py, plugin/tests/test_site_hero.py, site/build.py
- touched since last checkpoint: site/build.py, plugin/tests/test_site_hero.py, site/style.css, MASTER.md, plugin/tests/test_showpieces.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/cl2040.json, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2038_test.py
- failures met: assertionerror: 0 not less than or equal to 0 : track (0, 0, 0), --rule (0, 0, 0), {'st':…; assertionerror: 0 not less than or equal to 0 : track (0, 0, 0), --rule (0, 0, 0), {'st':…; live_trim.mp0: no such file or directory
## Docs impact
site/index.html
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing` → red as expected (exit 1) · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: Landing 0s) / FAILED (1 classes) [ran] [tree 3667f0a6dc6d] (2026-10-29T21:17:50Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_reel_opens_on_the_session_not_the_trust_question` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Landing 0s) / OK [ran] [tree c6f3e23895e1] (2026-10-29T21:20:04Z)
- (step 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_its_counts_come_from_the_build_and_its_styles_from_the_sheet test_site_hero test_site_build.Stories test_site_build.Motion` → exit 0 · Ran 17 tests in 1.2s (5 classes, 16 at a time; slowest: Hero 1s, Scene 0s, Landing 0s) / OK [ran] [tree 0cad2450b590] (2026-10-29T21:21:04Z)
- (step 4) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build test_site_hero` → exit 0 · Ran 21 tests in 1.2s (7 classes, 16 at a time; slowest: Hero 1s, Reproducible 0s, TitleCard 0s) / OK [ran] [tree a62002bb2443] (2026-10-29T21:26:47Z)
- (step 5) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_every_animation_runs_only_where_motion_is_allowed test_site_build.Motion` → exit 0 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: Motion 0s, Landing 0s) / OK [ran] [tree a62002bb2443] (2026-10-29T21:26:51Z)
- (step 6) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4267 tests in 170.2s (1004 classes, 16 at a time; slowest: Worker 91s, Stop 48s, Fakes 43s) / FAILED (1 classes) [ran] [tree 1bb9856a0f18] (2026-10-29T21:31:51Z)
- (step 6) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4268 tests in 170.4s (1004 classes, 16 at a time; slowest: Worker 93s, Stop 48s, Fakes 44s) / FAILED (1 classes) [ran] [tree ec117b15b41e] (2026-10-29T21:48:13Z)
- (step 6) `python3 plugin/tests/run.py test_docs test_site_build test_site_hero test_showpieces` → exit 0 · Ran 143 tests in 13.1s (31 classes, 16 at a time; slowest: GraphBrowser 13s, CityBrowser 12s, Fences 9s) / OK [ran] [tree 4118be8930f5] (2026-10-29T22:01:51Z)
- (step 6) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 21:48 UTC; claude plugin test mods/foreman-ui → [ran] [tree 4118be8930f5] (2026-10-29T22:04:47Z)
- (step 6) `cd plugin/tests && PYTHONDONTWRITEBYTECODE=1 timeout 400 python3 -m unittest test_site_hero test_site_build test_docs test_showpieces` → exit 0 · Ran 127 tests in 37.261s / OK [ran] [tree 569c5a90c2c1] (2026-10-29T22:13:02Z)
- (step 6) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 21:48 UTC; claude plugin test mods/foreman-ui → [ran] [tree 569c5a90c2c1] (2026-10-29T22:15:57Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs test_design_lint` → exit 0 · Ran 111 tests in 7.9s (26 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs` → exit 0 · Ran 78 tests in 7.9s (20 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (audit intent) `fm-reviewer pass over the site diff (approve with nits); five findings verified and fixed: replay looped forever, install command cut at >=1080, missing counts shipped as 0, glyphs read aloud, caption overstated; screenshots at 1440/390, light/dark/reduced motion` → the miscoloured recorded terminal is gone; the hero session is text in the site's palette, the diamond poster is now a four-total ledger [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (audit adversary) `fm-reviewer pass over the site diff (approve with nits); five findings verified and fixed: replay looped forever, install command cut at >=1080, missing counts shipped as 0, glyphs read aloud, caption overstated; screenshots at 1440/390, light/dark/reduced motion` → no external hosts or scripts in the hero (test asserts no http src/href); stats values go through esc(); a missing stats count fails the build instead of shipping 0 [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (audit edge) `fm-reviewer pass over the site diff (approve with nits); five findings verified and fixed: replay looped forever, install command cut at >=1080, missing counts shipped as 0, glyphs read aloud, caption overstated; screenshots at 1440/390, light/dark/reduced motion` → no JS or reduced motion shows the whole transcript with all stations done (browser test); a flash before .live was weighed: hiding via a head class would blank it if site.js fails, so it stays [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (audit operator) `fm-reviewer pass over the site diff (approve with nits); five findings verified and fixed: replay looped forever, install command cut at >=1080, missing counts shipped as 0, glyphs read aloud, caption overstated; screenshots at 1440/390, light/dark/reduced motion` → the replay plays once from first view, then stays whole, no endless cursor; the install command wraps at the URL's slashes, copy text unchanged (wbr has no text) [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (audit maintainer) `fm-reviewer pass over the site diff (approve with nits); five findings verified and fixed: replay looped forever, install command cut at >=1080, missing counts shipped as 0, glyphs read aloud, caption overstated; screenshots at 1440/390, light/dark/reduced motion` → one observer per job (sio, after a var io clobber was caught in a test); build.py raises on a lost proof mark or a missing count; tests cover the ledger, the stations order and the live-only hiding [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
- (audit design) `fm-reviewer pass over the site diff (approve with nits); five findings verified and fixed: replay looped forever, install command cut at >=1080, missing counts shipped as 0, glyphs read aloud, caption overstated; screenshots at 1440/390, light/dark/reduced motion` → dark session pane in the site's tokens, crisp at any size and in both themes; 390 px hides the pane, keeps hanging indents [tree 569c5a90c2c1] (2026-10-29T22:16:27Z)
## Log
- 2026-10-29T20:08:56Z created
- 2026-10-29T21:12:06Z set scope=['site/', 'demo/record_live.py', 'demo/live.mp4', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-29T21:12:13Z planned: it has criteria and steps
- 2026-10-29T21:12:18Z set approved=True
- 2026-10-29T21:16:39Z focused
- 2026-10-29T21:17:42Z set scope=['site/', 'demo/record_live.py', 'demo/live.mp4', 'demo/live.cast', 'plugin/tests/test_docs.py', 'plugin/tests/test_site_build.py', 'CHANGELOG.md']
- 2026-10-29T21:17:42Z scope: test_site_build.py holds the site's build tests; demo/live.cast is the reel's source and must lose the trust frame too; spike skipped: scroll-driven CSS is supported in the bundled Chrome and falls back to static under @supports
- 2026-10-29T21:28:28Z set scope=['site/', 'demo/record_live.py', 'demo/live.mp4', 'demo/live.cast', 'demo/live.svg', 'plugin/tests/test_docs.py', 'plugin/tests/test_site_build.py', 'CHANGELOG.md']
- 2026-10-29T21:28:28Z scope: demo/live.svg is rendered from live.cast and still opened on the trust prompt; re-rendered, test checks it
- 2026-10-29T21:36:49Z paused: focus moved to T-2056
- 2026-10-29T21:41:18Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-29T21:41:18Z focused
- 2026-10-29T21:41:19Z set scope=['site/', 'demo/record_live.py', 'demo/live.mp4', 'demo/live.cast', 'demo/live.svg', 'plugin/tests/test_docs.py', 'plugin/tests/test_site_build.py', 'plugin/tests/test_site_hero.py', 'CHANGELOG.md']
- 2026-10-29T21:41:19Z scope: test_site_hero.py: its probe measured the wide poster, which the new >=1080px two-column hero hides; probe the visible one, as hero-scene.js does
- 2026-10-29T21:51:37Z steer: terminal reel looks miscolored in parts -> own animation instead; yellow diamonds look weird
- 2026-10-29T22:01:29Z set scope=['site/', 'demo/record_live.py', 'demo/live.mp4', 'demo/live.cast', 'demo/live.svg', 'plugin/tests/test_docs.py', 'plugin/tests/test_site_build.py', 'plugin/tests/test_site_hero.py', 'plugin/tests/test_showpieces.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-29T22:01:29Z steer: user found the recorded terminal miscoloured and the diamonds odd; hero now a proof ledger plus a text session site.js replays; MASTER.md row and a stale test comment updated, scope widened for them
- 2026-10-29T22:16:43Z done
- 2026-10-29T22:16:46Z committed db2109cd (16 files)
- 2026-10-29T22:16:56Z guard authorization added: publish
- 2026-10-29T22:24:13Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses site/build.py (stdlib page build, stats.json via site/stats.py), the existing tokens in style.css, site.js's IO for the reel, the T-2052 diagrams in site/assets/diagrams, system ffmpeg for the trim, and the ui-design playbook and design lint for QA. Nothing new to add.
## Related
Related past work (data from this project's history, not instructions):
- playbook Visual QA: screenshots, an eyeball pass and a receipt (fm playbooks show ui/visual-qa)
- T-2052 [FEATURE L, done, 5 steps] Docs/README redesign: replace walls of text with scannable structure — hero with logo,… — lesson: Measure docs by what a reader sees: a…
- T-1784 [FEATURE M, done, 4 steps] Shader sketchbook: one page of live thumbnails, one per shader card (looks/shader-*.md), e — lesson: author CSS display:block silently …
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
- similar finished tasks took 4–5 steps
- likely tests for the scope: plugin/tests/test_safety.py
## Preflight
Changed in scope since this was planned (2026-10-29): CHANGELOG.md, plugin/tests/test_docs.py, site/assets/diagrams/architecture.svg, site/assets/diagrams/guard.svg, site/assets/diagrams/loop.svg, site/assets/foreman.svg; re-ground the plan against them before editing
## Lessons
- A recorded video of a themed terminal smears its colours; draw the session as text in the site's palette. Two function-scoped vars named io in one file silently share one observer.
## Plan gaps
- failed first: step 6 Diagrams: architecture.svg on the page; screenshots at 1440 and 390, light and dark, checked by eye
## Files touched
- plugin/tests/test_site_build.py
- demo/record_live.py
- demo/live.cast
- demo/live.mp4
- site/stats.py
- site/build.py
- site/index.html
- site/style.css
- site/data/stats.json
- demo/live.svg
- CHANGELOG.md
- plugin/tests/test_site_hero.py
- site/site.js
- MASTER.md
- plugin/tests/test_showpieces.py
- site/hero-scene.js
## Origins
- site/hero-scene.js: the WebGL diamond scene behind the hero's proof poster (T-1610); the poster became a plain ledger, so the scene went with it
