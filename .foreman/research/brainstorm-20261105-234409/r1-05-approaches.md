# Brainstorm — lens: approaches

- **Start with a zero-weight retrieval oracle, not a trained head** — APPROACH (FEATURE) — value 5 — effort S — risk low — category: training
  Why: The 2,900 closed briefs and the "briefs like this one" ask mean the strongest cheap first move is bge-m3 + a small linear head per decision, gated by leave-one-project-out, before any LoRA. It is fully testable, reversible, and the baseline every later approach must beat. Done when: a single `sampo decide --oracle <brief>` returns the top-3 similar closed briefs with a calibrated abstain probability that beats majority on the held-out split.

- **Distil the 27B only on its verified, green-test runs; keep every loop as a negative** — APPROACH (FEATURE) — value 5 — effort M — risk med — category: training
  Why: T-2966 proves small models loop. A Smith actor distilled from frontier runs whose closes held (tests green, close survived) with loop-runs as rejection negatives directly attacks the biggest observed failure. Trade-off: slow, GPU-bound; do it in idle windows that yield to the moons funnel. Done when: a 4B actor closes s0-001 train scenarios at a loop-rate at least 3× lower than the 4B acting alone, measured on the same split.

- **One shared embedding plus tiny frozen-embedding heads per slot, instead of a model zoo** — APPROACH (CLEAN) — value 4 — effort M — risk low — category: architecture
  Why: The pack already lists many per-slot models (decider, loop-predictor, close-verifier, Ward). One bge-m3 embedding reused across heads cuts VRAM and retraining, and makes cross-project adapters trivial to stack. Trade-off: shares the embedder's blind spots. Done when: every decision slot reads one embedding vector and each head is a ≤4B LoRA or linear layer on it.

- **kNN-over-closed-briefs as the shipping default decider; models are opt-in** — APPROACH (FEATURE) — value 4 — effort S — risk low — category: baseline
  Why: The standing rule says a capability is a top gap when its free arm beats the session arm. A retrieval-only decider is the free arm; it needs no training, no GPU, and is honest for projects with <20 briefs (where it should abstain). Trade-off: ceiling is limited to "similar past brief." Done when: `sampo decide` returns a retrieval verdict with a coverage-vs-accuracy curve, and abstains below the measured floor.

- **Retraining keyed on a content hash of the outcome lake, not a schedule** — APPROACH (PERFORMANCE) — value 4 — effort M — risk low — category: ops
  Why: "How it improves every Rune generation" implies periodic retrain, but time-based retrain wastes GPU and can regress. Hash-keyed retrain means the model changes exactly when new labelled outcomes arrive, and never otherwise. Trade-off: needs a stable, deduped, time-split lake first. Done when: `sampo model retrain` is a no-op (with a log line) when the outcome-lake hash is unchanged, and re-benches when it changes.

- **Champion/challenger registry with shadow mode and one-command rollback per slot** — APPROACH (FEATURE) — value 4 — effort M — risk med — category: governance
  Why: Adoption is the hard part; a registry that shadows a challenger beside the champion and rolls back per slot protects against silent regression. Trade-off: doubles the serving cost per slot during shadow. Done when: promoting a model to a slot is one command, and reverting is one command that restores the prior champion's weights and bench.

- **Do less: ship the data export, the kNN oracle, and the leave-one-project-out bench; defer all training** — APPROACH (CLEAN) — value 4 — effort S — risk low — category: scope
  Why: The standing lean rule says growth without a measurement waits. A provenance-tagged, name-stripped export plus a retrieval oracle and a real holdout bench is the minimum that makes every later idea falsifiable. Trade-off: no frontier-grade performance yet. Done when: `sampo model export` emits a flat, redacted, time-split table and `sampo model bench` reports leave-one-project-out accuracy with no trained weights present.

- **Constrained-decoding grammar for every typed decision, with bounded repair** — APPROACH (FEATURE) — value 4 — effort M — risk low — category: reliability
  Why: A decider that must output a brief-accept, escalate or abstain is best served by a grammar that makes invalid output unrepresentable, plus a bounded repair loop. This is the cheap way to make a small model trustworthy without enlarging it. Trade-off: grammar must cover the real decision space. Done when: 10,000 sampled decisions parse on the first pass or repair within two tries, and zero malformed decisions reach a session path.

- **Per-project LoRA adapter over one shared generic base, local only** — APPROACH (FEATURE) — value 4 — effort L — risk med — category: genericity
  Why: "Generic across every project built with Sampo" is the core ask. A shared base plus a thin per-project adapter gives cross-project generalisation with a small, local, reversible per-project layer that the trainer can enforce a consent flag on. Trade-off: adapter sprawl and cross-project leakage risk. Done when: two projects share the base, each trains a ≤0.5B adapter locally, and leave-one-project-out shows the adapter improves its own project without the other's data.

- **Distil a decision-maker from the *audit lenses and lessons*, not just outcomes** — APPROACH (FEATURE) — value 4 — effort M — risk med — category: training
  Why: Training on green/red outcomes alone misses the *why*. The pack has cold reads, lessons (T-0217) and audit findings as rich labels. A decider trained on lens verdicts learns the user's actual reasoning, not just the result. Trade-off: noisier labels. Done when: a head trained on lesson+outcome pairs scores higher on the held-out split than the outcome-only head on the same briefs.

- **Pairwise approach-chooser: a small model that ranks the two candidate plans, trained on which one the user accepted** — APPROACH (FEATURE) — value 4 — effort M — risk med — category: training
  Why: The "Kev-style decider" often isn't a binary, it's a pick-between-options. Training a pairwise ranker on the user's accept/reject history (already an idea to mine) directly targets the decision the user actually makes. Trade-off: needs paired options in the lake. Done when: given two brief options for the same gap, the model's pick matches the user's historical choice above chance on the held-out pairs.

- **wild — Replay the user's full accept/reject history as the training signal, never hand-label** — APPROACH (FEATURE) — value 5 — effort M — risk med — category: training
  Why: The strongest label the user has already produced is their own behaviour: what they accepted, reverted, and re-asked. A self-supervised "did the user keep this?" signal needs no annotation, scales with use, and is honest about what the user values. Trade-off: biased toward the user's own project. Done when: the decider's predictions correlate with the user's later keep/revert at least as well as a random model, on a held-out month.

- **wild — Run a "no-model" zero-model mode as a permanent arm, so every model must beat plain retrieval** — APPROACH (CLEAN) — value 5 — effort S — risk low — category: governance
  Why: The lean and free-arm rules make a standing zero-model arm the honest control. If a model slot can't beat the retrieval/baseline arm on the same held-out briefs, it should be deleted. Trade-off: some tasks need a model. Done when: `sampo model report` shows each slot's score beside the zero-model arm, and any slot below the arm is flagged for retirement.

- **wild — Federate only weights, never text, across the user's own machines, with a consent gate per project** — APPROACH (FEATURE) — value 4 — effort L — risk high — category: privacy
  Why: "Generic across every project" plus "local-first" means the user wants one model that improves from all their repos without raw code crossing machines or the network. A weight-only federation (e.g., merge LoRA adapters under a consent flag) satisfies both. Trade-off: complex, and leakage is hard to prove absent. Done when: a model trained on machine A improves a task on machine B, and the pack proves no raw brief text left either machine's storage.

- **wild — Self-test the corpus with a poisoned-row tripwire before any head is trained or adopted** — APPROACH (SECURITY) — value 4 — effort S — risk low — category: security
  Why: A decider trained on brief text is a taint surface: a brief containing instructions could steer the model. Planting known poisoned rows and probing every trained artifact for them is the cheap, falsifiable check that the lake is clean. Trade-off: not exhaustive. Done when: a seeded poisoned row is detected and rejected by the pre-train scan, and a planted prompt in a test brief does not change the model's verdict on a held-out brief.

Next question: What is the single decision slot with the largest measured gap between its current model and a human-labelled ceiling, so training can start there rather than everywhere at once?
Next question: For a project with fewer than 20 briefs, what exactly does the model return, and at what coverage floor must it refuse to answer instead of guessing?
