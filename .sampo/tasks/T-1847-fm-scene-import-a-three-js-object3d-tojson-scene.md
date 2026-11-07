---
id: T-1847
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:20:59Z
updated: 2026-10-28T17:56:07Z
base: 0cc39ea02d85c0d4df8e09412d3322a843479cdc
base_tree: 32fd41c97b209309f20783fd6da662472701d3ec
plan0_at: 2026-10-28T17:43:23Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# fm scene import: a three.js Object3D.toJSON() scene to scene.json
## Raw request
> fm scene import: a three.js Object3D.toJSON() scene (BoxGeometry, SphereGeometry, PlaneGeometry, BufferGeometry, MeshStandardMaterial, lights, camera) to scene.json (from T-1635)
## Interpretation
fm scene import FILE [--out PATH]: read three.js JSON (format 4, Object3D.toJSON / ObjectLoader) and emit a validated scene.json: Box/Sphere/Plane/BufferGeometry, MeshStandard/Basic/Lambert/Phong colours, roughness, metalness, emissive, Ambient/Hemisphere/Directional/Point lights, a PerspectiveCamera, the scene background; nested Groups composed into world transforms (T * R * S, Euler XYZ); what scene.json can't hold (lines, points, textures, a second material) is left out and named.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene import turns a three.js JSON scene into a scene.json fm scene check accepts: geometries, materials, lights, camera, background and nested transforms carried; what it can't carry named — verify with `python3 plugin/tests/run.py Import`
## Non-goals
## Approach (options → choice → why)
Options: (a) pure-Python reader of the JSON into a scene dict, then validate(); (b) run three.js's ObjectLoader in node and walk it; (c) glTF as the bridge. Choice (a): no node or three.js needed, the JSON is documented and small; validate() keeps the output honest. No camera in the file → three's usual default (fov 50 at [0,0,5] toward the origin), said in the output.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: from_three() and fm scene import (red)
2. [x] from_three + import action (green), docs
## Resume here
<!-- auto -->
- 2026-10-28T17:50:22Z step 1/2: test: from_three() and fm scene import (red)
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/references/ui/scene-3d.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/import-impl2.py, plugin/tests/test_scene.py, plugin/lib/fmscene.py
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Import` → ✗ exit 1 · Ran 16 tests in 12.5s (3 classes, 16 at a time; slowest: ImportCards 12s, Import 0s, HookImportCost 0s) / FAILED (1 classes) [ran] [tree 9f66838eda82] (2026-10-28T17:43:48Z)
- (step 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 30 tests in 5.0s (8 classes, 16 at a time; slowest: Soak 5s, Offline 1s, Three 1s) / OK [ran] [tree e9245a3a9f92] (2026-10-28T17:45:17Z)
- (step 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 31 tests in 4.7s (8 classes, 16 at a time; slowest: Soak 4s, Import 2s, Offline 1s) / OK [ran] [tree 6d702137deb7] (2026-10-28T17:50:21Z)
- (ac 1) `python3 plugin/tests/run.py Import` → exit 0 · Ran 17 tests in 8.0s (3 classes, 16 at a time; slowest: ImportCards 8s, Import 2s, HookImportCost 0s) / OK [ran] [tree 6d702137deb7] (2026-10-28T17:55:41Z)
- (step 1) `python3 plugin/tests/run.py Import` → exit 0 · Ran 17 tests in 8.0s (3 classes, 16 at a time; slowest: ImportCards 8s, Import 2s, HookImportCost 0s) / OK [ran] [tree 6d702137deb7] (2026-10-28T17:55:41Z)
- (audit adversary) `one fm-reviewer pass (full five lenses): 5 MEDIUM, 3 LOW, all fixed test-first (escaped notes, vertex cap after sharing, wrong-kind fields as ValueError, hidden objects skipped, every drop named, per-part validation, _write_out shared, hostile-input test)` → fixed — escapes shown via _show, vertices capped at 1M after geometry sharing, wrong kinds are ValueError [tree 6d702137deb7] (2026-10-28T17:55:41Z)
- (audit edge) `one fm-reviewer pass (full five lenses): 5 MEDIUM, 3 LOW, all fixed test-first (escaped notes, vertex cap after sharing, wrong-kind fields as ValueError, hidden objects skipped, every drop named, per-part validation, _write_out shared, hostile-input test)` → fixed — top-down camera tilted, roll/shear/far clamp noted, mesh named camera renamed [tree 6d702137deb7] (2026-10-28T17:55:41Z)
- (audit intent) `one fm-reviewer pass (full five lenses): 5 MEDIUM, 3 LOW, all fixed test-first (escaped notes, vertex cap after sharing, wrong-kind fields as ValueError, hidden objects skipped, every drop named, per-part validation, _write_out shared, hostile-input test)` → fixed — every property it can't carry is named in left out, never silently dropped [tree 6d702137deb7] (2026-10-28T17:55:41Z)
- (audit operator) `one fm-reviewer pass (full five lenses): 5 MEDIUM, 3 LOW, all fixed test-first (escaped notes, vertex cap after sharing, wrong-kind fields as ValueError, hidden objects skipped, every drop named, per-part validation, _write_out shared, hostile-input test)` → ok — printed scene on stdout, note on stderr; --out names the counts [tree 6d702137deb7] (2026-10-28T17:55:41Z)
- (audit maintainer) `one fm-reviewer pass (full five lenses): 5 MEDIUM, 3 LOW, all fixed test-first (escaped notes, vertex cap after sharing, wrong-kind fields as ValueError, hidden objects skipped, every drop named, per-part validation, _write_out shared, hostile-input test)` → fixed — --out logic shared in _write_out, from_three wraps one _from_three [tree 6d702137deb7] (2026-10-28T17:55:41Z)
## Log
- 2026-10-28T17:20:59Z created
- 2026-10-28T17:35:40Z set title=fm scene import: a three.js Object3D.toJSON() scene to scene.json, scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T17:43:22Z focused
- 2026-10-28T17:49:25Z steer: review — 3 MEDIUM (escapes in notes, shared-geometry amplification, TypeError tracebacks), 2 MEDIUM intent (hidden objects drawn, silent drops), LOWs; fixing test-first
- 2026-10-28T17:56:06Z done
- 2026-10-28T17:56:07Z committed 5c3e2df4 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1633 [FEATURE M, done, 3 steps] scene.json: schema, validation and a three.js module compiler (fm scene compile), modelled on templates/scene.html — lesson: A scene fo…
- research T-1633-review: Approve with nits. I found no blocker. I had no Bash tool, so I did not run any test, including `test_scene.Three`. [stale: plugin/lib/fmscene.py…
- playbook 3D on the web: a designed scene that never breaks the page (fm playbooks show ui/scene-3d)
- decision 2026-10-23: T-1670: left out the recorded-time clock, the fm page timeline and forked-skill QA
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Lessons
- validate each imported part alone so a refusal is a note, not a failed import; bound vertices after sharing, not by file size
## Plan gaps
- failed first: step 1 test: from_three() and fm scene import (red)
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmscene.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/ui/scene-3d.md
