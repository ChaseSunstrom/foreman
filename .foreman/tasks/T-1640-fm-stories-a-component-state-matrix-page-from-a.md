---
id: T-1640
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmstories.py, plugin/lib/fmcli.py, plugin/lib/fmflow.py, plugin/tests/test_stories.py, plugin/tests/test_flow.py, MASTER.md, plugin/skills/ui-design/SKILL.md, CHANGELOG.md]
depends_on: [T-1639]
source: user
created: 2026-10-22T20:57:57Z
updated: 2026-10-23T03:28:21Z
base: 62e809ada378a86a60b88f973c892bf0979ed66e
base_tree: 4ab04f40f69247c90a06e28c3e9a264cab8fc38a
plan0_at: 2026-10-23T02:43:13Z
plan0_scope: [plugin/lib/fmflow.py, plugin/lib/fmcli.py, plugin/tests/test_flow.py, CHANGELOG.md]
verified: strong
---
# fm stories: a component state-matrix page from a state-chart file listing the states to shoot
## Raw request
> fm stories: a component state-matrix page from a state-chart file listing the states to shoot
## Interpretation
fm stories CHART builds one page showing a component in every state a state-chart file lists (default, hover, focus, error, empty, loading…), one cell per state, for review and for fm shot. The chart names the component's page and how to put it into each state (a query string, a class, a journey).
## Assumptions (confidence)
## Acceptance criteria
- [x] a chart of 3 states builds a page with 3 cells — verify with `python3 plugin/tests/run.py test_stories`
## Non-goals
## Approach (options → choice → why)
Options: Storybook (a large dependency); a generated static page with one iframe per state; screenshots only. Choice: the generated page: no dependency, works with fm shot, reviewers see live states.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] chart format
3. [x] page builder
## Resume here
## Docs impact
plugin/skills/ui-design/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_stories` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 2.8s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 1f6a28143f92] (2026-10-23T02:46:13Z)
- (step 2) `python3 plugin/tests/run.py test_stories.Untrusted test_flow.Untrusted` → exit 0 · Ran 12 tests in 26.9s (2 classes, 16 at a time; slowest: Untrusted 27s, Untrusted 21s) / OK [ran] [tree 659db8519150] (2026-10-23T02:52:11Z)
- (step 3) `python3 plugin/tests/run.py test_stories` → exit 0 · Ran 10 tests in 21.8s (3 classes, 16 at a time; slowest: Stories 21s, Untrusted 20s, InABrowser 5s) / OK [ran] [tree 659db8519150] (2026-10-23T02:52:35Z)
- (step 3) `python3 plugin/tests/run.py test_stories test_flow.Untrusted` → ✗ exit 1 · Ran 21 tests in 21.4s (4 classes, 16 at a time; slowest: Stories 21s, Untrusted 15s, Untrusted 13s) / FAILED (2 classes) [ran] [tree c61bc6688707] (2026-10-23T03:10:01Z)
- (step 3) `python3 plugin/tests/run.py test_stories test_flow` → exit 0 · Ran 34 tests in 21.8s (7 classes, 16 at a time; slowest: Stories 21s, Untrusted 18s, Untrusted 17s) / OK [ran] [tree 33fd87b4af4b] (2026-10-23T03:12:12Z)
- (ac 1) `python3 plugin/tests/run.py test_stories test_flow` → exit 0 · Ran 34 tests in 18.6s (7 classes, 16 at a time; slowest: Stories 18s, Journey 11s, Untrusted 10s) / OK [ran] [tree 75dc9b1b7a05] (2026-10-23T03:26:28Z)
- (step 1) `python3 plugin/tests/run.py test_stories` → exit 0 · Ran 13 tests in 18.8s (3 classes, 16 at a time; slowest: Stories 19s, Untrusted 11s, InABrowser 3s) / OK [ran] [tree 75dc9b1b7a05] (2026-10-23T03:26:48Z)
- (ac 1) `python3 plugin/tests/run.py test_stories` → exit 0 · Ran 13 tests in 18.9s (3 classes, 16 at a time; slowest: Stories 19s, Untrusted 10s, InABrowser 2s) / OK [ran] [tree 75dc9b1b7a05] (2026-10-23T03:27:35Z)
- (audit intent) `fm-reviewer full pass; MEDIUM fixed test-first: with no browser, or one that dies before the first state, the page still lists the states and the run exits 2 'not run, not a pass' with ok false (tests for no browser and a fake executable); LOWs: one-line step and name text (U+2028/2029 refused), about:blank between states, a 12 MB cap on inline shots in total, the 300 s budget inside a state through fmflow's end deadline, ..%2F and %2e%2e path cases` → fm stories turns a state chart into one page of cells, each a screenshot of that state driven through fm flow [tree 75dc9b1b7a05] (2026-10-23T03:27:35Z)
- (audit adversary) `fm-reviewer full pass; MEDIUM fixed test-first: with no browser, or one that dies before the first state, the page still lists the states and the run exits 2 'not run, not a pass' with ok false (tests for no browser and a fake executable); LOWs: one-line step and name text (U+2028/2029 refused), about:blank between states, a 12 MB cap on inline shots in total, the 300 s budget inside a state through fmflow's end deadline, ..%2F and %2e%2e path cases` → targets go through fmflow's guard (Fetch blocks off-target requests); step and name text is one line, escaped; shots are capped in size [tree 75dc9b1b7a05] (2026-10-23T03:27:35Z)
- (audit edge) `fm-reviewer full pass; MEDIUM fixed test-first: with no browser, or one that dies before the first state, the page still lists the states and the run exits 2 'not run, not a pass' with ok false (tests for no browser and a fake executable); LOWs: one-line step and name text (U+2028/2029 refused), about:blank between states, a 12 MB cap on inline shots in total, the 300 s budget inside a state through fmflow's end deadline, ..%2F and %2e%2e path cases` → no browser exits 2 with the page listing states; a state over budget stops the run; states share cookies and storage (a ponytail ceiling) [tree 75dc9b1b7a05] (2026-10-23T03:27:35Z)
- (audit design) `fm-reviewer full pass; MEDIUM fixed test-first: with no browser, or one that dies before the first state, the page still lists the states and the run exits 2 'not run, not a pass' with ok false (tests for no browser and a fake executable); LOWs: one-line step and name text (U+2028/2029 refused), about:blank between states, a 12 MB cap on inline shots in total, the 300 s budget inside a state through fmflow's end deadline, ..%2F and %2e%2e path cases` → each cell names its state and step; a cell past the shot cap says so [tree 75dc9b1b7a05] (2026-10-23T03:27:35Z)
## Log
- 2026-10-22T20:57:57Z created
- 2026-10-22T20:57:58Z set scope=['plugin/lib/fmflow.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_flow.py', 'CHANGELOG.md']
- 2026-10-22T20:57:59Z split from T-1532 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:58:00Z set depends_on=['T-1639']
- 2026-10-22T21:29:56Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_flow.Stories`
- 2026-10-22T21:30:19Z criterion 1 text: a chart of 3 states builds a page with 3 cells — verify with python3 plugin/tests/run.py test_flow.Stories → a chart of 3 states builds a page with 3 cells
- 2026-10-23T02:42:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1640.builder.md
- 2026-10-23T02:43:13Z focused
- 2026-10-23T02:44:18Z criterion 1 verify: `python3 plugin/tests/run.py test_flow.Stories` → `python3 plugin/tests/run.py test_stories`
- 2026-10-23T02:46:03Z set scope=['plugin/lib/fmstories.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_stories.py', 'MASTER.md', 'plugin/skills/ui-design/SKILL.md', 'CHANGELOG.md']
- 2026-10-23T02:46:05Z steer: lead asked for a new fmstories module, test_stories.py, a MASTER sentence and a ui-design skill line; scope widened
- 2026-10-23T02:48:39Z set scope=['plugin/lib/fmstories.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmflow.py', 'plugin/tests/test_stories.py', 'plugin/tests/test_flow.py', 'MASTER.md', 'plugin/skills/ui-design/SKILL.md', 'CHANGELOG.md']
- 2026-10-23T02:48:41Z steer: fm flow goto keeps a relative path's ?query#fragment so a chart state can be a query string
- 2026-10-23T03:26:01Z merged worktree-agent-a9b761a50bb16d082 (8 file(s))
- 2026-10-23T03:26:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9b761a50bb16d082
- 2026-10-23T03:26:05Z focused
- 2026-10-23T03:27:16Z scope: plugin/lib/fmflow.py (end deadline), plugin/tests/test_flow.py, plugin/skills/ui-design/SKILL.md, MASTER.md, plugin/lib/fmcli.py, CHANGELOG.md
- 2026-10-23T03:28:21Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1532 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Journeys and states: fm flow runs user journeys as verify commands, fm s
- T-1490 [FEATURE M, done, 2 steps] UI playbook: composition, depth and states — lesson: Ship a measuring probe with a layout playbook; prose rules about rhythm are unrevi…
- playbook Visual QA: screenshots, an eyeball pass and a receipt (skills/playbooks/references/ui/visual-qa.md)
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_flow.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmflow.py, plugin/lib/fmstories.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_flow.py, plugin/tests/test_stories.py; re-ground the plan against them before editing
## Lessons
- A visual check that couldn't run must exit non-zero and say 'not run', never look like a pass
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_stories.py
- plugin/lib/fmstories.py
- plugin/lib/fmcli.py
- plugin/tests/test_flow.py
- plugin/lib/fmflow.py
- MASTER.md
- plugin/skills/ui-design/SKILL.md
- CHANGELOG.md
- plugin/commands/settings.md
- plugin/lib/city.html
- plugin/lib/fmcodetui.py
- plugin/lib/fmcritique.py
- plugin/lib/fmdesign.py
- plugin/lib/fmnew.py
- plugin/lib/fmpage.py
- plugin/lib/fmsettings.py
- plugin/lib/fmshot.py
- plugin/tests/helpers.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_control_room.py
- plugin/tests/test_critique.py
- plugin/tests/test_design_gates.py
- plugin/tests/test_settings_power.py
- plugin/tests/test_showpieces.py
- plugin/tests/test_site_hero.py
