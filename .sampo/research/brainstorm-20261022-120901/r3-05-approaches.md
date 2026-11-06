# Brainstorm — lens: approaches

- **Adopt W3C design tokens (DTCG JSON) as the one token format** — FEATURE — value 4 — effort M — risk low — category: design tokens
  Why: assumption: the pack has many "one token file drives every surface" ideas but no format. A standard format means Figma, Tokens Studio and Style Dictionary exports import for free, and it needs only stdlib `json`.
  Done when: `fm design tokens import x.tokens.json` emits a TUI theme and CSS custom properties, and a DTCG fixture round-trips losslessly.

- **Make native CSS the default motion tier** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the pack has motion tokens and a compositor lint, but no stance on tooling. Scroll-driven animations, View Transitions and `@property` give zero-JS motion that is cheap on phones, with JS libraries used only when the CSS can't do it. Assumption: target browsers are recent, with `@supports` fallbacks.
  Done when: the motion playbook's reference page animates with 0 bytes of motion JS, passes the compositor lint, and degrades to a static page under `prefers-reduced-motion`.

- **Bake 3D offline instead of rendering it at runtime** — FEATURE — value 4 — effort L — risk med — category: 3D
  Why: the pack weighs a stdlib TUI rasteriser against GPU scenes, and baking is a third path. A release-time render of a turntable gives deterministic golden frames, runs on any device, and costs almost nothing at runtime. Assumption: the baker may use a dev-only headless renderer, never a runtime dependency.
  Done when: `fm bake scene.json` emits one frame set that the TUI plays at 12 fps as half-block art and the site scrubs as an image sequence, and the output is byte-identical on re-run.

- **Open one design door and ratchet skill-description tokens** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: Foreman ships 12 skills, and every top-level skill description costs context each session. A single `/foreman:design` skill with a router table, and children loaded as reference files, lets the family grow to 15+ playbooks without that cost.
  Done when: CI fails if the startup skill-list tokens grow by more than one description after the design family lands.

- **Run `fm shot` in a locked-down browser** — SECURITY — value 4 — effort S — risk low — category: visual proof
  Why: the visual-proof ideas screenshot generated pages and cloned repos, which are untrusted. Use a throwaway profile, resolve only loopback, and allow no extensions or `file://` outside the fixture.
  Done when: a fixture page that fetches an outside host and one that reads `file:///etc/passwd` both fail in test, and the screenshot is still produced.

- **Scaffold every web and 3D template strict by default** — SECURITY — value 3 — effort S — risk low — category: scaffolds
  Why: the site already bans third-party loads, so generated scaffolds should too: a CSP meta tag, no `eval`, and self-hosted fonts and shaders.
  Done when: a scaffolded 3D page loads with `default-src 'self'` and zero console CSP violations, and `fm check ui` flags any added outside host.

- **Add a `:set` ex-line to the TUI** — FEATURE — value 3 — effort S — risk low — category: TUI config
  Why: the pack's settings ideas are screens, palettes and verbs. A schema-generated ex-line is a smaller, keyboard-fast approach: `:set theme?` shows the value and its source, and `:w project` picks the scope. Both can be scripted and recorded as macros.
  Done when: `:set theme=amber` applies live, an invalid value errors without applying, and Tab completes keys and values from the schema.

- **Simulate bad screens on every UI proof** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: devices are thin in the pack. Stdlib PNG filters (grayscale, deuteranopia and protanopia matrices, 40% contrast plus glare wash, 480px-wide downscale for a "10 feet away" view) turn "state not told by colour alone" into a testable gate.
  Done when: a fixture whose error and success states differ only by red versus green fails the colour-blind pass, and the fixed version passes.

- **Scaffold TUI panels with a hot-reload loop** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: there are many TUI ideas (extension API, inspector, golden frames) but no front door for authors. `fm code tui new-panel` writes a panel with its golden-frame test, and `--hot` reloads it on save behind the render firewall.
  Done when: the scaffolded test passes, and editing the file changes the live panel within 1 s without a restart.

- **Gate UI work on a numeric look fingerprint** — FEATURE — value 3 — effort M — risk med — category: design measurement
  Why: taste is currently judged by critics. A stdlib-computed fingerprint (palette spread in OKLCH, type-scale ratio, radius, density, contrast, median motion duration) lets a brief say "brutalist ink ±tolerance" and be checked. Assumption: about 12 numbers capture enough to separate a stock page from a distinct one.
  Done when: a default-Tailwind fixture scores far outside a declared "ink" target and fails the gate, while the crafted exemplar passes.

- **Wild: Test against surface profiles (10-foot TV, e-ink, car glance, wrist)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild, and the pack's devices are thin. A profile is a viewport, a palette limit, a minimum text size, a maximum number of items and "no hover" rules, and the brief names which profiles it must pass.
  Done when: `fm shot --profile eink` renders 2-level gray with no animation and fails a page that depends on hover.

- **Wild: Draw the layout builder as an exploded isometric view** — FEATURE — value 2 — effort L — risk med — category: TUI config
  Why: wild. Panels float as slabs in a braille or box-glyph axonometric stack, so reordering, resizing and hiding them is spatial and doubles as a showpiece for the 3D rasteriser. The saved result is still plain `tui.toml`.
  Done when: moving a slab and pressing save writes the same layout the flat editor would, and the golden frame matches in three themes.

- **Wild: Print the keymap as a poster in the current theme** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. An SVG or print-ready sheet generated from the keymap and theme registries, with swatches and a diagram of the layout, is a keepsake that stays in sync with the config.
  Done when: `fm code tui --poster` writes an SVG listing every bound key, a hand edit of `tui.toml` changes its output, and it makes no network calls.
