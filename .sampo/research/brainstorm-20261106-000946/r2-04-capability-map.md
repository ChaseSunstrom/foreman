# Brainstorm — lens: capability map

Reading the pack, the ask is a *trained* decider (Kev-style) that is generic across every Sampo-managed project, with an explicit scope: what it does, what it’s trained on, how it’s trained and served on this box, how it’s measured, and how it improves every Rune generation. I’m reading that as a request for a *complete* decider stack, not just a classifier — so I’ll map the full best-in-class capability set and propose what the pack doesn’t show. Note: the “Ideas so far” list already covers much of the genericity/training/serving surface (kNN oracle, frozen-embedding heads, provenance lake, champion/challenger, abstain curves, zero-model arm, regret training, federation). I’m going past those into the **measurement harness, data governance, the improvement causal loop, and the human interface** — the “thin” cells (reliability, performance, ui, observability, docs, devices, simplicity).

- **Build the Rune-generation improvement loop as a closed, causal, re-benched pipeline** (FEATURE) — value 5 — effort L — risk med — category: measurement/improvement
  Why: The ask’s last clause (“how it improves every Rune generation”) is the one thing no idea owns end-to-end. T-0866/T-0867 (bench vs plain, published scorecard) are deferred, and the standing rules already demand zero-token arms + Haiku smoke + end-of-run exam. A decider that re-trains must re-prove itself each generation or it’s untrustworthy.
  Done when: `sampo decide gen` produces a diffable scorecard (per-slot accuracy, coverage, abstain-rate, cost) vs the previous generation’s frozen weights, and fails the gate if any adopted slot regresses.

- **Ship a per-project consent + data-minimisation contract the trainer enforces** (FEATURE) — value 5 — effort M — risk low — category: privacy/training-data
  Why: “Generic across every project” means training rows from a private repo could leak into another project’s model. The pack’s steers demand local-first and no outward sends; but no idea defines *which* rows are in-scope per project, or the redaction boundary between projects.
  Done when: the collector tags every row with project-id + sensitivity class, refuses to merge across projects without an explicit `--federate`, and `sampo doctor` lists the per-project in-scope row count.

- **Make every model call a replayable, content-hashed ledger line with a named cause** (FEATURE) — value 5 — effort M — risk low — category: observability/reliability
  Why: “How it is measured” is unmeasurable if a fallback fires silently. The earlier question (which slot has “never left a ledger trace”) is a direct gap. T-0329 and the “name the fallback” ideas exist but none tie the call to a *reproducible* replay.
  Done when: `sampo decide replay TASK` reproduces the exact input, weights hash, output and abstain reason for any past call, offline.

- **Give each slot a typed stall-cause + rules fallback, and log which fallback won** (FEATURE) — value 4 — effort S — risk low — category: reliability
  Why: A trained head that silently falls back to rules is indistinguishable from a broken one. This is the “fail loud with a named cause” capability, owned here because the decider is the subject.
  Done when: every decider call returns `{verdict, source: model|rules, cause}`; `sampo doctor` reports fallback-rate per slot.

- **Define the decider’s serving contract: pinning, failover, GPU-sharing, cold-start** (FEATURE) — value 5 — effort L — risk med — category: serving/performance
  Why: “How it is served on this box” is asked but only lightly covered. The box runs Ollama, the moons funnel, exams, and a 2.4 GB state — the decider must share the GPU without starving the funnel (T-3252 CPU/cap concern) and must be a pinned, restartable artifact.
  Done when: the decider is three pinned files (weights, embeddings, stack) verified at session start; it yields the GPU to the funnel on a measured signal; cold-start is under a budget.

- **Add a per-slot statistical floor + calibrated abstain curve to the capability spec** (FEATURE) — value 4 — effort M — risk low — category: measurement
  Why: “How it is measured” needs a floor below which a slot abstains rather than guesses. The coverage-by-grid rule demands each cell be grounded; a slot with no measured floor is a templated cell.
  Done when: each slot publishes coverage-vs-accuracy, and refuses to vote below its floor, printing the abstain reason.

- **Build the human decider surface: one line in `sampo status`, a veto per class, an “I meant X not Y” propagate** (FEATURE) — value 4 — effort M — risk low — category: ui/simplicity
  Why: The user repeatedly pushes back on verbosity and on doing things by hand. A decider the user can’t *feel* (see the verdict, veto a class, correct a phrase in one keystroke) will be ignored. “Thin” ui and simplicity cells.
  Done when: `sampo status` shows the last decider verdict + source + abstain in one line; `sampo decide veto <class>` and a one-keystroke correction both propagate.

- **Make “does the decider beat plain” a permanent, falsifiable, nightly claim** (FEATURE) — value 5 — effort M — risk med — category: measurement
  Why: Standing rule: a capability whose free arm beats the session arm is a top gap. The decider must carry a live, retestable claim per slot or it can’t be retired or trusted. T-1231 (Foreman beats Claude) is the template.
  Done when: nightly, each adopted slot is re-run against its zero-model baseline on a held-out slice and the pass/fail is printed with a confidence interval.

- **Prove genericity with a redaction + leak scan on every training artefact, run leave-one-project-out** (FEATURE) — value 5 — effort M — risk low — category: privacy/genericity
  Why: “Generic” is the core ask; a leak of one project’s brief text into another is the exact failure it must avoid. No idea owns the *scan* of the built model, not just the rows.
  Done when: the build runs a redaction pass + a planted-canary leak probe; leave-one-project-out scores are published per slot.

- **Compile the decider into a readable, versioned rules file — a rulebook, not a black box** (wild, FEATURE) — value 4 — effort L — risk med — category: delight/transparency
  Why: Wild, but directly answers “what it is trained on / how it’s measured” for a user who distrusts opacity. The user’s own words lean toward receipts and plain words. A trained head that can also *print* the decision rule it used is the delight + trust move.
  Done when: `sampo decide explain TASK` renders the top contributing briefs and the rule, and a cold child can predict the verdict from it.

- **Federate only weights + regret, never text, across the user’s own machines, with a per-project consent gate** (wild, FEATURE) — value 4 — effort L — risk med — category: privacy/scale
  Why: “Generic across every project” + the steer to “manage across sessions/machines… even without direct access.” Sharing raw briefs breaks privacy; sharing only calibrated weights + regret signals is the genericity without the leak.
  Done when: two machines train, exchange only weight deltas + regret counters, and a text-leak canary fails closed.

- **Give the decider an orchestrator with specialist sub-agents, run unattended and checked** (wild, FEATURE) — value 4 — effort L — risk med — category: agents
  Why: The “agents of agents” lens and the standing self-advancing-tower rule: a single head can’t own training, serving, measurement and the improvement loop. An orchestrator with specialist sub-agents (trainer, server, examiner, regret-miner) run unattended and cold-read is the complete version.
  Done when: an overnight lane runs the whole train→serve→bench→retrain cycle unattended, each step cold-read, and files its regret.

- **Make the decider a “next user,” not a helper: it drafts the user’s next steer and answers routine asks** (wild, FEATURE) — value 3 — effort L — risk high — category: delight/anticipation
  Why: The pack’s own anticipation work (predict next ask, draft the pushback) is the decider taken to its logical end. Wild, and the user would love it if it’s honest; high risk because a wrong “user twin” is worse than no model.
  Done when: the decider drafts a steer in the user’s voice, tagged “predicted, not asked,” and is scored by edit distance to what the user actually typed.

- **Do less: ship the data export, the kNN oracle, the abstain contract and the per-project consent gate first; defer all weights** (CLEAN) — value 4 — effort M — risk low — category: simplicity
  Why: The pack’s strongest evidence is the user’s bias toward measured, provable, local, and “do less.” A zero-model kNN decider with a real consent gate and a replayable ledger answers most of the ask before any training, and is the honest baseline every model must beat.
  Done when: `sampo decide` works on kNN-over-closed-briefs with a consent gate and a per-slot abstain, and `sampo doctor` proves it beats the rules-only arm.

- **Make `sampo decide` one verb that answers in one typed sentence or abstains — collapse the slot zoo** (CLEAN) — value 4 — effort S — risk low — category: simplicity/ux
  Why: “Simplicity” is a thin cell and the user’s own words are anti-zoo. A generic decider should present as one decision surface; the slots are an internal detail.
  Done when: the only decider verb is `sampo decide`; it returns one typed sentence or a named abstain; slots are not user-facing.

Next question: what is the *smallest* project (fewest briefs) on this box where a shared generic head must not abstain — that floor decides whether per-project adapters are even worth it.
Next question: which single decider slot, if it abstains or silently falls back, has *never* left a ledger trace — that names the measurement gap no retrain can fix until the replay line lands.
