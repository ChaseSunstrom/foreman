---
id: T-1631
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmraster.py, plugin/tests/test_raster.py, CHANGELOG.md]
depends_on: [T-1630]
source: user
created: 2026-10-22T20:57:26Z
updated: 2026-10-22T22:27:45Z
base: 51613cee7ddf94281d5ca2f700a0f94e8a81d349
base_tree: b70f38fa5e28ee47eb85d42d03128d133efecbf7
plan0_at: 2026-10-22T21:56:16Z
plan0_scope: [plugin/lib/fmraster.py, plugin/tests/test_raster.py, CHANGELOG.md]
verified: strong
---
# Integer software rasteriser: z-buffer, flat shading, a lit cube byte-identical on every run
## Raw request
> Integer software rasteriser: z-buffer, flat shading, a lit cube byte-identical on every run
## Interpretation
plugin/lib/fmraster.py is an integer software rasteriser: triangles with edge functions, a z-buffer, flat shading from one directional light, a perspective camera, output as RGB rows written to PNG through fmimg (T-1630). A lit cube renders to identical bytes on every run and machine. It's the deterministic frame source for tests and terminal previews.
## Assumptions (confidence)
## Acceptance criteria
- [x] two renders of a lit cube are byte-identical PNGs — verify with `python3 plugin/tests/run.py test_raster.Cube`
## Non-goals
## Approach (options → choice → why)
Options: OpenGL via a binding (a dependency, GPU-dependent bytes); floating-point rasterisation (platform-dependent rounding); integer and fixed-point maths in pure Python. Choice: fixed-point integers: byte-identical everywhere, stdlib only; speed is fine for small test frames (ponytail: no textures, no clipping beyond the near plane).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] edge functions and z-buffer
3. [x] flat lighting, PNG through fmimg
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_raster.Cube` → ✗ exit 1 · run.py: no test matches test_raster.Cube [ran] [tree e79102f2d9fe] (2026-10-22T21:59:50Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Cube 2>&1 | grep -v "^ File\|^Traceback" | tail -30` → ✗ exit 1 · Ran 6 tests in 0.3s (1 classes, 16 at a time; slowest: Cube 0s) / FAILED (1 classes) [ran] [tree b28a11d9b5de] (2026-10-22T22:00:18Z)
- (step 2) `python3 plugin/tests/run.py test_raster.Cube` → exit 0 · Ran 6 tests in 0.3s (1 classes, 16 at a time; slowest: Cube 0s) / OK [ran] [tree 5d6e0de711b3] (2026-10-22T22:00:40Z)
- (step 3) `python3 plugin/tests/run.py test_raster.Cube` → exit 0 · Ran 6 tests in 0.3s (1 classes, 16 at a time; slowest: Cube 0s) / OK [ran] [tree cb7ee58bbcc9] (2026-10-22T22:01:13Z)
- (step 3) `python3 plugin/tests/run.py test_raster.Cube` → ✗ exit 1 · Ran 8 tests in 47.9s (1 classes, 16 at a time; slowest: Cube 48s) / FAILED (1 classes) [ran] [tree ae2d7c9ea4a8] (2026-10-22T22:11:47Z)
- (step 3) `python3 plugin/tests/run.py test_raster.Cube` → exit 0 · Ran 8 tests in 0.3s (1 classes, 16 at a time; slowest: Cube 0s) / OK [ran] [tree 73c8c320eadc] (2026-10-22T22:12:54Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Cube` → exit 0 · Ran 8 tests in 0.3s (1 classes, 16 at a time; slowest: Cube 0s) / OK [ran] [tree 04c1383ea274] (2026-10-22T22:27:19Z)
- (step 3) `python3 plugin/tests/run.py test_raster test_scene` → exit 0 · Ran 29 tests in 1.8s (4 classes, 16 at a time; slowest: Img 2s, Three 1s, Cube 0s) / OK [ran] [tree 04c1383ea274] (2026-10-22T22:27:21Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1631-review.md)` → ints-only inputs validated; colours can't silently become black; a work budget refuses runaway renders before drawing [tree 04c1383ea274] (2026-10-22T22:27:21Z)
- (audit edge) `review edge lens` → near-plane clipping in integer maths (floor quad test); 4 MP frame cap; far z documented [tree 04c1383ea274] (2026-10-22T22:27:22Z)
- (audit operator) `render/save via tests; byte-identical PNGs within a run, pixel hash pinned across seeds` → zlib-build dependence of PNG bytes documented [tree 04c1383ea274] (2026-10-22T22:27:22Z)
- (audit maintainer) `camera convention documented incl. winding reversal from three.js; fill-rule comment corrected` → clean [tree 04c1383ea274] (2026-10-22T22:27:22Z)
- (audit intent) `criterion: two renders of a lit cube are byte-identical PNGs` → met (20 tests) [tree 04c1383ea274] (2026-10-22T22:27:23Z)
- (ac 1) `python3 plugin/tests/run.py test_raster.Cube` → exit 0 · Ran 8 tests in 0.3s (1 classes, 16 at a time; slowest: Cube 0s) / OK [ran] [tree 04c1383ea274] (2026-10-22T22:27:24Z)
- (audit adversary) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → bounded work, validated inputs [tree 04c1383ea274] (2026-10-22T22:27:24Z)
- (audit edge) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → near-plane clipping [tree 04c1383ea274] (2026-10-22T22:27:24Z)
- (audit intent) `one fm-reviewer five-lens pass; all findings fixed test-first; criterion green after the merge` → met [tree 04c1383ea274] (2026-10-22T22:27:24Z)
## Log
- 2026-10-22T20:57:26Z created
- 2026-10-22T20:57:26Z set scope=['plugin/lib/fmraster.py', 'plugin/tests/test_raster.py', 'CHANGELOG.md']
- 2026-10-22T20:57:27Z split from T-1529 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:57:28Z set depends_on=['T-1630']
- 2026-10-22T21:29:52Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_raster.Cube`
- 2026-10-22T21:30:16Z criterion 1 text: two renders of a lit cube are byte-identical PNGs — verify with python3 plugin/tests/run.py test_raster.Cube → two renders of a lit cube are byte-identical PNGs
- 2026-10-22T21:55:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1631.builder.md
- 2026-10-22T21:56:15Z focused
- 2026-10-22T22:27:07Z merged worktree-agent-ae2e8d9645fd8f43a (4 file(s))
- 2026-10-22T22:27:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae2e8d9645fd8f43a
- 2026-10-22T22:27:08Z focused
- 2026-10-22T22:27:23Z scope: MASTER.md fmraster entry (self-docs)
- 2026-10-22T22:27:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1529 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Stdlib pixels: a software 3D rasteriser for deterministic frames (intege
- playbook 3D on the web: a designed scene that never breaks the page (skills/playbooks/references/ui/scene-3d.md)
- T-1630 [FEATURE M, done, 3 steps] fm img: stdlib PNG encode/decode and a pixel diff with a changed-pixel count — lesson: A bomb test must fail without the cap it protect…
- decision 2026-10-20: Self-approve T-1300 (L): an own ANSI truecolor renderer replaces curses; motion as a pure function of state and time
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmraster.py, plugin/tests/test_raster.py; re-ground the plan against them before editing
## Why not caught
the cube test draws 12 small triangles
## Lessons
- A renderer fed by data needs a work budget, not only a frame cap: cost is triangles times box area
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_raster.py
- plugin/lib/fmraster.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdesign.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmmotion.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmscene.py
- plugin/skills/doctor/SKILL.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/ui/scene-3d.md
- plugin/skills/playbooks/references/ui/templates/scene.html
- plugin/skills/playbooks/references/verify/verification-loop.md
- plugin/tests/fixtures/design/afterglow/crafted.css
- plugin/tests/fixtures/design/afterglow/crafted_nest.css
- plugin/tests/fixtures/design/afterglow/crafted_star.css
- plugin/tests/fixtures/design/afterglow/slop.css
- plugin/tests/test_guard_hardening.py
- plugin/tests/test_lanes.py
- plugin/tests/test_motion_score.py
- plugin/tests/test_motion_verify.py
- plugin/tests/test_playbook_machinery.py
- plugin/tests/test_scene.py
