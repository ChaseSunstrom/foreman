---
id: T-2767
type: FEATURE
tier: M
status: done
priority: normal
scope: [site/pages.py, site/build.py, site/stats.py, site/style.css, site/site.js, site/data/*, site/assets/*, plugin/tests/test_site_sections.py, plugin/tests/test_rename_scan.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-03T04:17:53Z
updated: 2026-11-03T16:42:04Z
builder_model: sonnet
base: 3a5ef9586abf05a2b4c98369c4062bacba3f68ed
base_tree: e3b71277c7297c1605796d9b6d0e82e2352bb152
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-03T04:18:20Z
plan0_scope: [site/pages.py, site/build.py, site/stats.py, site/style.css, site/site.js, site/data/*, site/assets/*, plugin/tests/test_site_sections.py, plugin/tests/test_rename_scan.py, CHANGELOG.md]
lane_stop: merged 2026-11-03T05:18:43Z
verified: strong
unproven: [ui-unshot]
---
# Louhi, Moons and Underworld pages from the tower's real records (T-2742 step 7c-1): Louhi's scorecard from exam.jsonl, the Moons catalogue from moonshot.md with each moon's stage, the Underworld from not-yet.md; each with its scroll scene (Louhi's trials, moons forged, the underworld's waiting runes), shader background and dials of real numbers only, in Sampo's design system
## Raw request
> Louhi, Moons and Underworld pages from the tower's real records (T-2742 step 7c-1): Louhi's scorecard from exam.jsonl, the Moons catalogue from moonshot.md with each moon's stage, the Underworld from not-yet.md; each with its scroll scene (Louhi's trials, moons forged, the underworld's waiting runes), shader background and dials of real numbers only, in Sampo's design system
## Interpretation
Reading 1 (chosen): SAMPO.md's site list names a Louhi scorecard, Moons and Underworld page, with scroll scenes (Louhi's trials, moons forged) and shaders, gears and dials as live data that is never invented. The tower already holds the records: state/projects/<id>/research/genesis/exam.jsonl (89 exam runs: keyed, found, false_alarms, brier_sum, scenarios …), moonshot.md (the M-NN catalogue: tier, domain, stage idea|kill|…, needs, kill test, evidence) and not-yet.md (ideas waiting on a blocker: blocker, tried, unblocks-with, added/retried). site/stats.py already reads state (models() reads exam.jsonl) into site/data/stats.json; site/pages.py holds the pages as blocks; site/build.py renders them and has T-2759's dials (log10 needle from --v) and site.js has fire(), the WebGL shader with a CSS still. Build the three pages as feature pages in that system: each figure from stats.json, each scene still under reduced motion, whole without JS. The pages say Louhi, Moons and Underworld; commands on them use the sampo verbs (sampo louhi, sampo moons, sampo underworld). Reading 2 (ruled out): pages that fetch the tower files at view time with JS. That fails 'works without JS'.
## Assumptions (confidence)
## Acceptance criteria
- [x] the Louhi, Moons and Underworld pages build from the tower's files (exam.jsonl, moonshot.md, not-yet.md through stats.py into stats.json), and other records give other numbers: nothing is typed into a page — verify with `python3 plugin/tests/run.py test_site_sections`
- [x] each page meets SAMPO.md's quality bar: no other hosts, a reduced-motion still for each scene, whole with JS off, light and dark, 320 px, AA contrast, fm design lint — verify with `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo`
- [x] the site's own suites and the rename ratchet stay green — verify with `python3 plugin/tests/run.py test_site test_site_build test_site_sampo test_rename_scan`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: extend stats.py with louhi(), moons() and underworld() collectors (pure functions over the files, unit-tested with fixtures), add three PAGES entries with block types build.py already renders (tiles, tables, prose) plus one scene block each, and reuse fire() and the dial markup for the shader and gauges. Likely outcome: about 300 lines plus tests, consistent with the landing. Fails if: a page needs a block type build.py lacks; then add the smallest one.
2. Hand-write three standalone HTML pages like site/genesis/index.html. Fails if: they drift from the design system and the nav, and their numbers would be typed or need JS.
3. Do less: one 'Tower' page with three sections. Fails if: SAMPO.md lists each as its own page.
Choice 1 (80%).
## Risks and rollback
Blast radius (fm graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py; past FIXes T-1129, T-1131, T-1132, T-1133, T-1134.
## Execution prompt
## Steps
1. [x] red tests in test_site_sections: each page exists in the nav, renders figures from a fixture stats.json (changing the fixture changes the page), meets the quality bar checks test_site_landing already makes
2. [x] stats.py collects louhi (runs, scenarios, found/keyed, false alarms, brier, per-generation trend), moons (each moon's id, title, tier, stage, needs) and underworld (each idea, blocker, tries); pages.py and build.py render them
3. [x] the three scroll scenes and shader backgrounds, reusing T-2759's fire() and dial patterns; screenshots at 1280, 768 and 320, light and dark, still and moving; a CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-03T04:46:33Z step 2/3: stats.py collects louhi (runs, scenarios, found/keyed, false alarms, brier, per-generation trend), moons (each moon's id, title, tier, stage, needs) and underworld (each idea, blocker, tries); pages.py and build.py render them
- git: worktree-agent-aa7e0d7390af3478d; 5 uncommitted: site/build.py, site/data/stats.json, site/pages.py, site/stats.py, plugin/tests/test_site_sections.py
- touched since last checkpoint: site/pages.py
## Docs impact
none: the pages are the docs
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_site_sections 2>&1 | tail -30` → ✗ exit 1 · Ran 5 tests in 7.2s (3 classes, 16 at a time; slowest: Built 2s, Collect 0s, Pages 0s) / FAILED (3 classes: test_site_sections.Pages, test_site_sections.Built, test_site_sections.Collect) [ran] [tree fe7007e1c79c] [world 2f1906870a] (2026-11-03T04:38:26Z)
- (step 1) `python3 plugin/tests/run.py test_site_sections` → ✗ exit 1 · Ran 5 tests in 3.7s (3 classes, 16 at a time; slowest: Built 3s, Collect 0s, Pages 0s) / FAILED (3 classes: test_site_sections.Pages, test_site_sections.Built, test_site_sections.Collect) [ran] [tree fe7007e1c79c] [world 2f1906870a] (2026-11-03T04:38:33Z)
- (step 2) `python3 plugin/tests/run.py test_site_sections.Collect test_site_sections.Pages` → exit 0 · Ran 12 tests in 0.3s (2 classes, 16 at a time; slowest: Pages 0s, Collect 0s) / OK [ran] [tree 97dc62e0a1d1] [world 2f1906870a] (2026-11-03T04:48:35Z)
- (step 3) `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo` → exit 0 · Ran 35 tests in 9.2s (6 classes, 16 at a time; slowest: Built 9s, Landing 4s, Built 0s) / OK [ran] [tree 799e0ce6cddb] [world 2f1906870a] (2026-11-03T04:49:53Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_goal test_map test_moonshot test_motion_verify test_replay test_sampo_design test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 664 tests in 31.7s (135 classes, 16 at a time; slowest: GenerationReview 24s, GenesisRead 23s, GenesisCheck 16s) / FAILED (1 classes: test_docs.Site) [ran] [tree 799e0ce6cddb] [world 2f1906870a] (2026-11-03T04:50:44Z)
- (step 3) `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo` → exit 0 · Ran 35 tests in 8.7s (6 classes, 16 at a time; slowest: Built 8s, Landing 4s, Built 0s) / OK [ran] [tree 3d52057fb301] [world 2f1906870a] (2026-11-03T04:51:39Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_goal test_map test_moonshot test_motion_verify test_replay test_sampo_design test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [27.33s] [ran] [tree 3d52057fb301] [world 2f1906870a] (2026-11-03T04:53:04Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sections` → exit 0 · Ran 18 tests in 8.6s (3 classes, 16 at a time; slowest: Built 8s, Pages 0s, Collect 0s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:25:35Z)
- (ac 2) `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo` → exit 0 · Ran 35 tests in 8.7s (6 classes, 16 at a time; slowest: Built 8s, Landing 4s, Built 0s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:25:35Z)
- (ac 3) `python3 plugin/tests/run.py test_site test_site_build test_site_sampo test_rename_scan` → exit 0 · Ran 75 tests in 8.8s (28 classes, 16 at a time; slowest: Built 8s, Header 5s, Landing 5s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:25:35Z)
- (step 1) `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo test_site test_site_build` → exit 0 · Ran 72 tests in 9.0s (27 classes, 16 at a time; slowest: Built 9s, Header 5s, Landing 5s) / OK [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:25:35Z)
- (audit intent) `self: read the merged diff; pages escape record text and say Sampo` → Louhi, Moons and Underworld pages are built from the tower's own records with real-number dials [tree 981c9f062662] (2026-11-03T16:25:35Z)
- (audit edge) `self: read the merged diff; pages escape record text and say Sampo` → missing records give an empty page with a sentence; scenes cap at 60 marks; idea names already public in CHANGELOG/MASTER [tree 981c9f062662] (2026-11-03T16:25:35Z)
- (audit adversary) `self: read the merged diff; pages escape record text and say Sampo` → every record string goes through esc() after _say(); no record text reaches a script or attribute unescaped [tree 981c9f062662] (2026-11-03T16:25:35Z)
- `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo test_site test_site_build` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:25:35Z [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:26:27Z)
- (audit intent) `self: read the merged diff; pages escape record text and say Sampo` → Louhi, Moons and Underworld pages are built from the tower's own records with real-number dials [tree 981c9f062662] (2026-11-03T16:26:27Z)
- (audit edge) `self: read the merged diff; pages escape record text and say Sampo` → missing records give an empty page with a sentence; scenes cap at 60 marks; idea names already public in CHANGELOG/MASTER [tree 981c9f062662] (2026-11-03T16:26:27Z)
- (audit adversary) `self: read the merged diff; pages escape record text and say Sampo` → every record string goes through esc() after _say(); no record text reaches a script or attribute unescaped [tree 981c9f062662] (2026-11-03T16:26:27Z)
- `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo test_site test_site_build` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:26:27Z [ran] [tree 981c9f062662] [world 2f1906870a] (2026-11-03T16:27:19Z)
- (audit intent) `self: read the merged diff; pages escape record text and say Sampo` → Louhi, Moons and Underworld pages are built from the tower's own records with real-number dials [tree 981c9f062662] (2026-11-03T16:27:19Z)
- (audit edge) `self: read the merged diff; pages escape record text and say Sampo` → missing records give an empty page with a sentence; scenes cap at 60 marks; idea names already public in CHANGELOG/MASTER [tree 981c9f062662] (2026-11-03T16:27:19Z)
- (audit adversary) `self: read the merged diff; pages escape record text and say Sampo` → every record string goes through esc() after _say(); no record text reaches a script or attribute unescaped [tree 981c9f062662] (2026-11-03T16:27:19Z)
- `python3 plugin/tests/run.py test_site_sections test_site_landing test_site_sampo test_site test_site_build` → exit 0 · Ran 72 tests in 9.1s (27 classes, 16 at a time; slowest: Built 9s, Header 5s, Landing 5s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:41:24Z)
- (audit intent) `self: read the merged diff; pages escape record text and say Sampo` → Louhi, Moons and Underworld pages are built from the tower's own records with real-number dials [tree 398b4aa61509] (2026-11-03T16:41:24Z)
- (audit edge) `self: read the merged diff; pages escape record text and say Sampo` → missing records give an empty page with a sentence; scenes cap at 60 marks; idea names already public in CHANGELOG/MASTER [tree 398b4aa61509] (2026-11-03T16:41:24Z)
- (audit adversary) `self: read the merged diff; pages escape record text and say Sampo` → every record string goes through esc() after _say(); no record text reaches a script or attribute unescaped [tree 398b4aa61509] (2026-11-03T16:41:24Z)
## Log
- 2026-11-03T04:17:53Z created
- 2026-11-03T04:18:06Z set approved=True
- 2026-11-03T04:18:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2767.builder.md
- 2026-11-03T04:18:19Z focused
- 2026-11-03T04:18:20Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T05:18:43Z merged worktree-agent-aa7e0d7390af3478d (7 file(s))
- 2026-11-03T05:20:45Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa7e0d7390af3478d
- 2026-11-03T05:59:44Z focused
- 2026-11-03T14:22:10Z paused: focus moved to T-2775
- 2026-11-03T15:07:37Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T15:07:37Z focused
- 2026-11-03T15:07:38Z paused: focus moved to T-2768
- 2026-11-03T16:24:56Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T16:24:56Z focused
- 2026-11-03T16:25:31Z paused: focus moved to T-2814
- 2026-11-03T16:30:31Z scope: .fm-scratch/merge_tower.py was a builder's scratch file (no commit holds it, not in the tree); the plugin/evals prompt.md files came in with the T-2812 merge, not this task's edits
- 2026-11-03T16:41:12Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T16:41:12Z focused
- 2026-11-03T16:42:04Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2759 [FEATURE M, done, 4 steps] The landing page in the forge world (T-2742 step 7b): a hero where the Sampo mill turns and runes write themselves into the headline ov…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-1784 [FEATURE M, done, 4 steps] Shader sketchbook: one page of live thumbnails, one per shader card (looks/shader-*.md), e — lesson: author CSS display:block silently …
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/tests/test_rename_scan.py, plugin/tests/test_site_sections.py, site/build.py, site/data/stats.json, site/pages.py, site/site.js, site/stats.py, site/style.css; re-ground the plan against them before editing
## Lessons
- Publish only what the record holds, escaped
## Plan gaps
- failed first: step 1 red tests in test_site_sections: each page exists in the nav, renders figures from a fixture stats.…
## Files touched
- plugin/tests/test_site_sections.py
- site/stats.py
- .fm-scratch/merge_tower.py
- site/data/stats.json
- site/build.py
- site/pages.py
- site/style.css
- site/site.js
- plugin/tests/test_rename_scan.py
