---
id: T-2041
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/assets/foreman.svg, README.md, plugin/tests/test_docs.py, site/index.html, site/build.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-29T20:08:56Z
updated: 2026-10-29T20:41:46Z
base: c2d6f013659ed2e6d8441ed02d1b292712cae44d
base_tree: ff5addc5fffd893d1b078e7d76b6ad5a6605b018
plan0_at: 2026-10-29T20:25:24Z
plan0_scope: [site/assets/foreman.svg, README.md, plugin/tests/test_docs.py, site/index.html, site/build.py]
verified: strong
---
# Redesign the Foreman logo, modern, used across the site, README and plugin
## Raw request
> FEATURE: redesign the Foreman logo, modern, used across the site, README and plugin
## Interpretation
Replace the 16x16 pixel-robot mark (site/assets/foreman.svg) with a modern vector logo that reads at 16 px (favicon) through 256 px, on light and dark grounds, and show it at the top of the README. Same file name, so the site's favicon, header and footer pick it up with no path changes.
## Assumptions (confidence)
## Acceptance criteria
The logo is a valid SVG with a viewBox, title, no external refs and under 2 KB; the README shows it; test_docs passes.
- [x] the logo is a valid small SVG (viewBox, title, no external refs, < 2 KB) and the README shows it — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Complete version: the mark, crisp at 16/24/32 px, a tile edge that holds on a dark page, a <title>, no external refs, small; README header; a test pinning those properties. Options: (1) amber hard hat with a check on a navy tile — the name (a site boss) plus the product's core (verified work), keeps the amber/navy palette; (2) navy hat on an amber tile — loud, loses the check; (3) hexagon nut with a check — generic, reads as a security badge. Chose (1): previewed all three at 16-128 px in both themes; (1) keeps the check legible at 16 px. Captured: none, the others are dropped.
## Risks and rollback
## Execution prompt
## Steps
1. [x] draw the mark and preview it at 16-256 px in both themes
2. [x] test first: pin the logo's properties and the README image
3. [x] swap site/assets/foreman.svg and add the README header
## Resume here
<!-- auto -->
- 2026-10-29T20:39:35Z steps 3/3 done
- git: foreman/build; 3 uncommitted: README.md, plugin/tests/test_docs.py, site/assets/foreman.svg
- touched since last checkpoint: plugin/tests/test_docs.py, site/assets/foreman.svg, README.md
## Docs impact
README.md
## Verification evidence
- (step 1) `~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --no-sandbox --hide-scrollbars --window-size=900,520 --virtual-time-budget=2000 --screenshot=/tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/logo/prev3.png file:///tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/logo/preview.html` → exit 0 · [1029/152817.664853:WARNING:sandbox/policy/linux/sandbox_linux.cc:405] InitializeSandbox() called with multiple threads in process gpu-process. / 62872 bytes written to file /tmp/claude-1000/-home-cha [ran] [tree ba095ce5d1a7] (2026-10-29T20:28:17Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs.Logo` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Logo 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0de06d17fc1a] (2026-10-29T20:39:18Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs.Logo` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Logo 0s) / OK [ran] [tree 0de06d17fc1a] (2026-10-29T20:39:18Z)
- (step 3) `~/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --no-sandbox --hide-scrollbars --window-size=1200,360 --virtual-time-budget=2000 --screenshot=/tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/site-nav.png file://~/.claude/foreman/site/index.html` → exit 0 · [1029/153930.607031:WARNING:sandbox/policy/linux/sandbox_linux.cc:405] InitializeSandbox() called with multiple threads in process gpu-process. / 37114 bytes written to file /tmp/claude-1000/-home-cha [ran] [tree 0de06d17fc1a] (2026-10-29T20:39:30Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs` → exit 0 · Ran 76 tests in 7.9s (19 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 62d84e0f6704] (2026-10-29T20:41:02Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 76 tests in 8.3s (19 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 62d84e0f6704] (2026-10-29T20:41:22Z)
- (audit intent) `self-review: rendered a2/a3 side by side at 16/32/96 px, checked nav at 1200 px, test_docs Logo locks size, viewBox, title, no text/href` → one mark used as favicon, nav and README header; site already pointed at site/assets/foreman.svg so no page edits needed [tree 62d84e0f6704] (2026-10-29T20:41:22Z)
- (audit edge) `self-review: rendered a2/a3 side by side at 16/32/96 px, checked nav at 1200 px, test_docs Logo locks size, viewBox, title, no text/href` → 16 px favicon keeps the hat silhouette and check readable; navy tile carries its own background so it works on dark and light themes [tree 62d84e0f6704] (2026-10-29T20:41:22Z)
- (audit adversary) `self-review: rendered a2/a3 side by side at 16/32/96 px, checked nav at 1200 px, test_docs Logo locks size, viewBox, title, no text/href` → the SVG is inert (no script, href or external url), test fails if any appear; the ux cards in range were reviewed at their own closes [tree 62d84e0f6704] (2026-10-29T20:41:22Z)
- (audit design) `self-review: rendered a2/a3 side by side at 16/32/96 px, checked nav at 1200 px, test_docs Logo locks size, viewBox, title, no text/href` → two-colour gold-on-navy with a hairline highlight, matches the site's amber accent; all paths, no fonts [tree 62d84e0f6704] (2026-10-29T20:41:22Z)
## Log
- 2026-10-29T20:08:56Z created
- 2026-10-29T20:25:18Z set tier=M, scope=['site/assets/foreman.svg', 'README.md', 'plugin/tests/test_docs.py', 'site/index.html', 'site/build.py']
- 2026-10-29T20:25:23Z planned: it has criteria and steps
- 2026-10-29T20:25:23Z set approved=True
- 2026-10-29T20:25:24Z focused
- 2026-10-29T20:29:52Z paused: focus moved to T-2039
- 2026-10-29T20:38:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-29T20:38:44Z focused
- 2026-10-29T20:40:47Z set scope=['site/assets/foreman.svg', 'README.md', 'plugin/tests/test_docs.py', 'site/index.html', 'site/build.py', 'CHANGELOG.md']
- 2026-10-29T20:40:48Z scope: CHANGELOG.md for the logo line
- 2026-10-29T20:41:13Z scope: cards/ux/* in the diff range came from the T-2039/T-2042 merges, not this task
- 2026-10-29T20:41:45Z done
- 2026-10-29T20:41:46Z committed 87d933de (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1652-review: Verdict: changes needed.** Three MEDIUM findings: the worker write guard, release versioning, and the DTCG importer silently dropping tokens. I r…
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- research T-1220-review: Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did no…
- decision 2026-10-28: T-1803 step 3: the next-step hint does not name the top routed book
- the similar finished task took 3 steps
## Lessons
- A mark that brings its own tile background survives both GitHub themes without a picture element
## Files touched
- plugin/tests/test_docs.py
- site/assets/foreman.svg
- README.md
- CHANGELOG.md
- MASTER.md
- plugin/commands/looks.md
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmtaste.py
- plugin/lib/looks.html
- plugin/skills/directions/SKILL.md
- plugin/skills/library/cards/frontend/anchor-positioning.md
- plugin/skills/library/cards/frontend/animated-counters.md
- plugin/skills/library/cards/frontend/blend-modes.md
- plugin/skills/library/cards/frontend/clip-paths-and-masks.md
- plugin/skills/library/cards/frontend/css-3d-transforms.md
- plugin/skills/library/cards/frontend/custom-cursors.md
- plugin/skills/library/cards/frontend/easing-curves.md
- plugin/skills/library/cards/frontend/fluid-typography.md
- plugin/skills/library/cards/frontend/frosted-glass.md
- plugin/skills/library/cards/frontend/gesture-input.md
- plugin/skills/library/cards/frontend/gradient-design.md
- plugin/skills/library/cards/frontend/grain-and-noise.md
- plugin/skills/library/cards/frontend/haptic-feedback.md
- plugin/skills/library/cards/frontend/kinetic-typography.md
- plugin/skills/library/cards/frontend/micro-interactions.md
- plugin/skills/library/cards/frontend/oklch-color.md
- plugin/skills/library/cards/frontend/parallax-depth.md
- plugin/skills/library/cards/frontend/popover-api.md
- plugin/skills/library/cards/frontend/progress-indicators.md
