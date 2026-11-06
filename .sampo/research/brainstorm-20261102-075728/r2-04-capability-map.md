# Brainstorm — lens: capability map

- **Add a security-baseline row pack with real scanners** — FEATURE — value 4 — effort M — risk low — category: security
  Why: the pack covers threat-model lines and secret sweeps for commits, but a goal's finish oracle has no rows that run the repo's own scanners. Semgrep, gitleaks, `pip-audit`, `cargo audit` and `npm audit` are the standard tools, and the pack's rule for #1 says to find them from manifests and stack cards. Assumption: a "complete" product row set should include them.
  Done when: a goal on a fixture web app gets scanner rows from its manifests, and a planted hard-coded key turns the finish oracle red naming that row.

- **Write a per-goal egress manifest** — FEATURE — value 4 — effort M — risk low — category: privacy
  Why: "Fence a goal's egress" and "nothing sent without a setting" exist as ideas, but nothing lists what actually left the machine over a multi-day goal (model calls, forge calls, fetched URLs, pasted packs). Assumption: users on private repos want a receipt.
  Done when: `fm goal egress` lists every outbound destination with a count and the kind of data sent, and a run with a local engine shows zero model destinations.

- **Taint rows derived from ingested PRDs, tickets and URLs** — SECURITY — value 4 — effort S — risk low — category: security
  Why: "Ingest a PRD, ticket or pasted spec" and "adopt a roadmap file" are in the idea list, but no idea gates rows that come from that text. Only the CI/issue watchers are marked hostile. Assumption: an ingested doc can plant "also run curl | sh" or "add dependency X".
  Done when: a fixture PRD containing an injected outward-action line produces a row marked `from-doc` that sits parked until one yes, and the test fails if it runs unattended.

- **Snapshot and truncate the goal journal** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: the goal is carried "over days, across crashes and compactions", and resume cost is only measured, never bounded. The pack shows 2125 files and a ratchet-minded user. Assumption: replaying a long journal on every resume grows without bound.
  Done when: a synthetic 60-day journal resumes in time within 20% of a 1-day one, and a replay of snapshot plus tail gives the same next-row pick as the full replay.

- **Schedule parallel rows by predicted file overlap** — PERFORMANCE — value 3 — effort M — risk med — category: scheduling
  Why: "Build contract-first so lanes run in parallel" and the parallel Missions 5-8 steer exist, but rows are merged in mission order with no conflict prediction. `fm graph blast` already exists to supply the overlap. Assumption: merge conflicts are the main cost of the fleet.
  Done when: two rows with overlapping blast radius are serialised and two disjoint ones run together, and a fixture shows fewer merge conflicts than the naive order.

- **Add a product compatibility-matrix row** — FEATURE — value 3 — effort M — risk low — category: completeness
  Why: the "journey matrix" is persona by state, but a best-in-class finished tool also lists supported OS, runtime and browser versions, each probed. The pack's own gates run on one Arch host. Assumption: goals that ship a product need this.
  Done when: a goal declares a matrix of at least 2 runtime versions, and each cell has a probe result of pass, fail or could-not-run, with the last shown honestly.

- **Audit the built product for phone-home** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the pack covers Foreman's own egress, not the deliverable's. A completed product should be shown to make no network calls it didn't declare. Assumption: this is cheap to run under the sandbox the project already probes.
  Done when: running the product's test suite in a network-denied sandbox, a planted undeclared HTTP call fails the "no surprise egress" row.

- **Publish a JSON schema for goal state with editor diagnostics** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: "let the user edit the goal as a plain markdown file" and the `--json` snapshot idea exist, but nothing makes a bad edit visible in the editor before resume. Assumption: users hand-edit goal files and hit refusals late.
  Done when: a malformed row in the goal file shows a diagnostic with file and line in a SARIF output, and `fm goal check` returns the same error.

- **Run the goal offline: park network rows, continue local ones** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the pack asks about waiting out usage limits and about hookless harnesses, but not about a laptop on a plane or a dropped connection. Assumption: one network row currently stalls the whole queue.
  Done when: with the network cut, the next pick skips the net-needing row, labels it `parked: offline`, and resumes it automatically when the network returns.

- **Add accessibility and i18n rows for UI goals, probed by axe** — FEATURE — value 3 — effort M — risk low — category: completeness
  Why: the web UI is a named surface, and the "beautiful UI" lens items are mostly about design, not about an automated pass. Assumption: a UI goal is "finished" only if a keyboard-only run and an axe pass are clean.
  Done when: a UI goal gets an a11y row, and a planted unlabeled button turns it red.

- **Wild: Field-test the finished product on real-world corpora from the user's machine** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: wild. A parser, linter or CLI built by the goal can be run on the user's own repos, logs and files, read-only, and compared with the reference tool where one exists. It checks "done" against inputs the goal's author never saw.
  Done when: a goal for a tool run against 100 local files yields a crash and mismatch report with no write to those files, and a planted bug shows up in it.

- **Wild: Sign the finish receipt with SLSA-style provenance** — SECURITY — value 2 — effort M — risk low — category: trust
  Why: wild. A done receipt that names the commit, the oracle results, the harness and model, signed by a local key, lets someone else check that "done" was not just "stopped". Assumption: the user will share goal results.
  Done when: `fm goal verify RECEIPT` passes on an untouched receipt and fails after one byte of the oracle results is changed.

- **Wild: Scan a QR on the finish card to open the read-only Goal page on a phone** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: wild. The web UI already exists on a local port. A QR with an expiring LAN token gives a pocket view of rows, evidence and the stop reason without any cloud service.
  Done when: scanning the code on the same network opens a read-only page showing the goal's rows, and the link stops working after its expiry.

- **Wild: Rehearse the plan's weakest row with a cheap model before committing to it** — PERFORMANCE — value 3 — effort M — risk low — category: planning
  Why: wild. Pilot the highest-risk row on the cheapest capable model on a throwaway copy, then use the real time and tokens to set that row's estimate and model tier. Assumption: estimates from a pilot beat guesses.
  Done when: the plan shows the pilot's measured cost beside the estimate for that row, and the estimate error on a fixture goal drops against the unpiloted baseline.

Next question: Which rows of a finished goal can only be checked by something that Foreman did not itself write or run, and where is that outside check recorded?
Next question: What does a goal do when the machine, the model or the host CLI version differs between day 1 and day 9, and which rows are re-proved?
