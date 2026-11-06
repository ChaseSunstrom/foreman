# Brainstorm — lens: bold bets

- **Compile one scene spec to WebGL, canvas and the TUI** — FEATURE — value 5 — effort L — risk med — category: 3D
  Why: the request wants 3D that isn't generic, but the pack has one terminal-ui playbook, library cards that teach no taste, and 3D ideas for the TUI, the site and `fm page` as separate efforts. Assumption: a small declarative scene format (meshes, lights, camera path, easing, seed) is enough for the recipes Foreman ships.
  Done when: `fm scene build hero.scene` emits a three.js module, a 2D-canvas fallback and a TUI half-block render, and a headless test shows the frame at t=0.5 matches across all three within a stated tolerance.

- **Check what the shell will really run with a stub-exec oracle** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: the guard has a 24-command evasion corpus (T-1263) and recent steers about verdicts depending on tree state. Corpora only catch the evasions someone thought of. Assumption: a throwaway PATH of recording stubs can run any command string without side effects.
  Done when: for every corpus entry and 1,000 generated variants, the argv vectors recorded by stubs under real `bash` equal the words the guard parsed, and any mismatch fails the suite.

- **Ablate every playbook line against its eval** — CLEAN — value 4 — effort M — risk low — category: playbooks
  Why: the request is for "way more" playbooks, but the pack gives no way to tell which lines change Claude's output. Assumption: the with/without playbook evals proposed earlier exist, so each line removed becomes one extra case.
  Done when: `fm playbook ablate ui/design-direction` reports each rule as load-bearing or inert, and a ratchet fails CI when a new playbook has inert rules above a set share.

- **Run the hostile-condition matrix on every UI** — FEATURE — value 4 — effort M — risk low — category: visual QA
  Why: the pack has screenshot proof, accessibility and motion audits only as single-condition ideas. Real distinctive UI breaks under 200% text zoom, forced-colors, reduced motion, pseudo-localised long strings, RTL and no-JS. Assumption: a headless Chromium is available; if not, the check says so rather than skipping.
  Done when: `fm shot --hostile` produces a contact sheet across at least 8 conditions and files a task for each overflow, contrast loss or missing fallback it detects.

- **Prove "faster" with a noise-aware perf evidence kind** — FEATURE — value 4 — effort M — risk low — category: performance
  Why: performance is listed as thin, and there is no perf stage beyond a playbook. The bench hook script exists, but performance tasks have no proof that survives noisy machines (see the canary failures dropped as "transient under load"). Assumption: stdlib `timeit` plus interleaved before/after runs is enough.
  Done when: `fm task prove --perf` runs interleaved before/after trials, reports the median change with a confidence interval, and refuses a pass when the interval spans zero.

- **Export any run as a Perfetto/OTLP trace** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: observability is thin, and the harness already has an event log that the TUI is meant to read. A standard trace file lets people use tools Foreman won't build. Everything stays local; nothing is sent.
  Done when: `fm trace RUN --perfetto` writes a JSON file that ui.perfetto.dev opens with lanes for station, worker, guard verdict and token spend.

- **Test skill triggers with should/shouldn't prompt suites** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: Foreman has about 1,161 skill files and 1,088 cards, and each new playbook raises the odds of one hijacking another's trigger. Assumption: descriptions can be scored against test prompts with a local matcher, or with the cheapest runner as a judge.
  Done when: each skill may carry `triggers.txt` with positive and negative prompts, and `fm skill triggers` fails if any negative prompt scores above a positive one of another skill.

- **Forge palettes from one seed with proofs** — FEATURE — value 4 — effort M — risk low — category: design
  Why: the pack has no colour playbook beyond a card, and the earlier ideas mention OKLCH and contrast separately. Assumption: a stdlib OKLCH implementation is small enough to ship.
  Done when: `fm palette forge --seed "#c0452a"` emits a token file with light and dark sets, APCA contrast figures and colour-blind simulations for every semantic role, and the TUI, pane and site all load that one file.

- **Critique screenshots with a local vision model, never a cloud one** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: a screenshot critic sends images of the user's unreleased product to a service. Assumption: a local vision-capable model reachable through the runner registry exists on the machine; otherwise this degrades to the static checks.
  Done when: with `--local-only`, the critique runs with no non-loopback connection (verified by the socket-denied test), and fails clearly when no local vision model is configured.

- **Play any playbook as a lesson (wild)** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: assumption: docs are thin because prose goes stale. A playbook already holds steps and checks, so the same file can walk a human through them in a scratch repo, and the checks keep it honest.
  Done when: `fm learn ui/motion-choreography` creates a scratch project, shows each step, and advances only when that step's check passes.

- **Seed taste from the user's own dotfiles and wallpaper (wild)** — FEATURE — value 3 — effort M — risk med — category: personalisation
  Why: the user's phrase "non generic" implies a preference nobody has asked about. Terminal colours, editor theme and wallpaper are on the machine already. Assumption: reading them is acceptable if listed first and off by default.
  Done when: `fm design taste --from-machine` lists the files it would read, asks once, then writes a preview palette and a style-shelf pick that the user can discard.

- **Give each release a generated cover from its changelog (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the user repeatedly asks for releases and wants non-generic visuals. A seeded scene from the scene spec above, driven by counts and task ids, costs little once that exists.
  Done when: `fm release` writes a deterministic cover image and animated SVG for the version, and the same changelog always yields the same bytes.
