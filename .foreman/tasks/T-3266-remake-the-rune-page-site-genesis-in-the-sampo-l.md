---
id: T-3266
type: FEATURE
tier: M
status: active
priority: normal
scope: [site/genesis/, plugin/lib/sampo/rune.py, plugin/lib/sampo/kalevala.py, plugin/tests/test_site*.py, plugin/tests/test_rune*.py, plugin/tests/genesis_page.js, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:19:24Z
updated: 2026-11-06T05:36:43Z
base_note: 
builder: 2026-11-06T02:22:35Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a6b595b832d51ef5d
lane_branch: worktree-agent-a6b595b832d51ef5d
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:22:47Z
plan0_scope: [site/genesis/, plugin/lib/sampo/rune.py, plugin/lib/sampo/kalevala.py, plugin/tests/test_site*.py, plugin/tests/test_rune*.py, CHANGELOG.md]
---
# Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts
## Raw request
> Remake the Rune page (site/genesis) in the Sampo look with Kalevala: every tower, the meta-generations and Väinämöinen's acts
## Interpretation
- The user asked (2026-11-06): "can you remake the rune page with the kalevala? etc.?" The Rune page is site/genesis/index.html (genesis.js + genesis.css render site/genesis/genesis.json, written by rune.export). Today it has hero, tower, caps, moons, louhi and docs sections and knows nothing of Kalevala.
- Kalevala (T-3050/T-3081/T-3082, "the genesis of genesis") now has 26 towers, one per aspect (sampo kalevala status), its own generations under research/genesis/kalevala/gen-N, and Väinämöinen's acts (kalevala.acts: act, tower, reason, undo). The page must show all of it: a towers grid (aspect, generation, stage, exam score trend, stuck/paused, spend today), Kalevala's generations (tower set, verdict, seed base), and the latest acts with their reasons.
- "Remake" means the whole page, not a section bolted on: the same Sampo look as the README figures (demo/figures, T-3247) and the live page's modern dashboard (T-3054: modern charts by default, the forge only as a setting), both themes, phone width. Keep every existing section's content (generations, capabilities, coverage, moons sky, exam, docs), restyled.
- "etc." covers the rest of Rune's state the page doesn't show well yet: the moons funnel at scale (moons_scale: candidates, kept per stage toward 10,000) and the root genesis's next step.
- Data only from genesis.json (rune.export gains a kalevala block); no hand-typed numbers. Towers with no data yet (gen 0, unscored) render an honest empty state, not zeros dressed as results.

Reading 1 (chosen): remake the whole Rune page in the current Sampo look, with Kalevala as a first-class part of it. Reading 2 (ruled out): add a Kalevala section to the page as it is; ruled out because "remake" and the README/live-page restyle the user just asked for point at the whole page.
## Assumptions (confidence)
## Acceptance criteria
- [ ] The Rune page shows Kalevala: each tower's aspect, generation, stage, exam trend and stuck/paused state; Kalevala's own generations; Väinämöinen's latest acts with reasons and undo — verify with `python3 plugin/tests/run.py test_site`
- [ ] Built from genesis.json (export carries a kalevala block), no hand-typed numbers — verify with `python3 plugin/tests/run.py test_site`
- [ ] Same look as the README figures and live page (modern charts, both themes, phone width), existing Rune content kept — verify with `python3 demo/shot.py --help`
## Non-goals
## Approach (options → choice → why)
1. Restyle in place: keep genesis.js's structure, add a Kalevala section and swap the CSS to the Sampo tokens. Likely outcome: fastest, but the forge-era layout and the new dashboard look fight each other; fails if the user reads it as "not remade".
2. Rebuild the page on the live page's chart kit (T-3092's small kit) and the README figure palette: new layout (overview tiles, Kalevala towers grid, generations timeline, acts feed, then the existing sections restyled), genesis.js rewritten around one render function per section. Likely outcome: one coherent look, Kalevala first-class, about the size of today's JS.
3. Server-rendered static HTML from build.py (no JS rendering). Likely outcome: simplest runtime, but loses the page's live refresh and filtering; fails if genesis.json updates between builds are expected to show without a rebuild.

4. Do less: only add a Kalevala section to today's page. Likely outcome: Kalevala visible today; fails if the user meant the restyle too, which "remake" says they did.

Choice 2 (85%): the user asked for a remake in the Sampo look with charts; option 1 is a patch and option 3 drops behaviour the page has. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_genesis.py, plugin/lib/fmgenesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] Export: genesis.json gains a kalevala block (towers, gens, acts) from kalevala.tower_rows/acts
2. [x] Page: remake genesis/index.html + genesis.js/css in the Sampo look with the Kalevala sections and charts
3. [x] Shots light/dark/phone; test_site covers the new block
## Resume here
<!-- auto -->
- 2026-11-06T05:21:46Z steps 3/3 done
- git: worktree-agent-a6b595b832d51ef5d; 6 uncommitted: plugin/lib/sampo/rune.py, plugin/tests/genesis_page.js, plugin/tests/test_site.py, site/genesis/genesis.css, site/genesis/genesis.js, site/genesis/index.html
- touched since last checkpoint: .fm-scratch/demo/m.html, plugin/tests/genesis_page.js, .fm-scratch/commit-msg.txt, .fm-scratch/lint-fix.json, site/genesis/genesis.css
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_site` → exit 0 · Ran 96 tests in 34.3s (44 jobs, 16 at a time; slowest: Built 33s, Landing 20s, CardsPage 20s) / OK [ran] [tree 8d72d59fca16] [world 2f1906870a] (2026-11-06T02:34:26Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_site` → exit 0 · Ran 98 tests in 159.9s (56 jobs, 2 at a time; slowest: CardsPage 34s, Built 28s, Session 26s) / OK [ran] [tree d0e3003caf58] [world 2f1906870a] (2026-11-06T05:04:22Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_site_sampo test_site` → exit 0 · Ran 98 tests in 239.7s (51 jobs, 2 at a time; slowest: Built 115s, Landing 81s, CardsPage 72s) / OK [ran] [tree 2e365185b1ed] [world 2f1906870a] (2026-11-06T05:17:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1083 tests in 693.7s (346 jobs, 2 at a time; slowest: Ship 123s, GenesisRead 85s, GenerationReview 66s) / FAILED (2 classes: test_doctor.Checks, test_design_lint.Site) [ran] [tree 2e365185b1ed] [world 2f1906870a] (2026-11-06T05:18:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1083 tests in 614.1s (485 jobs, 2 at a time; slowest: GenesisCheck 58s, GenesisLive 52s, ProofBeforePresentation 42s) / FAILED (1 classes: test_doctor.Checks) [ran] [tree dfa6b205b077] [world 2f1906870a] (2026-11-06T05:32:03Z)
## Log
- 2026-11-06T02:19:24Z created
- 2026-11-06T02:19:27Z criterion 3 verify: `python3 plugin/tests/shot.py site/genesis/index.html` → `python3 demo/shot.py --help`
- 2026-11-06T02:22:27Z set scope=['site/genesis/', 'plugin/lib/sampo/rune.py', 'plugin/lib/sampo/kalevala.py', 'plugin/tests/test_site*.py', 'plugin/tests/test_rune*.py', 'CHANGELOG.md']
- 2026-11-06T02:22:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3266.builder.md
- 2026-11-06T02:22:45Z focused
- 2026-11-06T02:22:47Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:28:10Z steer (user): keep the tower look for the root genesis; Kalevala drawn as a city / tower of towers; a switch with a transition between the initial genesis and the genesis of genesis
- 2026-11-06T02:28:34Z steer: user likes the current tower look on the Rune page; keep it for the root genesis. Kalevala gets its own view drawn as a city / tower of towers (one tower per aspect, sized/lit by generation and state, root tower at the centre), and a Genesis ⇄ Kalevala switch with an animated transition (the tower pulls back into the skyline), kept in the URL hash, keyboard accessible, prefers-reduced-motion respected, both themes, phone width
- 2026-11-06T02:56:58Z set scope=['site/genesis/', 'plugin/lib/sampo/rune.py', 'plugin/lib/sampo/kalevala.py', 'plugin/tests/test_site*.py', 'plugin/tests/test_rune*.py', 'plugin/tests/genesis_page.js', 'CHANGELOG.md']
- 2026-11-06T02:57:01Z scope: + plugin/tests/genesis_page.js, the stub DOM test_site/test_genesis drive the page through (its kalevala mode)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-3247 [FEATURE M, done, 5 steps] README figures (T-3245 part 1): demo/readme_figures.py draws every README table and four real-data charts as light and dark SVGs in Sam…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
