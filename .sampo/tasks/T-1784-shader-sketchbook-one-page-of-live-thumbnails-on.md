---
id: T-1784
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/library/cards/looks, plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_library.py, plugin/lib/fmcore.py, plugin/tests/test_scene_verify.py]
depends_on: []
source: followup
created: 2026-10-23T12:25:01Z
updated: 2026-10-29T20:22:10Z
base: bf08ca31a4d219a58ba4aa686ea30bdce9d1cc70
base_tree: d83a1c454cc1532796e0af668af7522fdb4c9911
plan0_at: 2026-10-23T18:00:09Z
plan0_scope: [plugin/skills/library/cards/looks, plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_library.py, plugin/tests/test_scene_verify.py, site/pages.py, site/build.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Shader sketchbook: one page of live thumbnails, one per shader card (looks/shader-*.md), e
## Raw request
> Shader sketchbook: one page of live thumbnails, one per shader card (looks/shader-*.md), each running its fragment shader with a ## Sketch preset of uniform values the card gains, a still frame under reduced motion and a text fallback without WebGL2 (from T-1650)
## Interpretation
Each of the eight shader look cards gains a ## Sketch line of preset uniform values; fm scene sketchbook writes one page with a live thumbnail per card (its fragment shader on a WebGL2 canvas, animated only while on screen), a still frame under reduced motion and the card's description when WebGL2 is missing or the shader fails; the site gets the same page.
## Assumptions (confidence)
## Acceptance criteria
- [x] every shader card's Sketch line sets each declared uniform but uRes and uTime with the right component count; the sketchbook page has a canvas, source and fallback per card and draws still under reduced motion — verify with `python3 plugin/tests/run.py test_scene_verify test_library`
## Non-goals
## Approach (options → choice → why)
Options: (a) screenshots of each shader (a browser and GPU at build time); (b) a page per card; (c) one page, the shader sources as non-executed script elements, one small module that compiles each with a full-screen-triangle vertex shader and draws while visible. Chosen (c): no build-time GPU, one page to compare looks, the cards stay the single source (presets live in each card's ## Sketch line, checked against its declared uniforms). A uniform with no clock (dither-fade's uProgress) takes sweep, a 0-1 ping-pong.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] Sketch lines on the cards
3. [x] sketchbook page and verb
4. [x] site page and docs
## Resume here
<!-- auto -->
- 2026-10-29T20:18:34Z steps 4/4 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/logo/a.svg, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/logo/b.svg, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/logo/c.svg, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/logo/preview.html
## Docs impact
CHANGELOG line from the lane; fm scene help names sketchbook
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene_verify test_library` → ✗ exit 1 · Ran 50 tests in 8.4s (12 classes, 16 at a time; slowest: LibSources 7s, Soak 4s, LibraryAdmit 2s) / FAILED (2 classes) [ran] [tree 89e6640cdf57] (2026-10-23T18:00:18Z)
- (step 1) `python3 plugin/tests/run.py test_scene_verify test_library` → exit 0 · Ran 50 tests in 7.5s (12 classes, 16 at a time; slowest: LibSources 7s, Soak 4s, LibraryAdmit 2s) / OK [ran] [tree 21493214c128] (2026-10-23T18:04:39Z)
- (step 2) `python3 plugin/tests/run.py test_scene_verify test_library` → exit 0 · Ran 50 tests in 7.5s (12 classes, 16 at a time; slowest: LibSources 7s, Soak 4s, LibraryAdmit 2s) / OK [ran] [tree 21493214c128] (2026-10-23T18:04:47Z)
- (step 3) `python3 plugin/tests/run.py test_scene_verify test_library` → exit 0 · Ran 50 tests in 7.4s (12 classes, 16 at a time; slowest: LibSources 7s, Soak 4s, LibraryAdmit 2s) / OK [ran] [tree 21493214c128] (2026-10-23T18:04:55Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_site_build test_cli test_suite_hygiene` → exit 0 · Ran 201 tests in 26.9s (58 classes, 16 at a time; slowest: TaskLifecycle 27s, AuditPrep 11s, StateViews 11s) / OK [ran] [tree 21493214c128] (2026-10-23T18:05:23Z)
- (ac 1) `python3 plugin/tests/run.py test_scene_verify test_library` → exit 0 · Ran 50 tests in 7.5s (12 classes, 16 at a time; slowest: LibSources 7s, Soak 4s, LibraryAdmit 2s) / OK [ran] [tree 21493214c128] (2026-10-23T18:05:31Z)
- (step 4) `python3 plugin/tests/run.py test_scene_verify test_library` → exit 0 · Ran 51 tests in 5.4s (12 classes, 16 at a time; slowest: LibSources 5s, Soak 4s, LibraryAdmit 2s) / OK [ran] [tree d74083a3bd16] (2026-10-29T20:14:11Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.1    31.5     150  [0] / SessionEnd                  25.5    27.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 151 tests across 4 files. [ [ran] [tree d74083a3bd16] (2026-10-29T20:17:47Z)
- (ac 1) `python3 plugin/tests/run.py test_scene_verify test_library` → exit 0 · Ran 52 tests in 5.7s (12 classes, 16 at a time; slowest: LibSources 5s, Soak 4s, LibraryAdmit 2s) / OK [ran] [tree a83fe5bd3d4a] (2026-10-29T20:21:33Z)
- (audit edge) `one fm-reviewer pass over the merged diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first` → bare --out crashed write_atomic (dirname ''); fixed at fmcore for every caller, tested from a temp cwd [tree a83fe5bd3d4a] (2026-10-29T20:21:33Z)
- (audit adversary) `one fm-reviewer pass over the merged diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first` → sketchbook now refuses foreign flags and a FILE like its siblings (exit 2) [tree a83fe5bd3d4a] (2026-10-29T20:21:33Z)
- (audit intent) `one fm-reviewer pass over the merged diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first` → fallback hides the canvas ([hidden] beats display:block); reduced motion draws the cards' own still [tree a83fe5bd3d4a] (2026-10-29T20:21:33Z)
- (audit operator) `one fm-reviewer pass over the merged diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first` → write failure prints one line, exit 1 [tree a83fe5bd3d4a] (2026-10-29T20:21:33Z)
- (audit maintainer) `one fm-reviewer pass over the merged diff (intent, adversary, edge, operator, maintainer); 4 findings fixed test-first` → one test pins all four fixes [tree a83fe5bd3d4a] (2026-10-29T20:21:33Z)
## Log
- 2026-10-23T12:25:01Z created
- 2026-10-23T17:59:43Z set type=FEATURE, tier=M, scope=['plugin/skills/library/cards/looks', 'plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_library.py', 'plugin/tests/test_scene_verify.py', 'site/pages.py', 'site/build.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:59:46Z lane: ~/.claude/foreman.lanes/T-1784 on foreman/T-1784
- 2026-10-23T18:00:09Z focused
- 2026-10-23T18:03:42Z set scope=['plugin/skills/library/cards/looks', 'plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_library.py', 'plugin/tests/test_scene_verify.py', 'plugin/tests/test_docs.py', 'site/pages.py', 'site/build.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T20:13:50Z merged foreman/T-1784 (16 file(s))
- 2026-10-29T20:13:55Z lane removed: ~/.claude/foreman.lanes/T-1784
- 2026-10-29T20:14:04Z focused
- 2026-10-29T20:21:11Z set scope=['plugin/skills/library/cards/looks', 'plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_library.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_scene_verify.py']
- 2026-10-29T20:21:11Z scope: fmcore.write_atomic bare-name fix covers every caller (review finding); test_scene_verify holds the sketchbook test
- 2026-10-29T20:22:08Z done
- 2026-10-29T20:22:10Z committed ee98a137 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook 3D on the web: a designed scene that never breaks the page (fm playbooks show ui/scene-3d)
- T-1499 [FEATURE M, done, 2 steps] Style shelf: shader looks, light and material recipes, an SVG icon system — lesson: Check a shader's promised neutral state by reading …
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/library/cards/looks/shader-aurora-bands.md, plugin/skills/library/cards/looks/shader-contour-lines.md, plugin/skills…; re-ground the plan against them before editing
## Lessons
- author CSS display:block silently beats the UA [hidden] rule: pair any [hidden] toggle with an explicit [hidden]{display:none}
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_scene_verify.py
- plugin/lib/fmcore.py
- plugin/lib/fmscene.py
- mods/foreman-ui/tests/fixtures/golden.ts
- mods/foreman-ui/tests/replay.test.tsx
- mods/foreman-ui/tools/pane_replay.py
- plugin/lib/fmcli.py
- plugin/skills/library/cards/looks/shader-aurora-bands.md
- plugin/skills/library/cards/looks/shader-contour-lines.md
- plugin/skills/library/cards/looks/shader-dither-fade.md
- plugin/skills/library/cards/looks/shader-grain-gradient.md
- plugin/skills/library/cards/looks/shader-halftone.md
- plugin/skills/library/cards/looks/shader-ink-diffusion.md
- plugin/skills/library/cards/looks/shader-paper-fibre.md
- plugin/skills/library/cards/looks/shader-soft-caustics.md
- plugin/tests/test_library.py
- plugin/tests/test_ui_replay.py
