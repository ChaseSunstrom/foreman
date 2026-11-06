---
id: T-1610
type: FEATURE
tier: M
status: done
priority: normal
scope: [site, plugin/tests/test_site_hero.py, plugin/tests/helpers.py, plugin/tests/test_library.py, CHANGELOG.md, MASTER.md]
depends_on: [T-1609]
source: user
created: 2026-10-22T20:46:48Z
updated: 2026-10-22T22:52:46Z
base: d5354fc71644a9d8a9e530a7bcd9a4ec09304c0d
base_tree: bf1b9d8c28709fa5cf238b383423b4c980baf849
plan0_at: 2026-10-22T21:56:13Z
plan0_scope: [site, plugin/tests/test_site_hero.py, CHANGELOG.md]
verified: strong
---
# Site hero scene: a single-file WebGL2 proof-chain scene over the poster (tasks as stations, red to green as light along the track), from the ui/scene-3d.md template
## Raw request
> Site hero scene: a single-file WebGL2 proof-chain scene over the poster (tasks as stations, red to green as light along the track), from the ui/scene-3d.md template
## Interpretation
Over T-1609's SVG poster, the site hero gets a single-file WebGL2 scene of the proof chain: the four stations as lit forms along a track, a pulse of light travelling red to green, fed by the same stats.json totals. It is built from the ui/scene-3d.md template (templates/scene.html) and inlined by site/build.py. The poster stays the first paint and stays put when prefers-reduced-motion is set, when WebGL2 is missing, or when the script fails; the canvas carries an aria-label and is aria-hidden when the poster is shown.
## Assumptions (confidence)
## Acceptance criteria
- [x] the built index carries the scene inline over the T-1609 poster: aria-label, a prefers-reduced-motion path that keeps the poster still, a no-WebGL2 path that keeps the poster, no external script or host — verify with `python3 plugin/tests/run.py test_site_hero`
## Non-goals
## Approach (options → choice → why)
Options: three.js from a CDN (a third-party load the site forbids, T-1411); a CSS 3D transform scene (no lighting, weak depth); raw WebGL2 from the template, inlined. Choice: raw WebGL2 inlined by build.py: no outside host, one file, and the template already carries the survival contract (context loss, DPR cap, pause offscreen).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] scene from templates/scene.html fed by stats.json
3. [x] reduced motion and no-WebGL fallbacks
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_hero` → ✗ exit 1 · Ran 8 tests in 3.9s (2 classes, 16 at a time; slowest: Scene 3s, Hero 2s) / FAILED (1 classes) [ran] [tree 17c622436ee7] (2026-10-22T22:04:21Z)
- (ac 1) `python3 plugin/tests/run.py test_site_hero` → exit 0 · Ran 8 tests in 8.0s (2 classes, 16 at a time; slowest: Scene 8s, Hero 2s) / OK [ran] [tree 9e4ab9b5af31] (2026-10-22T22:08:11Z)
- (step 2) `python3 plugin/tests/run.py test_site_hero test_library` → exit 0 · Ran 49 tests in 7.4s (11 classes, 16 at a time; slowest: LibSources 7s, Scene 4s, LibraryAdmit 2s) / OK [ran] [tree deb5efda9385] (2026-10-22T22:18:54Z)
- (step 3) `python3 plugin/tests/test_site_hero.py -v Scene` → exit 0 · Ran 4 tests in 2.777s / OK [ran] [tree deb5efda9385] (2026-10-22T22:18:59Z)
- (step 3) `python3 plugin/tests/test_site_hero.py Scene` → ✗ exit 1 · Ran 8 tests in 21.722s / FAILED (failures=4) [ran] [tree 05b96da5129c] (2026-10-22T22:31:35Z)
- (step 3) `python3 plugin/tests/run.py test_site_hero test_library` → exit 0 · Ran 53 tests in 21.8s (11 classes, 16 at a time; slowest: Scene 21s, LibSources 7s, LibraryAdmit 2s) / OK [ran] [tree b41dccaeeeb0] (2026-10-22T22:34:23Z)
- (ac 1) `python3 plugin/tests/run.py test_site_hero` → exit 0 · Ran 13 tests in 24.3s (2 classes, 16 at a time; slowest: Scene 24s, Hero 4s) / OK [ran] [tree b2285366c07b] (2026-10-22T22:52:02Z)
- (ac 1) `python3 plugin/tests/run.py test_site_hero` → exit 0 · Ran 13 tests in 18.9s (2 classes, 16 at a time; slowest: Scene 19s, Hero 1s) / OK [ran] [tree b2285366c07b] (2026-10-22T22:52:22Z)
- (audit intent) `fm-reviewer full pass on the lane; medium (frame/context claims unproven) fixed with a real-time DevTools-pipe test proven able to fail; small fixes (at(-1), readPoster try/catch, fail() frees GPU, pulse lead, label wording, newest Playwright build) each with a test` → the built index carries the WebGL2 scene inline over the T-1609 poster; reduced motion and no-WebGL2 keep the poster still; no external host [tree b2285366c07b] (2026-10-22T22:52:22Z)
- (audit edge) `fm-reviewer full pass on the lane; medium (frame/context claims unproven) fixed with a real-time DevTools-pipe test proven able to fail; small fixes (at(-1), readPoster try/catch, fail() frees GPU, pulse lead, label wording, newest Playwright build) each with a test` → reduced motion asks for no context and draws no frames; the loop stops (same frame count at 8 s and 12 s); a throwing poster read ends in state failed with one log line; context loss handled [tree b2285366c07b] (2026-10-22T22:52:22Z)
- (audit maintainer) `fm-reviewer full pass on the lane; medium (frame/context claims unproven) fixed with a real-time DevTools-pipe test proven able to fail; small fixes (at(-1), readPoster try/catch, fail() frees GPU, pulse lead, label wording, newest Playwright build) each with a test` → a drift test holds six survival markers in both site/hero-scene.js and templates/scene.html [tree b2285366c07b] (2026-10-22T22:52:22Z)
## Log
- 2026-10-22T20:46:48Z created
- 2026-10-22T20:46:52Z set scope=['site', 'plugin/tests/test_site_hero.py', 'CHANGELOG.md'], depends_on=['T-1609']
- 2026-10-22T21:29:47Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_site_hero`
- 2026-10-22T21:30:11Z criterion 1 text: the built index carries the scene inline over the T-1609 poster: aria-label, a prefers-reduced-motion path that keeps the poster still, a no-WebGL2 path that keeps the poster, no external script or host — verify with python3 plugin/tests/run.py test_site_hero → the built index carries the scene inline over the T-1609 poster: aria-label, a prefers-reduced-motion path that keeps the poster still, a no-WebGL2 path that keeps the poster, no external script or host
- 2026-10-22T21:55:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1610.builder.md
- 2026-10-22T21:56:12Z focused
- 2026-10-22T22:03:42Z set scope=['site', 'plugin/tests/test_site_hero.py', 'plugin/tests/helpers.py', 'plugin/tests/test_library.py', 'CHANGELOG.md']
- 2026-10-22T22:32:52Z set scope=['site', 'plugin/tests/test_site_hero.py', 'plugin/tests/helpers.py', 'plugin/tests/test_library.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T22:50:44Z merged worktree-agent-a431cf49f1ee10260 (8 file(s))
- 2026-10-22T22:50:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a431cf49f1ee10260
- 2026-10-22T22:50:47Z focused
- 2026-10-22T22:52:46Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1513 [FEATURE L, dropped, 3 steps] Brainstorm T-1479 round 2 (cluster 18): the site's hero becomes a single-file WebGL or can
- T-1609 [FEATURE M, done, 3 steps] Site hero poster: build.py draws the proof chain from site/data/stats.json as an inline SVG poster, the hero's first paint and its fall…
- research T-1609-review: Verdict:** approve with nits. One finding should be fixed before merge (the silent missing-marker case).
- decision 2026-10-15: Pane order: Needs you and waiting plans above the hero (T-0909)
- the similar finished task took 3 steps
- start here (files T-1609 touched): plugin/tests/test_site_hero.py, site/build.py, site/index.html, site/style.css, MASTER.md, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_safety.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/tests/helpers.py, plugin/tests/test_library.py, plugin/tests/test_site_hero.py, site/build.py, site/hero-scene.js, site/index.html, site/style.css; re-ground the plan against them before editing
## Lessons
- Headless Chrome's virtual time barely runs requestAnimationFrame; prove frame claims in real time over --remote-debugging-pipe with an init-script spy
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_library.py
- plugin/tests/test_site_hero.py
- site/hero-scene.js
- site/build.py
- site/style.css
- CHANGELOG.md
- MASTER.md
