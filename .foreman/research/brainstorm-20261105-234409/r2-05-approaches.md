# Brainstorm — lens: approaches

- **Start with a kNN retrieval oracle, not a trained head** — APPROACH — value 5 — effort S — risk low — category: decider
  Why: The ~2,900 closed briefs already carry provenance, outcome and lesson fields (T-0035, T-0217). A bge-m3 kNN over those rows answers "what happened to briefs like this?" today with zero training, and gives the hold-out baseline every later model must beat. This is the "do less" first step the standing rules demand before any weight is grown.
  Done when: `sampo decide` on 20 held-out briefs returns a nearest-3 with a rank that a 4B can act on, and the retrieval-only arm is wired into a real session path.

- **Distil the 27B on verified green runs only, loops as negatives** — APPROACH — value 4 — effort M — risk med — category: decider
  Why: T-2966 shows Smith breaks small models' loops; the fix is a trained actor that has only ever seen runs whose tests went green and whose closes held. Rejection-sample the 27B over Louhi train + real S tasks; keep only durable-success runs, keep every loop as a negative. The 27B is already on this box.
  Done when: the distilled actor passes Louhi s0-001 at a higher rate than the 27B raw, on the same train split, with reasoning off.

- **One shared embedding + tiny frozen heads per slot, instead of a model zoo** — APPROACH — value 4 — effort M — risk low — category: decider
  Why: The request lists many decision types (decider, loop-predictor, verify-suggester, Ward-tightener). Training one embedder once and slapping a linear head per slot is cheaper to serve, share and retrain, and keeps each slot independently abstain-able. Matches "generic across every project."
  Done when: `sampo doctor` shows each slot as (embedding-hash, head-weight, abstain-threshold) and a single retrain command updates all heads.

- **Constrained-decoding grammar on every typed decision** — APPROACH — value 3 — effort S — risk low — category: decider
  Why: Every earlier brainstorm assumes free-text model output. A grammar (or a verb menu) means a wrong model can only produce a *wrong-but-parseable* verdict, never a run-on that a lane executes. Bounded repair, then fall back to the rules.
  Done when: a fuzzed model output can never reach a lane; the repair path logs a "repaired, then fell back" count.

- **Do less: ship the export + kNN + bench, defer all training** — APPROACH — value 5 — effort S — risk low — category: decider
  Why: The standing "lean substance" rule says growth without measurement waits. A flat, redacted, project-tagged training table plus a leave-one-project-out bench is the honest deliverable this pack can prove now; every trained head must beat it before adoption.
  Done when: `sampo model export` emits the table and the bench prints per-project held-out scorecards for the kNN arm.

- **Retrain keyed on a content hash of the outcome lake, not a schedule** — APPROACH — value 3 — effort S — risk low — category: training
  Why: A scheduled retrain wastes the GPU (which the moons funnel and exams also need) and trains on nothing new. Retrain only when the lake's content hash changes; idempotent and VRAM-fenced so it yields to Ollama.
  Done when: two consecutive idle ticks cost zero GPU and one lake change triggers exactly one retrain.

- **Pairwise approach-chooser as the first *useful* slot** — APPROACH — value 4 — effort M — risk med — category: decider
  Why: The request wants "a better Kev-style decider." The highest-leverage single decision is "which of the two candidate plans/fixes do you pick." Train a small head on which candidate the user actually accepted (the user's undo is the label). Lower risk than predicting whole outcomes.
  Done when: on 30 held-out two-way decisions, the chooser matches the user's pick more often than majority/coin.

- **Champion/challenger shadow mode through the existing decide() paths** — APPROACH — value 4 — effort M — risk low — category: adoption
  Why: The standing rule requires a capability to beat its free arm before it's real. Shadow the new head behind the current rules, log every divergence and its eventual outcome, promote only with a measured margin and one-command rollback.
  Done when: `sampo model promote SLOT` shows the shadow margin and an auto-revert on regression.

- **wild — Let the user's own undo be the only label; the model's job is to predict it** — APPROACH — value 4 — effort S — risk low — category: decider
  Why: Hand-labeling is the bottleneck that kills these projects. Every revert, re-ask and "not what I meant" in the ledger is already a label. If the model can't beat "predict the user will undo this," it earns nothing. This inverts the whole training target.
  Done when: the model's undo-prediction AUC on held-out briefs exceeds a majority baseline and is shown per slot.

- **wild — Run a permanent zero-model arm so every model must beat plain retrieval** — APPROACH — value 4 — effort S — risk low — category: adoption
  Why: The standing rule says a capability whose free arm beats the session arm is a top gap. Make "no model, just kNN + rules" a permanent bench arm; any head that can't beat it on the same held-out set is killed, not deferred.
  Done when: `sampo model report` lists every slot as beat/lose vs the zero-model arm, and losing slots are auto-retired.

- **wild — Federate only weights, never text, across the user's own machines, with a per-project consent gate** — APPROACH — value 3 — effort L — risk med — category: genericity
  Why: "Generic across every project" plus the multi-machine steer (T-3321 fleet claims) means projects want to share what they learned without leaking text. Merge per-project LoRA adapters into a shared base on the owner's hardware; consent flag per project, enforced by the collector.
  Done when: a merged base generalises on a held-out project the adapters never saw, and the consent flag, when off, leaves that project's rows out of the merge.

- **wild — Dream the decider's mistakes overnight: replay yesterday's close decisions against the model and file the regrets** — APPROACH — value 4 — effort M — risk low — category: improvement
  Why: The improvement loop is missing an automatic negative signal. On idle-GPU windows (yielding to the funnel), replay the last night's real decisions through the model, diff model-vs-actual, and file each regret as a training row and a held-out scenario. Closes the "how it improves every Rune generation" ask.
  Done when: a nightly lane emits a "regrets" file with N model-wrong rows, and the next retrain consumes it.

- **wild — Make the decider a readable rulebook, not a black box** — APPROACH — value 3 — effort M — risk low — category: decider
  Why: The user repeatedly pushes legibility (plain receipts, "one page"). A distillation that compiles to a small, human-readable decision table (conditions → action) that a cold child can read and a Ward can audit is more trustworthy than an opaque head, and satisfies "how it is measured."
  Done when: a tool-less child reads the rulebook and answers 10 held-out briefs at ≥ the head's rate, and `sampo doctor` verifies the table matches the head's weights.

- **Pin weights, embeddings and serving by content hash, and refuse a model whose settings never reached the endpoint** — APPROACH — value 4 — effort S — risk low — category: reliability
  Why: The user's own recent fixes (think:false not reaching Ollama; reasoning eating budget) show serving settings silently not applying. A model whose declared settings can't be verified against the endpoint is unsound, however good its bench.
  Done when: each model card carries a settings-verification line, and a mismatch blocks the slot from adopting.

Next question: what is the single smallest slot (one decision type) where the user's undo-rate is highest, so the first trained head targets real pain, not a showcase?
Next question: where in an active session is the natural place to call the decider (plan-time, close-time, mid-loop), and does the free-arm baseline already exist at that exact call site?
