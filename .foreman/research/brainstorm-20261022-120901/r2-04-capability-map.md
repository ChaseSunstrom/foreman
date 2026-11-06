# Brainstorm — lens: capability map

- **Gate generated CSS on browser-support baselines** — FEATURE — value 4 — effort M — risk low — category: web compat
  Why: the pack has playbooks for motion and 3D but nothing that says whether `@property`, view transitions, scroll-driven animations or anchor positioning will run for the user's audience. Assumption: a small vendored support table (dated, hand-written) is enough; no network.
  Done when: `fm check ui` fails a page that uses a feature outside the target tier in `DESIGN.md`, and passes the same page once a fallback block is added.

- **Lint animations for compositor safety** — FEATURE — value 3 — effort S — risk low — category: motion perf
  Why: the pack lists motion playbooks and a paint budget for the TUI, but no check that web animation avoids layout-triggering properties.
  Done when: a fixture animating `width`/`top` is flagged with the transform/opacity alternative, and a transform-only fixture passes.

- **Validate 3D assets and shaders offline** — FEATURE — value 3 — effort M — risk low — category: 3D
  Why: the pack has three-js, react-three-fiber and glsl cards and a 3D playbook idea with a budget probe, but nothing inspects the assets themselves. Stdlib can parse glTF JSON and GLB headers.
  Done when: `fm check 3d scene.glb` reports triangle count, texture sizes and draw-call estimate, and exits non-zero over a budget set in `DESIGN.md`.

- **Publish a JSON Schema for tui.toml and code.toml** — FEATURE — value 4 — effort S — risk low — category: config
  Why: the pack notes that every setting is hand-edited TOML with no in-app screen. A schema gives completion and inline errors in any editor today, ahead of the settings screen. The `fm code config edit` verb should validate on save and fall back to the last-good copy.
  Done when: `fm code config schema` prints a schema that accepts the default `tui.toml`, and a file with a misspelled key is rejected with its line number.

- **Pseudo-localise and stress UI content** — FEATURE — value 3 — effort M — risk low — category: robustness
  Why: the TUI width bug (T-1468, `len()` padding of wide glyphs) shows layout breaking on unexpected text. The web equivalent is long German strings, RTL text and 200-character names. Assumption: the same pass can feed both the web check and the TUI golden frames.
  Done when: `fm check ui --stress` rewrites visible strings to 1.4x width with accents plus an RTL variant, and reports overflow or clipping per element.

- **Approve visual baselines in an inbox** — FEATURE — value 4 — effort M — risk low — category: visual QA
  Why: the pack's ideas include before/after frames and golden-frame tests, but no step where a person accepts a changed baseline (the Percy/Chromatic loop). Without one, golden frames either rot or get blindly regenerated.
  Done when: a changed frame blocks close until `fm shot approve ID` or reject, and the approval is recorded with the diff.

- **Add a `fm codemod` family with migration playbooks** — FEATURE — value 4 — effort L — risk med — category: playbooks
  Why: the playbooks cover build, clean and fix, but nothing for framework or language-version migrations (the work that Comby, jscodeshift and OpenRewrite handle). Python `ast` makes a stdlib codemod runner credible for Python, with a structural-grep fallback elsewhere.
  Done when: a recorded playbook migrates a fixture repo (for example `%` formatting to f-strings) and the repo's verify command passes before and after.

- **Add a font-pairing shelf with subset-and-self-host build** — FEATURE — value 3 — effort M — risk low — category: typography
  Why: the open work includes T-24, self-hosted fonts with a build failure on outside hosts, but the typography card teaches no taste. Original pairings come with a licence class each.
  Done when: `fm design font add NAME` copies a licensed font into `site/`, emits a `@font-face` with `font-display`, and the build passes the no-third-party check.

- **Write ops, incident and observability playbooks** — FEATURE — value 3 — effort M — risk low — category: playbooks
  Why: the 15 playbook stages listed have no ops or incident stage, although the library has ops and cloud cards.
  Done when: `/foreman:playbooks` lists an `ops` stage with at least three files, each carrying an eval that fails without it.

- **Wild: Run a squint test on screenshots** — FEATURE — value 3 — effort M — risk med — category: design QA
  Why: assumption: wild. Blur and downscale a screenshot using stdlib PNG decoding, then check the most salient region is the element `DESIGN.md` names as focal. It catches flat, everything-is-equal layouts, the generic tell the user keeps complaining about.
  Done when: a fixture page with a wrong focal element fails with the region named, and the corrected page passes.

- **Wild: Fuzz design tokens like a property test** — FEATURE — value 3 — effort M — risk low — category: design systems
  Why: assumption: wild. A monkey-test idea exists only for the settings screen. Random token combinations within declared ranges would catch contrast failures, unreadable themes and overlapping motion on the shared token file.
  Done when: a seeded run of 500 token sets reports each failing set with its seed, and fixing a rule makes the same seed pass.

- **Wild: Film a project's design history** — FEATURE — value 2 — effort L — risk med — category: delight
  Why: assumption: wild. Check out each release tag in a throwaway worktree, screenshot the site and the TUI, and assemble an animated SVG of the project's visual evolution for the release notes.
  Done when: `fm shot history` writes a looping SVG from at least three tags and is byte-identical on a second run.

- **Wild: Rank looks by what the user kept** — FEATURE — value 3 — effort M — risk low — category: taste learning
  Why: assumption: wild. Record which style recipe or theme the user accepted, edited or reverted, locally, and bias the next "style dice" roll toward their taste. The pack has the shelf and the dice but no signal on whether the user liked the result.
  Done when: after three recorded rejections of one recipe, a roll never returns it for that project, and `fm design taste --show` lists why.
