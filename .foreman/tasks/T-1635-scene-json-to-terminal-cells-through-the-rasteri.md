---
id: T-1635
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T20:57:40Z
updated: 2026-10-28T17:32:18Z
group: rasteriser-dependent 3D showpieces
base: 1339728913e19e3ce9fd6d70a50eb37439838bfb
base_tree: daf0a4fc8e67f164b77a44afb10d85938c6d9ffb
plan0_at: 2026-10-28T17:25:38Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md, MASTER.md]
verified: strong
---
# Scene.json to terminal cells through the rasteriser, a shader subset, import from three.js
## Raw request
> scene.json to terminal cells through the rasteriser, a shader subset, import from three.js (from T-1528; waits: after the rasteriser)
## Interpretation
Three pieces from T-1528: (1) fm scene cells FILE: scene.json drawn by fmraster and printed as terminal cells, two pixels per cell (an upper half block in 24-bit colour), so a scene previews in a terminal with no browser; (2) a shader subset; (3) import from three.js. This task ships (1); (2) and (3) are captured follow-ups, each its own task.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene cells FILE prints the scene as rows of 24-bit half-block cells, deterministic, back faces culled, a bad --cols refused — verify with `python3 plugin/tests/run.py Offline`
## Non-goals
## Approach (options → choice → why)
Options: (a) half blocks, fg = top pixel, bg = bottom pixel, truecolor; (b) a luminance ramp of ASCII characters; (c) sixel or kitty graphics. Choice: (a), because it is square pixels at twice the vertical density, works in any truecolor terminal, and reuses triangles() and fmraster.render() as turntable does. (b) loses colour; (c) is not supported everywhere.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: cells() and fm scene cells (red)
2. [x] build: fmscene.cells() and the cells action
3. [x] docs: scene-3d.md, CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-10-28T17:28:05Z step 1/3: test: cells() and fm scene cells (red)
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: plugin/lib/fmscene.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Offline` → ✗ exit 1 · Ran 8 tests in 1.4s (1 classes, 16 at a time; slowest: Offline 1s) / FAILED (1 classes) [ran] [tree 1cc838f7f214] (2026-10-28T17:25:50Z)
- (step 2) `python3 plugin/tests/run.py Offline Scene` → exit 0 · Ran 16 tests in 15.1s (2 classes, 16 at a time; slowest: Scene 15s, Offline 1s) / OK [ran] [tree 66ec453b7c38] (2026-10-28T17:26:25Z)
- (step 3) `grep -c 'fm scene cells' MASTER.md CHANGELOG.md plugin/skills/playbooks/references/ui/scene-3d.md` → ✗ exit 1 · CHANGELOG.md:0 / plugin/skills/playbooks/references/ui/scene-3d.md:0 [ran] [tree 66ec453b7c38] (2026-10-28T17:26:35Z)
- (step 3) `grep -c 'fm scene cells' MASTER.md CHANGELOG.md plugin/skills/playbooks/references/ui/scene-3d.md` → exit 0 · CHANGELOG.md:1 / plugin/skills/playbooks/references/ui/scene-3d.md:1 [ran] [tree b9130f60f8a9] (2026-10-28T17:26:49Z)
- (ac 1) `python3 plugin/tests/run.py Offline` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: Offline 1s) / OK [ran] [tree 83c2235ddcfc] (2026-10-28T17:31:52Z)
- (step 1) `python3 plugin/tests/run.py Offline` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: Offline 1s) / OK [ran] [tree 83c2235ddcfc] (2026-10-28T17:31:52Z)
- (audit intent) `one fm-reviewer pass over the diff (intent, edge, maintainer, operator); 3 LOW findings fixed; full gates green on the final tree` → ok, a scene.json previews in the terminal through fmraster with no browser [tree 83c2235ddcfc] (2026-10-28T17:31:52Z)
- (audit edge) `one fm-reviewer pass over the diff (intent, edge, maintainer, operator); 3 LOW findings fixed; full gates green on the final tree` → ok, cols 2-400 bound, a turned-away scene is all background, deterministic output [tree 83c2235ddcfc] (2026-10-28T17:31:52Z)
- (audit maintainer) `one fm-reviewer pass over the diff (intent, edge, maintainer, operator); 3 LOW findings fixed; full gates green on the final tree` → fixed, MASTER separator; _frame/_background shared with turntable [tree 83c2235ddcfc] (2026-10-28T17:31:52Z)
- (audit operator) `one fm-reviewer pass over the diff (intent, edge, maintainer, operator); 3 LOW findings fixed; full gates green on the final tree` → fixed, help names the truecolor need; NO_COLOR guard skipped (an explicit preview command) [tree 83c2235ddcfc] (2026-10-28T17:31:52Z)
## Log
- 2026-10-22T20:57:40Z created
- 2026-10-28T17:25:30Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/3d.md', 'MASTER.md']
- 2026-10-28T17:25:35Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md', 'MASTER.md']
- 2026-10-28T17:25:36Z focused
- 2026-10-28T17:32:16Z done
- 2026-10-28T17:32:18Z committed 579d11f7 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1528 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js,
- research T-1633-review: Approve with nits. I found no blocker. I had no Bash tool, so I did not run any test, including `test_scene.Three`. [stale: plugin/lib/fmscene.py…
- T-1530 [FEATURE L, done, 6 steps] Round 3 (T-1520): 3D verification: soak scenes headlessly for GPU leaks, a headless frame- — lesson: Check a lane for what the plan ass…
- decision 2026-10-23: T-1530 (L) self-approved after self-critique: offline-first 3D checks in fm scene; browser soak and frame budget split to T-1788
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Lessons
- A renderer's frame helper shared by turntable and cells keeps the camera maths in one place
## Plan gaps
- failed first: step 1 test: cells() and fm scene cells (red)
- failed first: step 3 docs: scene-3d.md, CHANGELOG, MASTER
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/ui/scene-3d.md
