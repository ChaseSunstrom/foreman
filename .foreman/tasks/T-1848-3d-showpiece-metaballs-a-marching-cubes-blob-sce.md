---
id: T-1848
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:30:40Z
updated: 2026-10-28T18:09:44Z
base: 5c3e2df4bc970b9ea8a8350c2aae420ff30cc2c1
base_tree: 6d702137deb7e083245003aaff610f6c17e1fea1
plan0_at: 2026-10-28T17:56:22Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655)
## Raw request
> 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655)
## Interpretation
fm scene metaballs [--balls N] [--grid G] [--seed S] [--out PATH]: a scene.json of a metaball blob, the field sum r²/d² of N seeded balls polygonised at threshold 1 on a G³ grid into one vertices mesh (outward, counter-clockwise faces), with a camera, lights and a floor; fm scene cells/compile/turntable then show it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene metaballs prints a scene.json fm scene check accepts: one closed blob mesh, deterministic per seed, faces facing out, bounded by --grid — verify with `python3 plugin/tests/run.py Metaballs`
## Non-goals
## Approach (options → choice → why)
Options: (a) marching cubes with the 256-entry edge/triangle tables; (b) marching tetrahedra, each cube split into 6 tets, 0-2 triangles per tet from 16 cases; (c) a static starter scene.json. Choice (b): about 40 lines with no tables, watertight and deterministic; a little more triangles than (a), bounded by the grid (G 8-48). Vertices shared by edge key so the mesh stays small; winding fixed by the field gradient.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: metaballs() and fm scene metaballs (red)
2. [x] marching tetrahedra + action (green), docs
## Resume here
<!-- auto -->
- 2026-10-28T17:59:06Z steps 2/2 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: plugin/tests/test_scene.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/terrain-test.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/terrain-impl.py
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Metaballs` → red as expected (exit 1) · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Metaballs 0s) / FAILED (1 classes) [ran] [tree 1f61bd1abf8d] (2026-10-28T17:56:29Z)
- (step 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 34 tests in 5.1s (9 classes, 16 at a time; slowest: Soak 5s, Import 3s, Offline 2s) / OK [ran] [tree a08f7de35fe6] (2026-10-28T17:57:03Z)
- (step 1) `python3 plugin/tests/run.py Metaballs` → red as expected (exit 1) · Ran 3 tests in 3.5s (1 classes, 16 at a time; slowest: Metaballs 3s) / FAILED (1 classes) [ran] [tree 3ce1fcaaa073] (2026-10-28T18:00:39Z)
- (step 2) `python3 plugin/tests/run.py Metaballs` → exit 0 · Ran 3 tests in 2.1s (1 classes, 16 at a time; slowest: Metaballs 2s) / OK [ran] [tree 4291b6351b2b] (2026-10-28T18:00:51Z)
- (ac 1) `python3 plugin/tests/run.py Metaballs` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: Metaballs 1s) / OK [ran] [tree e322cee0da00] (2026-10-28T18:09:18Z)
- (audit intent) `one fm-reviewer pass over five lenses (saved as T-1848-review); its three findings were confirmed and fixed test-first: the FILE check moved to the top of cmd_scene, metaballs refuses a FILE, and the test now asserts exit 2 with no traceback for check/shader/soak/compile` → criteria met; closed, outward, seeded, bounded by --grid [tree e322cee0da00] (2026-10-28T18:09:18Z)
- (audit adversary) `one fm-reviewer pass over five lenses (saved as T-1848-review); its three findings were confirmed and fixed test-first: the FILE check moved to the top of cmd_scene, metaballs refuses a FILE, and the test now asserts exit 2 with no traceback for check/shader/soak/compile` → no untrusted input reaches a sink; ints range-checked; --out through write_atomic [tree e322cee0da00] (2026-10-28T18:09:18Z)
- (audit edge) `one fm-reviewer pass over five lenses (saved as T-1848-review); its three findings were confirmed and fixed test-first: the FILE check moved to the top of cmd_scene, metaballs refuses a FILE, and the test now asserts exit 2 with no traceback for check/shader/soak/compile` → missing FILE crashed check/shader/soak, fixed; empty surface now a clean ValueError; grid 48 measured at 11.7k-16.5k vertices [tree e322cee0da00] (2026-10-28T18:09:18Z)
- (audit operator) `one fm-reviewer pass over five lenses (saved as T-1848-review); its three findings were confirmed and fixed test-first: the FILE check moved to the top of cmd_scene, metaballs refuses a FILE, and the test now asserts exit 2 with no traceback for check/shader/soak/compile` → grid 48 with 12 balls takes a few seconds; output well under MAX_FILE [tree e322cee0da00] (2026-10-28T18:09:18Z)
- (audit maintainer) `one fm-reviewer pass over five lenses (saved as T-1848-review); its three findings were confirmed and fixed test-first: the FILE check moved to the top of cmd_scene, metaballs refuses a FILE, and the test now asserts exit 2 with no traceback for check/shader/soak/compile` → the weak nonzero assertion replaced by exit 2 and no Traceback [tree e322cee0da00] (2026-10-28T18:09:18Z)
## Log
- 2026-10-28T17:30:40Z created
- 2026-10-28T17:46:39Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T17:56:20Z focused
- 2026-10-28T18:09:42Z done
- 2026-10-28T18:09:44Z committed a96e7df6 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1633 [FEATURE M, done, 3 steps] scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html — lesson: A scene fo…
- research T-1847-review: Verdict: changes needed.** The math and the three.js conventions check out. The faults are in hostile-input handling and in what the notes leave …
- T-1635 [FEATURE M, done, 3 steps] Scene.json to terminal cells through the rasteriser, a shader subset, import from three.js — lesson: A renderer's frame helper shared b…
- decision 2026-10-23: T-1670: left out the recorded-time clock, the fm page timeline and forked-skill QA
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Lessons
- Before the gates, run fm check playbooks after editing a playbook reference: the token ratchet allows 10% + 50 of growth per file, and two showpiece paragraphs in a row went past it
## Files touched
- plugin/tests/test_scene.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/skills/playbooks/references/ui/scene-3d.md
