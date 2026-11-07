---
id: T-3092
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/web/live/live.js, plugin/web/live/live.css, plugin/web/live/index.html, plugin/web/live/charts.js, plugin/lib/sampo/live.py, plugin/tests/test_live_page.py, plugin/tests/test_live.py]
depends_on: [T-3055]
source: user
created: 2026-11-05T01:50:34Z
updated: 2026-11-06T00:03:57Z
builder_model: haiku
base: 35f127cfc205283d604a1b1d17196ed8080679df
base_tree: b4cda626900300ad4b5fb40cc3ce82ac5906867c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T03:10:58Z
plan0_scope: [plugin/web/live/live.js, plugin/web/live/live.css, plugin/web/live/index.html, plugin/web/live/charts.js, plugin/lib/sampo/live.py, plugin/tests/test_live_page.py, plugin/tests/test_live.py]
lane_stop: merged 2026-11-05T04:41:51Z
paused_tree: 4a0c0294eeb52294dc9a63fde0c9789b3e43b42e
---
# Live page part 2: modern charts for every panel (time series, stacked GPU memory, a moons funnel, sparklines, job progress bars) from one small chart kit, in both themes (T-3054)
## Raw request
> Live page part 2: modern charts for every panel (time series, stacked GPU memory, a moons funnel, sparklines, job progress bars) from one small chart kit, in both themes (T-3054)
## Interpretation
Reading 1 (taken): part 2 of T-3054: the 'more modern graphs' half: every panel's chart redrawn as a current dashboard chart (axes, legends, tooltips, restrained colour), from one small hand-made kit so the page stays dependency-free, plus the job progress bars T-3044 needs. Reading 2 (ruled out): a chart library from a CDN: the page is served locally and must work offline.
## Assumptions (confidence)
## Acceptance criteria
- [ ] More modern graphs: calls per minute by model and spend over the day as time-series charts with axes and a legend; GPU memory as a stacked bar per model (no tank in the modern theme); the moons funnel as a funnel chart with counts per stage; sparklines in the stat tiles — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [ ] Running jobs show a progress bar with percent, rate and ETA from the snapshot's progress (T-3083), and tasks and lanes their steps done of total — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [ ] One chart kit (plugin/web/live/charts.js, no library) draws every chart from theme tokens, so both themes and light and dark read right; every chart has a text equivalent for screen readers and keeps 4.5:1 text contrast — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [ ] In the modern light scheme the network canvas is light too (ground, edges and labels from the light tokens), not a dark card on a light page — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
## Approach (options → choice → why)
1) use what exists: a ~300-line SVG chart kit (line, area, stacked bar, funnel, sparkline, progress bar) reading CSS tokens, the snapshot's existing series (calls, spend, GPU, moons counts) plus T-3083's progress fields: likely outcome: modern charts in both themes with no new dependency. 2) canvas for everything: fails if: charts lose text and accessibility. 3) a vendored chart library: fails if: a large file to maintain for six chart types. 4) do less: restyle the existing bars: fails if: the GPU tank and the stage chips stay forge widgets. Choice 1 (80%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/fixtures/live/machine.json, plugin/lib/sampo/models.py, docs/map/files-lib-2.md, plugin/lib/sampo/cli.py, plugin/tests/test_models.py; past FIXes T-3014, T-3021.
## Execution prompt
Read the parent's brief (state/projects/foreman-4a056f/tasks/T-3054-can-you-update-the-live-view-website-to-be-more.md) and T-3055's merged modern theme (tokens in live.css under [data-theme=modern]). Chart rules (from Sampo's dataviz guidance): one hue per series from a validated categorical palette mapped to theme tokens, sequential for magnitude; thin marks, no 3D, no gradients on data; axes with few ticks and units; a legend only when there are two or more series; tooltips on hover and focus; a visually hidden table or list as the text equivalent; light and dark from the same tokens. Keep the forge theme's existing widgets under [data-theme=forge] untouched. Tests in test_live_page (each chart renders from a fixture snapshot, the text equivalents exist, no console errors, no sideways scroll at 390). Shots under the scratchpad as t3056-*.png (both themes, 1440 and 390, dark and light), read them.
## Steps
1. [x] the chart kit and its tests
2. [x] the panels redrawn with it (time series, stacked GPU, funnel, sparklines)
3. [x] job progress bars and task steps
4. [x] shots in both themes, desktop and phone
## Resume here
<!-- auto -->
- 2026-11-06T00:03:57Z steps 4/4 done
- git: foreman/build; 10 uncommitted: CHANGELOG.md, README.md, docs/map/files-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/works.py, plugin/tests/test_design_works.py, demo/figures/, demo/readme_figures.py, plugin/tests/test_readme_figures.py, scripts/
## Docs impact
CHANGELOG line; no other doc names the live page's panels chart by chart (MASTER.md's live page row already covers the modern look from T-3054).
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_live test_live_page 2>&1 | tail -40` → ✗ exit 1 · Ran 84 tests in 107.2s (11 classes, 16 at a time; slowest: Page 105s, Serve 16s, Act 14s) / FAILED (2 classes: test_live_page.Page, test_live_page.Files) [ran] [tree afcf0f60e301] [world 2f1906870a] (2026-11-05T03:18:43Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_live_page 2>&1 | tail -40` → ✗ exit 1 · Ran 84 tests in 107.2s (11 classes, 16 at a time; slowest: Page 105s, Serve 16s, Act 14s) / FAILED (2 classes: test_live_page.Page, test_live_page.Files) [ran] [tree afcf0f60e301] [world 2f1906870a] (2026-11-05T03:18:43Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page 2>&1 | tail -40` → ✗ exit 1 · Ran 84 tests in 107.2s (11 classes, 16 at a time; slowest: Page 105s, Serve 16s, Act 14s) / FAILED (2 classes: test_live_page.Page, test_live_page.Files) [ran] [tree afcf0f60e301] [world 2f1906870a] (2026-11-05T03:18:43Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 84 tests in 127.1s (11 classes, 16 at a time; slowest: Page 127s, Serve 12s, Act 10s) / OK [ran] [tree 7d5890bdae9c] [world 2f1906870a] (2026-11-05T03:33:10Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 84 tests in 114.2s (11 classes, 16 at a time; slowest: Page 114s, Serve 11s, Act 10s) / OK [ran] [tree 7d5890bdae9c] [world 2f1906870a] (2026-11-05T03:35:10Z)
- (step 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 84 tests in 127.3s (11 classes, 16 at a time; slowest: Page 127s, Serve 11s, Act 9s) / OK [ran] [tree 7d5890bdae9c] [world 2f1906870a] (2026-11-05T03:37:21Z)
- (step 4) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 84 tests in 126.9s (11 classes, 16 at a time; slowest: Page 127s, Serve 11s, Act 10s) / OK [ran] [tree 7d5890bdae9c] [world 2f1906870a] (2026-11-05T03:39:28Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [12.84s] [ran] [tree 7d5890bdae9c] [world 2f1906870a] (2026-11-05T03:42:01Z)
- (step 1) `nice python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 52.7s (36 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 42s, Page.test_the_net_reads_as_several_agents_not_one_hub [ran] [tree 29dde1f4048a] [world 2f1906870a] (2026-11-06T00:01:54Z)
- (step 2) `nice python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 40.8s (80 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 39s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 29dde1f4048a] [world 2f1906870a] (2026-11-06T00:02:40Z)
- (step 3) `nice python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 32.4s (84 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 31s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 29dde1f4048a] [world 2f1906870a] (2026-11-06T00:03:14Z)
- (step 4) `nice python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 34.1s (80 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 33s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 29dde1f4048a] [world 2f1906870a] (2026-11-06T00:03:49Z)
## Log
- 2026-11-05T01:50:34Z created
- 2026-11-05T01:50:35Z set approved=True
- 2026-11-05T03:10:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3092.builder.md
- 2026-11-05T03:10:57Z focused
- 2026-11-05T03:10:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T03:43:05Z built (e46035c7 on worktree-agent-a08fbf005e14c3c9c); reviewed the shots (modern 1440 dark, 390 light): network canvas, stat tiles with sparklines, calls and spend time series, moons funnel read right in both themes; the Moons tile has no sparkline (a follow-up); merge waits for the gate noise fix
- 2026-11-05T04:41:51Z merged worktree-agent-a08fbf005e14c3c9c (8 file(s))
- 2026-11-05T04:41:54Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a08fbf005e14c3c9c
- 2026-11-06T00:00:31Z focused
- 2026-11-06T00:03:57Z paused: focus moved to T-3247
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3054 [FEATURE L, planned, 4 steps] The live page goes modern: a clean dashboard with modern charts by default, the forge look as a setting
- T-3055 [FEATURE M, planned, 3 steps] Live page part 1: a modern theme by default (clean dashboard shell, tokens, type, layout) and the forge look as a setting (T-3054)
- playbook Data viz: one claim, one axis, colour by job (fm playbooks show ui/data-viz)
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_design_surfaces.py, plugin/tests/test_design_tokens.py, plugin/tests/test_docs.py, plugin/tests/test_edit_cards.…
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/live.py, plugin/tests/test_live.py, plugin/tests/test_live_page.py, plugin/web/live/charts.js, plugin/web/live/index.html, plugin/web/live/live.css, plugin/web/live/live.js; re-ground the plan against them before editing
