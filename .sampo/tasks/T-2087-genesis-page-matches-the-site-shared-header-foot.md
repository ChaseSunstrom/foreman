---
id: T-2087
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T03:13:52Z
updated: 2026-10-30T03:24:22Z
base: 2a1575e878227046151933c36555d7b4c47daac4
base_tree: a5d6cb4652bad6f7c664717f8d67dbc4dd9afbee
plan0_at: 2026-10-30T03:14:01Z
plan0_scope: []
verified: ok
---
# Genesis page matches the site: shared header, footer and style.css tokens
## Raw request
> Genesis page matches the site: shared header, footer and style.css tokens
## Interpretation
The Genesis page was built on its own stylesheet (blueprint palette, Inter, its own top bar and footer) and never loads the site's style.css, so it looks like a different site. Make it share the site's shell: same header nav, footer, fonts, colours, width.
## Assumptions (confidence)
## Acceptance criteria
- [x] genesis/index.html loads ../style.css with the site's header nav and footer; genesis.css keeps only graph rules on site tokens; site and lint tests pass — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_design_lint test_site`
## Non-goals
## Approach (options → choice → why)
Options: (1) render genesis through build.py layout() (it brings a feature side-nav the page doesn't want); (2) mirror the landing header/footer markup in genesis/index.html, load ../style.css first and alias genesis.css's private tokens onto site tokens, dropping its base/header/footer/palette rules; (3) rewrite genesis.css from scratch. Chose (2): smallest diff, keeps every graph rule, the dark palette comes from style.css. build.py rewrites the style/icon links to their content-hashed URLs like the landing page.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test red: page links ../style.css and carries the site header nav
2. [x] Rebase index.html and genesis.css on the site shell; build hashes the style link
3. [x] Look at it: light and dark, 360 and 1440
## Resume here
<!-- auto -->
- 2026-10-30T03:17:06Z step 1/3: Test red: page links ../style.css and carries the site header nav
- git: foreman/build; 7 uncommitted: plugin/tests/test_genesis.py, plugin/tests/test_site_build.py, site/build.py, site/genesis/genesis.css, site/genesis/genesis.js, site/genesis/index.html, plugin/tests/test_exam.py
- touched since last checkpoint: plugin/tests/test_genesis.py, site/genesis/index.html, site/genesis/genesis.css, site/genesis/genesis.js, plugin/tests/test_site_build.py, site/build.py
## Docs impact
CHANGELOG line added; MASTER.md and README unchanged (no verb or flag changed, only the page's look).
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 9 tests in 1.5s (2 classes, 16 at a time; slowest: Genesis 1s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree d037f62bbcf8] (2026-10-30T03:14:18Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_design_lint test_site test_site_build` → exit 0 · Ran 67 tests in 2.7s (17 classes, 16 at a time; slowest: Header 3s, Genesis 2s, Landing 1s) / OK [ran] [tree ce58ca2ba507] (2026-10-30T03:21:07Z)
- (step 3) `Playwright shots of the built /genesis/ at 360x800 and 1440x900, light and dark (scratchpad shot2087b/g-*.png), read by eye` → Same header nav, footer, palette, type and width as the landing page in both themes; kicker margin 32px/64px after renaming .head→.ghead (style.css's features .head p rule was zeroing it); no horizontal scroll (scrollWidth = viewport), no console errors [tree ce58ca2ba507] (2026-10-30T03:21:12Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_site_build` → ✗ exit 1 · Ran 20 tests in 2.2s (7 classes, 16 at a time; slowest: Genesis 1s, Landing 1s, Reproducible 1s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree ce58ca2ba507] (2026-10-30T03:21:23Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_site_build` → exit 0 · Ran 20 tests in 1.5s (7 classes, 16 at a time; slowest: Genesis 1s, Landing 1s, Reproducible 1s) / OK [ran] [tree ce58ca2ba507] (2026-10-30T03:21:23Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_design_lint test_site` → exit 0 · Ran 67 tests in 2.7s (17 classes, 16 at a time; slowest: Header 3s, Genesis 2s, Landing 1s) / OK [ran] [tree 332883794333] (2026-10-30T03:21:50Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 9 tests in 1.5s (2 classes, 16 at a time; slowest: Genesis 1s, GenesisExport 1s) / OK [ran] [tree 332883794333] (2026-10-30T03:21:50Z)
- (audit intent) `self-review of the diff plus Playwright shots at 360/1440 in light and dark; computed-style probe for the kicker` → the page now loads ../style.css and carries the landing page's exact nav (test asserts link-for-link equality), footer and palette; the visible mismatch the user asked about is gone [tree 332883794333] (2026-10-30T03:21:50Z)
- (audit edge) `self-review of the diff plus Playwright shots at 360/1440 in light and dark; computed-style probe for the kicker` → class names shared with style.css (.head) silently overrode page rules; renamed to .ghead and the test refuses a top-level .head in genesis.css; 360px has no horizontal scroll; dark mode comes from style.css's own block [tree 332883794333] (2026-10-30T03:21:50Z)
- (audit maintainer) `self-review of the diff plus Playwright shots at 360/1440 in light and dark; computed-style probe for the kicker` → genesis.css lost its own palette and base rules (210→168 lines); only tower shades remain, mixed from site tokens, so a site palette change reaches this page [tree 332883794333] (2026-10-30T03:21:50Z)
## Log
- 2026-10-30T03:13:52Z created
- 2026-10-30T03:14:00Z focused
- 2026-10-30T03:21:33Z scope: CHANGELOG.md for the docs line; site/build.py hashes the page's shared style link
- 2026-10-30T03:21:54Z done
- 2026-10-30T03:21:56Z committed 0b64215c (7 files)
- 2026-10-30T03:22:15Z guard authorization added: publish
- 2026-10-30T03:24:22Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- research T-2063-review: Verdict:** approve with nits. I found no defect I can trigger, only one LOW test gap. [stale: plugin/tests/test_site_build.py, site/build.py, sit…
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- similar finished tasks took 4–6 steps
## Why not caught
No test compared the Genesis page with the site shell; the new test checks the shared stylesheet and nav link-for-link
## Lessons
- A sub-page that loads the site stylesheet inherits its class names too: probe computed styles (not just parsed rules) when a margin or colour won't apply, and give page-only blocks names the site doesn't use
## Plan gaps
- failed first: step 1 Test red: page links ../style.css and carries the site header nav
## Files touched
- plugin/tests/test_genesis.py
- site/genesis/index.html
- site/genesis/genesis.css
- site/genesis/genesis.js
- plugin/tests/test_site_build.py
- site/build.py
- CHANGELOG.md
