---
id: T-1852
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:30:42Z
updated: 2026-10-28T18:53:16Z
base: 5d8f01c658e4a2bddfa6980ad842057a065badca
base_tree: a88bb627c21c0ef8eb2ddb4c7cfa5f311ba7c15e
plan0_at: 2026-10-28T18:42:42Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# 3D showpiece: the lookbook room, look cards hung in a 3D gallery (from T-1655)
## Raw request
> 3D showpiece: the lookbook room, look cards hung in a 3D gallery (from T-1655)
## Interpretation
From T-1655's 3D showpieces: hang the look cards (fmtaste.looks(), ranked by fmtaste.rank()) in a three-walled gallery as a scene.json, each look a dark frame with its palette as colour-field bands, so fm scene cells/turntable/compile can show the taste library in 3D. No FILE; --count 1-12, default 8.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene lookbook prints a scene fm scene check accepts: a frame per look (best-ranked first, --count N), its palette as swatch boxes in the look's colours, walls and floor — verify with `python3 plugin/tests/run.py Lookbook`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm scene lookbook builds a gallery room from fmtaste.looks(): each look a dark frame box on a wall, its palette as a row of coloured swatch boxes inside the frame, best-ranked first (fmtaste.rank()); (b) textures of rendered cards (scene.json has no textures: no); (c) one long wall vs a U of three walls. Choice: (a) with a U of three walls, up to --count looks (default 8, 1-22), frames named after the look, swatches <look>-<j>. Why: reuses looks()/rank(), stays in scene.json's schema, fm scene check/cells/turntable/compile view it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Lookbook test, red
2. [x] lookbook(), CLI arm, docs, green
3. [x] Review fixes: every frame in view, flush on its wall, --count 0 tested
## Resume here
<!-- auto -->
- 2026-10-28T18:47:56Z steps 3/3 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: MASTER.md, plugin/lib/fmcli.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py, plugin/lib/fmscene.py, CHANGELOG.md
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Lookbook` → red as expected (exit 1) · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Lookbook 0s) / FAILED (1 classes) [ran] [tree c3dc134fe633] (2026-10-28T18:42:50Z)
- (step 2) `python3 plugin/tests/run.py Lookbook` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Lookbook 0s) / OK [ran] [tree 83e05863639c] (2026-10-28T18:43:52Z)
- (step 3) `python3 plugin/tests/run.py Lookbook` → red as expected (exit 1) · Ran 3 tests in 2.1s (1 classes, 16 at a time; slowest: Lookbook 1s) / FAILED (1 classes) [ran] [tree 2cc1c4693276] (2026-10-28T18:47:12Z)
- (step 3) `python3 plugin/tests/run.py Lookbook` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Lookbook 1s) / OK [ran] [tree 3fe8e2d35235] (2026-10-28T18:47:37Z)
- (ac 1) `python3 plugin/tests/run.py Lookbook` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Lookbook 0s) / OK [ran] [tree 3fe8e2d35235] (2026-10-28T18:52:49Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 4 fixed test-first (side frames in view, wording, flush frames, --count 0), 1 skipped` → every frame now hangs flush and in the camera's view; the docs say where each row hangs [tree 3fe8e2d35235] (2026-10-28T18:52:49Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 4 fixed test-first (side frames in view, wording, flush frames, --count 0), 1 skipped` → palettes are regex hex and material names c+hex, so no collision with walls or floor [tree 3fe8e2d35235] (2026-10-28T18:52:49Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 4 fixed test-first (side frames in view, wording, flush frames, --count 0), 1 skipped` → --count 0 and 13 exit 2 naming 1 to 12; odd card filenames would fail validate, shipped ones are safe [tree 3fe8e2d35235] (2026-10-28T18:52:49Z)
- (audit operator) `one fm-reviewer pass: approve with nits; 4 fixed test-first (side frames in view, wording, flush frames, --count 0), 1 skipped` → a local write only (--out); docs agree with the CLI help [tree 3fe8e2d35235] (2026-10-28T18:52:49Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 4 fixed test-first (side frames in view, wording, flush frames, --count 0), 1 skipped` → a flush-and-in-view test guards every slot [tree 3fe8e2d35235] (2026-10-28T18:52:49Z)
## Log
- 2026-10-28T17:30:42Z created
- 2026-10-28T18:31:54Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T18:42:41Z focused
- 2026-10-28T18:53:14Z done
- 2026-10-28T18:53:16Z committed 95c36696 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1848 [FEATURE M, done, 2 steps] 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655) — lesson: Before the gates, run fm check playbooks …
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- T-1849 [FEATURE M, done, 2 steps] 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-16 — lesson: A playbook trim can delete text a …
- decision 2026-10-23: T-1525: leave out 'borrow from' analogy cards and live exemplars on the field guide
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-28): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Lessons
- A gallery's slots need a field-of-view test: check every frame's corners against the camera's half-angle, not just the first row
## Plan gaps
- added late: Review fixes: every frame in view, flush on its wall, --count 0 tested
## Files touched
- plugin/tests/test_scene.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/skills/playbooks/references/ui/scene-3d.md
