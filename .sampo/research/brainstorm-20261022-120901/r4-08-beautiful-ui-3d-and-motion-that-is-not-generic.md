# Brainstorm — lens: beautiful UI, 3D and motion that is not generic

- **Ship a Look Grammar playbook: one signature motif, one material, one motion verb per project** — FEATURE — value 5 — effort M — risk low — category: design direction
  Why: the pack has one 13-line ui playbook and ~400 listed ideas but none that defines what "non-generic" means as a constraint set; cards give pitfalls, not taste. Assumption: three committed choices (motif, material, verb) are checkable and enough to break generic output.
  Done when: a UI task's DESIGN.md names a motif, material and motion verb, and `fm check design` fails a page where the motif appears in fewer than 3 distinct components.

- **Build a Light-and-Material shelf of ten original recipes with measured cost** — FEATURE — value 5 — effort L — risk med — category: 3D, shaders
  Why: the library has three-js, react-three-fiber, postprocessing and glsl cards but nothing teaches how a scene should look. Assumption: recipes (clay, brushed metal, frosted glass, phosphor, paper cut, wet ink, etc.) can be written originally, each a small runnable file plus a frame-time number.
  Done when: each recipe renders headlessly, a screenshot lands in the gallery, and the playbook lists its draw calls and ms per frame.

- **Add scene-camera blocking: named shots, dolly and focus pulls as data** — FEATURE — value 4 — effort M — risk low — category: 3D, motion
  Why: round-3 ideas cover scenes and scoring, none covers camera as a designed thing. Assumption: a short `shots.toml` (establishing, push-in, rack focus, orbit-settle) compiles to three.js tweens and a TUI pseudo-3D camera.
  Done when: one shots file drives both a web scene and the TUI track, and their keyframe times match within one frame in a test.

- **Write the Typography-as-Texture playbook with a measured type specimen generator** — FEATURE — value 4 — effort M — risk low — category: typography
  Why: typography cards exist; the site's self-hosting task (S24) implies fonts are chosen with no direction. Assumption: generating a specimen page from DESIGN.md tokens catches weak hierarchy before code.
  Done when: `fm design specimen` writes one self-contained HTML page showing the type scale, pairing and fluid sizes, with no third-party host.

- **Add a Dissonance pass: deliberately break one rule per screen and keep it if it survives review** — FEATURE — value 3 — effort S — risk low — category: design direction
  Why: generic UI comes from every rule obeyed equally; the user's "non generic" ask implies a point of tension. Assumption: a single sanctioned violation (scale jump, off-grid element, harsh colour) improves memorability.
  Done when: a UI task receipt names its one deliberate violation, and the critic reviewer confirms it reads as intentional.

- **Ship terminal sub-pixel 3D: a stdlib half-block rasteriser with lit, shaded solids for the station track** — FEATURE — value 4 — effort L — risk med — category: TUI 3D
  Why: the TUI has shimmer and fades but no depth; the ideas list mentions a rasteriser only as a wild line. Assumption: a few-hundred-line integer renderer at 12 fps fits the paint budget.
  Done when: `fm code tui --scene` shows a rotating lit extrusion of the stage rail, stays under the CPU ratchet, and a golden frame test passes.

- **Compile one Material Language into web CSS, SVG filters and TUI cell shading** — FEATURE — value 4 — effort L — risk med — category: design systems
  Why: round 3 proposes one token file; none gives materials (edge light, grain, shadow, depth) that translate across surfaces. Assumption: five material definitions map to a cell-shader function and CSS custom properties.
  Done when: switching material `paper`→`glass` changes the site, pane and TUI together, verified by three screenshots.

- **Add a Specimen Wall: every design recipe ships a living one-file example and a 3-second poster loop** — FEATURE — value 3 — effort M — risk low — category: gallery
  Why: playbooks teach in prose while the user wants visible results. Assumption: poster loops can be rendered headlessly into animated SVG or WebP.
  Done when: the site gallery lists each recipe with a loop under 300 KB, and the build fails if a recipe lacks one.

- **Gate motion by a Choreography Diff: before/after filmstrip with measured easing curves** — FEATURE — value 4 — effort M — risk med — category: motion QA
  Why: motion tokens are proposed, but nothing proves a change actually moved as specified. Assumption: sampling a page at fixed frames can recover timing within tolerance.
  Done when: a motion change task fails verify when sampled easing deviates more than 10% from its declared score.

- **Wild: Raymarch a living subway-map of the queue on the site hero, driven by the real task ledger** — FEATURE — value 4 — effort L — risk med — category: 3D hero — wild
  Why: assumption: the hero is a static SVG; a scene where closed tasks light stations makes the product's claim visible.
  Done when: the hero loads under 150 KB of script, falls back to a baked image without WebGL, and a test shows station count equals ledger count.

- **Wild: Run a Style Séance that deals three one-screen directions as playable thumbnails and learns from the pick** — FEATURE — value 4 — effort L — risk med — category: taste learning — wild
  Why: assumption: showing rendered directions beats asking taste questions; picks stay local.
  Done when: a vague brief produces three rendered directions in under a minute and the chosen one is written to DESIGN.md with a "because" line.

- **Wild: Make the TUI settings screen a physical control surface, with detented dials and a live ghost of the previous value** — FEATURE — value 3 — effort M — risk low — category: TUI config — wild
  Why: the user wants config in the TUI; most listed ideas are forms, not tactile. Assumption: arrow-key detents with a ghost preview make numeric settings feel tuned, not typed.
  Done when: adjusting motion intensity re-renders the live frame per detent and Esc restores the previous value exactly.

- **Add an Afterglow lint: every state change must leave a trace that decays, and no trace may exceed 600 ms** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: motion should explain state without lingering; assumption: a decay table and cap are checkable in both web CSS and the TUI clock.
  Done when: a linter flags any animation lacking a decay or exceeding the cap, with file and line.
