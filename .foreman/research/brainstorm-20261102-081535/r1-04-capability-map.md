# Brainstorm — lens: capability map

- **Type every claim with a proof kind, and refuse "proven" without an artifact** — FEATURE — value 5 — effort M — risk low — category: proof ledger
  Why: the request says unprovable things must be labelled unproven. The pack has "Not proven" receipts and gauge omissions, but no closed vocabulary (ran-command, screenshot, trace, diff, bet, reading-only) that a receipt line must cite. Assumption: today's labels are free text.
  Done when: a finish receipt line claiming "proven" with no artifact path or hash is rejected by `fm task finish`, and the unproven lines print under their own heading.

- **Add baseline-diffed screenshots to `fm shot`** — FEATURE — value 5 — effort M — risk low — category: UI proof
  Why: Playwright `toHaveScreenshot` and Percy/Chromatic are the standard. The pack mentions `fm shot` and `fm flow` but shows no stored baseline, masked regions or perceptual threshold. Assumption: shots are currently eyeballed.
  Done when: changing a CSS colour in a fixture app makes `fm shot --compare` exit non-zero and write a highlighted diff image, and a masked clock region does not trip it.

- **Write a trace bundle for every `fm flow`** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: Playwright's trace viewer keeps DOM snapshots, network calls and console errors per step. Assumption: `fm flow` keeps only pass/fail and screenshots.
  Done when: a failing flow leaves a single bundle holding per-step DOM, console errors and failed requests, and `fm flow --open` shows it.

- **Run accessibility and performance budgets inside flows** — FEATURE — value 4 — effort M — risk low — category: UI proof
  Why: axe-core and Lighthouse CI are the norm. The pack has accessibility rows only as plan ideas, with none running as proof. Assumption: no flow step runs axe today.
  Done when: a fixture page with an unlabeled input fails the flow with the axe rule id, and a page over a set LCP budget fails with the measured number.

- **Diff docs against code, with executable examples** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: the request names "docs against code". Tools in this space (doctest, mdx tests, lychee, Vale) check examples, links and prose. The pack mentions `fm lib` and claim lint only for numbers. Assumption: no check yet extracts README command blocks and runs them.
  Done when: a README block with a renamed flag fails in a scratch run, a dead link is listed, and a documented config key absent from the code is named.

- **Replay recorded real inputs through old and new builds** — FEATURE — value 4 — effort M — risk med — category: data proof
  Why: golden-master and approval testing, plus Keploy-style record-replay, catch "does what it did before" regressions that unit tests miss. The pack has a differential-test idea against a reference tool, but none against the project's own previous build. Assumption: the project has capturable inputs.
  Done when: `fm replay --against HEAD~1` runs 50 stored inputs and prints only the outputs that changed, each marked intended or not.

- **Verify data and migrations before and after** — FEATURE — value 4 — effort L — risk med — category: data proof
  Why: Great Expectations, Soda and data-diff check row counts, null rates, referential integrity and a before/after diff. Nothing in the pack touches databases or data files. Assumption: users do ship schema or data changes.
  Done when: a migration on a fixture DB prints the row-count and null-rate deltas per table, and an orphaned foreign key fails the check.

- **Dry-run infra: render and lint without applying** — FEATURE — value 4 — effort M — risk low — category: infra proof
  Why: hadolint, checkov, conftest and `systemd-analyze verify` check infra files without touching hosts. The pack's unit-liveness idea covers only Foreman's own timers. Assumption: the user's project has Dockerfiles, units or IaC.
  Done when: a Dockerfile running as root and a unit file with a bad `ExecStart` both fail with the tool's rule id, and no host state changes.

- **Fuzz API contracts from the project's own spec** — FEATURE — value 3 — effort M — risk low — category: API proof
  Why: Schemathesis and Pact derive hundreds of cases from an OpenAPI file or a consumer contract. Assumption: the project exposes HTTP or has a spec. The pack's web UI is a likely target.
  Done when: against a fixture server with a handler that 500s on an empty string, `fm check api` finds it and writes a replayable curl.

- **Turn the user's sentence into example pairs they confirm, then run them** — FEATURE — value 5 — effort M — risk med — category: intent proof
  Why: "does it do what the user meant" is the hardest item, and example mapping is the known method. The pack's missed asks come from meaning drift (a "2 characters" criterion versus a 7-character rule). Assumption: nothing currently shows concrete input/output examples for approval before building.
  Done when: a plan shows three input/output pairs, the user's edit to one is stored as a test, and the finished task runs all three.

- **Measure performance against a noise floor on the user's own project** — FEATURE — value 3 — effort M — risk low — category: perf proof
  Why: hyperfine and criterion report variance, and the pack's bench gate already needed the median-on-loaded-bench fix (T-2605). Assumption: that machinery serves only Foreman's own hooks, not the user's code.
  Done when: `fm bench cmd "<cmd>"` reports median and spread over N runs, marks a 5% slowdown inside a 10% noise band as inconclusive, and a 30% slowdown as a regression.

- **Wild: Run chaos shots of each screen under injected faults** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: wild. Empty, error, offline, slow-network, RTL, 200% zoom and dark-mode states are the ones real users hit and no one screenshots. Assumption: the web UI's states are only checked in the happy path.
  Done when: one command produces a contact sheet of one screen in eight forced conditions, and a blank white panel in any cell is flagged.

- **Wild: Cut a captioned proof video of each flow** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. A 20-second recording with step captions, the command run and the assertion result makes verification something a person can watch instead of trusting. Assumption: flows can be recorded headless.
  Done when: `fm flow --video` writes an mp4 or gif whose frames show each assertion with a pass or fail caption, and it attaches to the finish receipt.

- **Wild: Map the repo by proof kinds, not coverage** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: wild. Line coverage counts unit tests only. A map showing, per module, which proof kinds (unit, flow, replay, doc-run, perf, data) have ever exercised it makes the unproven area visible. Assumption: the proof-kind vocabulary from the first idea exists.
  Done when: `fm proofmap` lists the modules with no non-unit proof and names the cheapest missing kind for each.

- **Wild: Sign a provenance attestation of what was actually run** — SECURITY — value 2 — effort M — risk low — category: proof ledger
  Why: wild. in-toto and SLSA attestations bind commands, tree hash and outputs, so "I ran it" can be checked by someone who doesn't trust the agent. Assumption: a signing key the agent can't read is available.
  Done when: a finish receipt carries an attestation, and editing any recorded output makes `fm verify-receipt` fail.

Next question: Which proof kinds can run on every harness with no browser or network, and which silently become "unproven" when a dependency is missing?
Next question: For a user-meant check, who confirms the example pairs when the user is away, and what label does the task carry until they do?
