# Brainstorm — lens: reliability

- **Confirm-or-revert every TUI config change** — FEATURE — value 5 — effort M — risk low — category: config safety
  Why: the request asks for in-app config, and today every setting is hand-edited TOML. A live theme or keymap change that hides text or unbinds the settings key would strand the user. Treat it like a display-resolution change: apply, show "keep? 15s", and revert to the last-good file on timeout, crash or restart.
  Done when: a pty test applies a keymap that unbinds the settings and quit keys, waits out the timer, and finds tui.toml restored and the screen usable. Pressing Enter inside the window keeps the change.

- **Edit tui.toml and code.toml without losing the user's comments** — FIX — value 4 — effort M — risk med — category: config
  Why: assumption: stdlib `tomllib` only reads, so a naive save from the settings screen rewrites the file and drops comments and ordering. Users who hand-edited will lose their notes the first time they use the new screen.
  Done when: a property test sets 20 random keys through the settings layer and a diff shows only those lines changed. Comments, blank lines and unknown keys are byte-identical.

- **Serialize release checks and the canary with one machine-wide gate lock** — FIX — value 4 — effort S — risk low — category: gate stability
  Why: three dropped tasks (canaries after 1.2.47 and 1.2.50, T-1380/T-1435) were transient reds caused by the canary running beside the release's own checks. Reruns hide this but cost attention each time. A flock makes overlap impossible.
  Done when: a test starts a canary during `fm release` checks and sees it queue, with the wait named in output. Five consecutive releases produce no load-induced red.

- **Ship `fm check ui`, a stdlib design-and-safety asserter for generated pages** — FEATURE — value 5 — effort M — risk low — category: UI verification
  Why: the pack has one 13-line UI playbook and no way to prove generated UI is sound. The site rule "nothing from third parties" already exists. The asserter would check contrast pairs, a `prefers-reduced-motion` guard, no outside hosts or CDN script tags, a non-default font stack, and a WebGL context-loss handler with a fallback for any canvas.
  Done when: as a verify command it exits non-zero on a fixture page missing the reduced-motion guard and zero on the corrected page.

- **Require every new playbook to carry an eval that fails without it** — FEATURE — value 4 — effort M — risk low — category: playbook quality
  Why: the request is "way more playbooks", but with 48 playbooks and no efficacy gate, volume can add confident noise. `plugin/evals/` exists to host this. Each design, 3D or motion playbook gets a paired case scored by deterministic checks such as `fm check ui`.
  Done when: CI fails a playbook added without an eval case. The recorded with/without delta appears in `fm playbooks` output.

- **Pin the tool versions a card was verified against and flag stale ones** — FEATURE — value 4 — effort M — risk low — category: skill rot
  Why: about 1,088 cards give verify commands and pitfalls for fast-moving libraries (three-js, framer-motion, tailwind). Advice silently rots. A `verified_with:` field plus a drift check lets `fm doctor` say "37 cards older than the versions you use".
  Done when: a fixture card pinned to an old version is marked stale in `fm lib show` and counted in doctor.

- **Lint out `len()` as display width in the TUI modules** — CLEAN — value 3 — effort S — risk low — category: TUI correctness
  Why: T-1468 fixed padding by `len()` for wide glyphs on one path (focused and selected log lines). An AST check stops the same bug returning anywhere in `fmcodetui.py` and its extensions.
  Done when: the lint fails on a fixture that pads with `len(text)` and passes on one using the column-width helper. The current TUI modules pass.

- **Generate guard evasions from the 24-command corpus, seeded and ratcheted** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: T-1263 shipped a hand-written evasion corpus. A mutator would apply quoting, `$IFS`, variable indirection, base64-to-shell, unicode lookalikes and line continuations to each dangerous command, so coverage grows beyond what a person thought of.
  Done when: CI runs N seeded mutations per command and any allowed variant prints its seed and minimal form. Fixed seeds go into a never-shrinking regression file.

- **Add `fm fsck` for the task ledger, worktrees, locks and journals** — FEATURE — value 4 — effort M — risk med — category: state integrity
  Why: at 1,478+ tasks with builder lanes (T-1478), orphan worktrees, duplicate ids, dangling dependencies and tasks closed without proof become likely. Repair is dry-run by default and prints the exact command for each fix.
  Done when: a fixture with a planted duplicate id, a dangling worktree and a closed-without-proof task has each reported with a repair command. Nothing is changed without `--apply`.

- **Scan for stdlib removals and run the suite on the oldest and newest Python** — PERFORMANCE — value 3 — effort S — risk low — category: portability
  Why: Foreman is stdlib-only by constraint, so its main breakage risk is Python itself, and this machine runs a bleeding-edge hardened kernel and likely a new Python. A PEP 594-style removal list scan plus a two-version CI matrix catches this early. Assumption: the CI workflow currently tests a single version.
  Done when: CI passes on both the minimum and newest Python. A fixture importing a scheduled-for-removal module is flagged.

- **Auto-bisect a red canary across releases (wild)** — FEATURE — value 4 — effort M — risk low — category: regression hunt
  Why: canaries go red after releases (1.2.47, 1.2.50) and a person has to guess the cause. Use the sentinel check as the oracle in a throwaway worktree, rerun to rule out load flakes, and name the culprit commit in the task.
  Done when: with a regression injected two releases back, `fm bisect` names that commit. A transient failure is reported as "not reproducible" instead.

- **Soak 3D scenes headlessly for GPU-resource leaks (wild)** — FEATURE — value 3 — effort L — risk med — category: 3D reliability
  Why: 3D skills will produce scenes that leak geometries and textures by never disposing them, a classic failure that only shows after minutes. Assumption: a headless browser is available, and the check skips with a named reason if not. It would run 10k frames and compare `renderer.info` counts at start and end.
  Done when: a fixture scene that never disposes geometry fails the soak and the fixed version passes.

- **Monkey-test the settings screen with random sequences and a contrast invariant (wild)** — FEATURE — value 4 — effort M — risk low — category: TUI fuzz
  Why: once themes, layouts and keys are all live-editable, the number of combinations explodes. A seeded monkey in a pty applies random sequences and asserts the terminal is restored, the config validates, and every text/background pair meets contrast on the docked-pane background (T-1217).
  Done when: 500 seeded sequences pass in CI, and a failing run prints its seed and replays exactly.

- **Make the site and demo build byte-reproducible** — CLEAN — value 3 — effort S — risk low — category: build determinism
  Why: the site, stats pages and demo SVGs are generated, and "regenerate and fail on drift" only works if two builds from the same commit are identical. Pin timestamps, ordering and random seeds.
  Done when: two `site/build.py` runs in clean directories produce an empty `diff -r`.
