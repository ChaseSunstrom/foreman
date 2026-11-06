# Brainstorm — lens: deepen: 3d

- **Make `scene.json` the single source and add a `fm scene` verb** — FEATURE — value 5 — effort L — risk med — category: 3d-core
  Why: the list already has "compile one scene spec to WebGL, canvas and the TUI" and `<fm-scene>` as separate ideas; combined, one spec file plus one verb (`fm scene new|build|check|shot`) is the capability and the others become its targets. Assumption: the spec is declarative (meshes, lights, camera path, materials) and stdlib Python does the compile.
  Done when: `fm scene build demo.json` emits an HTML page, a canvas fallback and a TUI frame from the same file, and a test asserts all three list the same object ids.

- **Gate 3D work on a headless frame-budget check** — FEATURE — value 5 — effort M — risk med — category: 3d-verify
  Why: the pack says cards give verify commands but none teaches scene quality; "budget probe" and "WebGL survival contract" recur. Foreman's whole premise is proof by commands that ran. Assumption: a headless browser is optional, so the fallback is a static count of draw calls, triangles, texture bytes and lights read from the spec.
  Done when: `fm scene check` fails a fixture with 2M triangles, naming the budget exceeded, and passes the starter scene.

- **Add a visual-diff verify step for scenes and UI** — FEATURE — value 4 — effort M — risk med — category: 3d-verify
  Why: "visual QA" is missing from the playbooks, and `fm task prove` shows tests fail without the change; a pixel version proves a look changed on purpose. Assumption: screenshots come from the software rasteriser below, so they are deterministic.
  Done when: `fm scene shot` twice on the same spec gives byte-identical PNGs, and a changed material makes `fm scene diff` report a nonzero changed-pixel count.

- **Ship a stdlib software rasteriser for deterministic frames** — FEATURE — value 4 — effort L — risk med — category: 3d-render
  Why: the TUI needs 3D and the pack's constraint is stdlib-only; the same rasteriser gives CI a renderer with no GPU. This extends "integer-only maths in the TUI rasteriser" into the shared engine.
  Done when: a unit test renders a cube with flat shading to a 64x64 buffer and matches a stored hash.

- **Add a "taste" playbook set: look, motion, light** — FEATURE — value 5 — effort M — risk low — category: 3d-playbooks
  Why: cards give pitfalls, "none teaches taste". Three original-writing playbooks: palette and material direction (avoid default grey-blue gradient blobs), light rigs (key, rim, bounce, fog), and camera and easing choreography. Each carries a before/after checklist Claude must answer before writing code.
  Done when: `/foreman:playbooks` lists the three under ui, and an eval case shows the checklist is cited in a produced scene.

- **Record camera paths and replay them as the demo** — FEATURE — value 3 — effort M — risk low — category: 3d-motion
  Why: "direct the camera with a recorded path" is in the list; tying it to `demo/` makes the recorded path the repeatable hero shot for the site and the cast recordings. Assumption: the spec stores keyframes with named easings.
  Done when: replaying the same path twice produces identical frame hashes, and the site build embeds the result.

- **Generate a "proof chain" 3D hero from the task ledger** — FEATURE — value 3 — effort M — risk low — category: 3d-viz
  Why: the pack's own idea, but make it a standing `fm page` section: each task is a node, with edges for blocks and for tests-fail-without-change proofs, glowing when proven. Assumption: ledger data is readable as JSON by `fm`.
  Done when: `fm page` with a fixture ledger includes a scene whose node count equals the task count.

- **Add a shader looks shelf with generated thumbnails** — FEATURE — value 3 — effort M — risk low — category: 3d-shaders
  Why: the pack lists the shader shelf idea, and thumbnails come free from the rasteriser or a CPU GLSL-subset interpreter. Each snippet is original, licence-clean, and carries a cost note.
  Done when: `fm lib show shader-looks` lists at least 12 looks, each with a thumbnail file and an instruction-count estimate.

- **Add a 3D lint that catches common generated-scene failures** — FIX — value 4 — effort S — risk low — category: 3d-verify
  Why: the pack's "validate assets and shaders offline" extended into rules: unlit meshes, missing `dispose` of geometries, no resize handler, an unbounded `requestAnimationFrame` with no reduced-motion path, NaN-prone normalisation of zero vectors.
  Done when: `fm scene check` flags each seeded defect in a fixture directory by rule name.

- **Honour reduced-motion and a fallback poster in every scene** — FEATURE — value 4 — effort S — risk low — category: 3d-a11y
  Why: the pack notes accessibility audits are missing; this makes it a required property of `<fm-scene>`: a static poster, a pause control, keyboard-orbit, and a text description generated from the spec.
  Done when: with `prefers-reduced-motion` set, a test shows no animation loop starts and the alt description is present.

- **Wild: Let the fm code app show a live spinning 3D model of the running task graph** — FEATURE — value 3 — effort M — risk low — category: 3d-tui
  Why: wild. A half-block or braille rasteriser panel in the TUI, orbiting the agent graph, with the active slot pulsing. The pack has panels, extensions, shimmer and glow, so the panel slot exists.
  Done when: the panel renders at 30 fps on a 120x40 terminal in a test harness without exceeding a stated CPU budget, and degrades to a static frame when the terminal is narrow.

- **Wild: Turn the guard into a visible 3D airlock in demos** — FEATURE — value 2 — effort S — risk low — category: 3d-story
  Why: wild. The guard blocking dangerous commands is Foreman's main trust story; a short scene where commands travel as crates through a gate, red ones bounced, is shareable on the site. It is driven by real guard-corpus verdicts, not invented ones.
  Done when: the scene is generated from the evasion corpus's verdict list, and the crate counts match the corpus pass/block totals.

- **Wild: Render the bench as a diorama race** — FEATURE — value 2 — effort M — risk low — category: 3d-viz
  Why: wild. The duel against plain Claude Code (T-1231) becomes two tracks whose cars move by tasks passed, cost and time, built from the bench results file. It is a more memorable form for the benchmarks page and the "where Foreman loses" section (T-1261).
  Done when: the benchmarks page build includes a scene whose two lanes' lengths are proportional to the stored pass counts.

- **Add a scene-to-spec reverse import for hand-written three.js** — FEATURE — value 3 — effort L — risk high — category: 3d-migration
  Why: assumption: users already have three.js code. A conservative parser reads simple `new Mesh(...)` and light constructors into `scene.json`, and refuses anything it cannot map instead of guessing.
  Done when: a fixture with five meshes and two lights imports to a spec with those seven objects, and a fixture using a custom `ShaderMaterial` is reported as unsupported with its line.
