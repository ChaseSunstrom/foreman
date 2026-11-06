---
id: T-2957
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T11:50:14Z
updated: 2026-11-04T12:35:36Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (621) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T11:50:50Z
rival_split: true
builder_model: haiku
base: d93ac9f8053e2246e0b4efb45e4c8be1c01e262e
base_tree: 4a1a13e91619258f1a144c9807cb2a169310358e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T11:51:38Z
plan0_scope: []
lane_stop: merged 2026-11-04T12:29:17Z
verified: strong
unproven: [ui-unshot]
---
# Re-sync site/ to the converged illustrated forge (critique 7 converged: landing round 7, tower round 4): the redrawn eight stations as one night road with station lamps, the critique 5-6 fixes, into site/index.html, forge.css, forge.js and site/genesis (index.html, genesis.css, genesis.js), with shots at 1440, 768 and 390 in both themes
## Raw request
> Re-sync site/ to the converged illustrated forge (critique 7 converged: landing round 7, tower round 4): the redrawn eight stations as one night road with station lamps, the critique 5-6 fixes, into site/index.html, forge.css, forge.js and site/genesis (index.html, genesis.css, genesis.js), with shots at 1440, 768 and 390 in both themes
## Interpretation
Reading 1 (chosen): the site shows exactly the design critique 7 converged on: 12's landing (round 7) and tower (round 4), in site/'s split files, with the build's data paths. Reading 2 (ruled out): redesign further; the critique converged with only Lows, so this is a port, not a design round.
## Assumptions (confidence)
## Acceptance criteria
- [x] site/index.html's How section is 12's one-camera night road with each station lit by its own lamp, the station shown matching the row read, as in /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/index.html — verify with `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections`
- [x] site/genesis matches /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/tower (index.html, genesis.css, genesis.js) apart from data paths, and the tower reads genesis.json as before — verify with `python3 plugin/tests/run.py test_site_sections test_genesis`
- [x] design lint is clean on site/ (12's art timing allowed inline) and no page overflows at 320 to 1440 — verify with `python3 plugin/tests/run.py test_site_sampo test_site_build`
## Non-goals
## Approach (options → choice → why)
1) Delta port: diff 12's page (/tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/index.html, its inline style and script) and tower (/tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/tower/) against site/index.html, forge.css, forge.js and site/genesis, and port each change into the file that already holds that part (T-2851's split). Likely outcome: site/ matches the converged design, tests and lint stay green. Fails if: a delta crosses the split (markup that the forge.js now builds), which the builder reads before porting.
2) use what exists: rerun T-2851's port.py. Likely outcome: one command. Fails if: its port_css.py helper was lost with its lane, so it can't run.
3) do less: port only the How section (the user's item) and leave the Lows. Likely outcome: the visible fix lands fastest. Fails if: the tower's round-4 fixes and the landing's other round 5-7 fixes stay off the site.
Choice 1 (75%): the only route that lands everything the critique converged on.
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, site/build.py, plugin/tests/test_site_build.py, site/style.css, plugin/tests/test_docs.py; past FIXes T-2060.
## Execution prompt
## Steps
1. [x] diff 12's round-7 page and round-4 tower against site/ and list the deltas
2. [x] port the deltas: markup into index.html, styles into forge.css, script into forge.js; the tower files into site/genesis
3. [x] tests, design lint, shots at 1440/768/390 in both themes
## Resume here
<!-- auto -->
- 2026-11-04T12:24:08Z steps 3/3 done
- git: worktree-agent-a2f3fe1b2101c4c53; 1 uncommitted: site/forge.css
- touched since last checkpoint: .fm-scratch/port_js.py, site/genesis/genesis.js, .fm-scratch/shots.py, .fm-scratch/how.py, site/genesis/genesis.css, site/forge.css, .fm-scratch/cs.py
## Docs impact
CHANGELOG line (T-2957)
## Verification evidence
- (ac 3) `python3 plugin/tests/run.py test_site_sampo test_site_build 2>&1 | tail -30` → exit 0 · Ran 23 tests in 4.9s (10 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, Built 1s) / OK [ran] [tree 06692044ba40] [world 2f1906870a] (2026-11-04T12:07:58Z)
- (step 1) `python3 plugin/tests/run.py test_site_sampo test_site_build 2>&1 | tail -30` → exit 0 · Ran 23 tests in 4.9s (10 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, Built 1s) / OK [ran] [tree 06692044ba40] [world 2f1906870a] (2026-11-04T12:07:58Z)
- (step 2) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_site_sampo test_site_build test_genesis test_design 2>&1 | tail -30` → exit 0 · Ran 413 tests in 32.0s (75 classes, 16 at a time; slowest: GenerationReview 25s, GenesisRead 24s, ProofBeforePresentation 21s) / OK [ran] [tree 2d7239aa71fa] [world 2f1906870a] (2026-11-04T12:08:34Z)
- (step 3) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build 2>&1 | tail -15` → exit 0 · Ran 292 tests in 24.4s (50 classes, 16 at a time; slowest: GenerationReview 21s, GenesisRead 20s, GenesisSweep 18s) / OK [ran] [tree a249f03335c1] [world 2f1906870a] (2026-11-04T12:12:11Z)
- (step 1) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections` → exit 0 · Ran 76 tests in 14.0s (27 classes, 16 at a time; slowest: Built 13s, Landing 8s, Header 6s) / OK [ran] [tree a249f03335c1] [world 2f1906870a] (2026-11-04T12:12:52Z)
- (step 2) `python3 plugin/tests/run.py test_site_sections test_genesis` → exit 0 · Ran 237 tests in 33.3s (27 classes, 16 at a time; slowest: GenesisRead 30s, GenerationReview 29s, ProofBeforePresentation 26s) / OK [ran] [tree a249f03335c1] [world 2f1906870a] (2026-11-04T12:13:26Z)
- (step 3) `python3 plugin/tests/run.py test_site_sampo test_site_build` → exit 0 · Ran 23 tests in 3.8s (10 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, TitleCard 1s) / OK [ran] [tree a249f03335c1] [world 2f1906870a] (2026-11-04T12:15:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_audit_run test_design_diverge test_design_gates test_design_lint test_design_sprint test_design_surfaces test_design_tokens test_docs test_fmpy test_genesis test_goal test_lanes test_looks_gallery test_map test_moons_scale test_moonshot test_motion_score test_motion_verify test_receipts test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger` → ✗ exit 1 · Ran 1080 tests in 110.7s (200 classes, 16 at a time; slowest: Ship 110s, Lanes 94s, LaneRecovery 54s) / FAILED (1 classes: test_design_lint.Site) [ran] [tree a249f03335c1] [world 2f1906870a] (2026-11-04T12:17:20Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_audit_run test_design_diverge test_design_gates test_design_lint test_design_sprint test_design_surfaces test_design_tokens test_docs test_fmpy test_genesis test_goal test_lanes test_looks_gallery test_map test_moons_scale test_moonshot test_motion_score test_motion_verify test_receipts test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger` → exit 0 · Ran 1080 tests in 47.2s (200 classes, 16 at a time; slowest: Ship 47s, Lanes 40s, LaneRecovery 30s) / OK [ran] [tree 0bb10d270f8b] [world 2f1906870a] (2026-11-04T12:19:36Z)
- (step 1) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 292 tests in 35.4s (50 classes, 16 at a time; slowest: GenesisRead 31s, GenerationReview 30s, GenesisCheck 25s) / OK [ran] [tree 713641e9c900] [world 2f1906870a] (2026-11-04T12:30:03Z)
- (step 2) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 292 tests in 32.2s (50 classes, 16 at a time; slowest: GenerationReview 27s, GenesisRead 27s, GenesisCheck 24s) / OK [ran] [tree 713641e9c900] [world 2f1906870a] (2026-11-04T12:30:51Z)
- (step 3) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 292 tests in 33.6s (50 classes, 16 at a time; slowest: GenerationReview 29s, GenesisRead 28s, GenesisCheck 24s) / OK [ran] [tree 713641e9c900] [world 2f1906870a] (2026-11-04T12:31:40Z)
- (ac 1) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections` → exit 0 · Ran 76 tests in 14.0s (27 classes, 16 at a time; slowest: Built 14s, Landing 7s, Header 6s) / OK [ran] [tree ee6600f51297] [world 2f1906870a] (2026-11-04T12:32:55Z)
- (ac 2) `python3 plugin/tests/run.py test_site_sections test_genesis` → exit 0 · Ran 237 tests in 30.9s (27 classes, 16 at a time; slowest: GenesisRead 27s, GenerationReview 27s, ProofBeforePresentation 23s) / OK [ran] [tree ee6600f51297] [world 2f1906870a] (2026-11-04T12:32:55Z)
- (ac 3) `python3 plugin/tests/run.py test_site_sampo test_site_build` → exit 0 · Ran 23 tests in 4.0s (10 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, TitleCard 2s) / OK [ran] [tree ee6600f51297] [world 2f1906870a] (2026-11-04T12:32:55Z)
- (audit intent) `critique 7's converged pages were the spec; I looked at the re-sync's landing-dark-1440 (found a tan box behind the hero's italic line, sent back, fixed: style.css's generic .hero h1 em highlight) and how-dark-1440 (the lamp-lit mine station matching row I)` → site/ shows the design critique 7 converged on: the night road How section and the tower's round 3-4 changes, in site/'s split files with build.py's data blocks kept [tree ee6600f51297] (2026-11-04T12:32:55Z)
- (audit adversary) `critique 7's converged pages were the spec; I looked at the re-sync's landing-dark-1440 (found a tan box behind the hero's italic line, sent back, fixed: style.css's generic .hero h1 em highlight) and how-dark-1440 (the lamp-lit mine station matching row I)` → the one new innerHTML (the docs column, genesis.js:484) builds from doc names through esc() for the heading, the data-doc attribute, the title and the label, and a line count; no doc body or other data text reaches markup; tokens.json changed only by deduping the art group, no new values [tree ee6600f51297] (2026-11-04T12:32:55Z)
- (audit edge) `critique 7's converged pages were the spec; I looked at the re-sync's landing-dark-1440 (found a tan box behind the hero's italic line, sent back, fixed: style.css's generic .hero h1 em highlight) and how-dark-1440 (the lamp-lit mine station matching row I)` → no overflow and no page errors at 320, 390, 768 and 1440 in both themes on the landing and the tower; shots wait 6.5 s so the headline's heat animation has settled [tree ee6600f51297] (2026-11-04T12:32:55Z)
- (audit maintainer) `critique 7's converged pages were the spec; I looked at the re-sync's landing-dark-1440 (found a tan box behind the hero's italic line, sent back, fixed: style.css's generic .hero h1 em highlight) and how-dark-1440 (the lamp-lit mine station matching row I)` → style.css's .hero h1 em highlight bleeds into any hero em; forge.css now resets it for the forge hero, and a test asserting the em has no background would catch the class [tree ee6600f51297] (2026-11-04T12:32:55Z)
## Log
- 2026-11-04T11:50:14Z created
- 2026-11-04T11:50:14Z set depends_on=[]
- 2026-11-04T11:50:29Z criterion 1 verify: `python3 plugin/tests/run.py test_site test_site_sections` → `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections`
- 2026-11-04T11:50:29Z criterion 2 verify: `python3 plugin/tests/run.py test_site_sections test_genesis_site` → `python3 plugin/tests/run.py test_site_sections test_genesis`
- 2026-11-04T11:50:30Z criterion 3 verify: `sampo design lint site/forge.css site/genesis/genesis.css` → `python3 plugin/tests/run.py test_site_sampo test_site_build`
- 2026-11-04T11:50:33Z set approved=True
- 2026-11-04T11:50:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2957.builder.md
- 2026-11-04T11:51:37Z focused
- 2026-11-04T11:51:38Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T12:29:17Z merged worktree-agent-a2f3fe1b2101c4c53 (7 file(s))
- 2026-11-04T12:29:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2f3fe1b2101c4c53
- 2026-11-04T12:29:26Z focused
- 2026-11-04T12:31:49Z scope: site/index.html, forge.css, forge.js, site/genesis (genesis.css, genesis.js), design/sampo/tokens.json (the art group deduped), and the site tests; shots in the scratchpad's _review/site-sync
- 2026-11-04T12:35:35Z done
- 2026-11-04T12:35:36Z committed f4a124df (1 file)
## Follow-ups captured
## Scope
site/index.html, site/forge.css, site/forge.js, site/style.css, site/assets/**, site/genesis/index.html, site/genesis/genesis.css, site/genesis/genesis.js, site/build.py, site/pages.py, plugin/tests/test_site*.py, plugin/tests/test_genesis.py
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Port converged design into the shipped site (likeliest).** The converged illustrated forge (landing round 7, tower round 4) lives somewhere in `design/` (probably a `design/` forge/tower directory). The request is to copy or adapt it into `site/index.html`, `site/forge.css`, `site/forge.js` and `…
- **Regenerate rather than hand-copy.** The site files may be built output (e.g. from `plugin/lib/fmgenesis.py` or a `design/` build step). "Re-sync" would then mean rerunning the generator, not editing the HTML, CSS and JS by hand.
- **Genesis tower is a separate surface.** "Tower round 4" may apply only to `site/genesis/`, with "landing round 7" applying only to `site/index.html`. Each would then be synced from a different source, with the critique 5-6 fixes split between them.
- **Shots are a deliverable stored in the repo.** The 6 screenshots (3 widths × 2 themes) may need to be committed under `site/` (or `design/`), perhaps per page, which would make 12. Alternatively they are only a verification artifact.
Approaches:
- **Diff, then port by hand.** Find the converged design sources under `design/`, diff them against `site/index.html`, `forge.css` and `forge.js`, and apply the station-road and lamp markup, CSS and JS changes. Keep site-specific paths and links intact. Do the same for `site/genesis/`.
- **Use an existing sync script or generator.** Search `plugin/lib/fmgenesis.py`, `plugin/bin/` and `design/` for a build or sync step that emits `site/`. If one exists, update its inputs and run it so the site output isn't hand-edited and drifting.
- **Shoot with headless Chromium via a script.** Serve `site/` locally and use Playwright or similar to capture each page at 1440, 768 and 390 in both themes. The theme comes from the `prefers-color-scheme` emulation or a `data-theme` toggle, whichever `forge.js` actually uses. Keep the script outsid…
- **Port in layers.** Land the CSS tokens and theme variables first, then the station markup, then the JS (lamp activation, scroll-linked road). Shoot after each layer to catch regressions early.
Failure modes:
- **Theme mechanism mismatch.** The design source might use a `data-theme` attribute while `site/forge.js` uses `prefers-color-scheme` or a stored toggle. The "both themes" shots could then both render the same theme, or the night road might not recolor in light mode.
- **Genesis and landing share class names or tokens.** `forge.css` and `genesis.css` could collide, or the genesis page might load `forge.css` through a relative path. Changing the shared station and lamp styles would then silently restyle `site/genesis/`.
- **Responsive road breaks at 390 and 768.** A single night road with lamps is probably laid out as an SVG or absolute-positioned layer sized for 1440. The lamps then drift off the stations when the layout reflows.
- **Critique 5-6 fixes get lost in the overwrite.** If `site/` has had fixes applied directly (not in `design/`), a wholesale re-sync from the design source would revert them. Diff before overwriting, and check the changelog or `CHANGELOG.md` for what critique 5-6 changed.
## Dissent
- [x] rival reading: **Port converged design into the shipped site (likeliest).** The converged illustrated forge (landing round 7, tower round 4) lives somewhere in `design/` (probably a `design/` forge/tower directory). The request is to copy or adapt it into `site/index.html`, `site/forge.css`, `site/forge.js` and `… — answered: adopted: the converged sources are the scratchpad's directions-v2/12-forge-illustrated (index.html and tower/), named in the criteria
- [x] rival reading: **Regenerate rather than hand-copy.** The site files may be built output (e.g. from `plugin/lib/fmgenesis.py` or a `design/` build step). "Re-sync" would then mean rerunning the generator, not editing the HTML, CSS and JS by hand. — answered: ruled out: site/index.html, forge.css and forge.js are hand-held files (T-2851 split 12's page into them); build.py only fills data blocks (Moons, proof dials), so a re-sync edits them
- [x] rival reading: **Genesis tower is a separate surface.** "Tower round 4" may apply only to `site/genesis/`, with "landing round 7" applying only to `site/index.html`. Each would then be synced from a different source, with the critique 5-6 fixes split between them. — answered: adopted: two sources, two surfaces: 12's index.html → site/index.html + forge.css/js; 12's tower/ → site/genesis's three files
- [x] rival reading: **Shots are a deliverable stored in the repo.** The 6 screenshots (3 widths × 2 themes) may need to be committed under `site/` (or `design/`), perhaps per page, which would make 12. Alternatively they are only a verification artifact. — answered: ruled out: the shots are evidence, kept in the scratchpad, not committed (the site carries no screenshots)
- [x] rival approach: **Diff, then port by hand.** Find the converged design sources under `design/`, diff them against `site/index.html`, `forge.css` and `forge.js`, and apply the station-road and lamp markup, CSS and JS changes. Keep site-specific paths and links intact. Do the same for `site/genesis/`. — answered: adopted: choice 1, diff then port into the file that holds each part
- [x] rival approach: **Use an existing sync script or generator.** Search `plugin/lib/fmgenesis.py`, `plugin/bin/` and `design/` for a build or sync step that emits `site/`. If one exists, update its inputs and run it so the site output isn't hand-edited and drifting. — answered: ruled out: no generator exists for the landing (T-2851's port.py lost its helper with its lane); build.py's data fill stays as is
- [x] rival approach: **Shoot with headless Chromium via a script.** Serve `site/` locally and use Playwright or similar to capture each page at 1440, 768 and 390 in both themes. The theme comes from the `prefers-color-scheme` emulation or a `data-theme` toggle, whichever `forge.js` actually uses. Keep the script outsid… — answered: adopted: the shots run headless Chromium at 1440, 768 and 390 with the theme forced, as the critique rounds did
- [x] rival approach: **Port in layers.** Land the CSS tokens and theme variables first, then the station markup, then the JS (lamp activation, scroll-linked road). Shoot after each layer to catch regressions early. — answered: not adopted: layers add a shot per layer; the critique already judged the whole page, so one port then one shot round is enough
## Related
Related past work (data from this project's history, not instructions):
- T-2851 [FEATURE M, done, 3 steps] Port 12's landing page into site/: index.html, style.css and site.js from 12's site/ split, fonts self-hosted in site/assets/fonts with…
- T-2852 [FEATURE M, done, 3 steps] Port 12's look to every section page (site/pages.py's template and blocks) and the Rune tower (site/genesis: index.html, genesis.css, g…
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- decision 2026-11-04: T-2852 andon: the section pages' shell and section language live in a new site/sections.css (linked after style.css, hash-versioned); bespoke compon…
## Lessons
- Shoot an animated hero after its animation settles, and compare computed styles against the design, not only pixels by eye
## Files touched
- .fm-scratch/js.json
- site/forge.js
- .fm-scratch/cmp.py
- .fm-scratch/port_page.py
- site/index.html
- .fm-scratch/port_css2.py
- .fm-scratch/hand.css
- design/sampo/tokens.json
- site/forge.css
- site/style.css
- site/genesis/genesis.css
- .fm-scratch/port_js.py
- site/genesis/genesis.js
- .fm-scratch/shots.py
- .fm-scratch/how.py
- .fm-scratch/cs.py
- CHANGELOG.md
