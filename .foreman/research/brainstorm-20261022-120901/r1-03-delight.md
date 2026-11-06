# Brainstorm — lens: delight

- **Ship a UI direction playbook that forces a point of view before any pixels** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: the pack shows one 13-line `ui/terminal-ui.md` and no playbook for web design direction, while the user asks for "non generic" UI. Cards give verify commands but "none teaches taste".
  Done when: `/foreman:playbooks ui/direction` exists, and a UI task cannot enter the build stage until a one-page brief names a metaphor, a type pairing, a palette with a rule for when each colour is used, and three things the design refuses to do.

- **Add an AI-slop detector for UI diffs** — FEATURE — value 5 — effort M — risk low — category: design QA
  Why: assumption: "generic" is the user's main complaint, and it is checkable. Typical tells are default purple gradients, three-card feature grids, system-font stacks, uniform 8px radii and emoji bullets. A stdlib scanner over CSS/TSX can flag these.
  Done when: `fm check design` run on a fixture of a stock landing page reports at least 5 named tells, and passes a hand-crafted fixture with 0.

- **Close the loop with screenshot-driven visual review** — FEATURE — value 5 — effort L — risk med — category: verify
  Why: the pack's verification relies on commands, but UI quality is only visible when rendered. The playbooks have no visual QA step. Assumption: a headless browser is available as an optional local tool, never a new dependency.
  Done when: a UI task's proof includes before/after screenshots at three widths, and the close is refused if any capture shows horizontal overflow or an unstyled-text flash.

- **Write a 3D scene composition playbook with original recipes** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: the library has three-js, react-three-fiber, postprocessing and glsl cards but none on composition. Typical failures are flat lighting, centred product-on-grey scenes and missing depth cues. Recipes would cover a key/fill/rim light rig, fog as depth, restrained bloom, camera drift and a budget for draw calls and fps.
  Done when: the playbook has at least 6 original scene recipes, each with a verify command that checks frame time against a stated budget.

- **Write a motion choreography playbook with a timing vocabulary** — FEATURE — value 4 — effort S — risk low — category: playbooks
  Why: framer-motion and animation cards exist, but nothing says what moves, in what order, or why. The playbook would define stagger, anticipation and settle, a rule that one thing moves at a time, and a `prefers-reduced-motion` twin for every animation.
  Done when: the playbook states a duration and easing table, and `fm check design` flags any animation that lacks a reduced-motion branch.

- **Ship a style-recipe shelf of ten named, original looks** — FEATURE — value 4 — effort M — risk low — category: design library
  Why: the pack lists no stylistic range. Each recipe would give tokens, type pairing, texture technique, a motion personality and a "never do" list. Examples are risograph print, brutalist terminal, paper-cut layers, instrument-panel, and dusk-glass. They would be original writing, not copied from existing design systems.
  Done when: `fm lib show style/<name>` returns tokens that compile to a working CSS file, and each recipe renders a distinct sample page.

- **Give the project site a live WebGL hero and a pointer-reactive proof-chain scene** — FEATURE — value 3 — effort M — risk med — category: site
  Why: `site/` has `build.py` and `style.css`, and the pack makes the site a Foreman surface. A hand-written canvas or WebGL scene (no libraries, nothing from third parties) that visualises plan → edit → prove → close would exhibit the 3D skill. Assumption: the `site/build.py` rule against outside hosts stays.
  Done when: the built page has a hero scene running at ≥50fps in a headless run, a static fallback under reduced motion, and no external requests.

- **Generate a design-system extract from any URL or screenshot** — FEATURE — value 4 — effort L — risk med — category: design tooling
  Why: assumption: users say "make it look like X". A local extractor would pull palette, type scale, spacing rhythm and radius habits from a page's computed CSS and write a token file plus a short note on what makes the look distinctive.
  Done when: running it on a saved HTML fixture emits tokens that round-trip into the recipe format, with a licence note saying tokens are ideas, not assets.

- **Wild: Hold a design critique panel of three persona reviewers** — FEATURE — value 4 — effort M — risk low — category: agents (wild)
  Why: assumption: the existing eight code reviewers are all code-focused. A "type nerd", a "motion director" and an "accessibility skeptic" would each review screenshots plus CSS and return structured findings. The disagreement between them is the signal.
  Done when: `fm audit design` writes a findings file with one section per persona, and each finding cites a selector or a screenshot region.

- **Wild: Add a "make it worse on purpose" contrast pass** — FEATURE — value 3 — effort S — risk low — category: design QA (wild)
  Why: assumption: generic output comes from averaging. Before polishing, Claude generates the most template-like version, then the final design must differ from it on a measurable list (layout grid, type, colour hue distance).
  Done when: the task record holds both versions and a diff of at least 4 named axes, and closing fails if fewer than 4 differ.

- **Wild: Render the playbook itself as a browsable gallery of rendered examples** — FEATURE — value 3 — effort M — risk low — category: docs/delight (wild)
  Why: design guidance reads as vague text. A generated `fm page` gallery would show each recipe's live sample beside its rules and its anti-pattern, so choosing a look means pointing at one.
  Done when: `fm page design-gallery` builds one offline HTML file with every recipe's sample, a theme toggle, and reduced-motion honoured.

- **Wild: Let a design brief be an executable contract that fails the build** — FEATURE — value 4 — effort M — risk med — category: verify (wild)
  Why: tokens exist in the brief but nothing enforces them. A `design.brief` file would list colour roles, the type scale, a motion budget and the forbidden list, and a check would fail on a hardcoded hex outside the palette, an off-scale font size, or a motion over budget.
  Done when: a seeded violation (an off-palette hex) turns `fm check design` red, naming the file and line.

- **Add an accessibility-with-flair checklist that treats constraints as the design** — FEATURE — value 3 — effort S — risk low — category: playbooks
  Why: the pack mentions no accessibility audit playbook. The playbook would frame contrast, focus rings, keyboard paths and reduced motion as places to be distinctive (a branded focus ring, say) rather than as compliance chores.
  Done when: the playbook includes a verify script covering contrast ratios and focus visibility, and each rule shows one stylish compliant pattern.
