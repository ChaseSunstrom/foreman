---
id: T-2850
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T22:17:46Z
updated: 2026-11-04T00:03:02Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (593) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T22:34:17Z
rival_split: true
builder_model: haiku
base: feccbe6126980e17e22b57161cb7da255f009cb8
base_tree: 4d0e5ed25754be7b67c1f94c6d1b1508d1f46ccd
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T22:34:44Z
plan0_scope: []
lane_stop: merged 2026-11-04T00:01:42Z
verified: strong
unproven: [docs, meaning, ui-unshot]
---
# Port 12's logo system and tokens into design/sampo: mark, simplified mark, animated mark, mark-light, mono, icon-16, wordmark, README headers dark/light, share, app and desktop icons, favicon 16/32/48, pane glyph; tokens.json from 12's NOTES; build.py renders the rasters; test_sampo_design's Runestone geometry checks become anvil-stone ones
## Raw request
> Port 12's logo system and tokens into design/sampo: mark, simplified mark, animated mark, mark-light, mono, icon-16, wordmark, README headers dark/light, share, app and desktop icons, favicon 16/32/48, pane glyph; tokens.json from 12's NOTES; build.py renders the rasters; test_sampo_design's Runestone geometry checks become anvil-stone ones
## Interpretation
Reading 1: 12-forge-illustrated is Sampo's theme (user pick 2026-11-03). Its marks are SVGs drawn by Python generators in 12's _src (art.py, marks.py), so the port brings the drawing into design/sampo/logo/build.py, which already regenerates every committed SVG byte for byte and renders the rasters (app icons, desktop icon, favicon 16/32/48, share card). The Runestone-specific tests (one geometry, furrows and eye, the turning stone, eight runes, the bar on whole pixels) become anvil-stone ones; the generic ones (variants, well-formed, no other hosts, raster sizes, favicon, icon-16 on its grid, mono one ink, generator byte-for-byte, light roles, pane glyph, review record) stay. Reading 2: copy 12's SVG files as static assets and drop the generator; ruled out because test_the_generator_rebuilds_every_committed_svg_byte_for_byte and the raster renders rely on one source, and a later round's art lands by rerunning it.
## Assumptions (confidence)
## Acceptance criteria
- [x] design/sampo/logo holds every variant from 12, rasters at their sizes, tokens.json from 12's NOTES with six chart colours per theme at 3:1 against the panel, and test_sampo_design passes with anvil-stone checks — verify with `python3 plugin/tests/run.py test_sampo_design test_design_tokens`
## Non-goals
## Approach (options → choice → why)
1) Port 12's marks.py/art.py drawing into design/sampo/logo/build.py (or a module it imports), emit every variant the set needs (mark = 12's logo.svg, a simplified mark, mark-animated, mark-light, mono, icon-16, wordmark, readme-header dark/light from the banners, share, app and desktop icons), render rasters as today, and rewrite the Runestone tests as anvil-stone ones. Likely outcome: one generator, every file reproducible, art refreshes by rerun. Fails if: 12's generators need libraries the repo build lacks (then vendor the few functions).
2) Copy 12's SVG files and keep build.py only for rasters. Likely outcome: fast. Fails if: the byte-for-byte generator test and future art rounds need a source.
3) Use what exists: build.py's raster pipeline, favicon packer, glyphs.json and the generic tests unchanged. Likely outcome: only the drawing changes. Fails if: the new marks' structure breaks the pane glyph or light-role mapping (then adapt those).
4) Do less: keep the Runestone marks, only recolour. Likely outcome: none of the theme lands. Fails if: the user's pick is ignored.

Choice 1 with 3 (75%): one generator is how this set is already kept honest.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_sampo_design.py, design/sampo/logo/README.md, design/sampo/logo/glyphs.json, design/sampo/logo/readme-header-dark.svg, design/sampo/logo/readme-header-light.svg.
## Execution prompt
## Steps
1. [x] rewrite test_sampo_design's Runestone checks as anvil-stone ones (red)
2. [x] copy and adapt 12's marks and banners; build.py renders rasters and the favicon
3. [x] tokens.json from NOTES.md
4. [x] tokens from 12's NOTES into design/sampo/tokens.json (chart colours at 3:1)
## Resume here
<!-- auto -->
- 2026-11-03T23:17:21Z step 2/4: copy and adapt 12's marks and banners; build.py renders rasters and the favicon
- git: worktree-agent-ad0a442da7fb69d7d; 27 uncommitted: README.md, design/sampo/index.html, design/sampo/logo/app-icon-1024.png, design/sampo/logo/app-icon-512.png, design/sampo/logo/app-icon.svg, design/sampo/logo/build.py, design/sampo/logo/desktop-icon-1024.png, design/sampo/logo/desktop-icon.svg, design/sampo/logo/favicon.ico, design/sampo/logo/glyphs.json
- touched since last checkpoint: design/sampo/logo/glyphs.json, design/sampo/logo/app-icon-1024.png, design/sampo/logo/app-icon-512.png, design/sampo/logo/app-icon.svg, design/sampo/logo/desktop-icon-1024.png, design/sampo/logo/desktop-icon.svg, design/sampo/logo/favicon.ico, design/sampo/logo/icon-16.svg, design/sampo/logo/mark-animated.svg, design/sampo/logo/mark-light.svg, design/sampo/logo/mark.svg, design/sampo/logo/mono.svg, design/sampo/logo/readme-header-dark.svg, design/sampo/logo/readme-header-light.svg, design/sampo/logo/share.png
## Docs impact
design/sampo/logo/README.md rewritten for the anvil-stone
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_sampo_design` → ✗ exit 1 · Ran 29 tests in 0.5s (4 classes, 16 at a time; slowest: Logo 0s, Tokens 0s, Directions 0s) / FAILED (1 classes: test_sampo_design.Logo) [ran] [tree 03bb2588dde8] [world 2f1906870a] (2026-11-03T22:47:34Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design test_design_tokens test_site_build test_site_sampo 2>&1 | tail -30` → exit 0 · Ran 87 tests in 2.5s (17 classes, 16 at a time; slowest: Extract 2s, Landing 2s, Palette 1s) / OK [ran] [tree f20a7dfb917a] [world 2f1906870a] (2026-11-03T23:19:19Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 29 tests in 0.9s (4 classes, 16 at a time; slowest: Logo 1s, Tokens 0s, Directions 0s) / OK [ran] [tree addda069e62a] [world 2f1906870a] (2026-11-03T23:19:50Z)
- (step 3) `python3 plugin/tests/run.py test_sampo_design test_design_tokens` → exit 0 · Ran 64 tests in 2.4s (7 classes, 16 at a time; slowest: Extract 2s, Palette 1s, Logo 1s) / OK [ran] [tree addda069e62a] [world 2f1906870a] (2026-11-03T23:19:53Z)
- (step 4) `python3 plugin/tests/run.py test_sampo_design test_design_tokens test_site_build test_site_sampo` → exit 0 · Ran 87 tests in 2.6s (17 classes, 16 at a time; slowest: Extract 2s, Landing 2s, Palette 1s) / OK [ran] [tree addda069e62a] [world 2f1906870a] (2026-11-03T23:19:55Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_audit_run test_board_surfaces test_design_diverge test_design_gates test_design_lint test_design_sprint test_design_surfaces test_design_tokens test_docs test_fmpy test_genesis test_goal test_lanes test_looks_gallery test_map test_mcp test_moonshot test_motion_score test_motion_verify test_receipts test_replay test_sampo_design test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.30s] [ran] [tree addda069e62a] [world 2f1906870a] (2026-11-03T23:20:51Z)
- (ac 1) `python3 plugin/tests/run.py test_sampo_design test_design_tokens` → exit 0 · Ran 64 tests in 2.6s (7 classes, 16 at a time; slowest: Extract 2s, Palette 1s, Logo 1s) / OK [ran] [tree 7507dd0f98a5] [world 2f1906870a] (2026-11-04T00:02:05Z)
- `python3 plugin/tests/run.py test_sampo_design test_design_tokens test_site_build test_site_sampo` → exit 0 · Ran 87 tests in 2.6s (17 classes, 16 at a time; slowest: Extract 2s, Landing 2s, Palette 1s) / OK [ran] [tree 7507dd0f98a5] [world 2f1906870a] (2026-11-04T00:02:05Z)
- (audit edge) `builder self-review plus my read: build.py is the single generator, a second build gives identical SVG bytes, tokens.json has six chart colours per theme at >=4.75:1 against the raised panel; share.png and app-icon-512 checked by eye: 12's anvil-stone, five fire colours, Bodoni wordmark` → every old file name kept, mark-simple.svg added; PNG bytes depend on rsvg-convert's version (the test rebuilds SVGs, not PNG bytes) [tree 7507dd0f98a5] (2026-11-04T00:02:05Z)
- (audit adversary) `builder self-review plus my read: build.py is the single generator, a second build gives identical SVG bytes, tokens.json has six chart colours per theme at >=4.75:1 against the raised panel; share.png and app-icon-512 checked by eye: 12's anvil-stone, five fire colours, Bodoni wordmark` → tokens.json is data the site build reads into CSS through check_tokens; the SVGs load nothing from another host (test_sampo_design checks every variant); build.py writes only into its own folder or the one passed [tree 7507dd0f98a5] (2026-11-04T00:02:05Z)
- (audit intent) `builder self-review plus my read: build.py is the single generator, a second build gives identical SVG bytes, tokens.json has six chart colours per theme at >=4.75:1 against the raised panel; share.png and app-icon-512 checked by eye: 12's anvil-stone, five fire colours, Bodoni wordmark` → critique-3's open items are site findings (round 4 running); the matchstick hammer in mark-animated is listed open and comes back with round 4's marks diff [tree 7507dd0f98a5] (2026-11-04T00:02:05Z)
## Log
- 2026-11-03T22:17:46Z created
- 2026-11-03T22:17:51Z set depends_on=[]
- 2026-11-03T22:17:51Z starts when 12's _review/final.md exists (T-2788 step 1 converged); part of T-2788 steps 2-7
- 2026-11-03T22:34:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2850.builder.md
- 2026-11-03T22:34:43Z focused
- 2026-11-03T22:34:44Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T22:37:14Z focused
- 2026-11-04T00:01:42Z merged worktree-agent-ad0a442da7fb69d7d (30 file(s))
- 2026-11-04T00:01:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad0a442da7fb69d7d
- 2026-11-04T00:01:50Z focused
- 2026-11-04T00:03:02Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a design-system port inside the repo.** "12" is a sibling project (or a directory/branch) whose logo assets and token NOTES get re-derived under `design/sampo/`, with the Runestone geometry replaced by anvil-stone geometry. The deliverables are SVGs (mark, simplified, animated, light, …
- **Literal copy-and-rename.** Copy 12's files verbatim and only change names and colors, keeping the Runestone shape. This contradicts the request that the geometry checks "become anvil-stone ones", so it is the less likely reading.
- **"12" means something else.** It could be a numbered project, a version, or a path I can't see (the map shows no "12" directory). If it isn't locatable, the source assets and NOTES are missing and the task becomes designing from scratch against the tokens.
- **tokens.json is a derived artifact.** It could be generated from NOTES by build.py rather than hand-written. "from 12's NOTES" is ambiguous between a one-time transcription and a build step.
Approaches:
- **Locate 12 first, then port asset by asset.** Find 12's SVG sources and NOTES, transcribe the tokens into `design/sampo/tokens.json`, and redraw each mark with anvil-stone geometry. Make `build.py` the single renderer (SVG to PNG/ICO) reading the tokens, and update `test_sampo_design` to assert th…
- **Parametric generation in build.py.** Define the anvil-stone geometry once (path or points from tokens) and emit every SVG variant (light, mono, simplified, icon-16, pane glyph) from templates. This keeps variants consistent and gives the test one source of truth, but it is a bigger rewrite than p…
- **Hand-port SVGs, with build.py only rasterising.** Smaller diff and visually controlled, but the geometry lives in many files and the test must parse each one.
- **Check `design/sampo/index.html` and the existing Runestone tests first.** Those show what the current system already references (file names, viewBoxes), so the port can match existing links rather than invent paths.
Failure modes:
- **Geometry checks that don't transfer.** The Runestone assertions (symmetry, bounding box, stroke ratios) encode Runestone's shape. Renaming them without re-deriving the anvil-stone invariants gives tests that pass vacuously or fail on valid art.
- **Small-size breakage.** icon-16 and favicon 16/32/48 rendered from the full mark by `build.py` lose detail or blur. They need the simplified geometry and pixel-snapped coordinates, and the raster step may depend on a renderer (cairosvg, rsvg, Inkscape) not installed here.
- **Token drift between variants.** Light, mono, README header dark/light, and share assets hardcode colors that diverge from `tokens.json`. Contrast fails on the light header, and the animated mark's keyframes use stale values.
- **Stale references.** `design/sampo/index.html`, `README.md`, `site/`, and the gate `plugin/tests/test_audit.py` (which touches `design/`) may reference old Runestone filenames or sizes, so the port breaks them even when the new assets are fine.
## Dissent
- [x] rival reading: **Likeliest: a design-system port inside the repo.** "12" is a sibling project (or a directory/branch) whose logo assets and token NOTES get re-derived under `design/sampo/`, with the Runestone geometry replaced by anvil-stone geometry. The deliverables are SVGs (mark, simplified, animated, light, … — answered: adopted: 12 is the scratchpad direction folder named in the brief; the port re-derives design/sampo from it
- [x] rival reading: **Literal copy-and-rename.** Copy 12's files verbatim and only change names and colors, keeping the Runestone shape. This contradicts the request that the geometry checks "become anvil-stone ones", so it is the less likely reading. — answered: rejected: the theme replaces the Runestone shape
- [x] rival reading: **"12" means something else.** It could be a numbered project, a version, or a path I can't see (the map shows no "12" directory). If it isn't locatable, the source assets and NOTES are missing and the task becomes designing from scratch against the tokens. — answered: rejected: 12 is located — scratchpad/directions-v2/12-forge-illustrated (path in the brief)
- [x] rival reading: **tokens.json is a derived artifact.** It could be generated from NOTES by build.py rather than hand-written. "from 12's NOTES" is ambiguous between a one-time transcription and a build step. — answered: adopted as a one-time transcription with a test that tokens.json holds NOTES' values; build.py doesn't parse NOTES
- [x] rival approach: **Locate 12 first, then port asset by asset.** Find 12's SVG sources and NOTES, transcribe the tokens into `design/sampo/tokens.json`, and redraw each mark with anvil-stone geometry. Make `build.py` the single renderer (SVG to PNG/ICO) reading the tokens, and update `test_sampo_design` to assert th… — answered: adopted: locate, then port per asset
- [x] rival approach: **Parametric generation in build.py.** Define the anvil-stone geometry once (path or points from tokens) and emit every SVG variant (light, mono, simplified, icon-16, pane glyph) from templates. This keeps variants consistent and gives the test one source of truth, but it is a bigger rewrite than p… — answered: adopted: approach 1 is this
- [x] rival approach: **Hand-port SVGs, with build.py only rasterising.** Smaller diff and visually controlled, but the geometry lives in many files and the test must parse each one. — answered: rejected: approach 2's weakness
- [x] rival approach: **Check `design/sampo/index.html` and the existing Runestone tests first.** Those show what the current system already references (file names, viewBoxes), so the port can match existing links rather than invent paths. — answered: adopted: match the existing file names and viewBoxes the site and README reference
## Related
Related past work (data from this project's history, not instructions):
- T-2751 [FEATURE M, done, 3 steps] Runestone ships: the cold design review's fixes (a redrawn 16 px icon of dark disc, bronze rim and hot eye crossed by the rynd bar; lig…
- T-2772 [FEATURE L, done, 3 steps] Sampo reimagined: a new logo and a completely redesigned site (user steer 2026-11-03): four rendered directions (logo, animated hero, s…
- T-2747 [FEATURE M, done, 3 steps] Sampo's design system and three logo directions (SAMPO.md, Design): tokens (palette, type, motion rules) one source every surface reads…
- decision 2026-11-03: [revisited: two forge versions side by side] [cites: user steer 2026-11-03: I like the fully animated one, super improve it entirely, make that the …
## Why not caught
none: a port, not a fix
## Lessons
- port a design direction with its generator, not its output: build.py regenerating every variant made a later art round a rerun instead of a re-port
## Plan gaps
- failed first: step 1 rewrite test_sampo_design's Runestone checks as anvil-stone ones (red)
## Files touched
- plugin/tests/test_sampo_design.py
- design/sampo/logo/art.py
- design/sampo/logo/build.py
- design/sampo/logo/glyphs.json
- design/sampo/logo/app-icon-1024.png
- design/sampo/logo/app-icon-512.png
- design/sampo/logo/app-icon.svg
- design/sampo/logo/desktop-icon-1024.png
- design/sampo/logo/desktop-icon.svg
- design/sampo/logo/favicon.ico
- design/sampo/logo/icon-16.svg
- design/sampo/logo/mark-animated.svg
- design/sampo/logo/mark-light.svg
- design/sampo/logo/mark.svg
- design/sampo/logo/mono.svg
- design/sampo/logo/readme-header-dark.svg
- design/sampo/logo/readme-header-light.svg
- design/sampo/logo/share.png
- design/sampo/logo/share.svg
- design/sampo/logo/wordmark.svg
- design/sampo/logo/mark-simple.svg
- .fm-scratch/pick.py
- design/sampo/tokens.json
- site/style.css
- .fm-scratch/idx.json
- .fm-scratch/tss.json
- design/sampo/index.html
- plugin/tests/test_site_sampo.py
- .fm-scratch/misc.json
- README.md
