---
id: T-1653
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpage.py, plugin/lib/city.html, plugin/lib/fmcli.py, plugin/skills/playbooks/references/ui/templates, plugin/tests/test_showpieces.py, plugin/tests/helpers.py, plugin/tests/test_site_hero.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:58:35Z
updated: 2026-10-23T03:07:54Z
base: 08489a205a535196f28b8224743cb5f747ec9f62
base_tree: e51b49b4263e59758b4a1685d0899244a8294da2
plan0_at: 2026-10-23T02:08:33Z
plan0_scope: [plugin/lib/fmpage.py, plugin/skills/playbooks/references/ui/templates, plugin/tests/test_showpieces.py, CHANGELOG.md]
verified: strong
---
# The repo as a 3D city: one-file page from fm map data with a poster, aria-label and reduced-motion path
## Raw request
> The repo as a 3D city: one-file page from fm map data with a poster, aria-label and reduced-motion path
## Interpretation
fm page city builds a one-file 3D view of the repository: each file a building (height by lines, colour by recent churn) on blocks by folder, from fm map data; a poster first, an aria-label summarising the biggest areas, and a reduced-motion path with no camera drift. Built on the scene template.
## Assumptions (confidence)
## Acceptance criteria
- [x] the city page builds as one file from fixture data with a poster, aria-label and reduced-motion path — verify with `python3 plugin/tests/run.py test_showpieces.City`
## Non-goals
## Approach (options → choice → why)
Options: a 2D treemap (clear, no depth); a 3D city (memorable, shows churn and size together); a graph. Choice: the city, with the treemap's numbers in its aria-label and poster so nothing depends on seeing 3D.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] builder reusing templates/scene.html
3. [x] fixture data from fm map
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_showpieces.City` → ✗ exit 1 · Ran 7 tests in 5.6s (2 classes, 16 at a time; slowest: City 0s, CityBrowser 0s) / FAILED (2 classes) [ran] [tree 38279c4c5970] (2026-10-23T02:12:51Z)
- (step 2) `python3 plugin/tests/run.py -k test_showpieces` → exit 0 · Ran 10 tests in 24.0s (2 classes, 16 at a time; slowest: CityBrowser 24s, City 1s) / OK [ran] [tree 8d4d2bb169b9] (2026-10-23T02:24:23Z)
- (step 3) `python3 plugin/tests/run.py -k test_showpieces.City.test_fm_page_city_reads_the_repo_and_never_overwrites_a_foreign_file` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: City 1s) / OK [ran] [tree 8d4d2bb169b9] (2026-10-23T02:24:24Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces.City` → exit 0 · Ran 10 tests in 29.3s (2 classes, 16 at a time; slowest: CityBrowser 29s, City 1s) / OK [ran] [tree a826d0855eb3] (2026-10-23T02:30:01Z)
- (step 2) `python3 plugin/tests/run.py -k test_showpieces` → exit 0 · Ran 10 tests in 29.4s (2 classes, 16 at a time; slowest: CityBrowser 29s, City 1s) / OK [ran] [tree a826d0855eb3] (2026-10-23T02:30:30Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces.City` → exit 0 · Ran 19 tests in 32.4s (2 classes, 16 at a time; slowest: CityBrowser 32s, City 2s) / OK [ran] [tree b12dfdb1c946] (2026-10-23T02:57:48Z)
- (step 2) `python3 plugin/tests/run.py -k test_showpieces -k test_site_hero` → exit 0 · Ran 32 tests in 32.4s (4 classes, 16 at a time; slowest: CityBrowser 32s, Scene 26s, Hero 3s) / OK [ran] [tree b12dfdb1c946] (2026-10-23T02:58:26Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces test_site_hero` → exit 0 · Ran 32 tests in 32.1s (4 classes, 16 at a time; slowest: CityBrowser 32s, Scene 22s, Hero 3s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:05:44Z)
- (step 1) `python3 plugin/tests/run.py test_showpieces.City` → exit 0 · Ran 19 tests in 31.9s (2 classes, 16 at a time; slowest: CityBrowser 32s, City 1s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:06:23Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces.City` → exit 0 · Ran 19 tests in 31.9s (2 classes, 16 at a time; slowest: CityBrowser 32s, City 1s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:06:56Z)
- (audit intent) `fm-reviewer pass (shared with T-1642); MEDIUMs fixed test-first: the intro lasts 4.5 s and the first input ends it; a failed git log says history unavailable and --relative gets a subfolder project's churn; a hostile directory and hottest-file name now reach and are escaped in label, twin, poster and JSON; LOWs: rise from the poster's framing, a turn hint and grab cursor, a 256 MB read budget, Leak names the path, shared test helpers` → fm page city writes the repo as a one-file 3D city at dusk: files as buildings sized by lines with windows lit by commits, districts per folder, an isometric SVG poster first [tree dc2f7fc78782] (2026-10-23T03:06:56Z)
- (audit adversary) `fm-reviewer pass (shared with T-1642); MEDIUMs fixed test-first: the intro lasts 4.5 s and the first input ends it; a failed git log says history unavailable and --relative gets a subfolder project's churn; a hostile directory and hottest-file name now reach and are escaped in label, twin, poster and JSON; LOWs: rise from the poster's framing, a turn hint and grab cursor, a 256 MB read budget, Leak names the path, shared test helpers` → names reach HTML, SVG and JSON escaped (tested with hostile names); absolute paths refused; no external host [tree dc2f7fc78782] (2026-10-23T03:06:56Z)
- (audit edge) `fm-reviewer pass (shared with T-1642); MEDIUMs fixed test-first: the intro lasts 4.5 s and the first input ends it; a failed git log says history unavailable and --relative gets a subfolder project's churn; a hostile directory and hottest-file name now reach and are escaped in label, twin, poster and JSON; LOWs: rise from the poster's framing, a turn hint and grab cursor, a 256 MB read budget, Leak names the path, shared test helpers` → reduced motion and no WebGL2 keep the poster with no context; context loss restores; draws nothing after the intro until input; history failure is said [tree dc2f7fc78782] (2026-10-23T03:06:56Z)
- (audit design) `fm-reviewer pass (shared with T-1642); MEDIUMs fixed test-first: the intro lasts 4.5 s and the first input ends it; a failed git log says history unavailable and --relative gets a subfolder project's churn; a hostile directory and hottest-file name now reach and are escaped in label, twin, poster and JSON; LOWs: rise from the poster's framing, a turn hint and grab cursor, a 256 MB read budget, Leak names the path, shared test helpers` → a dusk palette, old-style serif with mono and a commit heat ramp, not a stock demo; motion within the 5 s budget with input ending it [tree dc2f7fc78782] (2026-10-23T03:06:56Z)
## Log
- 2026-10-22T20:58:35Z created
- 2026-10-22T20:58:36Z set scope=['plugin/lib/fmpage.py', 'plugin/skills/playbooks/references/ui/templates', 'plugin/tests/test_showpieces.py', 'CHANGELOG.md']
- 2026-10-22T20:58:37Z split from T-1542 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:00Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_showpieces.City`
- 2026-10-22T21:30:23Z criterion 1 text: the city page builds as one file from fixture data with a poster, aria-label and reduced-motion path — verify with python3 plugin/tests/run.py test_showpieces.City → the city page builds as one file from fixture data with a poster, aria-label and reduced-motion path
- 2026-10-23T02:08:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1653.builder.md
- 2026-10-23T02:08:33Z focused
- 2026-10-23T02:16:16Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/city.html', 'plugin/lib/fmcli.py', 'plugin/skills/playbooks/references/ui/templates', 'plugin/tests/test_showpieces.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T02:49:57Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/city.html', 'plugin/lib/fmcli.py', 'plugin/skills/playbooks/references/ui/templates', 'plugin/tests/test_showpieces.py', 'plugin/tests/helpers.py', 'plugin/tests/test_site_hero.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T03:04:18Z merged worktree-agent-a4d47bbd2c1133890 (8 file(s))
- 2026-10-23T03:04:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4d47bbd2c1133890
- 2026-10-23T03:05:10Z focused
- 2026-10-23T03:05:44Z scope: plugin/lib/city.html, plugin/tests/helpers.py (SPY/devtools shared), test_site_hero.py, fmcli page arg, MASTER.md
- 2026-10-23T03:07:54Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1654 [FEATURE M, planned, 3 steps] Live task graph showpiece: a one-file 3D page of the task graph, held to the same checks
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- T-1610 [FEATURE M, done, 3 steps] Site hero scene: a single-file WebGL2 proof-chain scene over the poster (tasks as stations, red to green as light along the track), fro…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_page.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/city.html, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/skills/playbooks/references/ui/templates/scene.html, plugin/tests/helpers.py, plugin/tests/test_showpi…; re-ground the plan against them before editing
## Lessons
- An escaping test must make the hostile value actually reach the output, or it proves nothing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_showpieces.py
- plugin/lib/fmpage.py
- plugin/lib/fmcli.py
- plugin/lib/city.html
- MASTER.md
- CHANGELOG.md
- plugin/commands/settings.md
- plugin/lib/fmcost.py
- plugin/lib/fmdesign.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmflow.py
- plugin/lib/fmhooks.py
- plugin/lib/fmroll.py
- plugin/lib/fmsettings.py
- plugin/lib/fmshot.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/fixtures/design-surfaces/DESIGN.md
- plugin/tests/test_control_room.py
- plugin/tests/test_design_gates.py
- plugin/tests/test_design_surfaces.py
- plugin/tests/test_design_tokens.py
- plugin/tests/test_docs.py
- plugin/tests/test_doctor.py
- plugin/tests/test_flow.py
- plugin/tests/test_fmshot.py
- plugin/tests/test_hooks.py
- plugin/tests/test_looks_gallery.py
- plugin/tests/helpers.py
- plugin/tests/test_site_hero.py
- plugin/lib/fmcodetui.py
