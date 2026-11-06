# Brainstorm — lens: approaches

- **Ingest other tools' verdicts as proof records** — FEATURE — value 5 — effort M — risk low — category: reuse
  Why: the request spans UI, data, docs, ops and performance, and each already has a mature tool (JUnit, TAP, SARIF, Lighthouse, k6, hyperfine, conftest, Hurl). Existing ideas such as "Find infra dry-run verifiers from manifests" discover tools to run. They don't cover importing a finished tool's output. Foreman would own only the label, the tree hash and the freshness, and write no new verifiers. Trade-off: it depends on each tool's output format.
  Done when: `fm prove import` on a fixture JUnit file and a SARIF file creates two proof records bound to the HEAD tree hash, and editing a covered file marks both expired.

- **Trace MASTER.md clauses to tests and code** — FEATURE — value 4 — effort M — risk low — category: docs vs code
  Why: MASTER.md already holds module clauses with task ids, and "already built at birth" already reads them. Nothing checks that each clause has a named test or prover, or that a test has a clause. Orphans in either direction are "unproven" or "undocumented" in the user's sense.
  Done when: `fm check` lists clauses with no proof and tests with no clause on a fixture, and a planted orphan clause is named.

- **Generate doc blocks from code instead of checking them** — CLEAN — value 4 — effort S — risk low — category: docs vs code
  Why: T-0365 (a generated section from `fm map`) is deferred, and the request asks for docs checked against code. Eliminating drift beats detecting it for flag tables, verb lists, env vars and defaults. Trade-off: it only covers what is mechanically derivable, and prose still needs the existing token checks.
  Done when: changing a CLI default without regenerating fails `fm check`, regenerating clears it, and the README flag table has no hand-edited rows.

- **Prove "no behaviour change" refactors by differential run** — FEATURE — value 4 — effort M — risk low — category: refactor proof
  Why: deferred items like T-0166 (move code out of register.tsx) claim "no behaviour change" on unit tests alone. Load the old function from `git show` beside the new one, feed recorded test arguments plus generated inputs, and compare results and exceptions.
  Done when: a planted semantic change inside a pure-move fixture yields a counterexample input, and an honest move passes N inputs.

- **Backtest each prover on the project's own past FIX commits** — FEATURE — value 4 — effort M — risk low — category: prover quality
  Why: "Ship a red fixture with every prover" uses synthetic breaks. This project has hundreds of real FIX commits, such as T-2606 and T-2605. Run each prover on the parent of each fix and report recall per proof kind. This is the only signal Foreman didn't author, which matches the standing steer.
  Done when: a report says "UI shots caught 3 of 11 historical fixes in scope" with the commits listed, and a prover that catches none is marked low-recall in `fm doctor`.

- **Add `fm challenge "<sentence>"` (pull-based proof, do less)** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the minimal approach is to prove nothing up front. The user pastes a sentence from a final report, Foreman maps it to the nearest claim, reruns its prover or says "unproven: no prover", and names the cheapest one. Trade-off: it relies on the user doubting.
  Done when: a challenged sentence with a proof reruns and prints a verdict, and one without prints unproven plus a suggested prover.

- **Run deep provers overnight on idle CPU** — FEATURE — value 4 — effort M — risk med — category: ops
  Why: the night tick already exists. Slow provers (a long fuzz run, a soak, mutation scoring) cost no tokens, so quick-checked claims can be upgraded to deep-checked by morning. Assumption: the user's machine is idle at night. Trade-off: it competes with the user's own CPU use.
  Done when: a tick upgrades a fixture claim from "quick" to "deep" with its run duration recorded, and it yields to a load threshold.

- **Use the app's own logs and traces as the witness** — FEATURE — value 3 — effort M — risk med — category: ops proof
  Why: the request lists "infra and ops", and workers and cron jobs have no UI to photograph. Run the flow, collect log lines or OTel spans, and assert on them, e.g. "retry fires once". Assumption: the target app emits usable telemetry.
  Done when: a planted regression that doubles an event fails the claim in a fixture app.

- **Record and replay external calls in flows** — FEATURE — value 3 — effort M — risk med — category: determinism
  Why: `fm flow` against live services is flaky and can't run offline. A cassette makes it repeatable and stamps the proof "replayed", and re-recording diffs flag upstream drift.
  Done when: a flow runs offline against a recorded cassette, and a changed upstream response shows as a diff on re-record.

- **Build a shape-preserving synthetic twin of private data** — FEATURE — value 3 — effort M — risk low — category: privacy
  Why: data proofs need data, but the owner's rows shouldn't reach CI, lanes or cloud children. Generate a synthetic set from the profile only (types, null rates, cardinalities, key relations).
  Done when: the twin matches its profile within tolerance, and a scan finds no real value from the source in it.

- **Run each UI flow in two browser engines and flag divergence** — FEATURE — value 3 — effort M — risk low — category: UI proof
  Why: web UI is the one declared surface, and there is no oracle for layout. Disagreement between engines is a free signal.
  Done when: a planted engine-specific CSS bug is flagged with both screenshots.

- **Wild: witness hardware or kiosk output through a camera** — FEATURE — value 2 — effort L — risk med — category: physical proof
  Why: wild. "Verifying anything" includes a printer, an LED or an e-ink display. A phone photo goes to a local vision model with a rubric, and a human tap confirms. Anything unconfirmed stays labelled unproven.
  Done when: a fixture photo of a lit and an unlit indicator gives the right verdict and a record with the photo hash.

- **Wild: reproduce receipts on a second host** — FEATURE — value 2 — effort M — risk med — category: replication
  Why: wild. A claim is "replicated" only when another machine reproduces a random claim from the receipts; otherwise it reports "single-host". Local-first, and different hardware shakes out different bugs.
  Done when: two hosts exchange a receipt, and a claim that fails on host B is reported as not replicated.

- **Wild: `fm bite <claim>` shows the proof fail on demand** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. A recorded sabotage patch is applied in a scratch copy and the prover goes red, then the patch is reverted and it goes green. The user sees that the proof can fail, which a plain "green" never shows. It reuses the red-fixture idea as a user-facing demonstration.
  Done when: running it on a fixture claim prints red then green, and the working tree is byte-identical afterwards.

On your earlier question about a private goal needing a remote-only capability: fail closed by default, and ask once with `fm ask`. Degrading silently to a weaker local model would produce a proof the user didn't expect.

Next question: Which proof kind has produced the most false greens or false reds on this repo's real history, and is that measurable without Foreman's own ledgers?
Next question: When the user doubts a finished claim a week later, which artifact would they want to see first: the rerun, the evidence, or the sabotage?
