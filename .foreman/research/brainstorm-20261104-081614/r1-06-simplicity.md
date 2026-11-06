# Brainstorm — lens: simplicity

- **Ship a nearest-neighbour decider before any training** — FEATURE — value 5 — effort S — risk low — category: decider
  Why: bge-m3 title-to-brief recall@1 is 0.85, and the best trained decider only reached 0.73 on intake type. Closed briefs carry their own labels, so a vote over the k nearest briefs needs no training run.
  Done when: a leave-one-project-out bench prints kNN against majority and the 4B decider for intake type, tier and playbook.

- **Gate every model on a leave-one-project-out bench** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the request requires generality and says to hold out whole projects. Nothing beats majority on tier (0.58) today. One rule keeps the project honest: a model is adopted only where it beats majority and the incumbent on projects it never saw.
  Done when: `sampo model bench` holds out each of the 13 projects in turn and prints a per-project table. A model that loses anywhere is not adopted there.

- **Export one flat training table, with project ids and names stripped** — CLEAN — value 4 — effort S — risk low — category: data
  Why: the 4,078 briefs and 149k ledger lines sit in per-project files. One export (brief text, labels, outcome, project hash) feeds every later model. A per-project `exclude` flag keeps sensitive data on the machine.
  Done when: the export is deterministic. A grep for repo-specific names in it finds none, and an excluded project contributes zero rows.

- **Train tiny heads on one shared embedding** — FEATURE — value 4 — effort M — risk low — category: models
  Why: bge-m3 is already installed, and logistic-regression heads train in seconds on 4k rows. Intake type, tier, playbook route, risk category and "needs ask" can share one embedding call and skip a 4B LLM call each. Assumption: heads match the 4B on intake type.
  Done when: each head's bench score is at least the current decider's, and a session path uses the head with the LLM call removed.

- **Make the model abstain and fall back to today's path** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: decide() already has typed decisions and a Ward. Below a calibrated confidence, the head returns "unsure" and the existing LLM or user path runs. A wrong model then costs nothing it doesn't cost today.
  Done when: on the held-out set, accuracy on answered cases beats the all-cases score, and an unsure case demonstrably takes the old path.

- **Retrain with one idempotent command per Rune generation** — FEATURE — value 4 — effort M — risk low — category: loop
  Why: the request says it improves every generation. `sampo model retrain` exports, fits, benches and swaps only on a win, then writes a scorecard row. The genesis sweep calls it, which meets the standing rule that every capability needs a session path.
  Done when: running it twice on unchanged data gives identical output and no swap. A degraded candidate is refused with the reason logged.

- **Write a model card that `sampo doctor` checks** — CLEAN — value 3 — effort S — risk low — category: provenance
  Why: privacy and generality are constraints. Each model gets a small file listing data fingerprint, projects included, held-out score and date. Doctor flags a model whose data is stale or that includes an excluded project.
  Done when: tampering with the data or the exclude flag makes doctor name the model.

- **Predict "will this brief survive?" from outcomes only** — FEATURE — value 4 — effort M — risk med — category: foresight
  Why: briefs end done, blocked or reverted, and later fixes are recorded. These labels are the safe ones, because they carry none of Claude's text. A head flags likely-reverted briefs at intake. Assumption: the signal beats the base rate.
  Done when: held-out AUC beats the base rate and a flagged brief shows a warning at intake.

- **Replace one moons judge with a head trained on the user's accepts and rejects** — PERFORMANCE — value 3 — effort M — risk med — category: funnel
  Why: the funnel runs judge batches at about 3 minutes each on a 2-slot 27B. The user's own accept and reject history is the label Sampo didn't author, which answers the open question about what kills what a human rejects.
  Done when: the head's kill-stage agreement with human rejects is measured and exceeds the judge's, and the stage's local-model call count drops.

- **Train a stuck-loop detector on the 74 Smith journals first** — FIX — value 3 — effort S — risk low — category: smith
  Why: loops are the main way Smith ends (4 of 10 scenarios), and the breaker is a hand rule. A small classifier over recent actions is far simpler than a LoRA actor and reads only local-model traces. Defer the distilled actor until closes stop being false-done.
  Done when: precision and recall on held-out journals beat the identical-action rule, and the breaker fires earlier on a replayed loop.

- **Wild: make the model a rulebook you can read** — FEATURE — value 4 — effort M — risk low — category: legibility — wild
  Why: assumption: a shallow decision tree over cheap features (files touched, verbs, stack) gets within a few points of the neural head. Printed as markdown, the Ward, cards and the user can all cite its rules, and an audit takes minutes.
  Done when: a generated `RULES.md` reproduces the tree's predictions exactly, and the held-out score is within 3 points of the best head.

- **Wild: commit the project's own weights in `.sampo/model.bin`** — FEATURE — value 3 — effort M — risk med — category: portability — wild
  Why: assumption: a head under 5 MB is small enough to commit. Every clone of a Sampo project then gets a decider tuned to that project, versioned and diffable. A sensitive project simply never exports its file.
  Done when: a fresh clone makes the same decisions as the original machine, and the file stays under the size limit.

- **Wild: train a Ward that learns what this user never accepts** — SECURITY — value 3 — effort M — risk high — category: guard — wild
  Why: the ledger holds guard refusals, asks and answers, and steers. A small head over them proposes tightening only, never loosening. It would be reachable by the same text channel as the other local models, so it can add refusals but never remove one.
  Done when: on held-out refusals it raises the catch rate, no existing rule is removed, and a crafted prompt cannot turn a refusal into an allow.

- **Wild: share weights, never text, across projects** — PRIVACY — value 3 — effort L — risk med — category: federation — wild
  Why: assumption: the heads can train per project and be averaged centrally without any brief leaving the machine. That serves the "generic but private" constraint with no new data movement.
  Done when: a model built this way, scored on a project it never saw, matches the pooled one within a few points. A byte-level scan of the shared files finds no brief text.

Next question: Does the user's accept-and-reject history exist in a form we can label, or is it only inferable from the ledgers?
Next question: Which of the 13 projects is too small or too sensitive to hold out, and does leaving it out make the generality claim meaningless?
