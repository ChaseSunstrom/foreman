# Brainstorm — lens: capability map

- **Add a patch-coverage-by-proof gate** — FEATURE — value 4 — effort M — risk low — category: proof coverage
  Why: the pack lists provers by kind but never asks whether the changed lines were executed by any proof. Assumption: coverage.py, c8 or llvm-cov data can be collected during `fm flow` or `fm shot` runs.
  Done when: a diff with one line no proof or test executed finishes with that line named "unexercised", and a diff fully hit finishes clean.

- **Add architecture-fitness provers** — FEATURE — value 4 — effort S — risk low — category: static proof
  Why: assumption: import-linter, dependency-cruiser, ArchUnit and `cargo-deny` encode "does it fit the design" cheaply, and `fm lib`/stack cards can detect which one applies. The pack's "verify plan's dependency claims" checks claims, not standing rules.
  Done when: a planted forbidden import in a fixture repo turns the proof red and names the rule.

- **Add a stack-vs-best-in-class prover gap report** — FEATURE — value 4 — effort M — risk low — category: capability map
  Why: `fm map` already detects stack cards. The user asked for "verifying anything", so the open question is which prover categories (visual, a11y, DAST, query plan, size budget, fuzz, contract) this stack still lacks. Queue installs through the existing path.
  Done when: `fm prove --gaps` on a fixture web+SQL repo lists at least 5 missing categories, each with the tool name and install command, and says "unproven" for claims in those categories.

- **Prove query plans, not just query results** — FEATURE — value 3 — effort M — risk low — category: data/performance
  Why: the pack has data invariants and perf A/B but nothing for slow-query regressions. Assumption: sqlite, postgres or mysql is reachable on a scratch copy, so `EXPLAIN` output can be diffed.
  Done when: dropping an index in a fixture makes the proof report a seq scan on the named query with the before/after plan.

- **Run a DAST baseline against the flow's running instance** — FEATURE — value 3 — effort M — risk med — category: security
  Why: the pack covers a two-role access matrix and dependency scanning, but nothing probes the live app for headers, cookies or reflected input. Assumption: OWASP ZAP baseline or nuclei is installable on request, and runs only against localhost.
  Done when: a fixture app missing CSP and with an unflagged cookie yields two named findings, and a refusal if the target host is not loopback.

- **Check size and startup budgets on built artifacts** — FEATURE — value 3 — effort S — risk low — category: performance
  Why: the pack has perf A/B and noise floors but no bundle, binary, image or cold-start budget. Done by `hyperfine`-style runs plus `du` on the artifact.
  Done when: adding a 2 MB dependency to a fixture exceeds the stored budget and fails with a per-file size delta.

- **Prove containers and compose files by structure and health** — FEATURE — value 3 — effort M — risk low — category: infra
  Why: the pack covers dry-run and offline checkers but not building the image and testing it. Assumption: hadolint and container-structure-test (or podman) are present or queueable.
  Done when: a fixture Dockerfile with a missing HEALTHCHECK and a root user fails with both findings, and a fixed one passes after an actual build.

- **Prove durability with kill-point injection on the user's own code** — FEATURE — value 4 — effort L — risk med — category: data/reliability
  Why: the pack kills Foreman's own provers, but "does the user's save/import survive a crash" has no prover. Assumption: write sites can be found by tracing `fsync`/rename or an `strace` pass.
  Done when: a fixture writer that skips atomic rename leaves a corrupt file at one injected kill point, and the proof reports the byte offset and the invariant broken.

- **Add a metamorphic-relation prover for outputs with no oracle** — FEATURE — value 3 — effort M — risk low — category: correctness
  Why: search, ranking, geometry and ML code have no expected values to test against. Reordering inputs, scaling units and adding noise give checkable relations. The pack has paraphrase twins only for the tick.
  Done when: a fixture ranking function that depends on input order fails the "shuffle input, same result" relation.

- **Check docs links with a cache and archive fallback** — FEATURE — value 2 — effort S — risk low — category: docs
  Why: the pack checks flags, env vars and paths against code but not external URLs. Link rot makes docs wrong without any code change. Timeouts are labelled "unproven", not red.
  Done when: a README with one dead URL reports it with the HTTP status, and a second run within a day makes zero network calls for unchanged links.

- **Wild: Run firmware under QEMU or Renode and assert on the serial output** — FEATURE — value 3 — effort L — risk med — category: embedded
  Why: wild; the pack's hardware answer is a phone camera witness, and an emulator is a deterministic one. Assumption: the project has a Renode or QEMU target.
  Done when: a fixture firmware image prints "READY" on UART within 2 s in emulation, and a build that hangs fails with the last 20 serial lines.

- **Wild: Replay a recorded playthrough of a game or canvas app with frame-hash checkpoints** — FEATURE — value 3 — effort L — risk med — category: UI
  Why: wild; `fm shot` diffs still screens, but canvas, WebGL and game loops need seeded input replay with perceptual hashes at set frames.
  Done when: a fixture canvas app replays a 300-frame input tape and fails at the first frame whose SSIM falls below the threshold, naming the frame.

- **Wild: Capture the screen-reader speech transcript as the accessibility proof** — FEATURE — value 3 — effort M — risk med — category: accessibility
  Why: wild; axe and the accessibility tree prove structure, not what a blind user actually hears. Assumption: Orca/speech-dispatcher logging or an espeak shim can be driven headless.
  Done when: a flow's transcript for an unlabeled button reads "button" with no name, and the proof flags it where axe passes the page.

Next question: Which of these provers can the user's three most recent projects actually run today, and which stack does each prover category cost the most to install for?
Next question: For claims the host machine physically cannot prove (GPU, hardware, a production network), what is the cheapest stand-in, and how should it be labelled so it is never mistaken for the real thing?
