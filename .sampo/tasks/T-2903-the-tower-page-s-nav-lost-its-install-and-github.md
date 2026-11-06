---
id: T-2903
type: FIX
tier: M
status: active
priority: normal
scope: [site/build.py, site/pages.py, site/index.html, site/genesis/index.html, plugin/tests/test_site_build.py]
depends_on: []
source: discovered
created: 2026-11-04T06:16:56Z
updated: 2026-11-06T10:45:34Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ad440d037d8d8e20b
lane_branch: worktree-agent-ad440d037d8d8e20b
base: 177fdfc5a8e5cb46c67896101e880f3b96caa9c3
base_tree: d5305a9a01fce005ed7d8914ad0390e51f6ddf69
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T10:24:13Z
plan0_scope: [site/build.py, site/pages.py, site/index.html, site/genesis/index.html, plugin/tests/test_site_build.py]
builder_returned: 2026-11-06T10:45:34Z
---
# One shared nav for the landing, the tower and the section pages, with Install and GitHub back on the tower
## Raw request
> FIX: the tower page's nav lost its Install and GitHub links when it was matched to the landing's; give the landing, the tower and the section pages one shared nav
## Interpretation
Reading 1 (chosen): the site's main nav comes from one list in site/build.py (label, href, and which page marks it current), rendered into the landing (site/index.html), the tower (site/genesis/index.html) and every section page, so Install and GitHub show on all and a new page (Cards, Works) is one entry. Reading 2: patch the tower's two links back; rejected, the three navs drifted once and will again.
## Assumptions (confidence)
## Acceptance criteria
- [ ] every built page's main nav has the same links in the same order, Install and GitHub included, from one NAV list in build.py; the current page is marked — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: build.py's section-page template already renders a nav; lift it into one NAV list and a render function the landing and tower builds call; likely outcome: one place to edit. 2. Do less: add the two links to the tower by hand; fails if: the next page drifts. 3. A client-side nav include in JS; fails if: a static page without JS loses its nav. Choice 1 (85%)
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, MASTER.md, site/genesis/genesis.js, plugin/tests/test_genesis.py, site/style.css; past FIXes T-2060, T-2061, T-2064, T-2087, T-2204.
## Execution prompt
## Steps
1. [ ] failing test: the landing's, the tower's and a section page's main nav links are equal and include Install and GitHub  <- CURRENT
2. [x] the NAV list and its render in build.py, used by the three builds
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_site_build.SharedNav test_site_build.CardsPage test_site_sections.Pages` → exit 0 · Ran 15 tests in 20.8s (3 jobs, 16 at a time; slowest: CardsPage 14s, SharedNav 1s, Pages 0s) / OK [ran] [tree f6faacfd0119] [world 2f1906870a] (2026-11-06T10:25:55Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.SharedNav` → exit 0 · Ran 1 tests in 90.5s (1 jobs, 16 at a time; slowest: SharedNav 1s) / OK [ran] [tree f6faacfd0119] [world 2f1906870a] (2026-11-06T10:27:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1081 tests in 153.8s (227 jobs, 16 at a time; slowest: Ship 37s, ProofBeforePresentation 13s, CardsPage 12s) / FAILED (4 classes: test_docs.Site, test_genesis.GenesisExport, test_docs.PluginFiles, [ran] [tree f6faacfd0119] [world 2f1906870a] (2026-11-06T10:30:05Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.SharedNav test_site_sections.Built test_docs.Site test_genesis.GenesisExport` → exit 0 · Ran 37 tests in 9.8s (4 jobs, 16 at a time; slowest: Built 9s, GenesisExport 6s, Site 1s) / OK [ran] [tree 59c5e3abb64c] [world 2f1906870a] (2026-11-06T10:44:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1081 tests in 34.9s (282 jobs, 16 at a time; slowest: ProofBeforePresentation 24s, GenerationReview 23s, GenesisRead 15s) / FAILED (2 classes: test_docs.MapShards, test_docs.PluginFiles) [ran] [tree 59c5e3abb64c] [world 2f1906870a] (2026-11-06T10:45:21Z)
## Log
- 2026-11-04T06:16:56Z created
- 2026-11-05T03:33:45Z planned from capture
- 2026-11-05T03:33:46Z set approved=True
- 2026-11-05T03:33:46Z set scope=['site/build.py', 'site/pages.py', 'site/index.html', 'site/genesis/index.html', 'plugin/tests/test_site_build.py']
- 2026-11-05T03:33:46Z blocked: approved; builder slot after T-3093's merge (site/pages.py); before T-3101, whose Cards page adds one nav entry
- 2026-11-06T03:53:37Z unblocked
- 2026-11-06T10:24:12Z focused
- 2026-11-06T10:24:13Z predicted from its closes: 6 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2957 [FEATURE M, done, 3 steps] Re-sync site/ to the converged illustrated forge (critique 7 converged: landing round 7, tower round 4): the redrawn eight stations as …
- T-2852 [FEATURE M, done, 3 steps] Port 12's look to every section page (site/pages.py's template and blocks) and the Rune tower (site/genesis: index.html, genesis.css, g…
- research mission-20261029-233102.pack: Genesis Mission 2 (#13 Genesis as a feature): fm genesis runs the whole tower by itself in any project — writes its own gen-0 from…
- decision 2026-10-30: [cites: user steer 2026-10-30: have your stuff automatically update the site] [check: python3 plugin/tests/run.py test_genesis.GenesisLive] Standing…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
## Preflight
Changed in scope since this was planned (2026-11-04): plugin/tests/test_site_build.py, site/build.py, site/genesis/index.html, site/index.html, site/pages.py; re-ground the plan against them before editing
