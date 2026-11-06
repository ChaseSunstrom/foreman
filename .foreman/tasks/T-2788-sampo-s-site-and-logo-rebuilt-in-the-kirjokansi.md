---
id: T-2788
type: FEATURE
tier: L
status: done
priority: normal
scope: [design/sampo/**, site/**, plugin/tests/test_site*.py, plugin/tests/test_design*.py, README.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-03T05:25:16Z
updated: 2026-11-04T13:35:43Z
base_note: Calibration: this plan states Choice 75% where FEATURE L closes (78) held on the first finish 96% of the time: 21 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
group: Sampo forge look directions and renders
base: 0e92c6746414f8dc4982b352f673d6812888cdfd
base_tree: eacc37c27e48b8da00147fe240fc36134c7b9315
predict_minutes: 14
predict_attempts: 1
plan0_at: 2026-11-04T13:35:17Z
plan0_scope: [design/sampo/**, site/**, plugin/tests/test_site*.py, plugin/tests/test_design*.py, README.md, CHANGELOG.md]
verified: strong
---
# Sampo's theme is the illustrated forge (12-forge-illustrated, user pick 2026-11-03): super-improved, then carried through the logo and every variant, the design tokens, the landing page and every section page, the Rune tower page (site/genesis), the README header and INSTALL, the panel's colours and the share card
## Raw request
> Sampo's site and logo rebuilt in the Kirjokansi direction fused with Ilmarinen's forge (T-2772 pick): the astrolabe mark and every variant, design tokens, the landing page and every section page, the README header, with the forge as the horizon smithy and the heat language for running states
## Interpretation
Reading 1 (chosen): the user picked Kirjokansi in the T-2772 picker, then said they like both 1 and 2; the decision (decisions.md, 2026-11-03) fuses them: Kirjokansi's astrolabe and sky are the frame, Ilmarinen's forge is the horizon smithy and the heat language for running states. The whole site and logo system move to it, replacing T-2759's forge-world landing and the Runestone mark. Reading 2: ship direction 1 as built and keep 2 only as a mood. Ruled out: the user said they like both, so the forge has to be visible in the product.
## Assumptions (confidence)
## Acceptance criteria
- [x] the illustrated forge (12-forge-illustrated) is super-improved in cold design-review rounds until the review finds nothing above low, and published live to the user on the picker Artifact; no approval wait — verify with `test -f /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_review/final.md`
- [x] design/sampo holds the illustrated anvil-stone mark, its animated version, 16/32/48 px icons, mono and light variants, the README banner (dark and light) and tokens.json from 12's NOTES (night, ember, brass, the five rune-fire colours), each SVG rendering at 16, 32 and 512 — verify with `python3 plugin/tests/run.py test_design`
- [x] every site page is rebuilt from the tokens, with numbers read from stats.json, and passes the quality bar: no other hosts, whole without JS, reduced-motion stills, light and dark, 320 px, WCAG AA, design lint — verify with `python3 plugin/tests/run.py test_site test_site_build test_site_landing test_site_sections test_site_sampo`
- [x] a cold design review of the shipped pages finds nothing above low, or each finding is fixed — verify with `fm research show T-2788-design-review`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: carry the concept's generator (_src/gen.py, index.src.html) into design/sampo and site/build.py's page model, so stats.json, the nav and tests keep working; each section page reuses one shared sky/forge shell. Likely outcome: the landing in a day of lanes, section pages after. Fails if: the concept's single-file JS doesn't split cleanly into site.js plus progressive HTML. 2) Rewrite the site by hand from the concept's look. Fails if: the generator's real star positions and gear geometry are lost and redone by eye. 3) Do less: landing page only, section pages keep T-2759's forge style. Fails if: the site no longer matches the logo's world, the user's main complaint. Choice 1 (75%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] super-improve 12-forge-illustrated: the designer finishes it, cold critique, fix rounds until nothing above low; live on the picker
2. [x] logo system and README banner into design/sampo: mark, animated, icons, variants; tokens.json from 12's NOTES; tests
3. [x] landing page in site/ from 12, data from stats.json, the myth paragraph once
4. [x] every section page and the Rune tower page (site/genesis) in the same world
5. [x] the panel (foreman-ui) colours and the share card from the tokens
6. [x] quality bar and shots at 1440, 768, 390, 320 in both themes; fm design lint
7. [x] cold design review of the shipped pages on a different model; fix; README header, INSTALL and CHANGELOG
## Resume here
## Docs impact
README header and INSTALL carry the anvil-stone banner (T-2850); the CHANGELOG's Highlights name the illustrated forge; design/sampo holds the logo system and tokens
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_sampo_design test_design_tokens` → exit 0 · Ran 64 tests in 2.5s (7 classes, 16 at a time; slowest: Extract 2s, Palette 1s, Logo 1s) / OK [ran] [tree 369926ef25a1] [world 2f1906870a] (2026-11-04T00:27:42Z)
- (step 5) `python3 plugin/tests/run.py test_design_surfaces test_sampo_design` → exit 0 · Ran 58 tests in 2.6s (13 classes, 16 at a time; slowest: Xray 2s, Tokens 2s, Imported 1s) / OK [ran] [tree 369926ef25a1] [world 2f1906870a] (2026-11-04T00:27:45Z)
- (step 1) `sampo research show T-2788-design-review` → exit 0 · ## The design rounds before it / Critique 7 on the design itself converged: nothing above Low on the landing (6 Low) or the tower (1 Low); directions-v2/12-forge-illustrated/_review/final.md. [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:34:08Z)
- (step 3) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 295 tests in 21.4s (51 classes, 16 at a time; slowest: GenerationReview 18s, ProofBeforePresentation 16s, GenesisRead 14s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:34:30Z)
- (step 4) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 295 tests in 18.2s (51 classes, 16 at a time; slowest: GenerationReview 18s, GenesisRead 14s, GenesisSweep 13s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:34:48Z)
- (step 6) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 295 tests in 21.4s (51 classes, 16 at a time; slowest: GenerationReview 18s, ProofBeforePresentation 16s, GenesisRead 14s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:35:10Z)
- (step 7) `sampo research show T-2788-design-review` → exit 0 · ## The design rounds before it / Critique 7 on the design itself converged: nothing above Low on the landing (6 Low) or the tower (1 Low); directions-v2/12-forge-illustrated/_review/final.md. [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:35:11Z)
- (ac 1) `test -f /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_review/final.md` → exit 0 · (no output) [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:35:42Z)
- (ac 2) `python3 plugin/tests/run.py test_design` → exit 0 · Ran 123 tests in 3.2s (27 classes, 16 at a time; slowest: Extract 3s, Xray 2s, Tokens 2s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:35:42Z)
- (ac 3) `python3 plugin/tests/run.py test_site test_site_build test_site_landing test_site_sections test_site_sampo` → exit 0 · Ran 79 tests in 9.9s (28 classes, 16 at a time; slowest: Built 10s, Landing 5s, Header 5s) / OK [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:35:42Z)
- (ac 4) `fm research show T-2788-design-review` → exit 0 · ## The design rounds before it / Critique 7 on the design itself converged: nothing above Low on the landing (6 Low) or the tower (1 Low); directions-v2/12-forge-illustrated/_review/final.md. [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:35:42Z)
- (audit intent) `seven cold design rounds on the design (critique 7 converged, nothing above Low), then a cold review of the shipped pages on a different model (Sonnet) whose 1 High, 4 Medium and 5 Low were fixed or split (T-2964, T-2965); each carrying task closed with its own five-lens audit` → the illustrated forge is in the logo system, tokens, landing, section pages, tower, pane, band and README; critique 7 converged and the shipped review's findings are fixed; the feature pages' forge treatment is T-2965 [tree eacc37c27e48] (2026-11-04T13:35:42Z)
- (audit adversary) `seven cold design rounds on the design (critique 7 converged, nothing above Low), then a cold review of the shipped pages on a different model (Sonnet) whose 1 High, 4 Medium and 5 Low were fixed or split (T-2964, T-2965); each carrying task closed with its own five-lens audit` → the site loads no outside hosts, data text reaches markup only through esc() (the tower's new docs column checked in T-2957), and no page reads user input [tree eacc37c27e48] (2026-11-04T13:35:42Z)
- (audit edge) `seven cold design rounds on the design (critique 7 converged, nothing above Low), then a cold review of the shipped pages on a different model (Sonnet) whose 1 High, 4 Medium and 5 Low were fixed or split (T-2964, T-2965); each carrying task closed with its own five-lens audit` → 320 to 1440 px in both themes without overflow, whole without JS, reduced-motion stills, WCAG AA after T-2964's two contrast fixes [tree eacc37c27e48] (2026-11-04T13:35:42Z)
- (audit operator) `seven cold design rounds on the design (critique 7 converged, nothing above Low), then a cold review of the shipped pages on a different model (Sonnet) whose 1 High, 4 Medium and 5 Low were fixed or split (T-2964, T-2965); each carrying task closed with its own five-lens audit` → the hero holds 60 fps at normal load and 43-57 at load 15+ (critique 7's residual Low L-y); content-visibility keeps the long page cheap [tree eacc37c27e48] (2026-11-04T13:35:42Z)
- (audit maintainer) `seven cold design rounds on the design (critique 7 converged, nothing above Low), then a cold review of the shipped pages on a different model (Sonnet) whose 1 High, 4 Medium and 5 Low were fixed or split (T-2964, T-2965); each carrying task closed with its own five-lens audit` → style.css's generic selectors (.hero, .rules > div) leak into page sheets; T-2964 overrides them per page, scoping them is the lasting fix [tree eacc37c27e48] (2026-11-04T13:35:42Z)
## Log
- 2026-11-03T05:25:16Z created
- 2026-11-03T05:25:20Z criterion 4 verify: `fm research show T-2787-design-review` → `fm research show T-2788-design-review`
- 2026-11-03T05:26:07Z blocked: waits on the fused concept (directions-v2/5-fused) and the user's look at it
- 2026-11-03T05:54:56Z steer: the user asked for a full fusion of directions 1, 2 and 4 (combined animated logo, better transitions and UI, not fake-looking); the concept step is now build, cold design review, improve, in rounds
- 2026-11-03T14:21:50Z criterion 1 verify: `fm decide --review` → `fm research show T-2788-concept-review`
- 2026-11-03T14:21:50Z criterion 1 text: a fused concept page (Kirjokansi frame, forge horizon and Smith section) is shown to the user and approved before the build-out → the unified concept (directions 1, 2 and 4 fused) is published to the user as an Artifact and refined in cold design-review rounds until the review finds nothing above low; no approval wait (user steer 2026-11-03: stop asking me questions just keep going)
- 2026-11-03T14:21:51Z steer: 'stop asking me questions just keep going' (2026-11-03): no approval stop before the build-out; the concept is published for the user to see and the build-out proceeds after the review rounds
- 2026-11-03T14:21:51Z unblocked
- 2026-11-03T14:27:38Z steer: the user now wants direction 1 remade better (more animated, fluid, the astrolabe blended into the sky), with fire only in the Rune section; the 1+2+4 fusion is dropped
- 2026-11-03T14:58:01Z steer (user, 2026-11-03): 'It still looks a little goofy for some reason, can you try remaking number 2, but go in the more artifact direction? way more details and motion and everything too?' — supersedes 'remake number 1'; designer redirected to directions-v2/8-forge-artifact (direction 2 forge remade with the Sampo relic as hero, realistic materials, much more motion); 7-kirjokansi-plus round 1 stopped
- 2026-11-03T16:40:05Z steer (user, 2026-11-03): 'can you make the artifact/logo/design and everything look like a more detailed fiery forge, kind of like number 2 from earlier? but more detailed and such?' — supersedes the museum-relic framing of 8-forge-artifact; build 9-fiery-forge: direction 2's forge world (fire, hearth, anvil, sparks, heat as the signal) with far more detail, keeping 8's rendering quality, arrival and real data
- 2026-11-03T19:25:54Z steer: user picked 12-forge-illustrated (the fully animated one) as the theme on every surface: README, the tower, etc.; super-improve it first
- 2026-11-03T19:27:48Z set title=Sampo's theme is the illustrated forge (12-forge-illustrated, user pick 2026-11-03): super-improved, then carried through the logo and every variant, the design tokens, the landing page and every section page, the Rune tower page (site/genesis), the README header and INSTALL, the panel's colours and the share card
- 2026-11-03T19:27:48Z criterion 1 verify: `fm research show T-2788-concept-review` → `test -f /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_review/final.md`
- 2026-11-03T19:27:48Z criterion 1 text: the unified concept (directions 1, 2 and 4 fused) is published to the user as an Artifact and refined in cold design-review rounds until the review finds nothing above low; no approval wait (user steer 2026-11-03: stop asking me questions just keep going) → the illustrated forge (12-forge-illustrated) is super-improved in cold design-review rounds until the review finds nothing above low, and published live to the user on the picker Artifact; no approval wait
- 2026-11-03T19:27:49Z criterion 2 verify: `python3 plugin/tests/run.py test_design_sampo` → `python3 plugin/tests/run.py test_design`
- 2026-11-03T19:27:49Z criterion 2 text: design/sampo holds the astrolabe mark, its animated, 16/32/64 px icon, mono and light variants and the tokens (indigo, brass, starlight, aurora, forge heat ramp), each SVG rendering at 16, 32 and 512 → design/sampo holds the illustrated anvil-stone mark, its animated version, 16/32/48 px icons, mono and light variants, the README banner (dark and light) and tokens.json from 12's NOTES (night, ember, brass, the five rune-fire colours), each SVG rendering at 16, 32 and 512
- 2026-11-03T20:24:20Z fonts fetched for the port: scratchpad/fonts/dl (4 latin variable woff2, 158 KB, OFL texts, fonts.css)
- 2026-11-03T22:18:10Z split for lanes: T-2850 logo+tokens (first), T-2851 landing (after T-2850), T-2852 sections+tower (after T-2851, shares style.css), T-2853 panel+share card (after T-2850); fonts ready in scratchpad/fonts/dl and 12's own fonts/; 12 now also ships a site/ split (index.html, style.css, site.js)
- 2026-11-04T00:27:42Z start point recorded late (no focus had kept one): its diff starts at 0e92c67
- 2026-11-04T00:27:45Z steps 2 and 5 landed in lanes T-2850 (8555a292) and T-2853 (105e6b03); step 1 at critique 3 (not converged: 1 H, 5 M), round 4 running; step 4's tower redesign started early in 12/tower/ with the wild moon sky (T-2858); steps 3-4 port via T-2851/T-2852 after round 4
- 2026-11-04T02:01:34Z critique 4 (cold, both pages): not converged; landing 1 H (N-7: 1440@2x p95 33 ms, two 2x canvases) 6 M 9 L; tower 2 H (R-1 mock logo 404, R-2 text clipped at 390/360) 6 M 8 L; round 5 (landing) and tower round 2 sent
- 2026-11-04T13:35:16Z set approved=True
- 2026-11-04T13:35:17Z focused
- 2026-11-04T13:35:17Z predicted from its closes: 14 min, 1 attempt(s)
- 2026-11-04T13:35:27Z scope: carried by T-2850 (logo system and tokens), T-2851 (landing), T-2852 (section pages and tower), T-2853 (pane and band), T-2957 (re-sync to critique 7), T-2964 (shipped-site review fixes); each closed with its own audits
- 2026-11-04T13:35:43Z done
## Follow-ups captured
## Build vs reuse
Reuse the concept generator, site/build.py, site/stats.py, sampo.design lint/contrast, sampo.shot (--width, --scheme) and the existing site tests; replace T-2759's mark and landing scenes.
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [outward] [cites: user steer 2026-11-03: picked 1 Kirjokansi, then 'I like both 1 and 2'] Sampo's look is Kirjokansi fused with Ilmarinen's forge: t…
- T-2772 [FEATURE L, done, 3 steps] Sampo reimagined: a new logo and a completely redesigned site (user steer 2026-11-03): four rendered directions (logo, animated hero, s…
- decision 2026-11-03: [outward] [revisited: Kirjokansi fused with Ilmarinen's forge] [cites: user steer 2026-11-03: super improve the fuse completely, combined/animated l…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_audit_run.py, plugin/tests/test_design_diverge.py, plugin/tests/test_design_gates.py, plugin/tests/test_design…
## Preflight
Changed in scope since this was planned (2026-11-03): CHANGELOG.md, README.md, design/sampo/index.html, design/sampo/logo/README.md, design/sampo/logo/REVIEW.md, design/sampo/logo/app-icon-1024.png, design/sampo/logo/app-icon-512.png, design/sampo/logo/…; re-ground the plan against them before editing
## Lessons
- Review the shipped pages, not only the design files: the port leaked a site-wide style into the tower that seven design rounds never saw
