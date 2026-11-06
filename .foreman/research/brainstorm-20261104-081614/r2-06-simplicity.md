# Brainstorm — lens: simplicity

- **Ship one model, one table, one verb** — FEATURE — value 5 — effort M — risk low — category: scope
  Why: the pack lists ~130 ideas (heads, LoRAs, twins, adversaries, registries). Assumption: the first win is one frozen-embedding head family over a single flat table, adopted per call site. Everything else waits for it to beat majority.
  Done when: `sampo model train` and `sampo model bench` run on one exported table and print one scorecard with leave-one-project-out numbers.

- **Delete every slot where the model doesn't beat majority** — CLEAN — value 4 — effort S — risk low — category: subtraction
  Why: the bench shows nothing beats majority on tier (0.58) and intake type is only 0.73 vs 0.595. A model that doesn't lead shouldn't be on the path.
  Done when: each call site either lists a bench margin over its baseline or is switched to the rule path, and `sampo doctor` flags any adopted slot without a margin.

- **Make kNN over closed briefs the default decider** — FEATURE — value 5 — effort S — risk low — category: baseline
  Why: bge-m3 title-to-brief recall@1 is 0.85, so retrieval already works and needs no training, GPU time or weights. Assumption: "briefs like this one, and how they ended" answers intake, tier and verify suggestions as well as a trained head.
  Done when: decide() returns the nearest closed briefs and their outcomes, and the bench compares it with the 4B decider on the 200 held-out tasks.

- **Use one adoption rule for all slots** — CLEAN — value 4 — effort S — risk low — category: governance
  Why: the ideas repeat the same gate (registry, champion/challenger, adoption card, abstain, rollback) under different names. Assumption: one rule covers all of them: a model is used only if it beats its baseline on held-out projects, otherwise the old path runs.
  Done when: a single function takes a slot name and returns "model" or "fallback", and every call site uses it.

- **Keep one training export with ids and names stripped** — SECURITY — value 4 — effort S — risk low — category: data
  Why: exclusion flags, provenance tags, redaction, null-tolerance and real-path resolution were all raised separately (T-2967 shows the real-path bug). One exporter fixes them in one place.
  Done when: a test shows the export refuses an excluded project, resolves symlinked homes, tolerates null fields, and tags every row's source.

- **Train on outcomes only, never on prose** — SECURITY — value 4 — effort S — risk low — category: data
  Why: Claude's text can't be trained on under Anthropic's terms, and ledger text is an injection channel. Features that are only outcomes, exit codes and embeddings avoid both problems. Assumption: that loses little signal for the tasks that matter.
  Done when: the exporter's schema lists only fields from the outcome, evidence and revert records, and a test rejects any free-text field from Claude sessions.

- **Replace the per-lens model zoo with one embedding plus tiny heads** — CLEAN — value 4 — effort M — risk low — category: architecture
  Why: the pack proposes LoRAs, a Ward classifier, a loop predictor and a close verifier. They can all be logistic heads on bge-m3 plus a few numeric features, each trainable in seconds on CPU and kept as a small file.
  Done when: five heads train from one command in under a minute without the GPU, and each reports its own leave-one-project-out result.

- **Let a rule beat a model on loops** — FEATURE — value 3 — effort S — risk low — category: Smith
  Why: loops are the main way Smith runs end (4 of 10), and T-2966 already breaks them on the third identical action. A repeat-count rule on the journal prefix may catch them earlier than any trained detector.
  Done when: a replay over the 74 journals shows the rule's earliest catch step and its false positives, and a trained detector is built only if it catches earlier.

- **Put the model's state on one status line** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: showing per-slot models, bench numbers and abstain reasons is a screen's worth of UI. A single `sampo doctor` line ("model: 3 slots on, 2 fallback, last trained gen N") shows what matters.
  Done when: `sampo doctor` prints that line and names any slot whose card is stale.

- **Retrain by a content hash, not a schedule** — PERFORMANCE — value 3 — effort S — risk low — category: Rune
  Why: nightly retrains, idle-GPU schedulers and resumable jobs add moving parts. Retraining only when the export's hash changes, at the start of a Rune generation, covers the stated need.
  Done when: running the retrain twice on unchanged data does nothing the second time, and a new closed brief triggers it.

- **Wild: Make the model a plain file of rules you can read** — FEATURE — value 4 — effort M — risk med — category: interpretability
  Why: wild. Fit a small decision tree on the outcome table and write it out as `if verify command missing and tier S then ...`. Anyone can read, edit and commit it, and no weights are involved.
  Done when: the exported file has under 50 readable rules, and a human edit to one changes decide() output in a test.

- **Wild: Use the user's own undo as the only label** — FEATURE — value 4 — effort M — risk med — category: labels
  Why: wild. Reverts, later fixes and rejected moons are the user's judgments that nobody had to write. Assumption: they are a cleaner label than green tests, so one signal ("was this undone?") could train every head.
  Done when: one target column, derived from revert and later-fix records, is used by at least three heads, and the bench reports each against its old label.

- **Wild: Ship the baseline as a zero-model mode** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: wild. A switch `models: off` runs Sampo on rules and retrieval only. It proves what the models add, and it is the answer for sensitive projects.
  Done when: the setting disables every model call, the test suite passes with it, and the bench prints the gap against models-on.

Next question: Of the ~130 ideas, which five have a ledger incident or a bench margin to justify them, and what does leave-one-project-out kNN score on those same decisions before any training?
