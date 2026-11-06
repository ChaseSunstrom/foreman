# Brainstorm — lens: bold bets

- **Write the design-direction playbook family** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: the pack shows one UI playbook (`ui/terminal-ui.md`, 13 lines) and ~180 frontend/web cards that give verify commands but "none teaches taste". This is the core of the request's part 3. Add `ui/direction`, `ui/motion`, `ui/3d-scenes`, `ui/typography`, `ui/colour-systems`, `ui/dataviz`, `ui/a11y-audit` and `ui/visual-qa`. Each is original writing with a worked before/after.
  Done when: `/foreman:playbooks` lists the 8 new ui files, each under the existing size cap and passing the skill-description lint.

- **Ship a lookbook of 40 named visual styles** — FEATURE — value 5 — effort L — risk low — category: design
  Why: "non generic styles" is an explicit ask. Each look card is a tokens file, a CSS recipe, a motion personality, a type pairing, a banned-cliché list and a self-contained demo HTML. Examples: Swiss grid, risograph, brutalist-terminal, glass-aurora, blueprint. `fm lib show look/NAME` prints it. Assumption: styles are described in original words, never cloned from a named product.
  Done when: `fm lib show look/swiss-grid` prints tokens plus a demo path, and a test renders every demo and checks it loads with no third-party host.

- **Require a design brief before any UI edit** — FEATURE — value 5 — effort M — risk med — category: discipline
  Why: Foreman's thesis is "plan before it edits", but there's no UI-specific plan. A UI task must first record a one-page brief: chosen look, palette, type pair, motion rules and three banned clichés. A verify step then checks the diff against the brief.
  Done when: a task tagged UI that edits `.css` or `.tsx` without a brief is refused by `fm task` with a `Next:` line, and passes once the brief exists.

- **Add `fm check design`, an anti-generic linter** — FEATURE — value 4 — effort M — risk low — category: verify
  Why: assumption: generic output has detectable tells. A stdlib scanner of CSS and TSX flags default font stacks, the purple-to-blue gradient, uniform radius on every card, untouched shadcn tokens, no type scale, and animations with no easing or reduced-motion branch. It reports counts and file:line.
  Done when: a fixture "generic landing page" scores at least 6 findings, and a fixture built from a lookbook card scores 0.

- **Build `fm shot`, a visual proof loop with animation frames** — FEATURE — value 5 — effort L — risk med — category: verify
  Why: Foreman proves work with commands that ran, but UI work has no proof beyond "it compiled". Assumption: a headless Chromium is on PATH, used as an external tool, not a dependency. It captures 3 viewports, a reduced-motion pass and animation frames at t=0, mid and end. These attach to the task as evidence with a rubric checklist (hierarchy, contrast, overflow).
  Done when: `fm shot URL --frames 3` writes the PNG set and a manifest, and `fm task prove` cites it. Without a browser it exits with "no browser found" and a `Next:` line.

- **Write the 3D scene playbook with budgeted starter scenes** — FEATURE — value 4 — effort L — risk med — category: 3D
  Why: the library has three-js, react-three-fiber, postprocessing and glsl cards, but nothing on composition. Cover lighting rigs, camera moves, scale, fog and depth, shader looks and a perf budget. Ship 5 templates in `plugin/templates/` (product turntable, particle field, raymarched hero, scroll-driven scene, low-poly diorama). Each has a draw-call and triangle budget check.
  Done when: each template builds and `fm shot` renders a non-blank canvas. The budget script fails a scene that exceeds its stated limits.

- **Generate the TUI settings screen from one schema** — FEATURE — value 5 — effort L — risk med — category: TUI config
  Why: the pack says "there is no settings screen inside the app: every setting is hand-edited TOML". A single schema (types, ranges, enums, docs) drives the form, validation, `--print-config` and the docs, so they can't drift. Edits preview live, show a diff, write atomically and keep an undo to the last-good file. Themes, keys, layout, runners and models are all editable.
  Done when: in `fm code app`, a keypress opens settings, changing a theme repaints immediately, and `u` restores the prior `tui.toml` byte for byte.

- **Make every playbook earn its place with a with/without eval** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: the user wants "way more skills", and the bench and `plugin/evals/` already exist. Each new playbook ships one task plus a rubric, and a bench run compares a worker with and without it. A playbook that doesn't improve its score is flagged for rewrite or removal.
  Done when: `fm bench playbooks` prints a per-playbook delta table, and CI fails any playbook with no case.

- **Draft playbooks from finished runs** — FEATURE — value 4 — effort M — risk med — category: skill factory
  Why: lessons already exist (T-0217), and the request says "way more skills" with a recursive loop. `fm playbook draft TASK` turns a task's failures and the fix that held into a candidate playbook with a spec-lint meter. It stays quarantined until the eval in the previous idea passes.
  Done when: running it on a closed task writes a draft that passes the frontmatter lint and is marked `draft`, and it is never listed until promoted.

- **Add `fm design extract` to turn a reference into enforced tokens** — FEATURE — value 4 — effort M — risk med — category: design systems
  Why: "make it feel like this" is how people actually brief design. Point it at screenshots or a local CSS file to get a tokens file (palette in OKLCH, type scale, spacing, radii, motion durations). The check from the linter idea then enforces it. Assumption: the user owns the reference.
  Done when: running it on a fixture site writes `design.tokens.json`, and a CSS change using an off-palette colour fails `fm check design`.

- **Wild: compile one motion score into CSS and the TUI clock** — FEATURE — value 4 — effort L — risk med — category: motion
  Why: motion ideas for the TUI are plentiful, but the web side has nothing. A declarative score (springs, easings, stagger, state to motion) compiles to CSS keyframes and WAAPI, and to the TUI frame scheduler. Foreman's site, `fm page` and the app then share one motion language.
  Done when: one `.motion.toml` produces a CSS file and a TUI profile, and a golden test confirms the same easing curve in both at 5 sample times.

- **Wild: render the repo as a 3D city in `fm page`** — FEATURE — value 3 — effort L — risk low — category: delight
  Why: the repo map has 1610 files across known layout areas, and `fm page` and the site already produce artifacts. Hand-written WebGL (no CDN, per the offline rule): folders are districts, file size is building height and edits glow as they land. The page works offline from one HTML file.
  Done when: `fm page --city` writes one HTML file that loads with no network request and shows non-blank WebGL output under `fm shot`.

- **Wild: run a four-look tournament on one brief** — FEATURE — value 4 — effort L — risk med — category: design
  Why: "pick between two looks" appears in the pack, but a bracket goes further. Four builders in separate worktrees each render the same brief in a different lookbook style, and `fm shot` captures them. The user picks in rounds, and the winner's tokens plus the rejects' tells go into the brief and the user's design memory.
  Done when: `fm look tournament BRIEF` produces 4 worktrees and a contact-sheet page, and the choice writes a brief with a `chosen:` look and `rejected:` lines.

- **Gate UI tasks on an accessibility and motion audit** — FEATURE — value 4 — effort M — risk low — category: accessibility
  Why: the pack has an a11y card but no gate. Via the `fm shot` DOM, check the contrast ratio, focus order, visible focus ring, and a `prefers-reduced-motion` branch for every animation. Findings fail the verify step with file:line.
  Done when: a fixture with a 2:1 contrast pair and an unguarded keyframe fails with both listed, and the fixed fixture passes.

- **Wild: turn a sketch or screenshot into a brief and a scaffold** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: assumption: the user will paste images into the request. This ties into the pasted-screenshot idea but produces a structured brief (layout regions, chosen look, tokens) before writing any code. The intake step asks one question if the match is ambiguous.
  Done when: a fixture wireframe PNG yields a brief with at least 4 labelled regions, and `fm shot` of the scaffold shows the same region order.
