# Brainstorm — lens: reliability

- **Watch the decider from outside the process** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: T-0828/0832 and the "drive" work show background loops (moons funnel, training, exams) share this box; a model slot that hangs or silently returns garbage mid-run has no external heartbeat. The user's standing rule "never block on the user" means an unattended bad decider is the worst failure. "assumption: current slots have no liveness probe."
  Done when: `sampo doctor` reports each slot as alive/stalled/absent with the last verdict timestamp, and a stuck slot is surfaced in the pane, not just a log.

- **Gate every adopted slot behind a shadow period with a statistical floor** — FEATURE — value 5 — effort M — risk med — category: safety
  Why: Standing rule "a capability whose free arm beats the session arm is a top gap" + "Haiku scores never decide done." A model that looks better on 20 samples and worse on 200 would be adopted blindly. Evidence: the whole exam/holdout apparatus already exists; it just isn't wired to *promotion*.
  Done when: a new slot must run in shadow for one full Rune generation and clear a pre-registered confidence interval before it may vote; `sampo decide adopt` refuses otherwise.

- **Make every verdict replayable from on-disk evidence, or fail the slot** — CLEAN — value 4 — effort M — risk low — category: audit
  Why: T-0791 (injection/supply-chain), the provenance-tagging ideas, and "join every model call to its eventual outcome" all imply it, but no idea forces it at the *slot* level. A decider whose verdict can't be re-derived from its stored inputs is an unauditable black box in a product whose whole point is legibility.
  Done when: `sampo decide replay <id>` reproduces the verdict from the stored evidence alone, byte-for-byte, on a fresh process; a non-reproducible verdict is logged as a defect.

- **Pin weights, embeddings and the serving stack by content hash, verified at session start** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: The user runs 4B/12B/27B locally and swaps models (T-2912, 2966 small-model work). A silently replaced or drifted weight file would change every decider with no signal. Evidence: "verify pinned model digests," "pin local model weights by digest" exist but none binds *serving settings* to the verdict.
  Done when: a session-start check confirms the served weights match the pinned hash and the verdict is stamped with it; a mismatch aborts the slot to the rules fallback.

- **Hold the model out of the Ward's decision path** — SECURITY — value 5 — effort S — risk low — category: safety
  Why: T-2967 shows the guard's core protection already breaks on path resolution; a *model* in that loop adds a learned, mutable, prompt-injectable layer where the Ward must be deterministic. The standing rule "the Ward refuses whatever it refuses under the Foreman names" is a correctness contract a model cannot honor. Several ideas say "tighten only," but none *exclude* it.
  Done when: no model output can flip a Ward refusal from deny to allow; only human-authored rule edits or the user's explicit grant change Ward behavior.

- **Treat training rows as untrusted until outcome-labeled** — SECURITY — value 4 — effort M — risk med — category: data hygiene
  Why: T-0791 (injection/supply-chain defenses) and "quarantine training text that came from a tool result" flag the risk, but the decider would be *trained* on this text, turning a prompt-injection into a weight-level backdoor. "assumption: current collectors don't separate user/tool/model-authored text."
  Done when: rows are tagged by author (user / verified close / tool / model), and the trainer refuses any row whose label is model- or tool-authored unless the user explicitly consents.

- **Give each slot a typed stall cause with a named rules fallback** — FIX — value 4 — effort S — risk low — category: degradation
  Why: T-0828 "shell prefilter in front of size-gated hooks" and T-2966 (loop break) show small models fail in specific, classifiable ways (timeout, loop, context overflow, budget). Today a failure is a generic error; the user can't tell "model busy" from "model wrong."
  Done when: every slot timeout/abort emits one of a fixed set of causes (busy, looped, overflowed, budget, absent) and names the exact rules path that took over.

- **Make retraining idempotent and resumable from the outcome-lake hash** — CLEAN — value 4 — effort M — risk low — category: build
  Why: Standing rule "don't stop or skip work for budget... wait out real usage limits and resume." A training run that can't be resumed after an OOM or GPU contention (shared with the moons funnel, T-2953) would block a Rune generation. Evidence: "make training resumable and VRAM-safe," "retrain by a content hash."
  Done when: killing and restarting `sampo decide train` resumes from the last completed chunk; the final model is bit-identical to a single-pass run.

- **Fence every model-made edit to its declared file set** — SECURITY — value 5 — effort M — risk med — category: containment
  Why: T-2745/T-2967 (guard core protection) and "bound the blast radius of a wrong model decision" imply it. A decider that approves a plan which then edits files outside the declared set is a silent scope violation. "assumption: plans carry a file list today."
  Done when: a canary at pre-edit rejects any write outside the plan's declared set, and the rejection is logged with the offending path.

- **Rehearse a "model gone" week: zero-model mode as a permanent arm** — FIX — value 4 — effort S — risk low — category: resilience
  Why: Standing rule "Haiku scores never decide done" + "do less: ship a data export and a bench, defer all training" + the user's "not burning a fuck ton of money" steer. If every slot degrades to a no-op when the endpoint is down (T-2912 silent-cut, GPU contention), the product must still *finish* work. Several ideas ship a "zero-model mode," but none makes it a *tested* fallback.
  Done when: a drill disables all local endpoints for 24h; the drive completes its queue using rules + retrieval only, and the morning card shows which slots fell back and why. (wild)

- **Wild — let the decider's own past mistakes be its teacher** — FEATURE — value 4 — effort L — risk high — category: self-improvement
  Why: "Run the decider's mistakes overnight and file the regrets" and "retrain on the previous generation's mistakes only" exist but are one-shot. A closed loop where *every* silent fallback or user undo feeds a nightly diff of "here is where I was wrong" makes improvement self-driving, matching the tower-advances-itself rule.
  Done when: a nightly lane replays the last 7 days of fallback/undo events against the current model, files a regret per disagreement, and the next retrain includes them as negatives. (wild)

- **Wild — ship a frozen "museum" decider as a permanent tripwire** — FEATURE — value 3 — effort S — risk low — category: drift
  Why: "Keep a frozen 'museum' model as a permanent tripwire" is listed but unelaborated. A first-gen decider re-run on every close forever catches silent drift: if the current model's verdict disagrees with the frozen one on a case the user *already accepted*, that's a regression signal no holdout set will catch.
  Done when: the frozen model's verdict is logged beside every close; a disagreement on an accepted case files a drift task. (wild)

- **Wild — let the decider *refuse the work* and pay for saying "no"** — FEATURE — value 3 — effort M — risk med — category: capability
  Why: "Let the model refuse the work, and pay it for saying no" is listed but has no mechanics. A decider that can say "this brief is ill-formed / will loop / will be undone" *before* work starts, with the refusal logged and scored against the later outcome, converts a cost-center into a gate. Matches "predict a brief's outcome before work starts" and "predict a loop before the third repeat."
  Done when: `sampo decide` can emit a typed refusal (ill-formed / will-loop / will-be-undone) before the first edit, and the refusal is scored against the actual outcome at close. (wild)

- **Reconcile state from git + ledgers on every resume, then diff the checkpoint** — FIX — value 5 — effort M — risk low — category: recovery
  Why: T-2967 (migrate/undo) and T-3185 (core.bare=true leak) show state can drift from what the model believes. A decider resuming a task that was edited, rebased or partially merged under it must re-derive truth from git and ledgers, not its last in-memory state. Evidence: "reconcile on resume," "rebuild state from the git common dir."
  Done when: on resume, the slot re-derives its inputs from git + ledgers, diffs against the last checkpoint, and aborts (to rules) if they disagree.

Next question: what does the decider do when the user's *undo* is the only label and the undo itself was accidental — is there a way to distinguish "I changed my mind" from "I fat-fingered"?
Next question: when two slots (e.g. loop-predictor and close-verifier) disagree on the same brief, is there an arbitration rule, or does the higher-value slot win, and has that tie-break ever been *measured* against the user's actual choice?
