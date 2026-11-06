# Brainstorm — lens: simplicity

- **Cut the decider to one verb that answers in one typed line** — CLEAN — value 5 — effort M — risk low — model
  Why: the pack shows a decider split across decide(), slots, adapters, registries, and a “show which slots use a model” UI; the user’s own steers push toward “still get done… quick,” not a dashboard. One `sampo decide <id>` returning either a single typed sentence or an abstain with a named cause removes most surface area; a dashboard earns nothing until the line is wrong.
  Done when: `sampo decide T-1234` prints one line (decision or abstain+cause) and no secondary pane is required to act on it; a grep of the CLI surface shows the old slot verbs gone or aliased to this one.

- **Make “no model” the default arm and every model must beat it per slot** — FEATURE — value 5 — effort M — risk med — model
  Why: earlier ideas already propose a kNN baseline and a zero-model mode; the simplicity win is inverting the default so the model is opt-in and a permanent control. This directly answers the earlier left question (“which five have a ledger incident to justify them”) with a falsifiable gate and keeps the cost/quality steers honest.
  Done when: on a fresh project, zero model calls occur; each adopted slot stores a margin vs the kNN/free arm and a slot is auto-demoted when it stops beating it on holdout.

- **One label, one command: the user’s undo is the only training signal** — CLEAN — value 4 — effort M — risk med — training
  Why: the pack’s 2,900 closed briefs plus the user’s own undos give a self-supervised label without a hand-labeling pipeline, T-0035 eval capture, or a per-slot labeler. Dropping multi-label schemes keeps the pipeline one file and one idempotent `sampo decide train`.
  Done when: `sampo decide train` runs from a content hash of the outcome lake using only undo/hold outcomes; no separate labeling task or UI exists.

- **One retrain is idempotent, resumable and VRAM-fenced** — FEATURE — value 4 — effort M — risk med — training
  Why: the GPU is shared with the moons funnel and exams (left question: “what does the model path do when the GPU is busy?”). A single resumable job that yields to Ollama and resumes by checkpoint makes training a background chore, not a mode the user babysits; this is the least-effort path to “how it is served on this box.”
  Done when: killing a retrain and re-running it resumes from the last checkpoint; a concurrent funnel run is not evicted, and the job logs its slot count.

- **Serve the decider as three pinned files with a canary at session start** — PERFORMANCE — value 4 — effort M — risk low — serving
  Why: the pack asks how it is “served on this box” and the earlier ideas keep weights/embeddings/serving as separate registries. Simplicity says one artifact: a weights file, an embeddings index, and a version line, all content-hashed and verified by a free canary so a stale or busy endpoint degrades to rules without the user noticing.
  Done when: `sampo doctor` prints one line naming the three files and their hashes, and a canary call confirms the endpoint; a missing or busy endpoint falls back to the rules arm automatically.

- **One abstain, one reason, one veto — and nothing else the model can say** — FEATURE — value 4 — effort S — risk low — model
  Why: the user’s words show a repeated need for trust and control (“show which slots use a model,” “a user veto,” “what the model changed in plain words”). Collapsing the model’s output space to decide/abstain/reason/veto makes every model interaction auditable and cheap to render, and removes the long tail of free-form model text that invites gaming.
  Done when: no model slot can emit text outside the four typed outcomes; the pane shows the abstain reason and a one-key veto, and a test proves a free-form response is rejected.

- **Do less: ship the export, the kNN arm, and the leave-one-project-out bench; defer all training** — CLEAN — value 5 — effort S — risk low — model
  Why: the strongest evidence in the pack is the open work and steers around cost, quickness, and genericity; a full trained decider is the riskiest, least-quick path. Shipping a redaction-safe export, a retrieval arm, and a whole-project holdout proves the value and the generalization claim before any weight is trained, and gives every later model a baseline to beat.
  Done when: `sampo decide export`, the kNN arm, and a leave-one-project-out bench all run with zero GPU and zero trained head, and the bench is the first thing `sampo decide` prints.

- **Wild: make the decider a readable rulebook, not a black box** — FEATURE — value 4 — effort M — risk med — model
  Why: the user’s standing rules and cold-read culture favour legibility over ambition; a decider that compiles its top rules into a short file the user can read and edit beats an opaque head for trust, and gives the “show which slots use a model” requirement a concrete surface. It is wild because it treats explainability as the primary output, not a debug view.
  Done when: `sampo decide rules` prints a ≤30-line rulebook covering the live slots, and editing a rule changes the next decision without a retrain.

- **Wild: let the decider refuse the work, and pay it for saying “no”** — FEATURE — value 4 — effort M — risk high — model
  Why: the user repeatedly pushes back on over-reach and cost; a model that can abstain or refuse with a reason is the simplest trust mechanism and the one nobody asked for. It is wild because it inverts the usual “model does more” pressure into “model may do less,” and it turns a refusal into a first-class receipt that the drive can park the task on.
  Done when: a slot can return refuse+reason, the task is parked with a typed wait, and the morning card shows the refusal; a test proves a refusal does not consume the push grant.

- **Wild: run a nightly “model autopsy” that replays silent fallbacks and files the regrets** — FEATURE — value 4 — effort M — risk med — model
  Why: the pack’s ledgers and the user’s “model saved you X” / “wrong calls” interests suggest the highest-value use of a decider is measuring its own mistakes, not making more decisions. A single overnight replay of the last 7 days against the rules arm is cheap, local, and answers the left questions about silent errors and coverage without a new UI.
  Done when: a nightly job writes a one-file report of each fallback where the model and rules disagreed, with the file set and outcome, and a task is filed when a slot’s regret ratio crosses a threshold.

- **One “off” switch that really turns the model off per project** — FEATURE — value 5 — effort S — risk low — model
  Why: the user’s words include explicit trust and veto needs and a steer to “never block on the user for a question about rules”; a hard per-project no-model flag is the simplest guarantee that the model cannot surprise them, and it is the one control a user who never read MASTER.md can find and trust.
  Done when: `sampo decide off <project>` makes all model slots return the rules arm, `sampo doctor` shows the flag, and a test proves no model call is made on a project with the flag set.
