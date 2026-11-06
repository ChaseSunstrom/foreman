# Brainstorm — lens: approaches

- **Ship a kNN-over-closed-briefs baseline first** — FEATURE — value 4 — effort S — risk low — category: baseline
  Why: the 4B decider scores 0.73 on intake type against a 0.595 majority, and bge-m3 title-to-brief recall@1 is 0.85. Nothing beats majority on tier. Retrieval needs no training and works unchanged on any new Sampo project. It is the floor any trained model must clear.
  Done when: `decide()` can run in retrieval mode, and the bench prints its score beside the heads and the LLM on the same 200 held-out tasks.

- **Train frozen-embedding heads per decision type** — FEATURE — value 4 — effort M — risk low — category: classifier
  Why: bge-m3 is installed and the Jeff stack exists. A head costs seconds to retrain, so it fits "every Rune generation retrains and re-benches". Trade-off: it cannot generate, so it only covers typed decisions (intake, route, risk category, tier).
  Done when: heads for 3 or more decision types retrain in under 5 minutes, and a leave-one-project-out table shows each beating majority or being marked not adopted.

- **Prove genericity with leave-one-project-out and a redaction pass** — FEATURE — value 5 — effort M — risk low — category: eval
  Why: the user asked for a model that works beyond the Sampo repo. Sampo is 1,767 of 4,078 briefs and volt is 773, so a random split would hide Sampo-only overfitting. Strip repo names and paths before training, and honour a per-project `exclude_from_training` flag.
  Done when: the scorecard reports held-out-project scores for volt, the git tool and the voice codebase, and a test fails if an excluded project's text reaches a training file.

- **Train a close-holds verifier from outcomes** — FEATURE — value 5 — effort M — risk med — category: verifier
  Why: labels are Sampo's own: done, then no later fix, versus blocked or reverted, plus evidence exit codes. The Smith uplift runs show false-done closes (1/8 fixed with 5 closed). This avoids Claude-text training restrictions. Trade-off: labels are noisy, since later fixes may be unrelated.
  Done when: on held-out briefs the verifier's AUC on "closed and later reverted or fixed" beats a rule using only exit codes, and Smith's close step can use it as a veto.

- **Distil a Smith actor from green-only local runs** — FEATURE — value 4 — effort L — risk med — category: distillation
  Why: T-2971 already proposes this, and 74 journals exist. Keep only runs whose tests passed and whose closes held. A LoRA on the 12B or 4B targets the loop failures behind 4 of 10 deaths. Trade-off: 74 journals is thin, so it needs the generator step.
  Done when: the LoRA beats its base on Louhi's held-out split (fixed count and loop deaths), and runs offline.

- **Run champion/challenger shadow mode through existing decide() paths** — FEATURE — value 4 — effort S — risk low — category: adoption
  Why: the project rule is to adopt a model only where the bench shows it leads. A challenger logs its answer beside the incumbent's without acting, and the ledger records the agreement. This needs no new verb (answering the earlier question), because it rides the `decide()` path sessions already call.
  Done when: after N real decisions the ledger has a per-type agreement and later-outcome table, and a challenger is promoted only if the gate passes.

- **Pick one multi-task LoRA or many small heads with a controlled comparison** — CLEAN — value 3 — effort M — risk low — category: architecture
  Why: assumption: a single 4B with task prefixes covers intake, tier, route, next-request and risk, and serves from one resident model on a 16 GB GPU. Many heads are cheaper and independently adoptable. Measure both before committing.
  Done when: a table compares the two on the same split for accuracy, retrain time and VRAM, with a recorded decide() pick.

- **Train a pairwise approach-chooser from brief options** — FEATURE — value 3 — effort M — risk low — category: ranking
  Why: each brief stores several approach options with the chosen one, which gives free preference pairs. This is a different target from classification, and it feeds planning (`--planner`).
  Done when: the ranker picks the recorded chosen approach more often than a length or position baseline on held-out projects.

- **Stack per-project adapters on a generic base, trained locally** — SECURITY — value 4 — effort L — risk med — category: privacy
  Why: the constraint is that a sensitive project's data never leaves the box. The generic base trains on opt-in projects only. Each project's adapter trains on its own ledger and stays under that project's directory.
  Done when: removing a project's directory removes its adapter, and the base's training manifest lists no excluded project.

- **Keep the Ward rule-based and let a model only tighten it** — SECURITY — value 4 — effort S — risk low — category: Ward
  Why: assumption: Ward rules and local judges read attacker-influenced text. A learned verdict that can loosen refusals is an attack surface. A model may flag extra risk, but it can never turn a refusal into an allow.
  Done when: a test feeds adversarial text to the model path and the Ward verdict never gets looser than rules alone.

- **Wild: build an overnight Smith dojo with rejection sampling** — FEATURE — value 5 — effort L — risk med — category: self-play — wild
  Why: assumption: Louhi's seeded bug generators can mutate any Sampo project's repo on idle GPU. Smith attempts them, tests grade them, and only green and held runs enter next generation's training set. No Claude text is involved, and the data grows without limit.
  Done when: one night produces 200 or more graded runs across 3 or more projects, and a generation retrained on them beats the previous one on the held-out exam.

- **Wild: train a ledger-event language model for surprise detection** — FEATURE — value 3 — effort M — risk med — category: anomaly — wild
  Why: 149,606 ledger lines are a sequence corpus. A small next-event model scores each new event, and high surprise flags loops, drift or odd guard refusals before a human sees them.
  Done when: replaying known loop and revert incidents ranks them in the top 5% of surprise on held-out sessions.

- **Wild: merge adapters across projects without sharing data** — FEATURE — value 3 — effort L — risk high — category: merging — wild
  Why: each project's adapter trains locally. Merging weight deltas (TIES or DARE style) yields a generic model from the opted-in set without moving any text. It would also work for other Sampo users later.
  Done when: the merged model matches or beats a pooled-data model on the held-out project scores, and the merge needs no raw text.

- **Wild: mine "regret" labels from later fixes** — FEATURE — value 4 — effort M — risk med — category: labels — wild
  Why: briefs link to later fixes, so each close has a hindsight label such as "this criterion was too weak". Train a criteria-quality scorer on it that warns at planning time.
  Done when: on held-out briefs the scorer's low-quality flags precede later fixes at a rate above a base-rate control.

Next question: which decision types in the ledgers have a label that a later event, such as a revert or a user correction, contradicts, and how often?
Next question: does the 27B's 2-session limit make nightly data generation, retraining and benchmarking compete for the same endpoint, and what does the schedule need?
