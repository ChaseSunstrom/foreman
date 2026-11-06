# Brainstorm — lens: bold bets

- **Mutation-test the guard itself** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: the guard has a 24-command evasion corpus (T-1263), but nothing measures whether the corpus would notice the guard getting weaker. Assumption: guard rules are regexes or tables that can be mutated mechanically.
  Done when: `fm guard mutate` flips each rule, tightening a pattern or dropping an alternative, and reports a kill rate; a surviving mutant fails CI, and a seeded mutant that weakens `rm -rf` handling is killed.

- **Bind playbook stages to guard modes** — SECURITY — value 5 — effort M — risk med — category: discipline
  Why: Foreman's promise is that Claude plans before editing. The stages (plan, build, review, verify) are advice in prose today. Assumption: the guard hook can read a "current stage" marker.
  Done when: in the `review` stage a Write or Edit is denied by the hook with the stage named, and the same edit passes in `build`; a test covers both.

- **Score a design's distance from what it must not resemble** — FEATURE — value 5 — effort M — risk med — category: design
  Why: the request is "non generic". The slop-lint and style-dice ideas check tells, not resemblance. Assumption: stdlib can decode PNG via `zlib`, and tokens can be extracted from CSS.
  Done when: `fm check distinct` takes up to three named reference pages or screenshots plus a bank of default-template renders, and fails a UI task whose hue, radius, type-ratio and layout-hash vector is within a threshold of any of them.

- **Measure the motion from a filmstrip, not the CSS** — FEATURE — value 4 — effort L — risk med — category: motion
  Why: motion is the weakest-verified part of "good animations". Static linters read declarations; no idea samples the pixels. Assumption: a headless browser is available (probed by `fm doctor`).
  Done when: `fm shot --motion` captures N timed frames, computes per-frame displacement, classifies the easing (linear, ease-out, spring, abrupt stop) and flags a hover that is linear or a transition that stalls; a fixture page with a known linear tween is flagged.

- **Serve a Control Room: a loopback web app generated from the config schema** — FEATURE — value 5 — effort L — risk high — category: surfaces
  Why: the pack lists "web UI" as a surface, and the user wants config editable without hand-editing TOML. The TUI settings screen and a phone view are planned separately, so one schema-driven server could feed both. Assumption: the settings schema idea ships first.
  Done when: `fm control` starts a stdlib `http.server` on 127.0.0.1 with a one-time pairing token, edits tui.toml and code.toml through the same atomic, last-good write path as the TUI, and a test confirms it refuses non-loopback binds unless `--lan` is passed.

- **Emit a glance protocol: one JSON line, many shells** — FEATURE — value 4 — effort S — risk low — category: devices
  Why: the ideas so far cover tmux, prompt segments and phone pages one at a time. A single stable feed with thin adapters costs less than each of those. Assumption: waybar, SwiftBar and Home Assistant users exist.
  Done when: `fm glance --json` prints `{state, task, needs_you, cost, age}` in under 50 ms, and `--format waybar|swiftbar|tmux|mqtt` each produce valid output in golden tests.

- **Answer "why didn't it?" for any skill, playbook or hook** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: there are 1,161 skill files and 48 playbooks, with routing evals planned, but a user who sees a playbook not fire has no way to ask. Assumption: skill descriptions and trigger logic can be replayed offline.
  Done when: `fm why-not <playbook> "<request>"` prints the nearest trigger phrase, the competing skill that won and a one-line fix to the description, and a fixture request that should trigger `ui/terminal-ui` is explained correctly.

- **Hot-reload a playbook against a scripted fake model** — FEATURE — value 4 — effort M — risk low — category: authoring
  Why: authors of the "way more playbooks" request have no fast edit-run-diff loop. A fake model removes the cost and the variance. Assumption: the fake-runner conformance harness exists or is built.
  Done when: `fm playbook watch ui/foo.md` re-runs a golden scenario on each save and shows the diff in gates fired and checks demanded; editing one line changes the diff output.

- **Infer design tokens from the user's hand edits** — wild — FEATURE — value 4 — effort M — risk med — category: design
  Why: assumption: people fix generated UI by hand, and three padding values changed to 18px are a token waiting to be named. Hand-edit lessons are planned, but not token inference.
  Done when: after a UI run, `fm design learn` diffs the user's follow-up commits and proposes `--space-3: 18px` with the touched files, and only writes it to DESIGN.md on accept.

- **Play Test Breakout while verify runs** — wild — FEATURE — value 2 — effort S — risk low — category: delight
  Why: "call the verdict" and celebrations exist, but nothing is playable. Each test is a brick, and a failing test is a hard brick. Assumption: the user wants play during the wait.
  Done when: `fm code app --arcade` renders the suite as bricks, bricks break as real test results stream in, and the game ends exactly when verify exits.

- **Exchange lessons by sneakernet git bundle** — wild — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: lessons carry between projects, and an immune feed is planned. Neither works between two people's machines without any server. Assumption: lessons are stored as files that can be redacted.
  Done when: `fm lessons export --to x.bundle` writes a redacted, hash-listed bundle, and `fm lessons import` shows each lesson and licence class, quarantines it and applies nothing without a keypress.

- **Compile a 3D "proof chain" hero scene from the task ledger** — wild — FEATURE — value 3 — effort L — risk med — category: 3D
  Why: the user asked for 3D and non-generic design; the site is the public face. The ledger already holds claims, evidence and time. Assumption: one scene spec can feed WebGL and the TUI rasterizer, as another idea proposes.
  Done when: `site/build.py` renders the real ledger as a rotating chain of nodes, with a static SVG fallback under reduced motion and a byte-budget check on the page.
