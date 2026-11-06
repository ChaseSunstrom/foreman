---
id: T-2964
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T13:10:30Z
updated: 2026-11-04T13:33:02Z
builder_model: haiku
base: 565a4418ca687a4daa7ac1573bbf36d0260d031c
base_tree: e2c89936e82d02c2375928613b9cfc91236ea631
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-04T13:11:00Z
plan0_scope: []
lane_stop: merged 2026-11-04T13:26:12Z
verified: strong
unproven: [meaning, ui-unshot]
---
# Fix the cold review of the shipped site (/tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/shipreview/review.md): H1 the tower's rules grid collapses at 820px and wider (site/style.css .rules>div overrides genesis.css .rule); M1 the landing hero sits ~90px below the spec at 1440 (eyebrow wraps, CTAs fall below the fold); M2 the hammer's motion trail is clipped by a hard edge; M3 the Smith section's 110px dead right margin at 768; L1 two AA contrast misses on features/code (.chip.pass, .plus); L2 the tower moons table wraps; L3 the tower header narrower than its content; L4 the code page's command box clips; L5 the pieces diagram unreadable at 390
## Raw request
> Fix the cold review of the shipped site (/tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/shipreview/review.md): H1 the tower's rules grid collapses at 820px and wider (site/style.css .rules>div overrides genesis.css .rule); M1 the landing hero sits ~90px below the spec at 1440 (eyebrow wraps, CTAs fall below the fold); M2 the hammer's motion trail is clipped by a hard edge; M3 the Smith section's 110px dead right margin at 768; L1 two AA contrast misses on features/code (.chip.pass, .plus); L2 the tower moons table wraps; L3 the tower header narrower than its content; L4 the code page's command box clips; L5 the pieces diagram unreadable at 390
## Interpretation
Reading 1 (chosen): fix the review's H1, M1-M3 and L1-L5 in the files that hold each rule, and shoot the same widths to show each fix. Reading 2 (ruled out): carry the forge onto the feature pages (M4); that is a design change (a hero figure per page, the landing's display face site-wide) captured as its own task.
## Assumptions (confidence)
## Acceptance criteria
- [x] the tower's rules show each card's title and body with its padding at 820, 1024 and 1440, and the landing hero's eyebrow, headline and CTAs sit where the spec's hero-1440 has them — verify with `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis`
- [x] every Medium and Low in the review is fixed or named with why not, shots at the review's widths show each fix — verify with `python3 plugin/tests/run.py test_site_sampo test_site_build`
## Non-goals
## Approach (options → choice → why)
1) Per finding, the smallest fix the review names (genesis.css .rules>.rule override; forge.css hero padding and eyebrow nowrap; the trail's clip bound; single-column .sec widths at 640-900; the two greens darkened; nowrap on the wild cell; the tower .top max-width; pre-wrap on the command box; the diagram scrolls at natural size on phones). Likely outcome: every finding fixed in one lane, tests green. Fails if: a fix in style.css moves another page; the shots at every width show it.
2) use what exists: rename the tower's .rules container so style.css can't match it. Likely outcome: H1 fixed with one rename. Fails if: genesis.js or tests read the class name, which a grep shows.
3) do less: only H1. Likely outcome: the High gone fast. Fails if: four Mediums stay on the shipped page.
Choice 1 (85%): the review already traced each cause to a rule.
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce each finding from the review's screenshots and selectors
2. [x] fix in the file that holds each rule; reshoot the review's widths in both themes and look at each
## Resume here
<!-- auto -->
- 2026-11-04T13:21:59Z step 1/2: reproduce each finding from the review's screenshots and selectors
- git: worktree-agent-a010fa1ccde079f2a; 6 uncommitted: plugin/tests/test_site_hero.py, site/forge.css, site/forge.js, site/genesis/genesis.css, site/genesis/genesis.js, site/style.css
- touched since last checkpoint: .fm-scratch/shoot2.py, .fm-scratch/m.py, site/forge.js, site/forge.css, site/genesis/genesis.css, site/genesis/genesis.js, plugin/tests/test_site_hero.py, site/style.css, .fm-scratch/shoot3.py
## Docs impact
CHANGELOG line (T-2964)
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 295 tests in 40.9s (51 classes, 16 at a time; slowest: GenesisRead 35s, GenerationReview 33s, GenesisCheck 29s) / OK [ran] [tree 826473a8a3bf] [world 2f1906870a] (2026-11-04T13:17:13Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_goal test_map test_moons_scale test_moonshot test_motion_verify test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.63s] [ran] [tree 826473a8a3bf] [world 2f1906870a] (2026-11-04T13:23:51Z)
- (step 1) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis` → exit 0 · Ran 295 tests in 39.0s (51 classes, 16 at a time; slowest: GenerationReview 33s, GenesisRead 33s, GenesisCheck 29s) / OK [ran] [tree 826473a8a3bf] [world 2f1906870a] (2026-11-04T13:24:33Z)
- (step 2) `python3 plugin/tests/run.py test_site_sampo test_site_build` → exit 0 · Ran 23 tests in 3.6s (10 classes, 16 at a time; slowest: Landing 3s, Reproducible 2s, Built 1s) / OK [ran] [tree 826473a8a3bf] [world 2f1906870a] (2026-11-04T13:24:43Z)
- `python3 plugin/tests/run.py test_site_hero test_genesis` → ✗ exit 1 · Ran 229 tests in 36.9s (27 classes, 16 at a time; slowest: GenesisRead 33s, GenerationReview 31s, ProofBeforePresentation 27s) / FAILED (1 classes: test_site_hero.Clash) (start tree + this task's tests) [ran] [tree 826473a8a3bf] [world 2f1906870a] (2026-11-04T13:27:37Z)
- `python3 plugin/tests/run.py test_site_hero test_genesis` → exit 0 · Ran 229 tests in 37.4s (27 classes, 16 at a time; slowest: GenesisRead 34s, GenerationReview 33s, GenesisCheck 29s) / OK [ran] [tree 826473a8a3bf] [world 2f1906870a] (2026-11-04T13:27:37Z)
- (ac 1) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis` → exit 0 · Ran 295 tests in 32.0s (51 classes, 16 at a time; slowest: GenesisRead 26s, ProofBeforePresentation 25s, GenerationReview 24s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:31:53Z)
- (ac 2) `python3 plugin/tests/run.py test_site_sampo test_site_build` → exit 0 · Ran 23 tests in 5.5s (10 classes, 16 at a time; slowest: Landing 5s, Reproducible 2s, TitleCard 2s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:31:53Z)
- (audit intent) `the cold review (a Sonnet critic, different model from the designers) traced each finding to a rule; the builder fixed each in that file; I looked at the H1 and M3 shots myself; a band above the sticky header in two tower shots is a capture offset (the header is sticky top:0)` → H1 and M1-M3 fixed with shots; L1-L5 fixed, L1 and L4 by measurement and tests only [tree eacc37c27e48] (2026-11-04T13:31:53Z)
- (audit adversary) `the cold review (a Sonnet critic, different model from the designers) traced each finding to a rule; the builder fixed each in that file; I looked at the H1 and M3 shots myself; a band above the sticky header in two tower shots is a capture offset (the header is sticky top:0)` → CSS and one canvas bound only; no new markup from data, no new hosts [tree eacc37c27e48] (2026-11-04T13:31:53Z)
- (audit edge) `the cold review (a Sonnet critic, different model from the designers) traced each finding to a rule; the builder fixed each in that file; I looked at the H1 and M3 shots myself; a band above the sticky header in two tower shots is a capture offset (the header is sticky top:0)` → style.css's generic .hero and .rules>div selectors clash with page sheets; the fixes override them per page, and scoping style.css is the lasting cure [tree eacc37c27e48] (2026-11-04T13:31:53Z)
## Log
- 2026-11-04T13:10:30Z created
- 2026-11-04T13:10:41Z set approved=True
- 2026-11-04T13:10:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2964.builder.md
- 2026-11-04T13:10:59Z focused
- 2026-11-04T13:11:00Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-04T13:26:12Z merged worktree-agent-a010fa1ccde079f2a (6 file(s))
- 2026-11-04T13:26:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a010fa1ccde079f2a
- 2026-11-04T13:26:20Z focused
- 2026-11-04T13:27:48Z scope: site/style.css, forge.css, forge.js, site/genesis/genesis.css and genesis.js, site/pages.py and the site tests, as the review traced; shots in the scratchpad's shipreview/fixed/ (I looked at tower-1440-dark-rules: cards with titles and bodies; landing-768-dark-s0: Smith rows on the full gutter)
- 2026-11-04T13:33:00Z done
- 2026-11-04T13:33:02Z committed befd80f0 (1 file)
## Follow-ups captured
## Scope
site/style.css, site/forge.css, site/forge.js, site/genesis/genesis.css, site/genesis/genesis.js, site/genesis/index.html, site/pages.py, plugin/tests/test_site*.py, plugin/tests/test_genesis.py
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- T-2957 [FEATURE M, done, 3 steps] Re-sync site/ to the converged illustrated forge (critique 7 converged: landing round 7, tower round 4): the redrawn eight stations as …
- playbook Composition, depth and states (fm playbooks show ui/composition)
- decision 2026-11-04: T-2852 andon: the section pages' shell and section language live in a new site/sections.css (linked after style.css, hash-versioned); bespoke compon…
- the similar finished task took 3 steps
## Why not caught
no test rendered the tower at 820 px and up with style.css loaded; the shipped-site review was the first to look at that width
## Lessons
- A site-wide stylesheet's generic selectors (.hero, .rules > div) leak into every page sheet: scope them, or test each page against them
## Files touched
- .fm-scratch/shoot2.py
- .fm-scratch/m.py
- site/forge.css
- site/forge.js
- site/genesis/genesis.css
- site/genesis/genesis.js
- site/style.css
- plugin/tests/test_site_hero.py
- .fm-scratch/shoot3.py
- CHANGELOG.md
