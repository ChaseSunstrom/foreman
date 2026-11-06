# Brainstorm — lens: approaches

- **Write a 12-playbook `ui/` family on taste, not tooling** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: the pack shows ONE 13-line `ui/terminal-ui.md` against ~94 frontend/web/three-js cards that give verify commands and pitfalls but no taste. Each playbook is original writing and opens with "pick a direction before code". Topics: direction and anti-defaults, type pairing, colour systems, layout rhythm, motion choreography, 3D scene composition, shader looks, data viz, empty/error states, a11y audit, visual QA, dark mode.
  Done when: `/foreman:playbooks` lists 12 `ui/*` files, each with a "wrong default → what to do instead" table, and `fm doctor` passes.

- **Gate UI edits on a DESIGN.md with banned defaults** — FEATURE — value 5 — effort M — risk med — category: design gate
  Why: assumption: generic output comes from skipping the direction step. Foreman already makes Claude plan before editing, so the plan for UI work must name palette, type, motion character and 3 things to avoid. `fm design lint` is a stdlib scan of CSS/TSX for token drift and stock patterns (default font stack, purple-to-blue hero gradient, uniform 8px radius). It runs as a verify command.
  Done when: a UI task with no DESIGN.md is refused at plan time, and lint fails a fixture page containing the stock patterns.

- **Add visual proof as an evidence kind** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: `fm task prove` accepts commands that actually ran, but a UI change can pass every test and still look wrong. Use any headless browser already on the machine, called through the guard (nothing new bundled), to capture 3 viewports plus a reduced-motion frame, saved beside the task. Fall back to "no browser, unproven visually" in the receipt.
  Done when: `fm task prove --shot URL` stores PNGs hashed in the receipt, and the closing summary says "visual: unproven" when no browser exists.

- **Run a three-variant divergence round for UI tasks** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: assumption: one pass regresses to the mean. Three builder lanes (the pack mentions lanes and worktrees) each get a different direction card (e.g. brutalist, editorial, instrument-panel). A design reviewer scores each against the DESIGN.md rubric, and the user or rubric picks one.
  Done when: `fm design fork` creates 3 worktrees with distinct direction cards and a score table. Only the chosen one merges.

- **Prove playbooks work with an A/B design eval** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: `plugin/evals` has 21 files, and "way more skills" is only worth it if output changes. Run N=5 prompts with and without a playbook, score with `fm design lint` plus a rubric. A playbook that doesn't move the score gets flagged for rewrite or deletion.
  Done when: `fm eval design` prints a per-playbook lift table, and one playbook is shown beating the baseline.

- **Ship scene recipes as runnable templates** — FEATURE — value 4 — effort M — risk low — category: 3D
  Why: `plugin/templates/mcp-server` proves the template pattern exists. Add `templates/scene-*` (lighting rig, camera dolly, post chain, particle field, shader hero), each a minimal three.js page with a budget comment (draw calls, fps). Playbooks point at them instead of describing them.
  Done when: `fm new scene-hero` writes a page that opens with no build step and the template passes `fm design lint`.

- **Make every setting a verb first, the TUI settings screen second** — FEATURE — value 4 — effort M — risk low — category: config
  Why: the pack says every setting is hand-edited TOML with no in-app screen. The cheapest durable route is `fm code set theme.name aurora` / `get` / `explain` over a schema, with the in-app screen a thin form calling the same verbs. Validation and last-good rollback then exist once.
  Done when: `fm code set` rejects a bad key with a line-accurate error, and the in-app screen changes a theme through that same code path with a test proving it.

- **Distil a project design card from the repo's own CSS** — FEATURE — value 3 — effort M — risk low — category: design memory
  Why: `fm map` already summarises gates and layout, and cards exist per stack. Extract tokens (colours, fonts, spacing, radii) into a project card so new UI matches the house style instead of the model's default.
  Done when: `fm design card` on `site/` lists its real tokens, and a new-component task cites them.

- **Ship the design playbooks as an optional `foreman-design` plugin** — CLEAN — value 3 — effort S — risk low — category: packaging
  Why: the open list has "Slim Foreman: Lite mode" (T-0794), and 12 more playbooks add weight to everyone's context. A separate plugin keeps core small, and the playbooks stay discoverable through `fm lib`.
  Done when: the core plugin installs with no `ui/` extras, and installing `foreman-design` adds them.

- **Dogfood: rebuild the site hero with the new playbooks** — FEATURE — value 4 — effort M — risk low — category: proof by shipping
  Why: `site/` has `build.py` and `style.css`, and the request asks for Foreman's own surfaces to show the craft. A WebGL or shader hero built under the DESIGN.md gate, with a hard budget, gives the playbooks their first real portfolio piece. It must stay third-party-free (T-S24).
  Done when: `site/build.py` passes with no outside hosts, the hero holds a stated fps/KB budget, and the DESIGN.md is committed.

- **Wild: write a stdlib software 3D rasteriser for the TUI** — FEATURE — value 3 — effort L — risk med — category: 3D terminal
  Why: wild; assumption: the "3D" in the request includes the terminal. About 300 lines of pure Python (projection, z-buffer, flat shading) drawing to half-block cells. First use is an isometric queue view where each task is a block that rises as it is proved. No dependencies, so the stdlib constraint holds.
  Done when: `fm code tui --scene` renders a rotating solid at a stated fps within the frame budget, and a golden frame test passes.

- **Wild: build a motion lab page from the motion tokens** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: wild. `fm page` already makes artifacts. One generated HTML page shows every easing, spring and stagger token with scrub controls and the TUI's equivalent frame sequence, so motion is chosen by eye and the same tokens drive web and terminal.
  Done when: `fm page motion` opens a page where changing a token updates a live preview and exports the value back to `tui.toml`.

- **Wild: add an art-director critique loop with a film strip** — FEATURE — value 4 — effort L — risk high — category: agents
  Why: wild. A bounded unattended loop (build, screenshot, critique against the rubric, adjust) stops at a score or a cap of 4 rounds, and keeps each iteration as a frame in a strip so the user sees the evolution. It reuses the visual-proof idea above, with an explicit budget to avoid endless polish.
  Done when: `fm design loop` stops at the cap or the score target, and writes a strip with one frame per round plus the scores.
