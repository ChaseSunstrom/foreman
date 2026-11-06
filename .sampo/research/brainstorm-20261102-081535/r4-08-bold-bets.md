# Brainstorm — lens: bold bets

- **Fingerprint the product's behaviour per flow** — FEATURE — value 4 — effort M — risk med — category: behaviour proof
  Why: assumption: existing proofs check outputs, not what the product touched. Nothing in the pack records syscalls, outbound hosts, files written, or child processes per `fm flow` run and diffs them across commits.
  Done when: a flow run writes a fingerprint file, and a commit that adds a new outbound host or an unexpected file write makes `fm prove` flag the delta by name.

- **Run a sandboxed red-team lane against the running app** — SECURITY — value 4 — effort M — risk med — category: security proof
  Why: assumption: the pack covers two-role access checks and LLM injection corpora, but no general DAST pass (ZAP or nuclei, if installed) on the locally booted app, confined to loopback.
  Done when: against a fixture app with a planted reflected-XSS route, the lane reports that route and exits clean on the patched fixture.

- **Walk the UI by keyboard and screen reader, and keep the transcript** — FEATURE — value 4 — effort M — risk med — category: accessibility proof
  Why: axe and accessibility-tree snapshots appear above, but a tab-order walk with focus-trap detection and a spoken-output transcript (Orca or AT-SPI) does not.
  Done when: a fixture page with a keyboard trap fails the walk, naming the element where focus stuck, and the fixed page passes with a stored transcript.

- **Rehearse infra in an ephemeral local cluster** — FEATURE — value 5 — effort L — risk med — category: ops proof
  Why: the pack has dry-run, lint and read-only probes, but nothing that applies the manifests to a throwaway kind, compose or localstack environment. Nothing kills a pod and checks recovery either.
  Done when: a fixture Helm chart is applied locally, a smoke request passes, a pod kill recovers within a stated deadline, and everything is torn down with no residue.

- **Smoke the packaged artifact in a clean room** — FEATURE — value 4 — effort S — risk low — category: release proof
  Why: assumption: proofs run against the source tree. A wheel, deb, AppImage or image can be broken (missing data files, wrong entry point) while all source-tree proofs pass.
  Done when: a fixture package missing one data file passes the source tests but fails `fm prove artifact`, which installs it in an empty container and runs its entry point.

- **Render the user-preference matrix in `fm shot`** — FEATURE — value 3 — effort S — risk low — category: UI proof
  Why: the pack lists locale and viewport variants, but not forced-colors, reduced-motion, 400% zoom, RTL, or colour-vision simulation. These are the first complaints a design-led team hears.
  Done when: one command writes a contact sheet of at least five preference variants, and a planted low-contrast state fails the forced-colors cell.

- **Prove canvas, WebGL and game UIs with deterministic frames** — FEATURE — value 3 — effort M — risk med — category: UI proof
  Why: DOM and accessibility-tree proofs can't see non-DOM UIs. Seeded RNG, a fixed timestep, and a perceptual hash at named frames would cover them.
  Done when: a fixture canvas animation yields identical hashes on three runs, and a one-pixel colour change at frame 30 fails the proof.

- **Rebuild the claim blind and diff the two implementations** — FEATURE — value 5 — effort M — risk med — category: meaning proof
  Why: "does it do what the user meant" has no independent oracle. A tool-less child that sees only the user's sentence and the public signature writes a second implementation, which is then differentially fuzzed against the real one. Disagreements point to either a bug or an ambiguous sentence.
  Done when: on a fixture with an ambiguous sentence, the report lists at least one input where the two readings differ, which feeds the confirm-an-example step.

- **Add a sanitizer sweep chosen from the manifest** — FEATURE — value 3 — effort S — risk low — category: memory-safety proof
  Why: race detectors appear above, but not ASan, UBSan, Miri or `-race` picked automatically from Cargo.toml, CMake or go.mod.
  Done when: a fixture Rust crate with a planted out-of-bounds read fails the sweep, and the clean crate passes.

- **Pre-warm the proof environment while the model codes** — PERFORMANCE — value 4 — effort M — risk med — category: proof latency
  Why: assumption: boot, seed and browser start dominate the cost of re-proving. A shadow lane that keeps the app and DB warm and rebuilds incrementally would make the first proof after an edit fast.
  Done when: median time from edit to first verdict drops at least 50% on the fixture against a cold run, and a stale warm environment is detected and rebuilt.

- **Drive Android emulator flows from the accessibility tree** — FEATURE — value 3 — effort L — risk high — category: mobile proof
  Why: only a wild real-phone-over-adb idea exists above. An emulator with a11y-tree assertions is the repeatable, hermetic version.
  Done when: a fixture APK completes a three-step flow headlessly in CI, and a planted missing-label bug fails it.

- **Let the user take over the streamed browser mid-flow (wild)** — FEATURE — value 4 — effort L — risk high — category: teach by demonstration
  Why: wild. The user watches Foreman use the product, grabs the cursor at the first wrong step, and their takeover is recorded as the corrected flow. The pre-takeover steps become a red-first regression, so "that's not what I meant" turns into a permanent probe.
  Done when: a takeover on a fixture app yields a saved flow that fails on the old build and passes on the fixed one.

- **Add a debug probe port that exposes app state to flows (wild)** — FEATURE — value 4 — effort L — risk high — category: state-level proof
  Why: wild. A dev-only, loopback-only endpoint, wired through a small stack-card shim, exposes the app's state tree. Flows then assert "the cart has 3 items" directly instead of via pixels or text. It is never built into release artifacts.
  Done when: a fixture app's flow asserts internal state, and a release build is checked to contain no probe endpoint.

- **Build a prover forge that qualifies its own provers (wild)** — FEATURE — value 5 — effort L — risk high — category: prover generation
  Why: wild. For a stack with no prover, a child drafts one. It is promoted to a stack card only if it catches a planted bug in a fixture and passes the clean twin.
  Done when: for a stack the repo has no prover for, the forge produces a prover that fails the planted fixture, passes the clean one, and is refused if it passes both.

Next question: Which of these proofs would the user still trust after reading one false positive, and what is the false-positive budget per prover before they stop reading verdicts?
Next question: What do the stack cards say about which of these provers can run offline and unprivileged on the user's actual machine today?
