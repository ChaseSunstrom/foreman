# Brainstorm — lens: beautiful UI, 3D and motion that is not generic

- **Write the design-direction playbook** — FEATURE — value 5 — effort M — risk low — category: ui-playbooks
  Why: the pack shows one 13-line `ui/terminal-ui.md`, and the 37 frontend and 57 web cards give verify commands and pitfalls but no taste. The request asks for "non generic" UI.
  Done when: `plugin/skills/playbooks/ui/direction.md` is listed by `/foreman:playbooks`. It requires a one-sentence point of view, a banned-defaults list, a type pairing, a palette rationale and a signature move before any code. A test asserts those sections exist.

- **Add `fm design lint` for generic tells** — FEATURE — value 5 — effort M — risk low — category: design-lint
  Why: assumption: generic output is recognizable by pattern. Examples are default system or Inter stacks, purple-to-blue gradients, one uniform radius, `shadow-md` on every card, an icon-over-title three-card row, and an emoji used as an icon. A stdlib regex and AST-lite scan over CSS, HTML and TSX can flag them, and the report feeds the playbook.
  Done when: a fixture "template-looking" page yields at least 6 named tells, a hand-designed fixture yields 0, and `fm design lint --json` is usable as a verify command.

- **Make one design-token file drive every surface** — FEATURE — value 5 — effort L — risk med — category: design-tokens
  Why: the site `style.css`, the foreman-ui pane, `tui.toml` themes and the demo SVGs each hold their own colors. A `design.toml` holds an OKLCH palette, type scale, spacing, radii, easing and spring constants. `fm design build` emits CSS variables, TUI theme TOML and SVG variables, and checks contrast on each. This extends the earlier shared-palette and motion-token ideas into one source with generators.
  Done when: changing one hue in `design.toml` and running `fm design build` changes the site, the TUI theme and a recorded SVG, and fails if any text pair drops below 4.5:1.

- **Ship a motion choreography playbook and audit** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the earlier ideas are all TUI-side. Web UI still needs guidance on staggers, springs vs easing, shared-element transitions, scroll-linked reveals, animating only compositor properties and a `prefers-reduced-motion` path. `fm design motion-audit` flags layout-thrashing animations and missing reduced-motion branches.
  Done when: the audit flags `transition: all`, animated `width`/`top`, and a missing reduced-motion media query in a fixture, and passes a corrected fixture.

- **Write the 3D scene composition playbook with a budgeted template** — FEATURE — value 5 — effort L — risk med — category: 3d
  Why: the three-js and react-three-fiber cards exist, but nothing teaches camera framing, a three-light rig, material choices, fog and depth cues, a post-processing budget, or a no-WebGL fallback. Ship the playbook plus a template scene with draw-call and triangle ceilings. Assumption: a headless browser may be absent, so the stdlib check parses the scene manifest.
  Done when: the template passes `fm design scene-check` (draw calls ≤ N, triangles ≤ M, a static poster fallback declared, a reduced-motion branch present), and the check fails when a fixture exceeds a ceiling.

- **Add an original shader-looks cookbook** — FEATURE — value 4 — effort M — risk low — category: shaders
  Why: the games cards cover glsl and wgpu, but no card teaches a look. Write ten original recipes (film grain, halftone, ordered dither, iridescence, caustics, CRT bloom, ink bleed, glass refraction, topographic lines, heat haze). Each lists its uniforms, cost class, a CSS fallback and a mobile caveat.
  Done when: ten cards appear in `fm lib show`, each with a compile-ready fragment shader, and a stdlib check confirms each declares a fallback and a cost class.

- **Close UI tasks with a screenshot proof loop** — FEATURE — value 5 — effort L — risk med — category: visual-qa
  Why: UI tasks can currently close on passing tests alone, so a broken layout slips through. `fm design shots` captures a viewport matrix (360/768/1440, light and dark, reduced motion) through whatever browser is installed. A stdlib PNG decoder (zlib) diffs against the previous frames, and `fm task prove` attaches the before/after pair.
  Done when: a UI task cannot close without a frame set, and a deliberate one-pixel-column regression is reported with its region.

- **Add a design-critic reviewer lens** — FEATURE — value 4 — effort M — risk med — category: review
  Why: there are 8 reviewers and none judges looks. A ninth scores screenshots on hierarchy, rhythm, contrast, density and originality against a written rubric, citing pixel regions and the lint tells. A score under threshold blocks the close with specific fixes.
  Done when: on two fixture screenshots (generic vs crafted) the critic returns structured findings, and the generic one scores lower on at least 3 of the 5 axes.

- **Replace the site hero with a hand-written WebGL scene of the run** — FEATURE — value 4 — effort L — risk med — category: site
  Why: `site/` has a build.py, a style.css and a rule that nothing loads from third parties. Without three.js, a roughly 300-line raw WebGL hero can show stations as lit blocks on a conveyor that advances as you scroll, with a pre-rendered poster, pointer parallax and reduced-motion respected. This also demonstrates the new playbooks on Foreman itself.
  Done when: `site/build.py` passes its no-external-host check, the page carries a canvas plus a static poster for no-JS, and the hero script is under 30 KB.

- **Add a data-viz playbook and generated animated SVG charts for bench and stats** — FEATURE — value 3 — effort M — risk low — category: dataviz
  Why: the bench and stats pages already exist. The playbook covers direct labels, small multiples, annotation and an honest axis. `site/build.py` emits SVG with CSS draw-in that is static under reduced motion.
  Done when: the bench page ships charts as inline SVG with no JS, each with a text table fallback, and the contrast check passes.

- **Capture reference boards into a DESIGN.md contract** (wild) — FEATURE — value 4 — effort M — risk med — category: design-brief
  Why: assumption: users describe taste by pointing at things. A pasted screenshot or URL becomes a short style brief (type, palette, spacing, motion character, forbidden moves). It is committed as `DESIGN.md`, and later UI tasks must cite it and are linted against it.
  Done when: `fm design brief <image-or-notes>` writes a `DESIGN.md` with all required fields, and a UI task whose diff violates a listed forbidden move fails `fm design lint`.

- **Run a taste duel across three directions** (wild) — FEATURE — value 4 — effort L — risk med — category: design-branches
  Why: a single run converges on the safest look. Three builder lanes build the same brief from different stated points of view in separate worktrees. Foreman screenshots all three into one grid and the user picks. The choice, with a one-line reason, is stored as a preference the next brief reads.
  Done when: one command yields three worktrees, a contact sheet with matching viewports, and a recorded pick that appears in the next `DESIGN.md` draft.

- **Build a tiny software 3D rasterizer for the TUI** (wild) — FEATURE — value 3 — effort L — risk med — category: terminal-3d
  Why: earlier ideas draw flat diorama scenes and treemaps. A stdlib z-buffered flat-shaded renderer onto a half-block canvas could show the repo as a slowly orbiting city, with one tower per directory, height from LOC, and lit windows for files edited this run. A frame budget caps its CPU.
  Done when: a golden-frame test renders a fixed mesh identically across two runs, the orbit stays under the frame budget in the bench, and `--calm` shows a static still.

- **Serve a live design gallery that edits the token file** (wild) — FEATURE — value 3 — effort M — risk low — category: gallery
  Why: the request asks for config in the TUI, and the same token file should be editable there too. `fm design gallery` serves a local, offline page showing type, palette, motion curves and the shader looks with sliders, and saves back to `design.toml` atomically. The TUI settings screen would edit the same file.
  Done when: moving a slider changes the page live, writes `design.toml` with a last-good copy, and the page makes no non-loopback requests.
