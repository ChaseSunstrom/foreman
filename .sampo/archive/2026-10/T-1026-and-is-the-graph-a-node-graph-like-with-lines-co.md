---
id: T-1026
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_ui.py, README.md, CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json]
depends_on: []
source: user
created: 2026-10-16T02:00:46Z
updated: 2026-10-16T02:28:30Z
base: 5dd2e84b232c55ee537a815d1f4bc589286ba318
base_tree: 5784ae3e4edbce5d5b2094e59f1aac2f4d6072e5
verified: strong
---
# And is the graph a node graph? like with lines connecting and stuff? how can we make the e
## Raw request
> and is the graph a node graph? like with lines connecting and stuff? how can we make the empty parts look less empty? like to the right/below the history pane, and make the seperators not as dull with the gray lines, and make text easier to read insttead of just gray? I don't know, then super improve foreman and the UI
## Interpretation
Agents becomes a node graph: this session is the root; subagents, a brainstorm and lone worktrees branch off it with ├─/└─ connectors, a builder's worktree hangs under its agent; each node keeps its Gantt bar in an aligned column. History fills its width and height: a structured fm ui history (60 events, each with its task's title) drawn as time, mark, id, coloured event, then the task title. Section dividers become a gradient in the section's colour. Secondary text moves from dim gray to a brighter muted tone. Then an improvement round on Foreman and the UI.
## Assumptions (confidence)
## Acceptance criteria
- [x] Agents draws a tree (├─/└─ connectors, a worktree under its agent) with a time bar per node; History rows carry the task title; dividers are gradient rasters; the pane still fills the dock — verify with `cd mods/foreman-ui && claude plugin test .`
- [x] fm ui --json carries a structured history of up to 60 events with task titles — verify with `python3 plugin/tests/run.py test_ui`
## Non-goals
## Approach (options → choice → why)
Node graph: (a) a free-form graph with arbitrary edges: unreadable in 74 columns; (b) a tree with box-drawing connectors and a timeline column (chosen: lines connect parent and child, still one row per node, keeps the Gantt); (c) a separate tree and Gantt: twice the rows. History: (a) parse recent lines in the mod (no titles); (b) a structured history from fm ui (chosen: titles and colours without string parsing). Rules: Raster gradient from the section colour to the track.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests: tree rows with connectors and a worktree under its agent; history rows with titles; gradient rules; muted text
2. [x] fm ui history (60, structured, with titles)
3. [x] render: node graph, history, gradient rules, muted tone
4. [x] look at it live; README, CHANGELOG, foreman-ui 0.13.0
5. [x] Done and left at a glance: a work bar (done today, now, queued, inbox, blocked) under the head; a segment per step under the title; Agents and Sessions keep their child rows
## Resume here
<!-- auto -->
- 2026-10-16T02:06:28Z step 4/4: look at it live; README, CHANGELOG, foreman-ui 0.13.0
- git: foreman/build; 7 uncommitted: mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_ui.py
- touched since last checkpoint: plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_ui.py, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/hooks/register.tsx
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ui` → ✗ exit 1 · Ran 23 tests in 9.3s (7 classes, 16 at a time; slowest: UiView 9s, UiSkills 1s, SkillRoute 1s) / FAILED (1 classes) [ran] [tree f3205cbeea7f] (2026-10-16T02:01:52Z)
- (step 2) `python3 plugin/tests/run.py test_ui test_board_surfaces` → ✗ exit 1 · Ran 29 tests in 9.2s (7 classes, 16 at a time; slowest: UiView 9s, BoardSurfaces 2s, UiSkills 1s) / FAILED (1 classes) [ran] [tree dbf7b90ed393] (2026-10-16T02:02:12Z)
- (step 2) `python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 29 tests in 9.4s (7 classes, 16 at a time; slowest: UiView 9s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree b61979cc37d2] (2026-10-16T02:02:39Z)
- (ac 2) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 23 tests in 9.3s (7 classes, 16 at a time; slowest: UiView 9s, UiSkills 1s, CloseOut 1s) / OK [ran] [tree b61979cc37d2] (2026-10-16T02:02:49Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 3 fail / Ran 99 tests across 1 file. [7.81s] [ran] [tree bce8475f2d1c] (2026-10-16T02:03:52Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 99 tests across 1 file. [8.18s] [ran] [tree ceccddea5775] (2026-10-16T02:05:55Z)
- (step 5) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 1 test across 1 file. [0.19s] [ran] [tree 78e3920028f2] (2026-10-16T02:11:55Z)
- (step 5) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 101 tests across 1 file. [8.94s] [ran] [tree 7f6ac301d3d0] (2026-10-16T02:14:55Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 101 tests across 1 file. [9.23s] [ran] [tree 7f6ac301d3d0] (2026-10-16T02:15:10Z)
- (step 4) `cd mods/foreman-ui && ~/.local/bin/claude plugin test . && cd ../.. && python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 30 tests in 15.0s (7 classes, 16 at a time; slowest: UiView 15s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree 5b48817f67f8] (2026-10-16T02:16:26Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 101 tests across 1 file. [9.50s] [ran] [tree 9ea07aab91d7] (2026-10-16T02:28:28Z)
- (ac 2) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 10.7s (7 classes, 16 at a time; slowest: UiView 11s, UiSkills 1s, SkillRoute 1s) / OK [ran] [tree 9ea07aab91d7] (2026-10-16T02:28:28Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 5 of 6 findings fixed, the duplicated event mapping skipped (the two formats differ on purpose: recent carries the command and result)` → node graph with connectors, History with titles, gradient dividers, done/left work bar and per-step bar all seen live in the 200x55 harness (ui-progress2.png) [tree 9ea07aab91d7] (2026-10-16T02:28:28Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 5 of 6 findings fixed, the duplicated event mapping skipped (the two formats differ on purpose: recent carries the command and result)` → empty history falls back to recent; a non-string ts never raises; work bar drops to labels when the head is too narrow; stop-button rows keep the bar column [tree 9ea07aab91d7] (2026-10-16T02:28:28Z)
## Log
- 2026-10-16T02:00:46Z created
- 2026-10-16T02:01:36Z focused
- 2026-10-16T02:07:35Z steer: show how many things are complete vs left (progress counts: steps, queue, today) — make it visible
- 2026-10-16T02:16:01Z set scope=['mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/types/index.d.ts', 'plugin/lib/fmwatch.py', 'plugin/lib/ui-demo.json', 'plugin/tests/test_ui.py', 'README.md', 'CHANGELOG.md', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']
- 2026-10-16T02:28:29Z done
- 2026-10-16T02:28:30Z committed 1a0d996 (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- T-1023 [FEATURE M, done, 4 steps] Can you have a graph of sub agents/worktrees/brainstorms? — lesson: A list kept for a time window must be filtered at every draw, not o…
- T-1002 [FEATURE M, done, 3 steps] Pane readability: zones with dividers, breathing room between sections, aligned label/picture/value rows, fewer facts per line; still f…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Lessons
- A flex-ordered layout gives spare rows to the first section that wants them: a section whose rows only make sense together (a tree's root and children) needs its own minimum, not just a cap.
## Plan gaps
- added late: Done and left at a glance: a work bar (done today, now, queued, inbox, blocked) under the head; a segment per step unde…
- failed first: step 1 tests: tree rows with connectors and a worktree under its agent; history rows with titles; gradient…
- failed first: step 2 fm ui history (60, structured, with titles)
- failed first: step 5 Done and left at a glance: a work bar (done today, now, queued, inbox, blocked) under the head; a s…
## Files touched
- plugin/tests/test_ui.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
