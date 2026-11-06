---
id: T-2060
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-29T23:28:30Z
updated: 2026-10-29T23:39:01Z
base: 70e924b9d2dbea99eaafbc97df513d5bd55fda89
base_tree: 6767e46b7c83dca1ea7dca5ea859e8940115d474
plan0_at: 2026-10-29T23:30:44Z
plan0_scope: []
verified: strong
---
# The site's tab icon (favicon) still shows the old logo; match the redesigned mark on…
## Raw request
> FIX!: the site's tab icon (favicon) still shows the old logo; match the redesigned mark on every page
## Interpretation
The live site serves the new hard-hat logo, but browsers keep a favicon by its URL, and assets/foreman.svg never changed name, so tabs still show the old mark. Two more leftovers of the old pixel logo: image-rendering: pixelated on the brand img, and the share image (og:image poster.jpg), an old terminal screenshot with the old mascot.
## Assumptions (confidence)
## Acceptance criteria
- [x] every built page links the favicon with the logo's content hash in its URL — verify with `cd plugin/tests && python3 -m unittest test_site_build.Landing.test_the_tab_icon_url_changes_with_the_logo`
## Non-goals
## Approach (options → choice → why)
Options: (a) rename the file each logo change (manual, forgotten again); (b) a ?v= query from the logo's content hash, filled by build.py on every page (chosen: automatic, deterministic, keeps the source page working unbuilt); (c) a favicon.ico beside it (no: a project site can't own /favicon.ico). Poster: shoot a 1200x630 card (logo, wordmark, one line) with headless Chrome once and commit the JPG; generating it per build would break byte-identical builds.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] hash the icon URL in build.py; drop the pixelated rendering
3. [x] new share poster with the current logo, checked by screenshot
## Resume here
<!-- auto -->
- 2026-10-29T23:33:26Z step 1/3: failing test
- git: foreman/build; 7 uncommitted: CHANGELOG.md, plugin/tests/test_site_build.py, site/build.py, site/index.html, site/style.css, site/assets/share.png, site/share.html
- touched since last checkpoint: plugin/tests/test_site_build.py, site/style.css, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/poster/poster.html, site/assets/share.png, site/index.html, site/share.html, site/build.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/cl2060.json, CHANGELOG.md
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_site_build.Stories.test_the_tab_icon_url_changes_with_the_logo` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree 6767e46b7c83] (2026-10-29T23:30:52Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_site_build.Landing.test_the_tab_icon_url_changes_with_the_logo` → ✗ exit 1 · Ran 1 test in 0.403s / FAILED (failures=1) [ran] [tree d0a5c1b5a9ac] (2026-10-29T23:31:11Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_site_build` → exit 0 · Ran 9 tests in 2.253s / OK [ran] [tree 9217652192a3] (2026-10-29T23:31:35Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_site_build test_docs` → exit 0 · Ran 70 tests in 10.528s / OK [ran] [tree 132f5480180b] (2026-10-29T23:33:00Z)
- `cd plugin/tests && python3 -m unittest test_site_build.Landing.test_the_tab_icon_url_changes_with_the_logo` → ✗ exit 1 · Ran 1 test in 0.307s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 655a692eb436] (2026-10-29T23:33:14Z)
- `cd plugin/tests && python3 -m unittest test_site_build.Landing.test_the_tab_icon_url_changes_with_the_logo` → exit 0 · Ran 1 test in 0.239s / OK [ran] [tree 655a692eb436] (2026-10-29T23:33:14Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 23:20 UTC; claude plugin test mods/foreman-ui → [ran] [tree 655a692eb436] (2026-10-29T23:36:18Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_site_build.Landing.test_the_tab_icon_url_changes_with_the_logo` → exit 0 · Ran 1 test in 0.242s / OK [ran] [tree 655a692eb436] (2026-10-29T23:36:39Z)
- (audit intent) `built the site to a temp dir: every page's icon link carries ?v=<sha256[:8] of foreman.svg>; share.html stays out of the build; poster.jpg kept for pages.py:482; two builds still byte-identical; share.png reviewed by screenshot` → the tab icon now changes whenever the logo does, on the landing page and every feature page [tree 655a692eb436] (2026-10-29T23:36:39Z)
- (audit adversary) `built the site to a temp dir: every page's icon link carries ?v=<sha256[:8] of foreman.svg>; share.html stays out of the build; poster.jpg kept for pages.py:482; two builds still byte-identical; share.png reviewed by screenshot` → the hash comes from the committed SVG bytes only, so there is no user input and nothing new to inject [tree 655a692eb436] (2026-10-29T23:36:39Z)
- (audit edge) `built the site to a temp dir: every page's icon link carries ?v=<sha256[:8] of foreman.svg>; share.html stays out of the build; poster.jpg kept for pages.py:482; two builds still byte-identical; share.png reviewed by screenshot` → a logo edit gives a new URL; an unchanged logo keeps the URL, so builds stay byte-identical [tree 655a692eb436] (2026-10-29T23:36:39Z)
- (audit operator) `built the site to a temp dir: every page's icon link carries ?v=<sha256[:8] of foreman.svg>; share.html stays out of the build; poster.jpg kept for pages.py:482; two builds still byte-identical; share.png reviewed by screenshot` → no new step; build.py computes the hash [tree 655a692eb436] (2026-10-29T23:36:39Z)
- (audit maintainer) `built the site to a temp dir: every page's icon link carries ?v=<sha256[:8] of foreman.svg>; share.html stays out of the build; poster.jpg kept for pages.py:482; two builds still byte-identical; share.png reviewed by screenshot` → share.html carries its own rebuild command; one test ties the URL to the logo's bytes [tree 655a692eb436] (2026-10-29T23:36:39Z)
- (audit design) `built the site to a temp dir: every page's icon link carries ?v=<sha256[:8] of foreman.svg>; share.html stays out of the build; poster.jpg kept for pages.py:482; two builds still byte-identical; share.png reviewed by screenshot` → the share card uses the current mark on site tokens; the header logo is no longer pixelated [tree 655a692eb436] (2026-10-29T23:36:39Z)
## Log
- 2026-10-29T23:28:30Z created
- 2026-10-29T23:29:45Z scope: also the brand img's leftover image-rendering: pixelated (old pixel logo) and the og:image poster.jpg, an old screenshot with the old mascot; live site serves the new svg, browsers keep the old favicon by URL
- 2026-10-29T23:30:32Z set tier=M
- 2026-10-29T23:30:33Z planned: it has criteria and steps
- 2026-10-29T23:30:43Z focused
- 2026-10-29T23:31:11Z criterion 1 verify: `cd plugin/tests && python3 -m unittest test_site_build.Stories.test_the_tab_icon_url_changes_with_the_logo` → `cd plugin/tests && python3 -m unittest test_site_build.Landing.test_the_tab_icon_url_changes_with_the_logo`
- 2026-10-29T23:36:42Z done
- 2026-10-29T23:36:44Z committed 389961bc (7 files)
- 2026-10-29T23:36:50Z guard authorization added: publish
- 2026-10-29T23:39:01Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2041 [FEATURE M, done, 3 steps] Redesign the Foreman logo, modern, used across the site, README and plugin — lesson: A mark that brings its own tile background survive…
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- T-2052 [FEATURE L, done, 5 steps] Docs/README redesign: replace walls of text with scannable structure — hero with logo,… — lesson: Measure docs by what a reader sees: a…
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
- similar finished tasks took 3–6 steps
## Why not caught
screenshot reviews run in fresh headless profiles, which never hold a cached favicon; no test tied the icon URL to the logo's content
## Lessons
- a fresh headless profile never holds a cached favicon, so a brand change needs the icon URL tied to its content
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_site_build.py
- site/build.py
- site/style.css
- site/assets/share.png
- site/index.html
- site/share.html
- CHANGELOG.md
