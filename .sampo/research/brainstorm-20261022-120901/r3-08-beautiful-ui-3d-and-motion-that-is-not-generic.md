# Brainstorm — lens: beautiful UI, 3D and motion that is not generic

- **Detect near-miss layout with `fm check layout`** — FEATURE — value 4 — effort M — risk low — category: visual QA
  Why: assumption: the pack's slop detector and three-viewport proof catch generic tells, but nothing catches crafted-looking pages with 3px misalignments, uneven gaps or widows. Those are what make UI feel amateur.
  Done when: on a fixture page with a planted 3px misalignment, a 7px-vs-8px gap and a one-word widow, headless rect measurement reports all three with selectors, and a clean fixture reports none.

- **Assert motion as sampled frames** — FEATURE — value 4 — effort M — risk low — category: motion testing
  Why: the pack proposes motion tokens, a linter and golden frames, but no way to assert an animation's shape. Assumption: a headless browser can sample `getAnimations()` at fixed times.
  Done when: a test states "card moves A→B in 180–240 ms, overshoot ≤ 4%, monotonic after the peak". It passes on a spring fixture and fails on a linear-ease fixture with the offending sample times named.

- **Ship a procedural mesh and studio-light kit with no downloaded assets** — FEATURE — value 4 — effort L — risk low — category: 3D
  Why: the pack plans 3D playbooks, but 3D needs meshes and environment maps, and fetching assets conflicts with the stdlib-only, licence-gated, third-party-is-data rules. Assumption: stdlib Python can emit glTF.
  Done when: `fm scene mesh lathe|superformula|terrain --seed N` writes a deterministic valid `.gltf` and an analytic three-point light rig description. A three.js page using only these renders non-blank in `fm shot`, and the same seed gives byte-identical output.

- **Bake any 3D scene into a no-GPU fallback** — FEATURE — value 4 — effort M — risk med — category: 3D resilience
  Why: the pack has a WebGL survival contract and a budget probe, but the fallback is unspecified. A baked orbit sprite sheet from the same scene, which scrubs with pointer or scroll, keeps the hero looking designed on weak devices.
  Done when: `fm scene bake` produces a ≤300 KB frame strip from a scene file. With WebGL disabled, the page shows the strip responding to scroll, and `fm shot` captures it.

- **Expose 3D scenes to assistive tech** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: assumption: canvas scenes are opaque to screen readers and keyboards, and the pack's accessibility ideas cover pages, not scenes. This also doubles as a testable scene graph.
  Done when: the scene template emits an ARIA tree of named objects, supports arrow-key orbit and focus-to-object with a live-region description, and a static check fails a scene that lacks any of the three.

- **Write a native-first motion playbook** — FEATURE — value 3 — effort S — risk low — category: playbook
  Why: the pack's motion playbooks assume libraries. Scroll-driven animation (`animation-timeline`), View Transitions, `@property` and `linear()` easing give distinctive motion with zero JS. Assumption: only the baseline gate and compositor lint touch this today.
  Done when: the playbook has five original recipes, each with a feature-detected fallback. A fixture page passes the baseline gate with JS disabled and still shows the scroll-linked effect.

- **Declare a signature motif and check it recurs** — FEATURE — value 3 — effort M — risk med — category: non-generic design
  Why: "non-generic" is the user's core demand. Distinct looks have one repeated shape, rhythm or motion idea, whereas random "creative" pages have none. A motif contract makes this checkable.
  Done when: DESIGN.md declares one motif, for example a 45° notch or a 3-beat stagger. A checker finds it in ≥80% of sections on a conforming fixture and flags a page where it appears once.

- **Overlay a token x-ray in the dev server** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: the pack has token-vs-code checks and a canary palette, but nothing live. A toggle that outlines every element whose computed colour, spacing or radius isn't from the token file speeds fixes.
  Done when: with the overlay on, a page with one hardcoded `#3a3a3a` shows exactly that element outlined, with a tooltip naming the nearest token.

- **Simulate vision conditions in `fm shot`** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: the pack lints "no state told by colour alone" statically. Rendered protanopia, deuteranopia, 200% zoom and `forced-colors` frames would prove it, and they fit the existing shot loop.
  Done when: `fm shot --vision all` writes labelled frames, and a fixture with red/green-only status fails the deuteranopia diff check.

- **Generate animated architecture diagrams with `fm diagram`** — FEATURE — value 3 — effort M — risk low — category: docs and motion
  Why: assumption: the README and site need diagrams of the proof chain and runner flow, and hand-made SVG rots. The pack has SVG export of runs but nothing for authored diagrams.
  Done when: a 15-line text spec renders a stdlib-only SVG with signals travelling along edges, honouring `prefers-reduced-motion`, and the build fails if the spec and the SVG disagree.

- **Swipe-to-approve spring dialogs on the phone status page (wild)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; assumption: the pack's LAN phone view is read-only. A thumb-sized guard approval with spring resistance, a hold detent and haptic `vibrate` would make "needs you" actionable. It needs a local-only, token-gated channel.
  Done when: on a phone viewport in headless touch emulation, a swipe past the detent approves the pending fixture ask, an early release springs back, and nothing is sent without the explicit setting.

- **Synthesise human cursor choreography for demos (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; assumption: demo casts and site videos show instantaneous or robotic pointer motion. Bezier paths with overshoot, hesitation and click-squash would make recordings feel alive.
  Done when: `fm demo --cursor human` renders a recording whose pointer paths are non-linear, seeded and reproducible, and two runs with the same seed are byte-identical.

- **Turn bench history into a walkable terrain (wild)** — FEATURE — value 3 — effort L — risk med — category: 3D data viz
  Why: wild; the bench and stats pages are flat tables and charts. A heightmap with one ridge per release and valleys for "where Foreman loses" makes the story spatial. A half-block TUI version could reuse the planned rasteriser.
  Done when: the benchmarks page renders the terrain from `bench` JSON with a reduced-motion static view, and a data-integrity test confirms each ridge height matches its source number.
