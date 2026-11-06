# Brainstorm — lens: approaches

Lens: approaches (round 2). Distinct ways to get "Sampo's own generic trained model", each with its trade-off. I skip anything already on the list and focus on ways to solve the request differently, including doing less.

- **Replace the model with a mined rule table first** — FEATURE — value 4 — effort S — risk low — category: decider
  Why: bench shows the best 4B decider beats majority only on intake type (0.73 vs 0.595) and nothing beats majority on tier (0.58). The signal may be shallow enough that a decision tree over cheap features (files touched, verbs, stack, prior-outcome counts) matches it. Trade-off: it caps at what features capture, but it is readable, instant, needs no GPU, and sets the floor any model must beat.
  Done when: `sampo model bench` prints the tree's score beside majority and the 4B decider on the same 200 held-out tasks, with the tree's rules listed in plain text.

- **Use few-shot retrieval on the existing 27B instead of training** — FEATURE — value 4 — effort S — risk low — category: prompting
  Why: the 27B endpoint is already served, and 4,078 briefs with bge-m3 recall@1 0.85 make "the five closest closed briefs and their outcomes" a ready in-context prompt. Trade-off: it costs latency and 2 slots, but it adapts the moment a project adds a brief, with no retraining cycle.
  Done when: decide() with retrieved neighbours beats the zero-shot 27B on the held-out project split, reported per slot.

- **Train only the embedder, and let everything else be lookups** — FEATURE — value 4 — effort M — risk low — category: embeddings
  Why: recall@1 of 0.85 title-to-brief is the strongest signal measured; assumption: contrastive tuning on brief to lesson and brief to later-fix pairs lifts cross-project recall. Trade-off: it gives one small artifact for every slot, but it can't generate or decide on its own.
  Done when: leave-one-project-out recall of the tuned embedder beats stock bge-m3 on at least 3 held-out projects.

- **Do less: ship a data export and a bench, defer all training** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: nothing yet beats majority on tier, so training now risks adopting noise. The reusable asset is the cleaned, name-stripped, provenance-tagged table plus a leave-one-project-out harness. Trade-off: no model for a while, but each Rune generation can drop a model in.
  Done when: `sampo model export` writes the table with a manifest, and the bench runs a trivial baseline end to end.

- **Rent the label from the outcome, not the human: self-supervised "next ledger event"** — FEATURE — value 3 — effort M — risk med — category: pretraining
  Why: 149,606 ledger lines are plentiful, while labelled decisions are scarce. A small model that predicts the next event gives representations for all heads. Assumption: ledger text is regular enough to learn from. Trade-off: it uses more data but leaves the downstream gain unproven.
  Done when: heads on its representations beat heads on bge-m3 for one slot on held-out projects.

- **Wild: make the 27B the teacher, and distil its retrieval-augmented answers into a 0.6B student** — FEATURE — value 4 — effort M — risk med — category: distillation
  Why: training on Claude's text is off limits, but the local 27B's outputs are safe. Rather than learning from sparse human labels, the student copies a stronger local model that already has retrieval. Trade-off: the ceiling is the teacher, and its errors are inherited. (wild)
  Done when: the student matches the teacher's held-out accuracy within 2 points at under a tenth of the latency.

- **Wild: let projects vote — a committee of per-project tiny models, weighted by similarity** — FEATURE — value 3 — effort M — risk med — category: ensemble
  Why: this fits the sensitivity constraint, since a sensitive project's model never merges its data into others. Trade-off: it costs inference across many members, but it has no shared-corpus leakage and exclusion is just deleting a member. (wild)
  Done when: removing one project's member changes no other member's weights, and the committee's held-out score is reported.

- **Wild: no model, a "decision cache" with Bayesian priors from similar briefs** — FEATURE — value 3 — effort S — risk low — category: statistics
  Why: with 4,078 briefs, per-stack and per-verb outcome rates give calibrated priors, and the prior itself may be the whole answer for tier. (wild)
  Done when: the cache's log-loss on held-out tasks is no worse than the 4B decider's.

- **Pick the training target by measured headroom** — CLEAN — value 4 — effort S — risk low — category: prioritisation
  Why: the pack shows slots with very different headroom (loops cause 4 of 10 Smith deaths; tier has none). Compute for each slot the gap between its best baseline and an oracle, then train only where the gap is large. Trade-off: it feels unambitious, but it avoids spending the GPU on tier.
  Done when: a table ranks the slots by headroom, and the first model targets the top one.

- **Use an existing small instruct model with a constrained-decoding grammar** — PERFORMANCE — value 3 — effort S — risk low — category: serving
  Why: many "decisions" are typed enums. Forcing valid output on qwen3.5:4b or gemma4 e4b may fix malformed answers without any weights change. Assumption: part of the weak scores is format failure, not judgment. Trade-off: it does nothing for judgment.
  Done when: the invalid-output rate on the bench drops to 0 and accuracy is re-measured.

- **Train on the audit lenses and lessons, not just outcomes** — FEATURE — value 3 — effort M — risk low — category: data
  Why: briefs carry lessons and audit lenses, which are richer supervision than done/blocked. Trade-off: the text is dense and project-flavoured, so name stripping matters more.
  Done when: a lesson-recall head scores above a keyword baseline on held-out projects.

Next question: for each slot, what is the gap between the best non-learned baseline (rules, priors, retrieval) and an oracle, and is it big enough to justify any training at all?

Next question: if the user's accept/reject history is the real label, how many such labelled decisions exist per project, and is that enough to personalise anything?
