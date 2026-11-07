---
id: T-2062
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T23:29:52Z
updated: 2026-10-30T00:16:34Z
base: 03b7feea5759378b99eed42c845a93e36c8a944c
base_tree: ea162eb7316cd9fc24b3b6a1bb893ec4b116f1d0
plan0_at: 2026-10-29T23:45:44Z
plan0_scope: []
group: site pages, shaders and motion
verified: strong
---
# Site shows the shader cards live: each shader-* card's fragment shader running in a…
## Raw request
> FEATURE: site shows the shader cards live: each shader-* card's fragment shader running in a WebGL canvas, with a still fallback
## Interpretation
The landing page shows no shader: the eight live shader looks only appear on features/shaders.html. The user said 'the shaders aren't visualized'; the landing should show them running.
## Assumptions (confidence)
## Acceptance criteria
- [x] The built landing runs four shader cards live, each a canvas with its card's shader source and a still fallback, and links to the shaders page — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
Options: (a) a section on the landing with four live tiles from fmscene.sketchbook_html, filled by build.py at a marker, linking to the full page; (b) one shader as the hero backdrop (hurts text contrast, one look stands for all); (c) a live shader header on every feature card (eight-plus WebGL contexts on one screen). Choice: (a): it reuses the sketchbook's tested runtime (draws only on screen, one still frame under reduced motion, the card's words without WebGL2), one marker and one replace in build.py. (b)/(c) go to T-2063's review if the strip reads well.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: the built landing has 4 figure.sketch tiles with sources and a link to features/shaders.html
2. [x] index.html section + build.py fills the mark from fmscene.sketch_cards()
3. [x] screenshot the landing (swiftshader) light and dark; read them
## Resume here
<!-- auto -->
- 2026-10-29T23:48:10Z step 2/3: index.html section + build.py fills the mark from fmscene.sketch_cards()
- git: foreman/build; 3 uncommitted: plugin/tests/test_site_build.py, site/build.py, site/index.html
- touched since last checkpoint: plugin/tests/test_site_build.py, site/index.html, site/build.py
- failures met: modulenotfounderror: no module named 'pil'
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_landing_runs_shader_cards_live` → red as expected (exit 1) · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Landing 1s) / FAILED (1 classes) [ran] [tree 1ef205d89af8] (2026-10-29T23:46:05Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build test_site_hero` → exit 0 · Ran 20 tests in 2.4s (7 classes, 16 at a time; slowest: Landing 2s, Proof 1s, Reproducible 1s) / OK [ran] [tree 7ecc8dbd636e] (2026-10-29T23:56:22Z)
- (step 3) `sh /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/shoot_looks.sh` → exit 0 · 4 shots, each over 100 KB [ran] [tree 7ecc8dbd636e] (2026-10-29T23:56:46Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_landing_runs_shader_cards_live` → ✗ exit 1 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: Landing 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7ecc8dbd636e] (2026-10-29T23:56:59Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build.Landing.test_the_landing_runs_shader_cards_live` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Landing 1s) / OK [ran] [tree 7ecc8dbd636e] (2026-10-29T23:56:59Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (48 pass, 6 warn, 0 fail) (slower: 18.5 s vs a usual 12.2 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 23:55 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 23 [ran] [tree 7ecc8dbd636e] (2026-10-30T00:02:38Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_site_build` → exit 0 · Ran 11 tests in 2.5s (5 classes, 16 at a time; slowest: Landing 2s, Reproducible 1s, TitleCard 1s) / OK [ran] [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
- (audit intent) `self-review of build.py mark fill, index.html section, test and four screenshots (light/dark, 390/1280)` → the landing now shows four shader cards running live, linking to all eight [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
- (audit adversary) `self-review of build.py mark fill, index.html section, test and four screenshots (light/dark, 390/1280)` → the GLSL is the repo's own cards; fmscene leaves out any card whose source holds </script [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
- (audit edge) `self-review of build.py mark fill, index.html section, test and four screenshots (light/dark, 390/1280)` → no WebGL2 shows each card's words; reduced motion draws one still frame; a renamed card or lost mark fails the build loudly; a dropped </script card trips the test's 4-tile count [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
- (audit operator) `self-review of build.py mark fill, index.html section, test and four screenshots (light/dark, 390/1280)` → build errors name the lost mark or missing card [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
- (audit maintainer) `self-review of build.py mark fill, index.html section, test and four screenshots (light/dark, 390/1280)` → one mark, one replace, reuses fmscene.sketchbook_html [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
- (audit design) `self-review of build.py mark fill, index.html section, test and four screenshots (light/dark, 390/1280)` → four screenshots read, tiles fill the grid at 390 and 1280 in both themes [tree 7ecc8dbd636e] (2026-10-30T00:11:07Z)
## Log
- 2026-10-29T23:29:52Z created
- 2026-10-29T23:43:01Z planned: it has criteria and steps
- 2026-10-29T23:45:43Z focused
- 2026-10-29T23:48:10Z paused: focus moved to T-2064
- 2026-10-29T23:56:13Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-29T23:56:13Z focused
- 2026-10-30T00:02:51Z paused: focus moved to T-2064
- 2026-10-30T00:10:51Z focused
- 2026-10-30T00:10:56Z scope: site/pages.py docstring SyntaxWarning fix sits in the site build path; build.py and pages.py edits were swept into T-2064's commit 7e4fccfa (edited while T-2064 was focused), so this commit carries index.html, the test and CHANGELOG
- 2026-10-30T00:11:13Z done
- 2026-10-30T00:11:15Z committed 6057976f (3 files)
- 2026-10-30T00:11:53Z guard authorization added: publish
- 2026-10-30T00:16:34Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1784 [FEATURE M, done, 4 steps] Shader sketchbook: one page of live thumbnails, one per shader card (looks/shader-*.md), e — lesson: author CSS display:block silently …
- research T-1784-review: Verdict: changes needed.** The default `fm scene sketchbook` crashes, and the fallback does not hide the canvas. Both are one-line fixes. I read …
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- the similar finished task took 4 steps
## Lessons
- Headless shots of one section: cut it into its own page; scrolling from JS gives blank or stale frames. And finish a task before editing for the next, or its close sweeps the edits into its commit.
## Files touched
- plugin/tests/test_site_build.py
- site/index.html
- site/build.py
- CHANGELOG.md
