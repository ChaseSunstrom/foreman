---
id: T-2753
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/**, plugin/tests/test_site*.py, plugin/tests/test_rename_scan.py, plugin/tests/genesis_page.js, plugin/tests/test_genesis.py, .github/workflows/pages.yml, plugin/tests/test_docs.py]
depends_on: []
source: user
created: 2026-11-03T02:39:56Z
updated: 2026-11-03T03:31:35Z
builder_model: sonnet
base: 8aa8ad27f389d7d0e642c7f1787156a8c906fdb7
base_tree: 6c63873325293d4f387f2a79554a8e0314db45a4
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T02:40:50Z
plan0_scope: [site/**, plugin/tests/test_site*.py, plugin/tests/test_rename_scan.py]
lane_stop: merged 2026-11-03T03:24:32Z
verified: strong
unproven: [infra, ui-unshot]
---
# The site takes Sampo's design system (T-2742 step 7a): style.css reads design/sampo/tokens.json, the Runestone mark and its variants replace the hard hat, and every page's chrome and copy names Sampo and the sampo verbs (old names only where the install page lists them as aliases)
## Raw request
> The site takes Sampo's design system (T-2742 step 7a): style.css reads design/sampo/tokens.json, the Runestone mark and its variants replace the hard hat, and every page's chrome and copy names Sampo and the sampo verbs (old names only where the install page lists them as aliases)
## Interpretation
Reading 1 (chosen): SAMPO.md's Website and Consistency paragraphs, first slice: the existing site (site/index.html, style.css, build.py's generated pages, site/genesis) moves onto design/sampo/tokens.json and the Runestone logo, and its words onto the Sampo names. The hero mill, scroll scenes and shaders (7b) and the new section pages (7c) follow in their own lanes. Reading 2: rebuild every page from scratch now; rejected as L and colliding with 7b/7c.
## Assumptions (confidence)
## Acceptance criteria
- [x] the site's colours, type and motion come from design/sampo/tokens.json (one source), in light and dark, with the logo, favicon and share image from design/sampo/logo — verify with `python3 plugin/tests/run.py test_site_sampo`
- [x] the site builds and its existing tests pass — verify with `python3 plugin/tests/run.py test_site test_site_build test_site_gallery test_site_hero`
- [x] site lines naming Foreman go down and the rename ratchet's BASELINE is lowered to match — verify with `python3 plugin/tests/run.py test_rename_scan`
## Non-goals
## Approach (options → choice → why)
1. Generate a :root token block from tokens.json at build time into the built style.css (site/build.py), so one source drives the site. Likely outcome: no hand-kept copy; test_site_sampo compares the built CSS to tokens.json. Fails if: the Pages runner's Python lacks something (stdlib json only, so it doesn't).
2. Hand-copy the token values into style.css with a test that they match. Likely outcome: a simpler build. Fails if: two copies drift and the test only catches it after the fact.
3. Use what exists: design/sampo/index.html already renders tokens.json into CSS custom properties, and design/sampo/logo/build.py emits every logo variant; build.py's _v() already hashes asset URLs, and fm shot takes the screenshots. Reuse that token-to-CSS mapping and copy the logo files rather than redrawing. Likely outcome: little new code. Fails if: the preview page's mapping is hand-written, in which case lift it into one function both use.
4. Do less: rename the words only and keep the old palette. Fails if: SAMPO.md wants one design system across every surface.
Choice 1 with 3 (80%): a generated block that reuses the preview's token mapping, plus the logo files copied from design/sampo/logo, checked by test_site_sampo.
## Risks and rollback
Blast radius (fm graph blast): unknown, no co-change history for plugin/tests/test_rename_scan.py.
## Execution prompt
## Steps
1. [x] test_site_sampo: tokens drive style.css (a build step or a checked copy, never hand-kept twice), the logo files are the Runestone ones, no page names Foreman outside the kept forms
2. [x] style.css and build.py on the tokens; assets swapped (assets/foreman.svg → sampo mark, favicon, share.png); old asset paths kept working if anything links them
3. [x] every page's chrome and copy renamed (Foreman→Sampo, fm→sampo, Genesis→Rune, exam/Inspector→Louhi, guard→Ward, moonshots→Moons, not-yet ledger→Underworld, task loop→Smith); site/genesis keeps its path for now (7c moves it)
4. [x] screenshots at 1280, 768 and 320 px in light and dark; fix what they show; lower BASELINE in test_rename_scan
## Resume here
<!-- auto -->
- 2026-11-03T03:16:56Z step 4/4: screenshots at 1280, 768 and 320 px in light and dark; fix what they show; lower BASELINE in test_rename_scan
- git: worktree-agent-a9730cf227a5d543d; 20 uncommitted: .github/workflows/pages.yml, plugin/tests/genesis_page.js, plugin/tests/test_docs.py, plugin/tests/test_genesis.py, plugin/tests/test_site.py, plugin/tests/test_site_build.py, plugin/tests/test_site_hero.py, site/assets/share.png, site/build.py, site/genesis/genesis.css
- touched since last checkpoint: site/genesis/genesis.js, plugin/tests/test_site_build.py, .fm-scratch/docs.json, plugin/tests/test_docs.py, .fm-scratch/dur.json, site/genesis/genesis.css, plugin/tests/test_site_sampo.py, site/style.css, .fm-scratch/shots.sh
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_sampo` → ✗ exit 1 · Ran 8 tests in 2.0s (2 classes, 16 at a time; slowest: Built 1s, Tokens 0s) / FAILED (2 classes: test_site_sampo.Tokens, test_site_sampo.Built) [ran] [tree 9f76e2a38822] [world 2f1906870a] (2026-11-03T02:55:00Z)
- (step 2) `python3 plugin/tests/run.py test_site_sampo.Tokens test_site_build test_site_hero test_site_gallery` → exit 0 · Ran 33 tests in 8.3s (12 classes, 16 at a time; slowest: Landing 7s, Session 5s, Reproducible 5s) / OK [ran] [tree 8431a7c80960] [world 2f1906870a] (2026-11-03T03:01:02Z)
- (step 3) `python3 plugin/tests/run.py test_site_sampo test_site test_site_build test_docs test_design_lint test_genesis` → exit 0 · Ran 392 tests in 17.9s (76 classes, 16 at a time; slowest: GenesisRead 16s, GenerationReview 14s, GenesisCheck 13s) / OK [ran] [tree 1b63b52db2c6] [world 2f1906870a] (2026-11-03T03:14:58Z)
- (step 4) `python3 plugin/tests/run.py test_site_sampo test_site test_site_build test_site_hero test_site_gallery test_design_lint test_docs test_genesis test_rename_scan` → exit 0 · ✓ exit 0 (29.7 s) · OK [ran] [tree 7e61a00ee524] [world 2f1906870a] (2026-11-03T03:18:33Z)
- (step 4) `python3 plugin/tests/run.py test_rename_scan test_site_sampo test_site test_site_build test_site_gallery test_site_hero` → exit 0 · Ran 47 tests in 6.7s (24 classes, 16 at a time; slowest: Header 6s, Landing 4s, Session 3s) / OK [ran] [tree 60ebcae23a34] [world 2f1906870a] (2026-11-03T03:18:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_ci_matrix test_design_gates test_design_lint test_design_sprint test_docs test_exam test_fmpy test_genesis test_goal test_map test_moonshot test_motion_verify test_rename_scan test_replay test_scene test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_sampo test_steer test_suite_hygiene test_taste_ledger test_workflows && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.74s] [ran] [tree 60ebcae23a34] [world 2f1906870a] (2026-11-03T03:22:21Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sampo` → exit 0 · Ran 8 tests in 1.2s (2 classes, 16 at a time; slowest: Built 1s, Tokens 0s) / OK [ran] [tree fa74652787b0] [world 2f1906870a] (2026-11-03T03:24:51Z)
- (ac 2) `python3 plugin/tests/run.py test_site test_site_build test_site_gallery test_site_hero` → exit 0 · Ran 45 tests in 6.3s (23 classes, 16 at a time; slowest: Header 6s, Landing 3s, Session 2s) / OK [ran] [tree fa74652787b0] [world 2f1906870a] (2026-11-03T03:24:58Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree fa74652787b0] [world 2f1906870a] (2026-11-03T03:25:00Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sampo` → exit 0 · Ran 9 tests in 2.0s (2 classes, 16 at a time; slowest: Built 1s, Tokens 0s) / OK [ran] [tree 2415a19133b8] [world 2f1906870a] (2026-11-03T03:25:51Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sampo` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T03:25:51Z [ran] [tree 2415a19133b8] [world 2f1906870a] (2026-11-03T03:26:06Z)
- (ac 2) `python3 plugin/tests/run.py test_site test_site_build test_site_gallery test_site_hero` → exit 0 · Ran 46 tests in 9.2s (23 classes, 16 at a time; slowest: Landing 8s, Header 7s, Proof 4s) / OK [ran] [tree 2415a19133b8] [world 2f1906870a] (2026-11-03T03:26:06Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 2415a19133b8] [world 2f1906870a] (2026-11-03T03:26:06Z)
- (audit intent) `reviewed the merged branch: rebuilt the site and screenshotted the landing at 1280 dark and 390 light (with and without reduced motion) and the Ward page at 1280 dark; type, palette and Runestone chrome read as one system; the hero's staggered fade predates this lane; exemptions in test_site_sampo are narrow phrases from quoted sources` → SAMPO.md Website/Consistency first slice: tokens drive the site, Runestone assets, Sampo names, old names only as listed aliases; hero mill, scroll scenes and shaders are 7b, section pages 7c [tree 2415a19133b8] (2026-11-03T03:26:06Z)
- (audit edge) `reviewed the merged branch: rebuilt the site and screenshotted the landing at 1280 dark and 390 light (with and without reduced motion) and the Ward page at 1280 dark; type, palette and Runestone chrome read as one system; the hero's staggered fade predates this lane; exemptions in test_site_sampo are narrow phrases from quoted sources` → 320/390 px, the 768 px nav overflow fixed, reduced motion shows stills, light and dark both from tokens; charts still the old blue (captured T-2757) [tree 2415a19133b8] (2026-11-03T03:26:06Z)
- (audit adversary) `reviewed the merged branch: rebuilt the site and screenshotted the landing at 1280 dark and 390 light (with and without reduced motion) and the Ward page at 1280 dark; type, palette and Runestone chrome read as one system; the hero's staggered fade predates this lane; exemptions in test_site_sampo are narrow phrases from quoted sources` → pages.yml only gained trigger paths (no permission change); the build copies symlink targets, so a link out of the repo would publish its file: test_every_link_in_site_stays_in_the_repo now fails on one; the three links point into design/sampo/logo [tree 2415a19133b8] (2026-11-03T03:26:06Z)
- (audit intent) `reviewed the merged branch: rebuilt the site and screenshotted the landing at 1280 dark and 390 light (with and without reduced motion) and the Ward page at 1280 dark; type, palette and Runestone chrome read as one system; the hero's staggered fade predates this lane; exemptions in test_site_sampo are narrow phrases from quoted sources` → SAMPO.md Website/Consistency first slice: tokens drive the site, Runestone assets, Sampo names, old names only as listed aliases; hero mill, scroll scenes and shaders are 7b, section pages 7c [tree 7871c445ef4a] (2026-11-03T03:30:39Z)
- (audit edge) `reviewed the merged branch: rebuilt the site and screenshotted the landing at 1280 dark and 390 light (with and without reduced motion) and the Ward page at 1280 dark; type, palette and Runestone chrome read as one system; the hero's staggered fade predates this lane; exemptions in test_site_sampo are narrow phrases from quoted sources` → 320/390 px, the 768 px nav overflow fixed, reduced motion shows stills, light and dark both from tokens; charts still the old blue (captured T-2757) [tree 7871c445ef4a] (2026-11-03T03:30:39Z)
- (audit adversary) `reviewed the merged branch: rebuilt the site and screenshotted the landing at 1280 dark and 390 light (with and without reduced motion) and the Ward page at 1280 dark; type, palette and Runestone chrome read as one system; the hero's staggered fade predates this lane; exemptions in test_site_sampo are narrow phrases from quoted sources` → pages.yml only gained trigger paths (no permission change); the build copies symlink targets, so a link out of the repo would publish its file: test_every_link_in_site_stays_in_the_repo now fails on one; the three links point into design/sampo/logo [tree 7871c445ef4a] (2026-11-03T03:30:39Z)
## Log
- 2026-11-03T02:39:56Z created
- 2026-11-03T02:40:00Z set approved=True
- 2026-11-03T02:40:00Z plan: M, one lane; site/ and the design tokens don't touch T-2748's plugin/lib move; the site ships only after T-2742 step 2 lands, since its copy names the sampo verbs
- 2026-11-03T02:40:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2753.builder.md
- 2026-11-03T02:40:48Z focused
- 2026-11-03T02:40:50Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T03:09:01Z set scope=['site/**', 'plugin/tests/test_site*.py', 'plugin/tests/test_rename_scan.py', 'plugin/tests/genesis_page.js', 'plugin/tests/test_genesis.py', '.github/workflows/pages.yml']
- 2026-11-03T03:09:03Z scope widened: test_genesis.py and genesis_page.js pin the Genesis nav text and the long row's foreman label, which the rename changes; pages.yml must rebuild when design/sampo tokens or logo change
- 2026-11-03T03:12:50Z set scope=['site/**', 'plugin/tests/test_site*.py', 'plugin/tests/test_rename_scan.py', 'plugin/tests/genesis_page.js', 'plugin/tests/test_genesis.py', '.github/workflows/pages.yml', 'plugin/tests/test_docs.py']
- 2026-11-03T03:12:50Z scope: + plugin/tests/test_docs.py: its Site class pins the site's renamed copy (Why use Sampo, where Sampo did worse) and copies site/ without design/, which the build now reads for tokens
- 2026-11-03T03:24:32Z merged worktree-agent-a9730cf227a5d543d (20 file(s))
- 2026-11-03T03:24:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9730cf227a5d543d
- 2026-11-03T03:24:47Z focused
- 2026-11-03T03:25:19Z scope: CHANGELOG.md line for the site's design system
- 2026-11-03T03:31:29Z done
- 2026-11-03T03:31:35Z committed ca345c60 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
## Lessons
- A design lane's shots must include the pages it didn't redesign: the Ward page showed chart colours outside the new palette
## Plan gaps
- failed first: step 1 test_site_sampo: tokens drive style.css (a build step or a checked copy, never hand-kept twice), th…
## Files touched
- plugin/tests/test_site_sampo.py
- site/build.py
- site/index.html
- site/genesis/index.html
- site/style.css
- .fm-scratch/css.json
- site/genesis/genesis.css
- plugin/tests/test_site_build.py
- .github/workflows/pages.yml
- plugin/tests/test_site_hero.py
- .fm-scratch/build.json
- .fm-scratch/scan.py
- .fm-scratch/pages.json
- site/pages.py
- .fm-scratch/build2.json
- .fm-scratch/index.json
- .fm-scratch/genesis.json
- plugin/tests/genesis_page.js
- plugin/tests/test_genesis.py
- site/genesis/genesis.js
- .fm-scratch/testsite.json
- plugin/tests/test_site.py
- .fm-scratch/docs.json
- plugin/tests/test_docs.py
- .fm-scratch/dur.json
- .fm-scratch/shots.sh
- plugin/tests/test_rename_scan.py
- CHANGELOG.md
- site/assets/favicon.ico
- site/assets/sampo.svg
