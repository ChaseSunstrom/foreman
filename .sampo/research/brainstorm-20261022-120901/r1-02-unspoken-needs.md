# Brainstorm — lens: unspoken needs

- **Require a design direction before any UI edit** — FEATURE — value 5 — effort M — risk low — category: ui-skills
  Why: the pack shows one 13-line terminal-ui playbook and no web design direction, yet the user's third ask is "non generic" UI. Unclear but likely: output is generic because nothing forces a point of view. A short brief (aesthetic stance, type pair, OKLCH palette roles, motion principle, one signature element) is written first, saved as `design.md`, and read by later edits.
  Done when: a UI-tagged task has no passing verify until `design.md` has all six fields, and a fixture task with an empty brief is refused with the missing field named.

- **Lint for generic-UI tells** — FEATURE — value 5 — effort M — risk low — category: ui-quality
  Why: the cards (tailwind, shadcn-ui, framer-motion) give commands and pitfalls but no taste. A stdlib `fm check ui-tells` scans CSS/TSX/HTML for the default font stack, blue-to-purple gradient heroes, uniform radius and shadow, three equal feature cards, emoji as icons, and lorem text. It reports each tell with file:line.
  Done when: a fixture generic landing page yields at least 5 named tells, a fixture page built from a brief yields none, and the check runs as a verify command.

- **Prove UI work with screenshots at three viewports** — FEATURE — value 5 — effort M — risk med — category: visual-qa
  Why: "UI design skills" without sight is guessing. Assumption: a headless Chromium exists on the machine, so degrade to "skipped, not proved" when it doesn't. Capture 375, 900 and 1440 px, once with reduced motion, as evidence on the task. Seeing the pixels also feeds the critique idea below.
  Done when: closing a UI task attaches 4 PNGs, and on a machine without a browser the receipt says "visual proof skipped" rather than passing.

- **Build a 3D scene playbook with a budget probe** — FEATURE — value 5 — effort M — risk med — category: 3d
  Why: the library has three-js, react-three-fiber, postprocessing and webgl cards but nothing on composition, lighting, camera moves, or restraint. The playbook is original writing. A probe loads the page headless and reports draw calls, triangles, texture MB and frame time. It checks a no-WebGL fallback and a reduced-motion still.
  Done when: the playbook exists with a verify block, and the probe fails a fixture scene over budget and passes a trimmed one.

- **Render 3D in the terminal with a stdlib rasterizer** — FEATURE — value 4 — effort L — risk med — category: tui-3d
  Why: the user asked for "3d" and the idea list has pixel-canvas primitives but no actual 3D. A z-buffered flat-shaded renderer draws to half-block or braille cells. Uses: a logo turntable on launch, and a queue "city" with bar height as cost per project. A frame budget keeps it cheap.
  Done when: a golden-frame test renders a rotating cube at 3 angles deterministically, and the city view draws within the TUI frame budget.

- **A/B every playbook against no playbook** — FEATURE — value 5 — effort L — risk med — category: playbook-quality
  Why: there are 1161 skill files and the user wants "way more", but nothing says any of them changes results. Assumption: bench cases can be blind-scored. Run a task with the playbook on and off, score blind, and mark a playbook "earned" or "unproven". Unproven ones are flagged, not deleted.
  Done when: `fm playbooks --earned` lists each playbook with its measured delta on at least 3 cases, and one is shown as unproven.

- **Run a three-persona design critique on the screenshots** — FEATURE — value 4 — effort M — risk low — category: review
  Why: T-0034 (`fm audit run`, headless read-only lens reviewers) is deferred and the pack has 8 code reviewers but no design reviewer. Add an art director, a motion designer, and an accessibility reviewer. Each reads the captured screenshots and `design.md` and writes structured findings.
  Done when: a fixture UI produces a findings file with at least one finding per persona, each citing a screenshot and a rule from `design.md`.

- **Check accessibility statically with stdlib** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: the frontend cards cover accessibility and color-contrast but there is no executable check, and contrast is only mentioned for the TUI. `fm check a11y` covers contrast ratios from computed token pairs, missing labels and alt text, focus-order traps, and `prefers-reduced-motion` coverage for every animation.
  Done when: a fixture page with 4 planted violations reports exactly those 4, and a clean fixture passes.

- **Generate one token set for web, TUI and pane** — FEATURE — value 4 — effort M — risk low — category: design-system
  Why: the site's `style.css`, `tui.toml` and the `foreman-ui` TSX each carry their own palette. Assumption: they have drifted. `design.md` emits `tokens.css`, a `tui.toml` theme and a TSX module, with a drift check.
  Done when: editing one palette role in `design.md` changes all three outputs, and the drift check fails if one is hand-edited.

- **Ship a gallery where every design playbook has a reproducible example** — FEATURE — value 4 — effort M — risk low — category: docs-dogfood
  Why: playbooks that claim taste need visible proof, and the site already has a build pipeline. Each design playbook gets a small example built from it, with a screenshot and the command that regenerates it. A broken regeneration fails `site/build.py`.
  Done when: the gallery page lists every design playbook with a thumbnail, and a deliberately broken example fails the site build.

- **Wild: Keep a shader sketchbook of original looks** — FEATURE — value 3 — effort L — risk low — category: 3d-assets
  Why: wild; assumption: GLSL fragments render headless. Twenty original, parameterized looks (grain, caustics, halftone, aurora) come with a thumbnail sheet and a drop-in snippet. The user picks one by sight, not by name.
  Done when: `fm lib show shader-sketchbook` prints 20 entries each with a rendered PNG, and a picked look compiles in a fixture three.js page.

- **Wild: Turn a pasted screenshot into a token sheet** — FEATURE — value 4 — effort M — risk med — category: reference
  Why: wild; assumption: the user has "that look" in mind and no vocabulary for it. A screenshot or URL becomes extracted palette, type scale, spacing rhythm and a motion guess, written as a draft `design.md` that is a starting point, not a copy. The extraction runs locally, with no upload.
  Done when: a fixture screenshot yields a draft `design.md` whose palette matches the dominant colours within tolerance, and nothing leaves the machine.

- **Wild: Show a playbook coverage heatmap by stage and stack** — FEATURE — value 3 — effort S — risk low — category: skill-gaps
  Why: wild; the pack shows 48 playbooks in 15 stages, with ui at one file. A stage-by-stack grid, filled from playbooks plus the requests the user actually made, shows the blank cells. Each blank can be queued as an authoring task.
  Done when: `fm playbooks --map` prints the grid with ui visibly sparse, and `--queue` creates a task for a chosen blank cell.

- **Offer a motion spec the page must honor** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the idea list has a lot about the TUI's motion and almost nothing on web motion. `design.md` carries named durations, easings and stagger rules. A lint flags inline magic numbers in animations and any animation lacking a reduced-motion branch.
  Done when: a fixture with 3 off-spec animations reports all 3, and the same page using tokens passes.
