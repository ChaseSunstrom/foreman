---
id: T-1530
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, plugin/tests/test_scene_verify.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:45Z
updated: 2026-10-23T15:44:07Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 8457fa336a6a8b59a799749c3d7e3fbec9f712dc
base_tree: ac5efa8739f2506dad81487f8dd1fc0c460908a5
plan0_at: 2026-10-23T15:25:31Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): 3D verification: soak scenes headlessly for GPU leaks, a headless frame-
## Raw request
> Round 3 (T-1520): 3D verification: soak scenes headlessly for GPU leaks, a headless frame-budget gate, turntable contact sheets, offline asset and shader validation, recorded camera paths replayed as the demo, and an injectable 3D dev HUD (a074 c160 c046 a167 c017 c164 c059). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
3D verification, offline where it can be: a camera path (an animation targeting the camera, replayed by the compiled module as the demo), a --hud dev build (frame rate, draw calls, triangles, geometries, textures and each render's ms on globalThis.__fmScene), fm scene check (a scene: validate and count; a .gltf/.glb: structural checks offline), fm scene turntable (a contact sheet drawn by fmraster, no browser or GPU), fm scene shader (glslangValidator when installed; card uniform tables match the code) and fm scene soak (the --hud build in headless Chrome when a browser and a three.js build are here: leaks, a frame budget, dispose back to the poster; skipped with the reason otherwise).
## Assumptions (confidence)
## Acceptance criteria
- [x] each check runs or skips with a reason; offline glTF validation catches a broken file — verify with `cd plugin/tests && python3 -m unittest test_scene_verify`
- [x] camera paths, the hud build, check, turntable and shader checks work, and the shipped shader cards pass — verify with `python3 plugin/tests/run.py test_scene`
## Non-goals
## Approach (options → choice → why)
Options: (a) everything in headless Chrome (needs three.js and WebGL, neither here); (b) offline first: the rasteriser for turntables, glslangValidator for shaders, the runtime for paths and the HUD; (c) a separate fm 3d verb. Choice: (b) inside fm scene: the scene→triangles step (T*R*S, look-at, the documented z flip and winding swap) is the rasteriser path T-1635 wanted anyway, and every check is deterministic and testable here. Risk: winding mistakes cull the wrong faces — a plane turned half round must vanish, which the test pins.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] soak and frame budget
3. [x] turntable and camera paths
4. [x] validation and HUD
5. [x] red tests: camera path, hud, turntable culling, check, shader cards
6. [x] fmscene: camera path, HUD, faces/triangles/turntable, shader checks, the CLI actions; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (3D checks offline), fm scene's own help and SCHEMA (camera paths)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene` → ✗ exit 1 · Ran 18 tests in 1.5s (5 classes, 16 at a time; slowest: Three 1s, Component 0s, Tag 0s) / FAILED (1 classes) [ran] [tree 16d588265504] (2026-10-23T15:25:18Z)
- (step 1) `python3 plugin/tests/run.py test_scene test_suite_hygiene test_cli test_raster` → exit 0 · Ran 166 tests in 23.4s (46 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 9s, AuditPrep 8s) / OK [ran] [tree 26eb1db52f09] (2026-10-23T15:26:34Z)
- (step 2) `python3 plugin/tests/run.py test_scene_verify` → ✗ exit 1 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: Soak 0s, Gltf 0s) / FAILED (2 classes) [ran] [tree 9c101958221c] (2026-10-23T15:28:26Z)
- (step 1) `python3 plugin/tests/run.py test_scene test_scene_verify test_suite_hygiene test_cli test_docs` → exit 0 · Ran 220 tests in 23.2s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 9s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:31:36Z)
- (step 2) `python3 plugin/tests/run.py test_scene test_scene_verify test_suite_hygiene test_cli test_docs` → exit 0 · Ran 220 tests in 23.2s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 8s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:32:00Z)
- (step 3) `python3 plugin/tests/run.py test_scene test_scene_verify test_suite_hygiene test_cli test_docs` → exit 0 · Ran 220 tests in 23.1s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 8s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:32:24Z)
- (step 4) `python3 plugin/tests/run.py test_scene test_scene_verify test_suite_hygiene test_cli test_docs` → exit 0 · Ran 220 tests in 23.4s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 8s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:32:48Z)
- (step 5) `python3 plugin/tests/run.py test_scene test_scene_verify test_suite_hygiene test_cli test_docs` → exit 0 · Ran 220 tests in 23.3s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, AuditPrep 9s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:33:12Z)
- (step 6) `python3 plugin/tests/run.py test_scene test_scene_verify test_suite_hygiene test_cli test_docs` → exit 0 · Ran 220 tests in 23.4s (61 classes, 16 at a time; slowest: TaskLifecycle 23s, Fences 9s, StateViews 9s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:33:36Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_scene_verify` → exit 0 · Ran 6 tests in 4.362s / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:33:41Z)
- (ac 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 24 tests in 4.5s (7 classes, 16 at a time; slowest: Soak 4s, Offline 1s, Three 1s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:33:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_scene_verify` → exit 0 · Ran 6 tests in 4.363s / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
- (ac 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 24 tests in 4.5s (7 classes, 16 at a time; slowest: Soak 4s, Offline 1s, Three 1s) / OK [ran] [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget); verified by eye: a turntable of a sphere, a turned box and a floor shows them orbiting with back faces culled; a real soak in headless Chrome with three r186 drew a moving scene, held geometries steady and returned to the poster on dispose; every shipped shader card passes glslangValidator and its uniform table` → soak, frame budget, turntable contact sheets, offline asset (glTF) and shader validation, camera paths as the demo and an injectable HUD — all six parts the request named, each an fm scene verb usable from Claude Code; the optional browser and three.js are detected, never installed [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget); verified by eye: a turntable of a sphere, a turned box and a floor shows them orbiting with back faces culled; a real soak in headless Chrome with three r186 drew a moving scene, held geometries steady and returned to the poster on dispose; every shipped shader card passes glslangValidator and its uniform table` → a static scene draws only on change, so its soak has few frames (said in the count); a guidance card with no glsl block isn't a failure; a sphere's empty pole faces are dropped; --frames 1-36 and --seconds 1-600 are bounded; a .glb's missing BIN chunk leaves buffer 0's length unknown rather than wrong [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget); verified by eye: a turntable of a sphere, a turned box and a floor shows them orbiting with back faces culled; a real soak in headless Chrome with three r186 drew a moving scene, held geometries steady and returned to the poster on dispose; every shipped shader card passes glslangValidator and its uniform table` → a glTF buffer URI that leaves the asset's folder (../, absolute) is reported and never opened; the soak serves only a temp folder it wrote, on 127.0.0.1 with port 0, and stops the server and browser in finally; the SwiftShader shim lives in the soak page, never in the compiled module, so production keeps failIfMajorPerformanceCaveat; glslangValidator gets a temp file path, no shell [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
- (audit operator) `self review in the main thread (subagents paused by the usage budget); verified by eye: a turntable of a sphere, a turned box and a floor shows them orbiting with back faces culled; a real soak in headless Chrome with three r186 drew a moving scene, held geometries steady and returned to the poster on dispose; every shipped shader card passes glslangValidator and its uniform table` → every new verb says what it skipped and why (no glslangValidator: compile checks skipped; no browser or three.js: soak skipped, exit 0), exits 1 only on a finding and 2 on a bad input; the soak's cost is bounded by --seconds and one browser; turntable is pure Python, about a second a megapixel, noted in its docstring [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
- (audit maintainer) `self review in the main thread (subagents paused by the usage budget); verified by eye: a turntable of a sphere, a turned box and a floor shows them orbiting with back faces culled; a real soak in headless Chrome with three r186 drew a moving scene, held geometries steady and returned to the poster on dispose; every shipped shader card passes glslangValidator and its uniform table` → the scene→triangles step documents the same conventions SCHEMA states (Rx*Ry*Rz, T*R*S, the z flip and winding swap) and a culling test pins them; the HUD is one string spliced at one RENDER_CALL marker; glTF and soak live beside the compiler in fmscene with their own test file (test_scene_verify) [tree cd04b7d6d601] (2026-10-23T15:34:15Z)
## Log
- 2026-10-22T17:43:45Z created
- 2026-10-22T17:58:09Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_scene_verify.py', 'CHANGELOG.md']
- 2026-10-23T15:03:31Z set tier=L, scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:25:12Z lane: ~/.claude/foreman.lanes/T-1530 on foreman/T-1530
- 2026-10-23T15:25:29Z set approved=True
- 2026-10-23T15:25:30Z focused
- 2026-10-23T15:31:12Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'plugin/tests/test_scene_verify.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:34:39Z done
- 2026-10-23T15:34:41Z committed 0ac9bc70 (6 files)
- 2026-10-23T15:44:02Z merged foreman/T-1530 (6 file(s))
- 2026-10-23T15:44:07Z lane removed: ~/.claude/foreman.lanes/T-1530
## Follow-ups captured
## Build vs reuse
Reuses fmscene's validate/load/compile_three and RUNTIME (camera path and HUD are small edits there), fmraster.render for every turntable frame (no new renderer), fmimg.save for the PNG, and glslangValidator from PATH for GLSL (no parser of our own). New code is only the scene→triangles step the rasteriser lacked and the card uniform-table check.
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1528 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js,
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Lessons
- Check a lane for what the plan assumed missing: a headless Chrome and a three.js build were both on this machine, so the browser soak shipped tested instead of deferred
## Plan gaps
- failed first: step 1 failing tests
- failed first: step 2 soak and frame budget
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/tests/test_scene.py
- plugin/tests/test_scene_verify.py
