# Brainstorm — lens: bold bets

- **Run a red canary beside every proof** — SECURITY — value 5 — effort S — risk low — category: verifier integrity
  Why: assumption: every earlier idea trusts that the runner can still fail (a repo `conftest`, a PATH shim, `|| true`, or a patched reporter can swallow a failure). Nothing checks the runner in the user's own environment on each run.
  Done when: a fixture repo whose `conftest` forces exit 0 makes `fm prove` report "runner cannot fail, verdict void" instead of "proven"; the canary is a deliberately failing test run through the same runner and environment.

- **Lint every number in a final report against the tool log** — SECURITY — value 5 — effort M — risk low — category: agents
  Why: assumption: agents fabricate exit codes, counts and timings in prose. This is a zero-run lookup of each quoted figure, exit code and path in the session's tool-call log; it is cheaper than the existing re-verification of report claims. Unmatched figures are tagged "hearsay" in the rendered report.
  Done when: a report that says "23 passed" while the log shows 21 is flagged with both figures, and a fully matching report passes untouched.

- **Bisect a decayed claim to its breaking commit** — FEATURE — value 4 — effort M — risk low — category: proof lifecycle
  Why: assumption: proofs that expire or are re-verified nightly say that something broke, not which commit broke it. The claim's own probe is a ready-made `git bisect run` predicate.
  Done when: planting a regression three commits back in a fixture makes `fm prove --bisect CLAIM` print that commit and the probe output.

- **Set proof floors by path in a repo file** — SECURITY — value 4 — effort M — risk low — category: policy
  Why: assumption: depth today is chosen per task. Auth, billing and migration paths need a minimum proof kind whoever is working on them. A glob-to-kinds table is also the simple version of risk-based routing.
  Done when: `fm ship` refuses a diff touching `billing/**` with only unit proof, and names the missing kind from the table.

- **Run a shadow verifier lane that interrupts the builder** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: assumption: proof arrives at the end, when a wrong turn is already expensive. A read-only lane on a different model family re-runs the claims whose covered files just changed and posts "claim C-4 just went false" into the builder's next turn.
  Done when: in a scripted session where step 3 breaks a claim, the interrupt reaches the builder before step 4 starts, and the verifier wrote no files.

- **Build service twins from OpenAPI with fault modes** — FEATURE — value 4 — effort L — risk med — category: integration proof
  Why: assumption: "verify anything" fails at third-party boundaries (payments, mail, OAuth, object storage). A generated local twin with 429, timeout and malformed-body modes lets the integration be proven offline.
  Done when: an app calling a twin of a sample API is shown to survive an injected 503, and the proof run makes zero external network calls.

- **Prove whether an advisory is reachable** — SECURITY — value 4 — effort L — risk med — category: supply chain
  Why: assumption: a dependency alert is not actionable without knowing if the vulnerable function can be reached from an entry point. `fm graph` already holds the call data. Output is "reachable via path X / not reachable / unknown".
  Done when: a fixture with a vulnerable function called from `main` reports a path, and an unused one reports "not reachable".

- **Prove LLM-powered features with intervals and an injection corpus** — FEATURE — value 4 — effort L — risk med — category: AI products
  Why: assumption: many users' projects now call models, and unit tests cannot prove them. This runs held-out cases N times, reports the pass rate with an interval, and runs a prompt-injection set. "Inconclusive" is allowed.
  Done when: a toy classifier gets a pass rate with a 95% interval and a stated N, and a planted injection that changes its output fails the injection check.

- **Minimise provers by set-cover and track each one's value** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: assumption: proof kinds accumulate. Plant a break set, find the smallest prover subset that still catches every break, and propose retiring provers that never caught a real or planted break.
  Done when: on a fixture with four provers, the report names a subset that catches all planted breaks and lists the redundant ones.

- **Promote one-off provers into reusable cards** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: assumption: models hand-write a custom probe for each unusual claim. After one passes with a verified red-first run and a cold read, it becomes a parameterised prover in `fm lib` for the next claim of that shape.
  Done when: a second claim of the same shape resolves to the stored prover without new model-written code.

- **Fuzz thread schedules for the user's project** — FEATURE — value 3 — effort M — risk low — category: concurrency
  Why: assumption: "works once" is the common false-done for concurrent code. Run under the ecosystem's race detector or a shuffled or stress mode N times and report flake rate and the failing seed.
  Done when: a fixture with a planted race fails within the budget and prints a re-runnable seed.

- **Perturb the claim, not the code (wild)** — TEST — see type below — value 3 — effort M — risk low — category: proof sensitivity
  Why: wild; assumption: a probe may pass for "under 200 ms" and also for "under 20 ms", which means it never checked the stated threshold. Mechanically flip thresholds and quantifiers in the claim and require the probe to fail for each perturbed version.
  Done when: a probe that ignores its threshold is flagged "non-discriminating", and a correct probe fails for every perturbation.

- **Verify physical output with a phone camera (wild)** — FEATURE — value 2 — effort L — risk med — category: hardware proof
  Why: wild; assumption: embedded, IoT and print outputs have no software-visible state. The user points a phone at the device or screen, and a local vision model checks the stated LED, display or print against the claim, stored as an image receipt marked "human-eye adjacent".
  Done when: a photo of a known screen state passes a matching claim and fails a deliberately different one.

- **Hold a receipt forgery contest (wild)** — SECURITY — value 3 — effort M — risk low — category: verifier integrity
  Why: wild; assumption: the receipt checker is only as strong as its hardest forgery. A red-team child that sees only the checker's spec tries to produce a passing receipt without running the probe, and each success becomes a permanent checker rule plus a regression case.
  Done when: one forged receipt that initially passes is rejected by the added rule, and the corpus replays green.

Correction on item 12: its type is FEATURE, not "TEST".

Next question: which of these proofs would the user trust enough to skip looking, and what record of their past skipping or re-checking, not Foreman's guess, would show it?
Next question: what does a proof run do to the user's machine (ports, files, credentials, cost) that no claim declares, and who would notice first?
