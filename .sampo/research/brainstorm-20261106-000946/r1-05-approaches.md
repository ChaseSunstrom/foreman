# Brainstorm — lens: approaches

- **Ship the kNN-over-closed-briefs oracle as the decider’s default, and make every trained head opt-in** — APPROACH — value 5 — effort S — risk low — category: decider
  Why: the standing rules demand a free-arm baseline and the exam gates adoption; a retrieval oracle over ~2,900 closed briefs (bge-m3 + cosine, no weights on the machine) is the cheapest “better Kev” that the current pack already implies and can run on the box today. Every trained slot must beat it per project or it retires.
  Done when: `sampo decide --slot close-holds` returns a typed answer from retrieval alone on 100 held-out briefs, and its F1 prints beside the rules arm in `sampo exam`.

- **Do less: export the outcome lake, run the leave-one-project-out bench, and defer all training** — APPROACH — value 5 — effort S — risk low — category: data
  Why: the user asked what it is trained on and how it is measured before how; T-0035 (eval capture) and T-2912 (silent-cut) are the blockers. A flat, redacted CSV with provenance tags plus a bench is the minimum artifact that lets any model be scored and lets the user audit before any GPU is spent.
  Done when: `sampo decide export` produces one table; `sampo exam generic` reports per-project F1 with names stripped; no `.bin` weights exist.

- **Pairwise approach-chooser as the first *useful* trained head, from the user’s accept/reject history** — APPROACH — value 4 — effort M — risk med — category: decider
  Why: the decider’s highest-leverage job is picking between two candidate plans (the plan-before-edit loop). The user’s own undo/accept history is a free preference label set, and a tiny head over the shared embedding only needs to rank two items, a far easier and more auditable target than free-form answers.
  Done when: on a held-out project, the chooser beats the current planner’s default pick on 60% of the pairs, with the loss printed in `sampo exam steer`.

- **Train frozen-embedding heads per slot, not a model zoo: one bge-m3, tiny linear heads** — APPROACH — value 4 — effort M — risk med — category: training
  Why: the pack mentions bge-m3 + a trained head and a LoRA option; a single shared embedding with one small head per decision type (close-holds, loop-predict, approach-choose) is cheaper to serve, easier to roll back, and trivially generic across projects, which matches “generic across every project.”
  Done when: `sampo decide train --slot close-holds` updates one head file; `sampo doctor` verifies the embedding digest is unchanged.

- **Use constrained-decoding grammar over an existing 0.6–4B instruct model, no fine-tune** — APPROACH — value 3 — effort S — risk low — category: serving
  Why: the user already runs qwen3.5:4b and gemma4:12b through Ollama; a typed decision (answer / abstain + reason / veto) can be enforced by a grammar so the model never invents output, removing a whole class of training and safety risk while still giving a “smarter Kev” on hard briefs.
  Done when: `sampo ask` returns only the grammar’s three typed forms, and a bench shows zero schema violations over 500 calls.

- **Rehearse a “model-gone” week as a permanent zero-model arm before any adoption** — APPROACH — value 4 — effort S — risk low — category: resilience
  Why: the standing rule that a free arm beating the session arm is a top gap implies the model must always have a rules/retrieval fallback. A permanent no-model mode is the only way to prove the decider isn’t a single point of failure and to measure what the model actually adds.
  Done when: `sampo doctor` reports the zero-model arm’s F1; flipping `SAMPo_MODEL=off` changes no session path except the decide() call.

- **Distil the 27B only on its verified, green-test runs; keep every loop as a negative** — APPROACH — value 4 — effort L — risk med — category: distillation
  Why: T-2966 (loop break) and the uplift exam are the evidence; running Smith on the 27B over Louhi train scenarios and keeping only runs whose tests went green and closes held gives a clean, self-supervised actor dataset with no hand labels.
  Done when: the distilled 4B passes the same Louhi s0-001 split at ≥90% of the 27B’s score with reasoning off, and no loop-run is in the training set.

- **Invert the teacher: let the 0.6–4B student grade the 27B, and keep only where they agree** — APPROACH — value 3 — effort M — risk med — category: distillation
  Why: the user runs both models locally; a cheap disagreement signal between the student and teacher on the same verified runs is a free quality filter that catches teacher errors and reduces the distillation corpus to high-confidence rows, saving VRAM.
  Done when: the distillation pipeline drops rows where the student and 27B disagree, and the final student model’s F1 is reported against the full corpus baseline.

- **Federate only weights, never text, across the user’s own machines, with a consent gate per project** — APPROACH — value 3 — effort L — risk med — category: privacy
  Why: the user’s standing rule is no software installs and local-first; federating the tiny per-project adapters across the user’s own boxes (not the internet) gives cross-project genericity without sharing any repo text, which is the natural next step after “generic across every project.”
  Done when: two machines on the LAN merge adapter weights via `sampo decide federate`, and a leak scan proves no project text left either box.

- **Run the decider in shadow for one full Rune generation before it may vote, gated on a statistical floor** — APPROACH — value 4 — effort M — risk low — category: adoption
  Why: the pack’s exam and outcome rules imply adoption must be measured, not assumed. A shadow period where the model’s verdicts are logged but not used, compared against the rules/retrieval arm, is the cheapest way to prove a slot earns its place before it touches a real close.
  Done when: `sampo decide shadow --slot close-holds` logs one generation’s verdicts; `sampo exam` prints the lift over baseline before the slot is allowed to vote.

- **Hold out whole projects and strip names in the training build, as the genericity proof** — APPROACH — value 5 — effort M — risk low — category: evaluation
  Why: the user explicitly said “we don’t want it to just work on the sampo repo itself”; leave-one-project-out is the only honest test of genericity, and name-stripping is the minimal privacy step that also catches overfitting to Sampo’s own vocabulary.
  Done when: `sampo exam generic` drops one project’s rows, retrains, and reports F1 on that project’s held-out briefs with all names replaced by placeholders.

- **Build a provenance-tagged training lake with exclusion flags, and quarantine any row from tool output** — APPROACH — value 4 — effort M — risk med — category: data
  Why: T-2912 (silent-cut) and the standing rule about untrusted text mean the lake must know where each row came from. Tagging provenance at collection time lets the trainer exclude tool-result and repo-file text, preventing the model from memorizing or leaking code it was only shown as data.
  Done when: every row in the lake has a `source` field; `sampo decide train` refuses rows with `source=tool_result` and prints the exclusion count.

- **Wild — train on regret, not labels: mine later-fix pairs as the negative signal** — APPROACH — value 4 — effort M — risk med — category: training
  Why: the user’s own undo and later-fix history is a natural regret signal that no manual labeling can match; a later fix to a closed brief is a “this close was wrong” label that is free, abundant, and directly tied to the decider’s job of predicting whether a close holds.
  Done when: the close-holds head’s training set includes later-fix pairs as negatives, and its F1 on the held-out project beats the accept/reject-only baseline.

- **Wild — make the decider a readable rulebook, not a black box: compile its decisions into a versioned rules file the user can edit** — APPROACH — value 3 — effort M — risk med — category: trust
  Why: the user’s standing rules are prose that a model can’t audit; a “readable rulebook” is the decider’s decisions compiled into a human-editable file that the model reads at serve time, giving the user a direct veto over the model’s behavior without retraining.
  Done when: `sampo decide rules` prints the current decision rules; editing the file changes the model’s output on the next call without a retrain, and `sampo doctor` verifies the rules file’s hash.

- **Wild — run a “model autopsy” lane overnight: replay every silent-fallback decision from the last 7 days against the rules arm, and file the disagreements** — APPROACH — value 4 — effort M — risk low — category: measurement
  Why: the pack’s question about the slot that has “never left a ledger trace” points at silent fallbacks; an overnight replay that compares the model’s decisions against the rules/retrieval arm on the same inputs is the only way to measure the model’s true contribution and find the decisions it got wrong without a user noticing.
  Done when: `sampo decide autopsy` runs on the last 7 days of ledger rows and files a task for each disagreement where the model and rules arm disagree, with the brief id and the two verdicts.
