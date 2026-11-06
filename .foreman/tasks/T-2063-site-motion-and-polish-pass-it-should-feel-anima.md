---
id: T-2063
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T23:29:52Z
updated: 2026-10-30T00:35:39Z
group: site pages, shaders and motion
base: 6057976f7b94bf49d4832e40b50108c03ba3f0e7
base_tree: 7ecc8dbd636e4bc2fea5239154a5034058de9dbc
plan0_at: 2026-10-30T00:12:09Z
plan0_scope: []
verified: strong
---
# Site polish: hashed CSS/JS URLs, drifting hero light, proof figures count up, pointer glow on feature cards
## Raw request
> FEATURE: site motion and polish pass: it should feel animated and well made, per the motion playbook, reduced motion respected
## Interpretation
The user said the site doesn't feel animated or well made enough. Live CSS matches the build, so the look is current, but style.css and site.js have no version in their URLs (a returning browser can keep old styles), the hero backdrop is static, the proof figures sit still and the feature cards only lift on hover.
## Assumptions (confidence)
## Acceptance criteria
- [x] every built page's stylesheet, script and icon URLs carry their file's content hash, and every animation stays inside prefers-reduced-motion: no-preference — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
A complete version: fresh assets for every visitor, ambient motion in the hero, one counted moment, direct feedback under the pointer, every bit still and whole under reduced motion. Options: (a) CSS/JS-only polish on the drafting-table direction: hashed URLs, the two lights drift on their own paths, figures count up once, a pointer-follow glow on fcards; (b) a live shader as the hero backdrop (hurts text contrast; the looks strip already shows shaders); (c) a scroll-scrubbed hero (pinning fights reading on phones); (d) a motion library (a host or vendored dependency for what 40 lines do). Choice: (a): no dependency, no host, each piece small and reversible.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: style.css and site.js URLs carry ?v=<hash> on the landing, a feature page and a story
2. [x] build.py hashes style.css and site.js like the icon
3. [x] hero lights drift, proof figures count up once, fcards get a pointer-follow glow, shader ids wrap whole
4. [x] screenshot the landing light and dark at 390 and 1280; read them
## Resume here
<!-- auto -->
- 2026-10-30T00:18:47Z step 3/4: hero lights drift, proof figures count up once, fcards get a pointer-follow glow, shader ids wrap whole
- git: foreman/build; 4 uncommitted: plugin/tests/test_site_build.py, site/build.py, site/site.js, site/style.css
- touched since last checkpoint: plugin/tests/test_site_build.py, site/build.py, site/style.css, site/site.js, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/shoot_polish.sh
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_asset_urls_change_with_their_content` → red as expected (exit 1) · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Landing 1s) / FAILED (1 classes) [ran] [tree fcb59a154e5e] (2026-10-30T00:12:39Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → exit 0 · Ran 11 tests in 4.2s (5 classes, 16 at a time; slowest: Landing 4s, Reproducible 2s, TitleCard 1s) / OK [ran] [tree 1f0cf15f3730] (2026-10-30T00:13:27Z)
- (step 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → exit 0 · Ran 11 tests in 2.5s (5 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 87503fd943ae] (2026-10-30T00:20:27Z)
- (step 4) `sh /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/shoot_polish.sh` → exit 0 · 102399 p-glow-1.png / 227141 p-phone.png [ran] [tree 87503fd943ae] (2026-10-30T00:20:35Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build 2>&1 | grep -E "^(FAIL|ERROR)|AssertionError|^OK|^FAILED|Ran " | head` → exit 0 · Ran 11 tests in 2.3s (5 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 3a55a4e41d19] (2026-10-30T00:21:40Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build 2>&1 | grep -E "^(FAIL|ERROR)|Error|^OK|Ran " | head` → exit 0 · Ran 11 tests in 2.6s (5 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 5cad1dc37ea1] (2026-10-30T00:23:50Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → exit 0 · Ran 11 tests in 2.4s (5 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
- (audit intent) `one fm-reviewer pass over the diff (all six lenses); its LOW test gap fixed test-first in test_site_build; settled headless shots light, dark, 390 px and looks section viewed` → hashed URLs on every built page (icon link, header and footer logo, CSS, JS), the hero lights drift, figures count up, card light follows the pointer, shader names wrap whole [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
- (audit adversary) `one fm-reviewer pass over the diff (all six lenses); its LOW test gap fixed test-first in test_site_build; settled headless shots light, dark, 390 px and looks section viewed` → no new input surface; the build raises if index.html loses a tag it rewrites, so a reworded tag can't ship a stale cached file [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
- (audit edge) `one fm-reviewer pass over the diff (all six lenses); its LOW test gap fixed test-first in test_site_build; settled headless shots light, dark, 390 px and looks section viewed` → stalled frames → a 1700 ms backstop writes the exact figures; non-numeric dd skipped; tabular-nums stops layout shift; no WebGL or no JS leaves the static text [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
- (audit operator) `one fm-reviewer pass over the diff (all six lenses); its LOW test gap fixed test-first in test_site_build; settled headless shots light, dark, 390 px and looks section viewed` → the drift repaints the hero gradient while it's on screen (offscreen paint is skipped); browsers without @property step instead of glide; both acceptable for a landing page [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
- (audit maintainer) `one fm-reviewer pass over the diff (all six lenses); its LOW test gap fixed test-first in test_site_build; settled headless shots light, dark, 390 px and looks section viewed` → one _v() helper hashes all three files at import; a test pins every tag on four page kinds and pins the JS motion behind the reduced-motion return [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
- (audit design) `one fm-reviewer pass over the diff (all six lenses); its LOW test gap fixed test-first in test_site_build; settled headless shots light, dark, 390 px and looks section viewed` → lights move ~15% across 16 s, eased and alternating, so it reads as breathing not sliding; glow at 14% accent, 240 px, hover only; all motion off under reduced motion [tree 5cad1dc37ea1] (2026-10-30T00:24:10Z)
## Log
- 2026-10-29T23:29:52Z created
- 2026-10-29T23:53:01Z plan: (1) style.css/site.js URLs carry a content hash like the favicon (a returning visitor got stale styles); (2) the hero's warm light drifts slowly; (3) proof numbers count up once on first view; (4) fcards get a pointer-follow glow; (5) DESIGN.md ## Direction written; all motion inside no-preference, still and whole without it
- 2026-10-30T00:08:05Z planned from capture
- 2026-10-30T00:12:07Z focused
- 2026-10-30T00:24:16Z done
- 2026-10-30T00:24:19Z committed 4c6b3dee (5 files)
- 2026-10-30T00:24:41Z guard authorization added: publish
- 2026-10-30T00:35:39Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- T-1784 [FEATURE M, done, 4 steps] Shader sketchbook: one page of live thumbnails, one per shader card (looks/shader-*.md), e — lesson: author CSS display:block silently …
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- similar finished tasks took 4–6 steps
## Lessons
- A favicon fix (T-2060) that hashed only the icon left CSS and JS on bare URLs: when one asset needs cache-busting, hash every asset the page references in the same pass.
## Files touched
- plugin/tests/test_site_build.py
- site/build.py
- site/style.css
- site/site.js
- CHANGELOG.md
