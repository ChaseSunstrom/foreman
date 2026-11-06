---
id: T-2852
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T22:18:02Z
updated: 2026-11-04T04:54:35Z
group: port the illustrated forge look
rival_at: 2026-11-04T03:25:51Z
rival_split: true
builder_model: haiku
base: a8f5a791527a175ebfb5a7ca228fc869c5b9875e
base_tree: ec05857242498d0896aedd08d1ccd31f0a58eb07
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T03:26:22Z
plan0_scope: []
lane_stop: merged 2026-11-04T04:45:36Z
verified: strong
---
# Port 12's look to every section page (site/pages.py's template and blocks) and the Rune tower (site/genesis: index.html, genesis.css, genesis.js, which shares ../style.css), each page a close view of the same forge, with shots at 1440, 768, 390 and 320 in both themes
## Raw request
> Port 12's look to every section page (site/pages.py's template and blocks) and the Rune tower (site/genesis: index.html, genesis.css, genesis.js, which shares ../style.css), each page a close view of the same forge, with shots at 1440, 768, 390 and 320 in both themes
## Interpretation
Reading 1 (chosen): every page past the landing joins the same forge. The 28+ feature pages (site/pages.py's one template, with chart, text and term blocks), the stories, gallery and features index all render through build.py's layout() and the shared style.css. Once T-2851 makes style.css 12's, the template's markup is aligned to 12's section language: engraved kicker, Bodoni headline, brass rule, forged plate for charts. The chart colours come from tokens.json's six fire series. The Rune tower (site/genesis) takes the tower redesign built in 12/tower/: the carved-course tower hero and the wild moon sky over the real genesis.json, keeping its tested contracts (../style.css, the nav, esc/plural/md markers, moonshotTable without innerHTML). Reading 2 (ruled out): restyle the CSS only and leave the template's markup; 12's look depends on its markup (kickers, plates, rules), so pages would read as the old site in new colours.
## Assumptions (confidence)
## Acceptance criteria
- [x] every built section page and site/genesis render in 12's theme from the shared style.css, pass the site tests and design lint, with shots at 4 widths x 2 themes — verify with `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis test_design_lint`
- [x] the tower's moon sky draws every catalogue moonshot from genesis.json (size by tier, light by Wild score, phase by stage) with the text table kept, and the page's contract tests pass — verify with `python3 plugin/tests/run.py test_genesis test_moonshot test_steer test_site_build`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: layout() and the block renderers emit 12's section classes; style.css (from T-2851) carries them; the tower takes 12/tower/'s index.html, genesis.css and genesis.js after its own cold critique. Likely outcome: one template change restyles every page; the tower is a reviewed drop-in. Fails if a block (chart, term) has no counterpart in 12; then it gets one forged-plate style, checked by shots.
2. A per-page hand restyle. Fails: 28 pages diverge; one template is the single source.
3. Do less: the tower only. Fails the ask ('on all aspects of it').
Choice 1 (80%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, MASTER.md, site/stats.py, plugin/tests/test_site.py, plugin/tests/test_docs.py; past FIXes T-2061, T-2064.
## Execution prompt
## Steps
1. [x] section template and blocks (chart, text, term) restyled
2. [x] site/genesis restyled on the shared style.css
3. [x] shots at 1440/768/390/320 x dark/light
## Resume here
<!-- auto -->
- 2026-11-04T04:15:24Z step 3/3: shots at 1440/768/390/320 x dark/light
- git: worktree-agent-aef1fc025ffce5d6a; 1 uncommitted: ANDON.md
- touched since last checkpoint: site/genesis/index.html, site/genesis/genesis.js, plugin/tests/test_site_sections.py, site/build.py
## Docs impact
CHANGELOG line at T-2742 step 8 with the port
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis test_design_lint` → ✗ exit 1 · Ran 283 tests in 31.5s (42 classes, 16 at a time; slowest: GenesisRead 28s, GenerationReview 27s, GenesisCheck 24s) / FAILED (1 classes: test_site_sections.Built) [ran] [tree 02d79f17753f] [world 2f1906870a] (2026-11-04T03:39:49Z)
- (step 1) `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis test_design_lint` → ✗ exit 1 · Ran 283 tests in 19.0s (42 classes, 16 at a time; slowest: GenerationReview 17s, ProofBeforePresentation 15s, GenesisRead 13s) / FAILED (2 classes: test_site_sections.Built, test_design_lint.Site) [ran] [tree 40c846b5ab76] [world 2f1906870a] (2026-11-04T03:44:35Z)
- (step 1) `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis test_design_lint` → exit 0 · Ran 283 tests in 19.1s (42 classes, 16 at a time; slowest: GenerationReview 17s, ProofBeforePresentation 15s, GenesisRead 13s) / OK [ran] [tree 463a84a85435] [world 2f1906870a] (2026-11-04T03:44:59Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_moonshot test_steer test_site_build` → ✗ exit 1 · Ran 270 tests in 28.8s (48 classes, 16 at a time; slowest: GenesisRead 25s, GenerationReview 24s, ProofBeforePresentation 22s) / FAILED (1 classes: test_genesis.GenesisExport) [ran] [tree 10f9b048f1a3] [world 2f1906870a] (2026-11-04T03:52:40Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis test_design_lint 2>&1 | tail -6` → exit 0 · Ran 285 tests in 21.9s (42 classes, 16 at a time; slowest: GenerationReview 19s, ProofBeforePresentation 18s, GenesisRead 16s) / OK [ran] [tree e9ba20f2f90d] [world 2f1906870a] (2026-11-04T04:08:58Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_moonshot test_steer test_site_build test_site_sections` → exit 0 · Ran 290 tests in 59.2s (51 classes, 16 at a time; slowest: GenesisRead 55s, GenerationReview 49s, ProofBeforePresentation 46s) / OK [ran] [tree e9ba20f2f90d] [world 2f1906870a] (2026-11-04T04:10:43Z)
- (step 3) `sampo shot --width 1440,768,390,320 --scheme both --frames 1 --out .fm-scratch/shots-rich http://127.0.0.1:8731/genesis/index.html http://127.0.0.1:8731/features/moons.html http://127.0.0.1:8731/features/benchmarks.html` → exit 0 · viewport.png / frame-00.png (1 frames 250 ms apart, real time) [ran] [tree e9ba20f2f90d] [world 2f1906870a] (2026-11-04T04:18:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_brainstorm_skill test_budget test_clean_helpers test_cli test_cognition test_compact test_core test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_ecosystem test_find test_fmpy test_genesis test_goal test_hooks test_ideas test_ideation test_knowledge test_lane_twins test_lanes test_learning2 test_loop test_louhi_models test_map test_mcp test_models test_models_systemone test_moons_scale test_moonshot test_motion_verify test_night test_outcomes test_outside test_page test_panic test_portability test_proof test_recall test_reliability_tools test_rename_scan test_replay test_research test_research_rigor test_roles test_safety test_sampo_design test_scout test_second test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_sync test_taste_ledger test_tidy test_trust test_ui test_verbs_nopipe test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2415 tests in 134.6s (521 classes, 16 at a time; slowest: Stop 104s, Lanes 58s, NoTaskGate 53s) / FAILED (3 classes: test_docs.Site, test_rename_scan.RenameScan, test_site_sampo.Built) [ran] [tree 129c1605482b] [world 2f1906870a] (2026-11-04T04:21:31Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_moonshot test_steer test_site_build test_site_sections test_design_lint` → exit 0 · Ran 324 tests in 37.4s (58 classes, 16 at a time; slowest: GenesisRead 35s, GenerationReview 33s, GenesisSweep 30s) / OK [ran] [tree 5cfaebbb8d7d] [world 2f1906870a] (2026-11-04T04:32:37Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_brainstorm_skill test_budget test_clean_helpers test_cli test_cognition test_compact test_core test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_ecosystem test_find test_fmpy test_genesis test_goal test_hooks test_ideas test_ideation test_knowledge test_lane_twins test_lanes test_learning2 test_loop test_louhi_models test_map test_mcp test_models test_models_systemone test_moons_scale test_moonshot test_motion_verify test_night test_outcomes test_outside test_page test_panic test_portability test_proof test_recall test_reliability_tools test_rename_scan test_replay test_research test_research_rigor test_roles test_safety test_sampo_design test_scout test_second test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_sync test_taste_ledger test_tidy test_trust test_ui test_verbs_nopipe test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.93s] [ran] [tree 5cfaebbb8d7d] [world 2f1906870a] (2026-11-04T04:34:39Z)
- `python3 plugin/tests/run.py test_site_sections` → ✗ exit 1 · Ran 20 tests in 12.4s (3 classes, 16 at a time; slowest: Built 12s, Pages 0s, Collect 0s) / FAILED (1 classes: test_site_sections.Built) [ran] [tree 981bf220d21b] [world 2f1906870a] (2026-11-04T04:47:42Z)
- `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis` → exit 0 · Ran 251 tests in 20.9s (35 classes, 16 at a time; slowest: GenesisRead 19s, GenerationReview 18s, GenesisCheck 16s) / OK [ran] [tree 2bef4f49e26b] [world 2f1906870a] (2026-11-04T04:52:26Z)
- `python3 plugin/tests/run.py test_site_sections` → ✗ exit 1 · Ran 20 tests in 12.7s (3 classes, 16 at a time; slowest: Built 11s, Pages 0s, Collect 0s) / FAILED (1 classes: test_site_sections.Built) (start tree + this task's tests) [ran] [tree 2bef4f49e26b] [world 2f1906870a] (2026-11-04T04:53:02Z)
- `python3 plugin/tests/run.py test_site_sections` → exit 0 · Ran 20 tests in 9.9s (3 classes, 16 at a time; slowest: Built 9s, Pages 0s, Collect 0s) / OK [ran] [tree 2bef4f49e26b] [world 2f1906870a] (2026-11-04T04:53:02Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sections test_site_build test_genesis test_design_lint` → exit 0 · Ran 285 tests in 15.8s (42 classes, 16 at a time; slowest: GenerationReview 14s, GenesisRead 13s, ProofBeforePresentation 12s) / OK [ran] [tree 2bef4f49e26b] [world 2f1906870a] (2026-11-04T04:53:51Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis test_moonshot test_steer test_site_build` → exit 0 · Ran 270 tests in 18.8s (48 classes, 16 at a time; slowest: GenerationReview 17s, ProofBeforePresentation 15s, GenesisRead 13s) / OK [ran] [tree 2bef4f49e26b] [world 2f1906870a] (2026-11-04T04:53:51Z)
- (audit intent) `lane diff read (sections.css, build.py roles and layout, genesis.js, the tower page); 251 tests green; builder's shots at 1440/768/390/320 in both schemes; roles() narrowed red-to-green in the main thread` → the tower and every section page in 12's look: carved tower under the moon sky, the Moons funnel and families as text, kicker, Bodoni headline, brass rule, forged chart plates; models named by role [tree 2bef4f49e26b] (2026-11-04T04:53:51Z)
- (audit edge) `lane diff read (sections.css, build.py roles and layout, genesis.js, the tower page); 251 tests green; builder's shots at 1440/768/390/320 in both schemes; roles() narrowed red-to-green in the main thread` → the role swap keeps a repo named jarvis ('jarvis (1,853)') and Claude's model names (Opus, Haiku, Sonnet, Fable); running it twice changes nothing; footer links are added only after the tower draws [tree 2bef4f49e26b] (2026-11-04T04:53:51Z)
- (audit adversary) `lane diff read (sections.css, build.py roles and layout, genesis.js, the tower page); 251 tests green; builder's shots at 1440/768/390/320 in both schemes; roles() narrowed red-to-green in the main thread` → every innerHTML built from export data passes text through esc() (moon ids, titles, stats, rules) and numbers through F(); the footer and arcs are fixed strings or computed geometry; the export is Sampo's own file, never a fetch from another host [tree 2bef4f49e26b] (2026-11-04T04:53:51Z)
- (audit design) `lane diff read (sections.css, build.py roles and layout, genesis.js, the tower page); 251 tests green; builder's shots at 1440/768/390/320 in both schemes; roles() narrowed red-to-green in the main thread` → sections.css reads the generated tokens with 12's names first, so the pages hold whichever way T-2851's style.css lands; the :where() fallback colours stay until 12's sheet merges [tree 2bef4f49e26b] (2026-11-04T04:53:51Z)
- (audit maintainer) `lane diff read (sections.css, build.py roles and layout, genesis.js, the tower page); 251 tests green; builder's shots at 1440/768/390/320 in both schemes; roles() narrowed red-to-green in the main thread` → the committed genesis.json is stale (no moons_scale): re-export at T-2742 step 7's verify; the swap belongs in the export itself (T-2895) [tree 2bef4f49e26b] (2026-11-04T04:53:51Z)
- (audit operator) `lane diff read (sections.css, build.py roles and layout, genesis.js, the tower page); 251 tests green; builder's shots at 1440/768/390/320 in both schemes; roles() narrowed red-to-green in the main thread` → sampo shot captures only the first screen, so footers were checked in HTML, not by eye (T-2896) [tree 2bef4f49e26b] (2026-11-04T04:53:51Z)
## Log
- 2026-11-03T22:18:02Z created
- 2026-11-03T22:18:10Z set depends_on=['T-2851']
- 2026-11-04T03:25:39Z set depends_on=[]
- 2026-11-04T03:25:39Z started in parallel with T-2851 (the user asked why the site takes so long); it leaves the nav block to T-2851 and merges foreman/build in before its own merge
- 2026-11-04T03:26:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2852.builder.md
- 2026-11-04T03:26:21Z focused
- 2026-11-04T03:26:22Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T04:45:36Z merged worktree-agent-aef1fc025ffce5d6a (9 file(s))
- 2026-11-04T04:45:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aef1fc025ffce5d6a
- 2026-11-04T04:45:40Z focused
- 2026-11-04T04:54:33Z done
- 2026-11-04T04:54:35Z committed aaebcf34 (3 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Restyle, not rebuild (likeliest):** "Port 12's look" means apply the visual design of a reference named "12" (probably a `design/` variant or a numbered theme/mock) to the shared section-page template in `site/pages.py` (its page template and per-section blocks) and to the Rune tower in `site/gen…
- **"12" is a section or page:** it could be page/section number 12 in `site/pages.py` or a genesis stage, and "port its look" copies that page's treatment to the others. This is plausible if `design/` has no obvious "12".
- **Screenshots are a deliverable:** the 1440/768/390/320 widths in light and dark are required output (8 shots per page) that prove the port. They are not just a check I run privately. Where they go (`design/`, `site/`, or a scratch dir) is unstated.
- **Narrow scope:** only the template and blocks change, with no per-page content edits, and the tower only gets CSS/JS parity.
Approaches:
- **Token-first port:** find what "12" is by listing `design/` and grepping `site/` for "12". Lift its tokens (colors, type, spacing, forge motif) into `site/style.css` as theme variables for light and dark. Then change `site/pages.py` to emit the new markup once, in the template and block functions,…
- **Per-page "close view" via a data attribute:** have `pages.py` stamp each page with a section id (`data-view="…"`). CSS then shifts the forge's crop, accent or focal element per section, which gives the "same forge, closer" feel without separate stylesheets.
- **Screenshot harness:** write one script that builds the site, serves it statically, and runs headless Chromium through pages × {1440, 768, 390, 320} × {light, dark}. It forces the theme through whatever mechanism `style.css` uses (a `data-theme` attribute or `prefers-color-scheme`). Keep the scrip…
- **Regenerate, don't hand-edit:** if the section HTML in `site/` is generated by `pages.py`, rebuild it instead of editing outputs. Hand-edit only `genesis/index.html`, which is not generated.
Failure modes:
- **Tower regressions from shared CSS:** changes to `site/style.css` can break `genesis.css` and `genesis.js`, for example selectors or class names the tower's JS toggles, or tower CSS that overrides the new tokens. A page that looks right at 1440 can still break at 320.
- **Theme coverage gaps:** a theme switch that only works through one mechanism (the `prefers-color-scheme` media query vs a `data-theme` toggle in `genesis.js`) leaves one theme unverified or unreachable in screenshots, and hard-coded colors in the blocks ignore it.
- **Narrow-viewport overflow:** fixed-width forge art, wide code or table blocks, and the tower's layout overflow horizontally at 390 and 320, and only a check of `scrollWidth` against the viewport catches it.
- **Wrong target for "12":** if "12" is guessed without confirming what it names, the whole port copies the wrong look. Confirm it before restyling.
## Dissent
- [x] rival reading: **Restyle, not rebuild (likeliest):** "Port 12's look" means apply the visual design of a reference named "12" (probably a `design/` variant or a numbered theme/mock) to the shared section-page template in `site/pages.py` (its page template and per-section blocks) and to the Rune tower in `site/gen… — answered: adopted in part: the section pages restyle through the one template; the tower is a rebuild from its reviewed design (12/tower/)
- [x] rival reading: **"12" is a section or page:** it could be page/section number 12 in `site/pages.py` or a genesis stage, and "port its look" copies that page's treatment to the others. This is plausible if `design/` has no obvious "12". — answered: rejected: 12 is the chosen design direction (scratchpad directions-v2/12-forge-illustrated)
- [x] rival reading: **Screenshots are a deliverable:** the 1440/768/390/320 widths in light and dark are required output (8 shots per page) that prove the port. They are not just a check I run privately. Where they go (`design/`, `site/`, or a scratch dir) is unstated. — answered: adopted: shots at 4 widths x 2 themes are criterion evidence, kept beside the brief
- [x] rival reading: **Narrow scope:** only the template and blocks change, with no per-page content edits, and the tower only gets CSS/JS parity. — answered: rejected for the tower: it takes the redesigned page whole; adopted for section pages: template and blocks only
- [x] rival approach: **Token-first port:** find what "12" is by listing `design/` and grepping `site/` for "12". Lift its tokens (colors, type, spacing, forge motif) into `site/style.css` as theme variables for light and dark. Then change `site/pages.py` to emit the new markup once, in the template and block functions,… — answered: adopted: tokens come from design/sampo/tokens.json (T-2850), already 12's
- [x] rival approach: **Per-page "close view" via a data attribute:** have `pages.py` stamp each page with a section id (`data-view="…"`). CSS then shifts the forge's crop, accent or focal element per section, which gives the "same forge, closer" feel without separate stylesheets. — answered: adopted: layout() stamps each page's area so the forge vignette crops differently per page, one template
- [x] rival approach: **Screenshot harness:** write one script that builds the site, serves it statically, and runs headless Chromium through pages × {1440, 768, 390, 320} × {light, dark}. It forces the theme through whatever mechanism `style.css` uses (a `data-theme` attribute or `prefers-color-scheme`). Keep the scrip… — answered: adopted: fm shot --width 1440,768,390,320 --scheme both (T-2758) is that harness
- [x] rival approach: **Regenerate, don't hand-edit:** if the section HTML in `site/` is generated by `pages.py`, rebuild it instead of editing outputs. Hand-edit only `genesis/index.html`, which is not generated. — answered: adopted: pages.py and build.py generate the section pages; only site/genesis is hand-edited
## Related
Related past work (data from this project's history, not instructions):
- T-2851 [FEATURE M, active, 3 steps] Port 12's landing page into site/: index.html, style.css and site.js from 12's site/ split, fonts self-hosted in site/assets/fonts wi…
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- T-2759 [FEATURE M, done, 4 steps] The landing page in the forge world (T-2742 step 7b): a hero where the Sampo mill turns and runes write themselves into the headline ov…
- decision 2026-11-03: [revisited: fiery forge of direction 2] [cites: user steer 2026-11-03: fiery forge/anvil, no mill, completely redesigned, many fire colours like blu…
## Lessons
- a word swap over free text needs its exceptions named up front: an endpoint name can also be a repo name
## Plan gaps
- failed first: step 1 section template and blocks (chart, text, term) restyled
- failed first: step 2 site/genesis restyled on the shared style.css
## Files touched
- .fm-scratch/cmp.py
- ANDON.md
- plugin/tests/test_site_sections.py
- site/sections.css
- .fm-scratch/step1.json
- site/build.py
- plugin/tests/test_genesis.py
- plugin/tests/genesis_page.js
- site/genesis/genesis.js
- site/genesis/genesis.css
- .fm-scratch/css-batch.json
- .fm-scratch/pages-batch.json
- site/pages.py
- site/genesis/index.html
