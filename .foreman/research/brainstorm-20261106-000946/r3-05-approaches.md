# Brainstorm — lens: approaches

- **Ship a "Decision Log First" sprint** — FEATURE — value 5 — effort S — risk low — category: decider
  Why: The 2,900 closed briefs are the raw material. Before training a single weight, `sampo decide` should be a pure, versioned, and auditable log of every decision Sampo makes (accept, reject, defer, abstain) with a reason. This turns the current implicit logic into explicit, trainable data and gives the user a "rulebook" to read. The pack's request for "what it is trained on" is answered by making the log *the* training set.
  Done when: `sampo decide log --last 10` prints the last 10 decisions with reasons, and the log file is a valid, append-only JSONL that a trainer can ingest without preprocessing.

- **Build a "kNN Oracle" as the default decider** — FEATURE — value 4 — effort M — risk low — category: decider
  Why: The user asked for a "better Kev-style decider." A kNN over the closed briefs, using bge-m3 embeddings, is the simplest, most transparent, and most "generic" decider. It requires no training, is instantly generic across projects, and provides a baseline that any future trained model must beat. It directly addresses "how it is trained" (it isn't, it's retrieved) and "how it improves" (the corpus grows with every close).
  Done when: `sampo decide` uses the kNN oracle by default, returning the nearest closed brief's decision and a similarity score, with a `--model` flag to opt into a trained head later.

- **Train a "Regret Head" on `samo undo` events** — FEATURE — value 5 — effort M — risk med — category: training
  Why: The user's "own words" show a pattern of undos and "I meant X, not Y." The most valuable training signal is the user's own correction. A tiny head trained *only* on pairs of (decision, user-undo) will learn the user's specific taste and pushback patterns. This is the "improves every Rune generation" loop: every undo becomes a negative example that sharpens the next decision.
  Done when: A `sampo decide train --regret` command runs, a small head is trained on the last 500 undo events, and a `--eval` flag shows its accuracy on held-out undos.

- **Create a "Decision Distillation" pipeline from `fm decide` logs** — FEATURE — value 4 — effort L — risk med — category: training
  Why: The user asked "how it is trained." The existing `fm decide` calls are a free, labeled dataset. A pipeline that extracts these, cleans them, and uses them to fine-tune a small model (e.g., 0.6B) via LoRA is the direct path to a "trained" decider. It reuses existing infrastructure (the "Jeff training stack" mentioned in the user's words) and makes the training process transparent.
  Done when: `sampo decide distill` runs, producing a new LoRA adapter that `sampo decide` can load, with a `--card` flag printing a model card describing the training set and metrics.

- **Implement a "Two-Tier" serving strategy** — PERFORMANCE — value 4 — effort M — risk med — category: serving
  Why: The user asked "how it is served on this box." A 0.6B model for fast, routine decisions and a 27B model for complex, high-stakes ones is the practical answer. This requires a router that classifies the decision's complexity (e.g., by the number of similar briefs or the stakes of the decision) and a local serving stack that can swap models quickly. It directly addresses "served on this box" with a cost-effective, local-first approach.
  Done when: `sampo decide` automatically routes a "simple" decision to the 0.6B model and a "complex" one to the 27B model, with a `--force-model` flag to override, and the serving stack logs which model was used.

- **Build a "Genericity Test" with a "canary project"** — FEATURE — value 5 — effort M — risk low — category: genericity
  Why: The user explicitly asked for a "generic model in the sense that we don't want it to just work on the sampo repo." A "canary project" is a small, synthetic project with its own briefs, undos, and decisions. The decider must be evaluated on this project to prove it isn't overfit to Sampo's specific domain. This is the direct, testable answer to the "generic" requirement.
  Done when: `sampo decide test --canary` runs on a pre-built canary project, reporting the decider's accuracy on that project's held-out decisions, and a `--leak` flag confirms no Sampo-specific data was used.

- **Wire every decider slot to a real session path** — FEATURE — value 5 — effort M — risk low — category: integration
  Why: The user's standing rule is "every capability Genesis builds must be called by a real session path." The decider is currently a standalone concept. It must be integrated into the actual `samo` loop: called at the point of decision (e.g., when a brief is ready to close, or when a task is being deferred), and its verdict must influence the outcome. This is the "improves every Rune generation" part of the request.
  Done when: `samo task close` calls the decider, and if the decider abstains or rejects, the close is blocked with a reason. A `--decide-log` flag shows the decider's input and output for the last close.

- **Build a "Decision Veto" surface for the user** — FEATURE — value 4 — effort S — risk low — category: ui
  Why: The user's "own words" show they push back on decisions. The decider must be overridable. A simple `samo decide veto --id <decision-id>` command that records the user's override as a new training example (regret) is the most direct way to make the decider "improve" from user interaction. It turns every pushback into a training signal.
  Done when: `samo decide veto` is available, and vetoes are logged to the regret dataset. A `samo decide vetoes --last 5` shows the last 5 vetoes with the user's reason.

- **Create a "Decision Replay" tool** — FEATURE — value 4 — effort M — risk low — category: audit
  Why: The user asked "how it is measured." A replay tool that takes a past closed task, re-runs the decider on it with the *current* model and corpus, and compares the verdict to the original decision is the perfect way to measure improvement. It shows whether the decider is getting better or worse over time, and it's a direct answer to "how it improves."
  Done when: `samo decide replay --task <id>` runs, printing the original decision, the current decision, and a diff. A `--all` flag replays the last 100 tasks and prints a summary of agreement rate.

- **Implement a "Decision Confidence" score** — FEATURE — value 3 — effort S — risk low — category: decider
  Why: The user's "own words" show they want to know when Sampo is "guessing." A confidence score (e.g., based on the similarity of the kNN match or the margin of the trained head) is a simple, transparent way to communicate the decider's certainty. It's also a key input for the "Two-Tier" router: low confidence triggers the 27B model.
  Done when: `samo decide` returns a confidence score in [0,1] with every verdict, and a `--low-confidence` flag prints all decisions with confidence < 0.5.

- **Wild: Train a "User Twin" that drafts the next steer** — FEATURE — value 4 — effort L — risk high — category: decider
  Why: The user's "own words" show a pattern of steers and pushbacks. A "User Twin" is a decider that predicts the user's *next* steer or pushback before it's made. It's trained on the sequence of (decision, user-response) pairs. It's "wild" because it's not just deciding *for* the user, but predicting *about* the user. It's the ultimate "improves every Rune generation" loop: the decider learns the user's intent and pre-empts their corrections.
  Done when: `samo decide twin` runs, printing a draft of the user's next likely steer. A `--eval` flag shows its accuracy on held-out steers.

- **Wild: Make the decider a "living rulebook" that the user can edit** — FEATURE — value 5 — effort L — risk med — category: decider
  Why: The user's "own words" show they want to "teach" Sampo. A "living rulebook" is a decider that stores its logic as a set of editable rules (e.g., "if brief type is X and undo rate > Y, then reject"). The user can edit these rules directly, and the decider applies them. It's "wild" because it's not a black-box model, but a transparent, editable policy. It's the most "generic" decider possible: the rules are domain-agnostic.
  Done when: `samo decide rules` prints the current rulebook as a JSON file. The user can edit the file, and `samo decide` uses the new rules. A `samo decide diff` shows the diff between the last two rulebook versions.

- **Wild: Run the decider as an "adversary" in the funnel** — FEATURE — value 3 — effort M — risk high — category: integration
  Why: The user's "own words" show they want the decider to "kill" bad ideas. A "wild" integration is to run the decider as an *adversary* in the moon funnel: it generates "attack" briefs (e.g., "this idea is a duplicate," "this idea is too costly") and the funnel must defend against them. It's "wild" because the decider is not just deciding, but *challenging* the project's own ideas. It's a direct, "improves every Rune generation" loop: the decider learns to find weaknesses in the project's reasoning.
  Done when: `samo decide attack` runs, generating a list of "attack" briefs. A `samo funnel defend` command runs, showing how the funnel responds to the attacks. A `--score` flag prints a score of the funnel's defense.
