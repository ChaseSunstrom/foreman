# Brainstorm — lens: user value

- **Check a pasted outside claim** — FEATURE — value 4 — effort M — risk low — category: claim-check
  Why: the request says "verifying anything", but every verb in the pack proves Foreman's own diff. Users also hold claims from a vendor doc, a colleague or another chatbot ("this call is idempotent", "that lib is thread-safe"). Assumption: users do this often.
  Done when: `fm check-claim "<text>"` runs a sandbox experiment and prints proven, disproven or unproven with the command it ran, and the planted-false claim in the fixture is disproven.

- **Store the user's proof standard once** — FEATURE — value 4 — effort S — risk low — category: proof profile
  Why: "does it do what the user meant" varies per user. One person means no console errors and load under 2s, another means ±1px. Assumption: today each prover re-guesses tolerances and what counts as "works".
  Done when: `fm prove --standard` asks 3 questions once, saves them in the repo, and `fm shot`, the data prover and the perf prover read those tolerances, shown in the proof line.

- **Show reopen rate per proof kind** — FEATURE — value 4 — effort M — risk low — category: trust calibration
  Why: the pack has bet calibration and the done-detector, but nothing tells the user which kind of proof has been wrong most often in their own repo. Assumption: the ledgers hold enough closed-then-reopened tasks to compute it.
  Done when: `fm doctor` prints "UI flow: 2 of 14 later reopened" for each proof kind with denominators, and prints "insufficient" below 5 samples.

- **Rank "unproven" items by cost if wrong** — FEATURE — value 4 — effort S — risk low — category: unproven labels
  Why: the request says unproven things must be labelled, but a bare label doesn't tell the user what to do. Assumption: adding who is hurt and how makes the label actionable.
  Done when: every unproven line carries "if false: <consequence in the user's terms>" plus a 1–3 stake rating, and the finish card sorts by it.

- **Print a "where to look" card for the residual risk** — FEATURE — value 4 — effort S — risk low — category: finish receipt
  Why: the user has about 60 seconds at the finish. Assumption: the highest-value use of that time is the claim Foreman is least sure of, and today it must be found in the receipt.
  Done when: the finish prints the top 3 uncertain claims, each with the exact click or command to check it by hand, and a fixture task with one weak proof ranks it first.

- **Let the user spend a verification budget in minutes or dollars** — FEATURE — value 3 — effort M — risk med — category: proof routing
  Why: the pack has cost receipts and a cheapest-prover router, but no way for the user to cap spend and have the best set chosen. Assumption: the user would trade depth for time on small tasks and the reverse on risky ones.
  Done when: `fm prove --budget 3m` picks provers whose estimated cost fits and lists the claims it left unproven for lack of budget.

- **Stream a verdict so far, and allow an early stop** — FEATURE — value 3 — effort M — risk med — category: progressive proof
  Why: long provers (soak, flows, data) leave the user staring at nothing. Assumption: cheap provers can run first and give a partial verdict.
  Done when: during a multi-prover run a "so far 3 proven, 1 running, 2 queued" line updates, and stopping early records the queued claims as unproven with reason "stopped".

- **Draw a proof implication graph** — FEATURE — value 3 — effort M — risk med — category: proof reuse
  Why: assumption: one passing end-to-end flow already covers several unit-level claims and a type check covers shape claims. Proving each separately wastes time and inflates the claim count.
  Done when: a claim covered by a stored, still-valid stronger proof is marked "implied by P-12" and not re-run, and the graph rejects an implication whose files differ.

- **Re-bind proofs through renames instead of expiring them** — FIX — value 3 — effort S — risk low — category: proof expiry
  Why: the pack's expiry-on-change idea would falsely stale every proof after a pure file move. Assumption: this would create re-prove churn that erodes trust.
  Done when: a proof whose covered files were only renamed (same content hash) stays valid and logs "rebound", while one with edited content expires.

- **Cache proofs by tree hash across branches** — PERFORMANCE — value 3 — effort S — risk low — category: proof cache
  Why: assumption: switching branches, stashing or reverting returns to a tree already proven, and the user pays again.
  Done when: returning to a previously proven tree hash reports "proven at <time>, no re-run" and a one-byte edit forces a re-run.

- **Recompute every quoted figure by a second route** — FEATURE — value 3 — effort M — risk low — category: non-code deliverables
  Why: "verifying anything" includes a report, spreadsheet or analysis the user will quote. The pack's lint compares numbers to the tool log, not to an independent calculation. Assumption: users hand Foreman data work.
  Done when: each marked figure is recomputed with a different library or query and shown as matching or differing, and a planted off-by-one in the fixture is caught.

- **Wild: turn a screenshot of the user's own bug into a red flow** — FEATURE — value 4 — effort L — risk med — category: repro
  Why: wild. Users show "it looks wrong" as a screenshot or clip. The pack covers reports and rival recordings, not the user's own failure image becoming the red-first check.
  Done when: given a screenshot of a broken fixture page, `fm flow --from-shot` produces a flow that fails on the broken build and passes on the fixed one.

- **Wild: learn a personal "feels right" score** — FEATURE — value 3 — effort L — risk high — category: subjective quality
  Why: wild. The user rates how a finished thing feels, 1–5, in one keystroke. Foreman correlates the ratings with measurables (latency, layout shift, error count) and builds a per-user score. Assumption: after about 20 ratings some measurable predicts them.
  Done when: after 20 fixture ratings the predictor ranks held-out builds in the right order better than chance, and it prints "insufficient" before that.

- **Wild: watch field signals that contradict a proven claim** — FEATURE — value 4 — effort L — risk high — category: field evidence
  Why: wild. The pack seeds goals from feedback and warranties finished work, but proven claims aren't tied to later issues, support mail or crash text. Local only, nothing sent.
  Done when: a fixture issue saying "login fails" flips the proven "login works" claim to "contradicted by field report #", and the finish card says so.

Next question: Which proof kinds have users overridden or ignored in practice, and does that match what the reopen rates say?
Next question: When the user's sentence names something no prover can observe (taste, trust, a third party's behaviour), what will they accept as sufficient instead?
