---
id: T-1655
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_showpieces.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: followup
created: 2026-10-22T20:58:41Z
updated: 2026-10-28T17:43:09Z
group: rasteriser-dependent 3D showpieces
base: 579d11f7bd5b065092d90dd5ff553f86abe73837
base_tree: 83c2235ddcfcb1debc2a292c0cec99b7a14e5e6f
plan0_at: 2026-10-28T17:32:36Z
plan0_scope: [plugin/lib/fmpage.py, plugin/lib/fmcli.py, plugin/tests/test_showpieces.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# fm page graph --cells: the task graph in the terminal as half blocks
## Raw request
> More 3D showpieces: metaballs, guard airlock, bench diorama, terrain, lookbook room, half-block graph (from T-1542; waits: after the city and the task graph)
## Interpretation
Of T-1542's showpieces, ship the half-block graph now (it reuses fm scene cells from T-1635); the rest become their own tasks (T-1848 to T-1852).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm page graph --cells [--cols N] prints the graph's plan as a scene through fmscene.cells: a box per task (height by tier, colour from graph.html's status tokens), a ground per layer, then a key naming each status's count (status isn't colour alone) — verify with `python3 plugin/tests/run.py Graph`
## Non-goals
Edges in the terminal (thin boxes read as noise at 64 columns). The other showpieces are captured as their own tasks.
## Approach (options → choice → why)
Options: (a) graph_scene(plan) builds a scene.json dict from graph_layout and prints it with fmscene.cells; (b) draw the SVG poster's isometric shapes as text; (c) a separate half-block rasteriser for the graph. Choice (a): one renderer, colours read from graph.html's --graph-* tokens so the page and the terminal can't drift. A key line names each status's count, so status isn't colour alone.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: graph_scene() and fm page graph --cells (red)
2. [x] graph_scene(plan) + --cells/--cols on fm page (green), docs
## Resume here
<!-- auto -->
- 2026-10-28T17:39:51Z step 1/2: test: graph_scene() and fm page graph --cells (red)
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/tests/test_showpieces.py
- touched since last checkpoint: plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/import-test.py, plugin/lib/fmpage.py, plugin/tests/test_showpieces.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/import-impl.py
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Graph` → ✗ exit 1 · Ran 30 tests in 13.4s (3 classes, 16 at a time; slowest: GraphBrowser 13s, Graph 4s, Graphify 1s) / FAILED (1 classes) [ran] [tree 4c1744708786] (2026-10-28T17:33:01Z)
- (step 2) `python3 plugin/tests/run.py Graph` → exit 0 · Ran 30 tests in 13.4s (3 classes, 16 at a time; slowest: GraphBrowser 13s, Graph 3s, Graphify 1s) / OK [ran] [tree 58cc0e539d1f] (2026-10-28T17:34:48Z)
- (ac 1) `python3 plugin/tests/run.py Graph 2>&1 | grep -B3 -A12 "^FAIL:" | head -30` → ✗ exit 1 · Ran 25 tests in 1.589s / FAILED (failures=1) [ran] [tree db34fd4f10a9] (2026-10-28T17:37:48Z)
- (step 2) `python3 plugin/tests/run.py Graph` → exit 0 · Ran 30 tests in 12.4s (3 classes, 16 at a time; slowest: GraphBrowser 12s, Graph 2s, Graphify 0s) / OK [ran] [tree 32fd41c97b20] (2026-10-28T17:38:35Z)
- (ac 1) `python3 plugin/tests/run.py Graph` → exit 0 · Ran 30 tests in 12.4s (3 classes, 16 at a time; slowest: GraphBrowser 12s, Graph 2s, Graphify 1s) / OK [ran] [tree 32fd41c97b20] (2026-10-28T17:42:40Z)
- (audit intent) `one foreman:fm-reviewer pass (all five lenses) over the diff; 6 LOW findings, all fixed test-first; full gates exit 0` → fixed — older tasks past GRAPH_MAX now get an '(N older not drawn)' note [tree 32fd41c97b20] (2026-10-28T17:42:40Z)
- (audit adversary) `one foreman:fm-reviewer pass (all five lenses) over the diff; 6 LOW findings, all fixed test-first; full gates exit 0` → ok — only status names, counts and token colours reach the terminal; no task titles or paths [tree 32fd41c97b20] (2026-10-28T17:42:40Z)
- (audit edge) `one foreman:fm-reviewer pass (all five lenses) over the diff; 6 LOW findings, all fixed test-first; full gates exit 0` → fixed — near=far/5000 keeps validate's ratio; cols 2-400 checked before layout; --cells refuses --out and other pages [tree 32fd41c97b20] (2026-10-28T17:42:40Z)
- (audit operator) `one foreman:fm-reviewer pass (all five lenses) over the diff; 6 LOW findings, all fixed test-first; full gates exit 0` → ok — one-shot, bounded by fmraster WORK, 0.36 s on the real repo [tree 32fd41c97b20] (2026-10-28T17:42:40Z)
- (audit maintainer) `one foreman:fm-reviewer pass (all five lenses) over the diff; 6 LOW findings, all fixed test-first; full gates exit 0` → fixed — _graph_newest shared by html and cells; 12-layer framing test [tree 32fd41c97b20] (2026-10-28T17:42:40Z)
## Log
- 2026-10-22T20:58:41Z created
- 2026-10-28T17:30:37Z set title=fm page graph --cells: the task graph in the terminal as half blocks, scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_showpieces.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T17:32:34Z focused
- 2026-10-28T17:43:08Z done
- 2026-10-28T17:43:09Z committed 0cc39ea0 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1542 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, ta
- T-1635 [FEATURE M, done, 3 steps] Scene.json to terminal cells through the rasteriser, a shader subset, import from three.js — lesson: A renderer's frame helper shared b…
- T-1626 [FEATURE M, done, 5 steps] fm code's motion clock reads the project's Motion Score; fm motion compile --to lab: a page to play, scrub and edit each motion — lesso…
- decision 2026-10-23: T-1650: build the trading cards now (fm page looks --cards); the shader sketchbook and the site gallery become their own items
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_page.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_showpieces.py; re-ground the plan against them before editing
## Lessons
- A framing test must keep boxes at least 1 px: 64 half-block columns hold about 12 graph layers, so a 40-layer chain draws nothing and proves nothing
## Plan gaps
- failed first: step 1 test: graph_scene() and fm page graph --cells (red)
## Files touched
- plugin/tests/test_showpieces.py
- plugin/lib/fmpage.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
