# Brainstorm — lens: capability map

- **Write a web UI design-direction playbook set** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: the only UI playbook is the 13-line `ui/terminal-ui.md`, and nothing teaches web taste. Split it into direction brief, type, colour, layout, motion, empty/error states, and data viz. Each file is original writing with a "what makes this generic" section.
  Done when: `fm playbooks` lists at least 8 `ui/` files, each ending in a checklist that a lint verifies is present.

- **Add `fm check design`, an anti-generic gate** — FEATURE — value 5 — effort M — risk med — category: UI quality
  Why: assumption: a stdlib CSS/Tailwind-config scan can flag default-looking output (system or Inter-only type, stock indigo gradient, one radius everywhere, no type scale). It runs as a task verify command.
  Done when: a fixture app with stock Tailwind defaults fails with named reasons, and a fixture with a distinct token set passes.

- **Capture visual evidence for UI tasks** — FEATURE — value 5 — effort M — risk med — category: visual QA
  Why: the user wants "way better UI", but `fm task prove` proves only commands. Run the project's own browser tool at 3 breakpoints in light and dark, and attach before/after screenshots to the proof. Assumption: Playwright or an equivalent is installed in the project, not in Foreman.
  Done when: closing a UI task stores 6 images in the proof, and a missing browser tool says so instead of passing.

- **Write a 3D scene playbook with a perf budget** — FEATURE — value 4 — effort M — risk low — category: 3D
  Why: the library has three-js, r3f, postprocessing and webgl cards, but none covers composition: camera, lighting rig, material choice, post-processing cost, and a no-WebGL fallback.
  Done when: the playbook ships with a verify recipe that fails when a headless run exceeds a draw-call or frame-time budget.

- **Write a motion playbook with lintable tokens** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: only the TUI motion ideas are covered. Web needs durations, easings, springs, choreography and scroll-driven effects. It also needs `prefers-reduced-motion` handling, and a lint for animating layout properties instead of transform and opacity.
  Done when: the lint flags `animation: … width` in a fixture and passes the transform/opacity version.

- **Extract a DESIGN.md from an existing repo** — FEATURE — value 4 — effort M — risk low — category: design systems
  Why: assumption: UI tasks go generic because Claude never sees the project's palette, type scale, spacing and motion. `fm design extract` reads CSS variables and Tailwind and theme files, then writes one file that intake injects into UI tasks.
  Done when: running it on a fixture repo yields a DESIGN.md listing its real tokens, and a later hard-coded hex value that is off-palette is reported.

- **Eval every playbook against a no-playbook baseline** — FEATURE — value 4 — effort M — risk med — category: playbook quality
  Why: `plugin/evals/` exists, and T-0035 and the bench show the appetite for evidence. Without scoring, "way more playbooks" risks being filler.
  Done when: each new playbook has a rubric-scored case, and one that doesn't beat the baseline is flagged.

- **Check accessibility statically** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: a stdlib check computes WCAG and APCA contrast from CSS tokens, flags missing focus styles and sub-24px targets, and checks for a reduced-motion branch. The accessibility card gives pitfalls but no tool.
  Done when: a fixture with 3:1 body text fails and names the token pair.

- **Fill the playbook stage gaps beyond UI** — FEATURE — value 4 — effort L — risk low — category: playbooks
  Why: 15 stages exist, but none covers database migrations, observability, incident response, infra-as-code, mobile (SwiftUI/Compose), docs sites, or print/PDF/email HTML. Add them in priority order, ranked by `fm lib` card counts.
  Done when: each new stage has at least 2 playbooks, and `fm playbooks` lists them by stage.

- **Run a design-critic panel (wild)** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: assumption: a typographer, motion director and a11y reviewer sub-agent, each reading the screenshot evidence, can catch what one generalist misses. Each returns scored findings, and the loop runs until the score clears a threshold or a cap.
  Done when: on a fixture page with planted flaws (cramped leading, jarring easing), all three critics report at least one finding each.

- **Generate a lookbook of N style directions (wild)** — FEATURE — value 4 — effort L — risk med — category: design direction
  Why: "non generic" is hard to say in words. `fm lookbook` renders the same content in 6 distinct directions (editorial, brutalist, skeuomorphic, synthwave and so on) as one offline page. The user picks one, and it becomes DESIGN.md.
  Done when: running it produces a self-contained HTML file with 6 renderings and no external requests.

- **Rebuild the site hero as a WebGL station track (wild)** — FEATURE — value 3 — effort L — risk med — category: dogfood
  Why: `site/` has a README hero SVG but the user wants Foreman's own surfaces to show the new skills. Self-host the 3D scene, give it a no-JS fallback and honour reduced motion, which also fits the third-party-free fonts task (S24). The new playbooks and visual-evidence check must gate it.
  Done when: the built page passes the build's no-outside-host check and has desktop and mobile screenshots attached to its task proof.

- **Ship a tested shader-recipe card set** — FEATURE — value 3 — effort M — risk low — category: 3D looks
  Why: the games cards cover GLSL generally but not looks like grain, halftone, gradient mesh or noise fields. Each recipe is original, with a parameter table and a headless-render hash test.
  Done when: each recipe's snippet renders to the stored hash.
