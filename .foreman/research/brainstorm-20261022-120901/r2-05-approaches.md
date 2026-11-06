# Brainstorm — lens: approaches

- **Gate the playbook family on a five-rule UI contract** — FEATURE — value 5 — effort S — risk low — category: design
  Why: assumption: a short contract (commit to one direction, banned defaults, one easing family, one type pair, one focal element) may capture most of the lift. The pack shows 12-plus playbooks proposed, but no measurement of what a small contract does.
  Done when: an A/B eval of the contract alone against plain Claude on 5 UI briefs is recorded, and the longer playbooks are written only for the failure classes it leaves open.

- **Wrap the upstream frontend-design skill instead of rivalling it** — FEATURE — value 4 — effort S — risk med — category: reuse
  Why: assumption: anthropics/skills ships a frontend-design skill. The pack says the six anthropics repos are default `fm lib` sources, and the only UI playbook is 13 lines. Foreman's own contribution would be the proof tail: a brief file, `fm check design`, and screenshots.
  Done when: a UI task using the adopted skill cannot close without a brief artifact and a screenshot artifact, and the card shows its licence class and token cost.

- **Split UI work into four checked layers** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: generic output comes from the model making structure, colour, motion and scene choices in one pass. The plan template would be structure (semantic, unstyled), then tokens, then motion, then scene, each its own step with its own verify command, and the tokens step reads only the design card.
  Done when: `fm plan` for a UI request emits those four steps, and the tokens step fails if no direction is committed.

- **Compile one `scene.json` to three renderers** — FEATURE — value 4 — effort L — risk med — category: 3D
  Why: the pack has three.js and R3F cards but no scene composition teaching, and a stdlib TUI rasterizer is already proposed. A declarative scene (camera, lights, meshes, motion score) compiles to three.js, to the TUI rasterizer and to an SVG poster, so the model writes data, not shader boilerplate.
  Done when: one `scene.json` renders in all three targets, and a golden-frame test shows the TUI and SVG outputs agree on object placement.

- **Store design guidance as a bank of runnable exemplars** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: assumption: models imitate 40-line working code better than they follow advice. The bank would hold original CSS, SVG-filter, GLSL and TUI-motion fragments retrievable by vibe words ("grainy", "ledger", "brass"), and it would be original writing, per the constraints.
  Done when: 30 exemplars each pass a headless smoke test, and `fm lib exemplar "grainy hover"` returns the 3 best with their licence and token cost.

- **Add a browser ladder for visual proof** — FEATURE — value 4 — effort M — risk low — category: verify
  Why: visual QA loops are proposed, but nothing says what happens on a machine without Playwright. The ladder would try Playwright, then headless Chromium, then Firefox, then a stdlib static-layout lint, and the proof would name the rung it used.
  Done when: `fm shot` on a box with no browser exits 0 with a "degraded: static lint" receipt, not a stack trace.

- **Edit one setting through a generated `$EDITOR` fragment** — FEATURE — value 3 — effort S — risk low — category: tui-config
  Why: the user asked for config in the TUI, and every setting is hand-edited TOML today. This is the do-less route to it. A key opens only the relevant section in `$EDITOR`, the app validates it on save, and the change applies live with comments preserved. It could ship before any form-based settings screen.
  Done when: saving a bad value shows a line-accurate error and leaves the running config unchanged, while a good value changes the live theme.

- **Ship each design rule with a slop/crafted pair** — CLEAN — value 3 — effort M — risk low — category: testing
  Why: assumption: a design checker without paired fixtures drifts toward false positives. Each rule would carry one failing snippet and one passing snippet, which are also the playbook's before/after examples.
  Done when: every rule in `fm check design` has a pair and a test asserts the checker flags the first and passes the second.

- **Bisect taste across git history (wild)** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: wild; the idea is to run the design check and screenshots on each commit of a UI file, then report which commit made the page generic, with a before/after strip. It is a bisect for look regressions, and "count a taste regression" exists only as a one-line idea.
  Done when: on a fixture repo with a known bad commit, `fm design bisect` names that commit.

- **Run a nightly design residency that grows the exemplar bank (wild)** — FEATURE — value 3 — effort L — risk med — category: unattended
  Why: wild; during idle hours an unattended lane picks the thinnest vibe word in the bank, builds one original fragment, and keeps it only if the smoke test, the slop check and a second model's critique all pass.
  Done when: a night run adds at least one fragment with its three checks logged, and a rejected candidate leaves the bank unchanged.

- **Learn taste from pages the user chooses, on-box only (wild)** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: wild; `fm design learn saved/*.html` extracts palette, type scale, spacing and motion timings from files the user hands over and writes a local taste card. Nothing is fetched and nothing leaves the machine, which keeps third-party content as data under the pack's constraints.
  Done when: the command runs with sockets denied and produces a card that `fm check design` then enforces.

- **Record each design run as a replayable process cast** — FEATURE — value 2 — effort M — risk low — category: docs
  Why: the pack already records casts for demos, and a gallery that shows only results hides the process. Each playbook's example would link to the cast of Claude building it, with the layer steps marked.
  Done when: the gallery page for one playbook plays its cast and lists the layer steps with timestamps.
