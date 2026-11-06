# Brainstorm — lens: beautiful UI, 3D and motion that is not generic

- **Ship a Sketchbook of Light: ten original, tested shader-and-material recipes for 3D UI** — FEATURE — value 5 — effort L — risk med — category: 3D playbook
  Why: pack shows 57 web cards (three-js, r3f, postprocessing, glsl) that give verify commands but "none teaches taste (shader looks, 3D scene composition)". Prior ideas name a shader cookbook but not the material/lighting layer: glass, brushed metal, ink-on-paper, dithered fog, toon rim-light, caustics, each with a palette, a lighting rig, a post stack and a frame-cost number.
  Done when: `fm lib show shader-looks` lists ten recipes; each has a self-contained HTML file that renders headless in under 16 ms/frame budget stated in the card, and an eval shows output differing from a no-playbook baseline.

- **Add a Composition Rules playbook for 3D scenes (camera, scale, focal depth, negative space)** — FEATURE — value 4 — effort M — risk low — category: 3D playbook
  Why: generic 3D output is a centred rotating cube under default lights. assumption: Claude lacks a checklist for lens length, rule-of-thirds anchors, depth layering and idle-camera drift. Prior ideas cover budget probes, not composition.
  Done when: the playbook lists eight named composition moves, each with a code snippet, and a test renders three scenes and asserts the focal object sits off-centre with at least two depth layers.

- **Build a Motion Score file format that compiles to CSS, WAAPI, three.js tweens and the TUI clock** — FEATURE — value 5 — effort L — risk med — category: motion
  Why: pack lists many motion ideas (state-to-motion tables, tokens, springs) but each surface has its own clock. One declarative score (events, durations, spring params, stagger, reduced-motion substitute) makes the site, pane and fm code app move with the same personality.
  Done when: one `motion.toml` generates a CSS file and a TUI constants module, and a test checks both produce identical duration/easing values for every named motion.

- **Add a Type-as-Image playbook: variable fonts, optical sizing, kinetic type and fluid scale** — FEATURE — value 4 — effort M — risk low — category: typography
  Why: the typography card exists but none teaches pairing with intent or kinetic type; generic UI is mostly default sans at default sizes. Include self-hosted font rules, matching the "no third-party loads" constraint (S24).
  Done when: playbook plus a checker that fails a page using only system-ui, with no fluid clamp scale and no second typeface role.

- **Create a Material Language chooser: paper, glass, ink, metal, clay, terminal-phosphor, each with tokens for light, edge, grain and shadow** — FEATURE — value 4 — effort M — risk low — category: design language
  Why: the request says "non-generic styles". Most slop comes from flat cards with a blur. Naming a physical material forces consistent edge, shadow and noise decisions across web, SVG and TUI half-block rendering.
  Done when: each material is a token block that renders in `fm shot` and in the TUI palette, and a test confirms the six sets differ in at least four token families.

- **Add an Interaction Feel playbook: hover physics, magnetic targets, scroll-linked scenes, press response** — FEATURE — value 4 — effort M — risk low — category: interaction
  Why: pack covers TUI key feedback but no web equivalent. Distinctive sites are felt through pointer response and scroll choreography, with `prefers-reduced-motion` and touch fallbacks required.
  Done when: playbook includes five tested patterns and a checker confirms each has a reduced-motion branch and a touch alternative.

- **Ship a Depth-Without-WebGL recipe set: CSS 3D transforms, parallax layers, SVG filters, canvas 2D lighting** — FEATURE — value 4 — effort M — risk low — category: 3D playbook
  Why: WebGL is heavy for many pages and fails on low-power devices. A fallback ladder (WebGL → CSS 3D → layered parallax → flat) lets Claude pick depth that degrades well.
  Done when: one demo page renders the same hero at all four tiers, selected by a capability probe, and screenshots at each tier pass a non-blank pixel check.

- **Write a Generative Backdrop playbook: noise fields, flow fields, reaction-diffusion, particles with seeds** — FEATURE — value 3 — effort M — risk low — category: generative art
  Why: seeded, deterministic backgrounds give every project a signature without stock gradients, and seeds make screenshots reproducible for visual QA.
  Done when: three seeded generators produce byte-identical canvas output for the same seed in a headless test.

- **Wild: Render the TUI's 3D station track with a stdlib half-block raymarcher at 12 fps** — FEATURE — value 3 — effort L — risk med — category: terminal 3D — wild
  Why: assumption: signed-distance raymarching of a few primitives fits in pure Python at a coarse resolution if limited to a small viewport and run only on state change. It would give the run a lit, rotating 3D track in the terminal.
  Done when: a frame of a 60x20 cell scene renders in under 80 ms on the CI machine and the golden frame matches across two runs.

- **Wild: A "Style Séance" command that generates six one-screen directions from a sentence and keeps the one you pick as DESIGN.md** — FEATURE — value 4 — effort M — risk med — category: design direction — wild
  Why: the request wants non-generic output. Showing six rendered micro-directions (type, palette, material, motion) before building turns taste into a pick rather than a prompt, and the pick becomes enforced tokens.
  Done when: running it on one sentence writes six preview HTML files and, after choosing one, a DESIGN.md that a later UI edit is checked against.

- **Wild: Reaction-diffusion "ink" that blooms from each closed task on the site hero** — FEATURE — value 3 — effort M — risk low — category: site delight — wild
  Why: the demo site is static proof; a living surface seeded by real task ids and verdicts makes it unlike any template and ties visuals to evidence.
  Done when: the hero generates a deterministic pattern from a list of task ids, honours reduced motion with a still frame, and the build fails if the pattern differs between two builds.

- **Add a Motion Budget linter for web pages: long tasks, layout-thrashing properties, off-compositor animation** — FEATURE — value 4 — effort M — risk low — category: performance
  Why: heavy animation is the usual way crafted UI ships janky. A stdlib check can scan CSS for animated width/height/top/left, unbounded `will-change`, and missing reduced-motion queries.
  Done when: `fm check motion` flags a seeded bad stylesheet with three named findings and passes the site's own CSS.

- **Add a Dark-and-Light Pair generator that derives both themes from one OKLCH seed with contrast proofs** — FEATURE — value 3 — effort S — risk low — category: colour
  Why: dark-mode and color-contrast cards exist but a derived pair avoids the hand-tuned, mismatched second theme that most generated UIs ship.
  Done when: one seed yields two token sets where every text/background pair meets 4.5:1, verified by a stdlib contrast test.
