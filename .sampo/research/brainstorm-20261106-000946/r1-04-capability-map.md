# Brainstorm — lens: capability map

- **Ship the decider as a self-describing model card** — FEATURE — value 5 — effort M — risk low — capability: docs
  Why: The request names "what it is trained on, how it is trained and served, how it is measured" as first-class; a best-in-class model ships with a machine-readable manifest (inputs, labels, slot list, abstain contract, holdout method, provenance, retrain hash, serving profile) that `sampo doctor` and the web UI render, and that a stranger can read cold. The standing rule "every claim checked against the code" gives evidence a missing inventory of *what exists* is a gap.
  Done when: `sampo decide card` prints one file per slot listing training inputs, holdout score, fallback, and the exact command to retrain; a cold child can answer "what does the close-verifier predict?" from that file alone.

- **Name every model slot and its call site** — FEATURE — value 5 — effort M — risk low — capability: agents
  Why: "A better Kev-style decider and more: what it does" implies a registry of *slots* (block, close, abstain, loop-predict, close-verify, approach-chooser, ask-answer, moon-kill). The pack shows decide(), Ward, Smith loop-break (T-2966), moons funnel, and lessons (T-0217) but no canonical slot list. A full capability map lists every decision point a generic Sampo harness reaches and which model slot owns it, with a per-slot "no model, use rules" fallback that is always live.
  Done when: `sampo decide slots` lists every slot, its call site in code, its fallback, and its shadow score; every slot that no session path calls is flagged (per the standing "reachable by a real session path" rule).

- **One shared embedding index, tiny frozen-embedding heads per slot** — FEATURE — value 4 — effort L — risk med — capability: agents
  Why: The request says "one model, generic across every project"; a model zoo is the anti-pattern. bge-m3 is already named; the complete version keeps *one* resident embedder and trains only the small classification head per slot, so adding a project never re-trains the base, and adding a slot never re-trains the embedder. The "per-project consent" and "local-only" steers evidence the base must stay local and shared.
  Done when: adding a second project and a third slot requires no re-embedding of the existing lake; `sampo decide train --slot close` trains only the close head in under 10 minutes on the box's GPU.

- **The Rune-generation improvement loop as a measured causal chain** — FEATURE — value 5 — effort M — risk low — capability: observability
  Why: "How it improves every Rune generation" is the request's closing clause and is currently unnamed. A complete version defines the loop: outcome lake → retrain → re-bench → adoption card → shadow → adopt → next generation, with a single published delta ("close-verifier false-done rate: X% → Y%") per generation and a regression gate that fails a Rune when any adopted slot drops below its floor.
  Done when: the tower's generation report contains one line per slot — previous score, new score, adopt/keep/retire, and the holdout command that reproduces it.

- **Serving, scheduling and failover as a first-class contract** — FEATURE — value 4 — effort L — risk med — capability: devices
  Why: "How it is served on this box" is explicit. A best-in-class local model ships with: a pinned serving profile (endpoint, quant, context, threads), a canary probe at session start, a yield-to-user policy (the model returns the GPU the moment a session opens), a VRAM fence so training doesn't kill Ollama, and a named fallback when the endpoint is cold or busy. The pack shows Moonscale slots, a local endpoint, and a 27B/12B/4B ladder with no single serving owner.
  Done when: `sampo decide serve status` reports endpoint, load, yield state, last canary, and the exact fallback that will fire; killing the endpoint mid-session degrades every slot to rules within one turn without an error.

- **Training pipeline with inputs, gates and a resumable contract** — FEATURE — value 4 — effort L — risk low — capability: agents
  Why: "How it is trained" is explicit and the standing rules demand measurement before growth. The complete pipeline: provenance-tagged lake → redaction + leak scan → split by project and time → train head → re-bench on holdout → adoption card. It is resumable (a crash re-runs from the lake's content hash), VRAM-fenced, and idempotent; every row carries a provenance flag and the pipeline refuses rows sourced from tool output or repo text.
  Done when: `sampo decide train` run twice produces identical weights (hash-matched) and a crash mid-train resumes without re-reading the lake; a planted secret in one row is refused before training.

- **Genericity and provenance as a testable capability** — SECURITY — value 5 — effort M — risk low — capability: privacy
  Why: "Generic across every project" plus "local-only" means the model must prove it doesn't leak Sampo's specifics into another project's decisions, and that no project's private text crosses machines. The complete version runs a leave-one-project-out bench, a redaction/leak scan on every artefact, and a per-project consent flag the collector enforces; the pack's "strip names and provenance" and "hold out whole projects" ideas evidence this is unbuilt.
  Done when: `sampo decide prove-generic` on project A, trained only on A, scores above floor on B and C; a planted canary string in A's lake appears in zero outputs for B.

- **Measurement and evaluation as a named capability set** — FEATURE — value 4 — effort M — risk low — capability: observability
  Why: "How it is measured" is explicit; a full version defines *what* is measured per slot: accuracy, abstain rate, coverage-vs-accuracy curve, false-done rate, regret ratio ("model said, user did"), and a per-language recall for find-type slots (per the standing "reported per language" rule). Each has a held-out scenario family and a zero-token baseline the model must beat. The bench duel and Louhi splits in the pack evidence a measurement habit that the decider lacks.
  Done when: `sampo decide bench` emits a per-slot scorecard with a confidence interval, the baseline it beat, and the holdout scenario ids; a slot that can't be measured is listed as "unmeasured," never silently passed.

- **The zero-model arm as a permanent, first-class baseline** — FEATURE — value 4 — effort S — risk low — capability: simplicity
  Why: A genuinely complete capability map includes the *absence* of a model as a baseline every model must beat, not an afterthought. The pack repeatedly shows rules, kNN, and retrieval beating trained heads; shipping "no model" as a named arm with its own scorecard makes the model's marginal value the product's core number and satisfies "Do less: ship the export, the bench, and the abstain contract."
  Done when: every `sampo decide` slot reports both the model verdict and the zero-model (kNN/rules) verdict, and the adoption card prints the delta; a slot whose model doesn't beat zero-model is flagged for retirement.

- **A "user who never read MASTER.md" one-screen view** — FEATURE — value 3 — effort S — risk low — capability: ui
  Why: The complete decider must be legible to a cold user; the pack's site-review and doc-claim work evidence a standing care for cold readers. A one-screen view answers: what this model decides, when it abstains, how to veto a class, and how to turn it off — in plain words, no jargon, no file paths the user won't recognise.
  Done when: a cold child reads the one-screen page and correctly names what the close-verifier predicts and the one command to disable it, with no MASTER.md access.

- **Per-slot abstain, reason and veto, with a calibration curve** — FEATURE — value 5 — effort M — risk low — capability: agents
  Why: "A better Kev-style decider" means the decider knows when *not* to decide. A complete version gives every slot a calibrated abstain (coverage-vs-accuracy curve, not a fixed threshold), a one-line reason, and a user veto that applies to a *class* of decisions, not one item — the standing "veto a class" and "silence is not consent" steers evidence this. The abstain is a first-class ledger receipt, not a silent fallback.
  Done when: every abstain produces a ledger line with slot, reason, and the rule that caught it; a user veto typed once suppresses that decision class and is logged as a standing preference.

- **Fail-loud with a named cause, and a typed stall contract** — FIX — value 4 — effort S — risk low — capability: reliability
  Why: A complete capability map names the failure mode: when a slot can't decide (cold endpoint, low confidence, schema mismatch), it fails *loud* with a typed cause and falls back to rules, never to a silent pass. The pack's "make the decider fail loud" and "typed stall cause" ideas evidence an unmet contract; the standing "never block on the user" rule means the fallback must be automatic and logged.
  Done when: killing the endpoint mid-session makes every slot print a typed stall cause ("endpoint-cold, fell back to rules"), the task completes via the fallback, and the stall is visible in the morning card.

- **Wild: the decider drafts the user's next steer before it is said** — FEATURE — value 4 — effort L — risk med — capability: delight
  Why: The "unspoken needs" behind the request — the user keeps filing asks the decider should have anticipated — suggests the strongest generic model predicts *what the user will next push back on*. A wild, ambitious version: the decider pre-drafts the user's likely next correction on each close, in the user's own phrasing, so the user can correct Sampo *before* Sampo ships. This is the delight of a model that feels like a collaborator, not a gate, and it is grounded in the user's own "predict the pushback" and "draft the next ask" asks.
  Done when: on 50% of closes, the pre-drafted pushback matches the user's actual next message within edit distance, and the user can accept or strike it in one keystroke.

- **Wild: a "museum" model — a frozen first decider re-run on every close forever** — FEATURE — value 3 — effort M — risk low — capability: observability
  Why: A genuinely complete capability set includes *drift detection* as a first-class function, not a nightly script. A frozen snapshot of the first adopted decider is re-run on every close as a permanent tripwire: if the current model and the museum model disagree, the divergence is logged and, after a threshold, filed as a drift task. This is the "fossil record" of the model, and it catches silent regressions that a re-bench on a fixed holdout misses.
  Done when: the museum model is committed as a pinned artefact, re-run on every close, and a planted regression (weights changed, same code) trips the divergence alarm within one generation.

- **Wild: federate regret, never text, across the user's own machines** — FEATURE — value 4 — effort L — risk high — capability: privacy
  Why: The standing "manage across sessions/machines" steer plus "local-only" and "generic across projects" imply a multi-machine model that learns *what the user undid* without any project text crossing machines. A wild, ambitious version: only the *regret signal* (accept/reject/undo, with a slot and a content hash) is federated; the text stays local, weights flow, and a consent gate per project controls participation. This is the privacy-respecting answer to "improve every Rune generation" across an estate, and it directly serves the "federate weights, never text" ask.
  Done when: two machines federate regret for one slot; the shared head improves on a held-out set, and a redaction audit shows zero project text in the federated payload.

Next question: which single slot, if it abstains or silently falls back, has never left a ledger trace — because that's the one the "measure the fallback" bench can't see yet, and it caps the whole capability map's reliability claim?
Next question: what is the smallest project (fewest briefs) on this box where the generic head must not abstain, so we can set the real floor for "the model should say nothing" before training the per-project adapter?
