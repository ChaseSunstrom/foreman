---
id: T-3247
type: FEATURE
tier: M
status: done
priority: normal
scope: [demo/readme_figures.py, demo/figures/*, plugin/tests/test_readme_figures.py, CHANGELOG.md, README.md, plugin/lib/sampo/works.py, plugin/lib/sampo/cli.py, plugin/tests/test_design_works.py, docs/map/files-1.md, docs/map/files-lib-3.md]
depends_on: []
source: followup
created: 2026-11-05T21:12:34Z
updated: 2026-11-06T00:36:53Z
base: 1abcaddff1f0976804e109c8dc7fdaed858a4e0f
base_tree: d6dbd35056a9aee9a629dce26b034b833449fe75
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T21:14:47Z
plan0_scope: [demo/readme_figures.py, demo/figures/*, plugin/tests/test_readme_figures.py, CHANGELOG.md]
group: README figures and diagrams
verified: strong
unproven: [docs, ui-unshot]
---
# README figures (T-3245 part 1): demo/readme_figures.py draws every README table and four real-data charts as light and dark SVGs in Sampo's tokens, gated by sampo works check, with --check for staleness
## Raw request
> README figures (T-3245 part 1): demo/readme_figures.py draws every README table and four real-data charts as light and dark SVGs in Sampo's tokens, gated by sampo works check, with --check for staleness
## Interpretation
The user asked for the README to look like Sampo with charts, and every table turned into a picture. Reading 1 (chosen): each README pipe table becomes a themed SVG (light and dark, swapped by a <picture> element) drawn from the table's rows, plus real-data charts in the live page's modern chart style. Reading 2: one hero dashboard image replaces all tables; rejected because each table carries distinct facts the README text refers to.
## Assumptions (confidence)
## Acceptance criteria
- [x] every pipe table in README.md has a dark and a light SVG drawn by demo/readme_figures.py from its rows, each passing sampo works check — verify with `python3 plugin/tests/run.py test_readme_figures`
- [x] at least four charts from measured data (tests in the suite, tasks closed per day, merge time, models bench or moons kept and cards written), dated, in the live page's modern chart style, both themes — verify with `python3 plugin/tests/run.py test_readme_figures`
- [x] python3 demo/readme_figures.py --check exits 0 when every figure is current and 1 naming the stale ones — verify with `python3 plugin/tests/run.py test_readme_figures`
## Non-goals
## Approach (options → choice → why)
1) use what exists: demo/readme_figures.py beside demo/record.py reads each pipe table out of README.md (rows as data, so a table edit redraws), draws a card-like SVG table in the live page's tokens (live.css colours, its modern theme), and four charts from measured data (sampo stats, ledger, research/models/bench.jsonl, moons and cards counts); writes demo/figures/<slug>-{light,dark}.svg; sampo works check gates each; --check names stale ones. likely outcome: figures that redraw with one command. 2) hand-drawn static SVGs: fails if: numbers go stale. 3) headless-Chrome PNG screenshots: fails if: heavy, blurry, can't follow theme. 4) do less, restyle Markdown only: fails if: the user asked for pictures. Choice 1 (80%): generated, themed, gated SVGs stay current with one command. Keep each table's Markdown inside a details block so text stays searchable; alt text names the table.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] failing tests: a figure per table in both themes, works check passes, four charts, --check
2. [x] the generator and the table figures
3. [x] the charts from measured data
4. [x] a figure type for sampo works: document figures render near display size, unique doesn't apply
5. [x] review fixes: safe re-wrap, orphans and missing data stale, wide glyphs, history-wide first commits, a render test
## Resume here
<!-- auto -->
- 2026-11-06T00:29:28Z steps 5/5 done
- git: foreman/build; 11 uncommitted: CHANGELOG.md, README.md, docs/map/files-1.md, docs/map/files-lib-3.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/works.py, plugin/tests/test_design_works.py, demo/figures/, demo/readme_figures.py, plugin/tests/test_readme_figures.py
- touched since last checkpoint: plugin/lib/sampo/works.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3252/test_slots.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3252/perf_bench.py, .claude/worktrees/agent-a615cb8d3c1e381e4/ANDON.md
- failures met: uv.lock
## Docs impact
README, CHANGELOG, docs/map files-1 (demo/figures) and files-lib-3 (works figure type)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_readme_figures` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.7s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 4c4ce55b39de] [world 2f1906870a] (2026-11-05T21:17:39Z)
- (step 1) `python3 plugin/tests/run.py test_readme_figures` → ✗ exit 1 (never ran: no ~/.claude/foreman/demo/figures) · Ran 7 tests in 0.8s (3 jobs, 16 at a time; slowest: Tables 0s, Check 0s, Charts 0s) / FAILED (3 classes: test_readme_figures.Tables, test_readme_figures.Check, test_readme_figures.Charts) [ran] [tree 01016a503cc7] [world 2f1906870a] (2026-11-05T21:17:51Z)
- (step 4) `python3 plugin/tests/run.py test_design_works` → ✗ exit 1 · Ran 29 tests in 4.8s (11 jobs, 16 at a time; slowest: Rendered.test_a_document_figure_renders_near_its_size_and_is_told_apart_by_its_text 4s, Rendered.test_icons_blank_clipped_still_and_duplicate_fail [ran] [tree 1604b42d72f2] [world 2f1906870a] (2026-11-05T21:23:04Z)
- (step 4) `python3 plugin/tests/run.py test_design_works` → ✗ exit 1 · Ran 29 tests in 5.9s (11 jobs, 16 at a time; slowest: Rendered.test_a_document_figure_renders_near_its_size_and_is_told_apart_by_its_text 5s, StaticGates 5s, Rendered.test_icons_blank_clipped_still_an [ran] [tree 0ce96b4e214b] [world 2f1906870a] (2026-11-05T21:23:32Z)
- (step 4) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 29 tests in 14.9s (27 jobs, 16 at a time; slowest: Rendered.test_a_document_figure_renders_near_its_size_and_is_told_apart_by_its_text 14s, Rendered.test_icons_blank_clipped_still_and_duplicate_fa [ran] [tree fcc684c9a668] [world 2f1906870a] (2026-11-05T21:24:04Z)
- (step 2) `python3 plugin/tests/run.py test_readme_figures` → ✗ exit 1 · Ran 7 tests in 1.3s (3 jobs, 16 at a time; slowest: Check 1s, Tables 0s, Charts 0s) / FAILED (1 classes: test_readme_figures.Tables) [ran] [tree 213dfcb19cbd] [world 2f1906870a] (2026-11-05T23:58:11Z)
- (step 2) `python3 plugin/tests/run.py test_readme_figures` → exit 0 · Ran 7 tests in 1.2s (3 jobs, 16 at a time; slowest: Check 1s, Tables 0s, Charts 0s) / OK [ran] [tree 3b8ca4bbf2fb] [world 2f1906870a] (2026-11-05T23:58:19Z)
- (step 3) `python3 plugin/tests/run.py test_readme_figures` → exit 0 · Ran 7 tests in 1.2s (3 jobs, 16 at a time; slowest: Check 1s, Tables 0s, Charts 0s) / OK [ran] [tree 3b8ca4bbf2fb] [world 2f1906870a] (2026-11-05T23:58:24Z)
- (step 5) `python3 plugin/tests/run.py test_readme_figures` → ✗ exit 1 · Ran 11 tests in 92.5s (4 jobs, 16 at a time; slowest: Rendered 92s, Check 1s, Tables 1s) / FAILED (3 classes: test_readme_figures.Check, test_readme_figures.Rendered, test_readme_figures.Tables) [ran] [tree 5ec98c0d9a94] [world 2f1906870a] (2026-11-06T00:06:03Z)
- (step 5) `nice python3 plugin/tests/run.py test_readme_figures` → ✗ exit 1 · Ran 11 tests in 117.2s (4 jobs, 16 at a time; slowest: Rendered 116s, Check 1s, Tables 1s) / FAILED (2 classes: test_readme_figures.Rendered, test_readme_figures.Tables) [ran] [tree 22723f3c3941] [world 2f1906870a] (2026-11-06T00:09:57Z)
- (step 5) `python3 plugin/tests/run.py test_design_works.TextRatio` → ✗ exit 1 · Ran 1 tests in 0.9s (1 jobs, 16 at a time; slowest: TextRatio 0s) / FAILED (1 classes: test_design_works.TextRatio) [ran] [tree 05907d3dc9b6] [world 2f1906870a] (2026-11-06T00:12:19Z)
- (step 5) `python3 plugin/tests/run.py test_design_works.TextRatio` → ✗ exit 1 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: TextRatio 0s) / FAILED (1 classes: test_design_works.TextRatio) [ran] [tree 35ea34fad177] [world 2f1906870a] (2026-11-06T00:12:33Z)
- (step 5) `nice python3 plugin/tests/run.py test_readme_figures test_design_works` → exit 0 · Ran 41 tests in 57.5s (10 jobs, 16 at a time; slowest: Rendered 57s, Rendered 15s, StaticGates 2s) / OK [ran] [tree e4289656610a] [world 2f1906870a] (2026-11-06T00:14:06Z)
- (ac 1) `python3 plugin/tests/run.py test_readme_figures` → exit 0 · Ran 11 tests in 49.4s (4 jobs, 16 at a time; slowest: Rendered 49s, Check 1s, Tables 0s) / OK [ran] [tree dff69c4704d0] [world 2f1906870a] (2026-11-06T00:16:10Z)
- (ac 2) `python3 plugin/tests/run.py test_readme_figures` → exit 0 · Ran 11 tests in 49.4s (4 jobs, 16 at a time; slowest: Rendered 49s, Check 1s, Tables 0s) / OK [ran] [tree dff69c4704d0] [world 2f1906870a] (2026-11-06T00:16:10Z)
- (ac 3) `python3 plugin/tests/run.py test_readme_figures` → exit 0 · Ran 11 tests in 49.4s (4 jobs, 16 at a time; slowest: Rendered 49s, Check 1s, Tables 0s) / OK [ran] [tree dff69c4704d0] [world 2f1906870a] (2026-11-06T00:16:10Z)
- (audit intent) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → every README table is a picture with its text kept, four dated charts, --check exits 1 naming stale, orphan or missing; all 24 figures pass works check --type figure [tree dff69c4704d0] (2026-11-06T00:16:10Z)
- (audit edge) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → hand-edited picture opener left alone (no lines eaten), escaped pipes, code fences skipped, em dashes and CJK estimated wide, a 1-level raster diff no longer fails contrast while faint text still does [tree dff69c4704d0] (2026-11-06T00:16:10Z)
- (audit maintainer) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → one script, data.json the only input to --check, --refresh CHART re-measures one chart (hooks on a quiet machine) [tree dff69c4704d0] (2026-11-06T00:16:10Z)
- (audit intent) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → every README table is a picture with its text kept, four dated charts, --check exits 1 naming stale, orphan or missing; all 24 figures pass works check --type figure [tree dff69c4704d0] (2026-11-06T00:21:59Z)
- (audit edge) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → hand-edited picture opener left alone (no lines eaten), escaped pipes, code fences skipped, em dashes and CJK estimated wide, a 1-level raster diff no longer fails contrast while faint text still does [tree dff69c4704d0] (2026-11-06T00:21:59Z)
- (audit maintainer) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → one script, data.json the only input to --check, --refresh CHART re-measures one chart (hooks on a quiet machine) [tree dff69c4704d0] (2026-11-06T00:21:59Z)
- (audit intent) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → every README table is a picture with its text kept, four dated charts, --check exits 1 naming stale, orphan or missing; all 24 figures pass works check --type figure [tree 1395d0f856bc] (2026-11-06T00:33:07Z)
- (audit edge) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → hand-edited picture opener left alone (no lines eaten), escaped pipes, code fences skipped, em dashes and CJK estimated wide, a 1-level raster diff no longer fails contrast while faint text still does [tree 1395d0f856bc] (2026-11-06T00:33:07Z)
- (audit maintainer) `fm-reviewer (intent, edge, maintainer) on the diff; every finding fixed test-first (render test over all figures, safe re-wrap, orphans/missing data/unknown pictures stale, wide glyphs, history-wide first commits, POSIX grep class, docs map) except the unused-parameter nit` → one script, data.json the only input to --check, --refresh CHART re-measures one chart (hooks on a quiet machine) [tree 1395d0f856bc] (2026-11-06T00:33:07Z)
## Log
- 2026-11-05T21:12:34Z created
- 2026-11-05T21:14:46Z focused
- 2026-11-05T21:14:47Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T21:21:19Z scope: README.md, since the generator wraps each table in its picture and text copy
- 2026-11-05T21:22:59Z scope: plugin/lib/sampo/works.py, cli.py, test_design_works.py: the card type renders a tall table at 0.54 scale (contrast 2.57 from antialiasing) and its 24x24 unique thumb calls every plate-coloured figure one work
- 2026-11-05T21:23:14Z set scope=['demo/readme_figures.py', 'demo/figures/*', 'plugin/tests/test_readme_figures.py', 'CHANGELOG.md', 'README.md', 'plugin/lib/sampo/works.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_design_works.py']
- 2026-11-05T23:59:24Z set scope=['demo/readme_figures.py', 'demo/figures/*', 'plugin/tests/test_readme_figures.py', 'CHANGELOG.md', 'README.md', 'plugin/lib/sampo/works.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_design_works.py', 'docs/map/files-1.md']
- 2026-11-06T00:00:31Z paused: focus moved to T-3092
- 2026-11-06T00:03:57Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T00:03:57Z focused
- 2026-11-06T00:07:59Z set scope=['demo/readme_figures.py', 'demo/figures/*', 'plugin/tests/test_readme_figures.py', 'CHANGELOG.md', 'README.md', 'plugin/lib/sampo/works.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_design_works.py', 'docs/map/files-1.md', 'docs/map/files-lib-3.md']
- 2026-11-06T00:10:01Z Rendered failed under load 60 with 116 s; reading its output next
- 2026-11-06T00:13:20Z paused: focus moved to T-3253
- 2026-11-06T00:15:12Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-06T00:15:12Z focused
- 2026-11-06T00:21:52Z scope: mods/foreman-ui/* and plugin/lib/sampo/hooks.py edits are the T-3163 builder's, in its own worktree (same session); plugin/tests/test_hunks.py is T-3253's, committed as 4a79fe32; none is in this task's diff
- 2026-11-06T00:29:30Z paused: focus moved to T-3256
- 2026-11-06T00:32:56Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T00:32:56Z focused
- 2026-11-06T00:32:58Z scope: test_smith_cards.py, smith.py, mods/foreman-ui/*, .fm-scratch/shot/README.txt, ANDON.md were builder edits in their own worktrees, booked here by the bug T-3256 fixed (f41ebf15); none is in this task's diff
- 2026-11-06T00:36:51Z done
- 2026-11-06T00:36:53Z committed fd073c44 (33 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3245 [FEATURE L, planned, 6 steps] Completely update the README to the Sampo look with the charts and such; turn every…
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- research T-2052-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: approve with nits.** I read the brief, the diff and the ful…
- decision 2026-11-03: [outward] [revisited: Kirjokansi fused with Ilmarinen's forge] [cites: user steer 2026-11-03: super improve the fuse completely, combined/animated l…
- similar past tasks were L: consider --tier L
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cockpit.py, plugin/tests/test_code_tui.py, plugin/tests/test_core.py, plugin/tests/test_demo.py, plugin/tests/test_docs.py, plugin/tests/t…
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md; re-ground the plan against them before editing
## Lessons
- A render gate that compares two renders must ignore raster noise between them, or a busy batch fails a clear figure; and a document figure has to be gated at the size a reader sees, not a thumbnail
## Plan gaps
- added late: a figure type for sampo works: document figures render near display size, unique doesn't apply
- added late: review fixes: safe re-wrap, orphans and missing data stale, wide glyphs, history-wide first commits, a render test
- failed first: step 1 failing tests: a figure per table in both themes, works check passes, four charts, --check
- failed first: step 2 the generator and the table figures
- failed first: step 4 a figure type for sampo works: document figures render near display size, unique doesn't apply
- failed first: step 5 review fixes: safe re-wrap, orphans and missing data stale, wide glyphs, history-wide first commits…
## Files touched
- plugin/tests/test_readme_figures.py
- demo/readme_figures.py
- README.md
- demo/figures/chart-closed-dark.svg
- demo/figures/chart-closed-light.svg
- demo/figures/chart-hooks-dark.svg
- demo/figures/chart-hooks-light.svg
- demo/figures/chart-models-dark.svg
- demo/figures/chart-models-light.svg
- demo/figures/chart-tests-dark.svg
- demo/figures/chart-tests-light.svg
- demo/figures/data.json
- demo/figures/documentation-dark.svg
- demo/figures/documentation-light.svg
- demo/figures/features-dark.svg
- demo/figures/features-light.svg
- demo/figures/headless-on-a-server-dark.svg
- demo/figures/headless-on-a-server-light.svg
- demo/figures/quick-start-dark.svg
- demo/figures/quick-start-light.svg
- demo/figures/talking-to-it-dark.svg
- demo/figures/talking-to-it-light.svg
- demo/figures/the-ward-dark.svg
- demo/figures/the-ward-light.svg
- demo/figures/when-not-to-use-sampo-dark.svg
- demo/figures/when-not-to-use-sampo-light.svg
- demo/figures/why-dark.svg
- demo/figures/why-light.svg
- plugin/tests/test_design_works.py
- plugin/lib/sampo/cli.py
