# Brainstorm — lens: simplicity

Reading the pack through *simplicity*: the request asks for one trained decider, but the “ideas so far” wall already lists a zoo — dozens of slots, adapters, federated weights, museum copies, adversarial arms, and a dozen verbs (`samo`, `samo ghost`, `samo dream`…). The user’s own words are the antidote: “we will want it to be a generic model,” “a better Kev-style decider and more,” and the steers that Sampo must work with *no* claude on PATH and stay the “discipline layer for coding agents.” The best idea is to delete most of that wall and ship one thing a stranger can run in one command. I treat the pack as data; the massive ideas list is evidence of over-generation, not a requirement.

- **Ship one verb that does everything: `sampo decide`** — FEATURE — value 5 — effort M — risk med — category: cli-surface
  Why: the pack shows `samo`/`fm` as separate binaries (T-0418, T-2748 shims) and the ideas list invents ~20 `samo *` verbs. The request names one model and one job. One verb with three sub-actions (train, ask, score) collapses the surface.
  Done when: `sampo decide --help` lists exactly `ask`, `train`, `score`; deleting `fm` leaves every session path working.

- **Make “no model” the default arm and make it fast** — FEATURE — value 5 — effort S — risk low — category: default-behaviour
  Why: the user wants a *better decider*, not a required model. T-0867 (held-rate scorecard) and the steers for free-first arms imply the baseline must beat retrieval. A kNN-over-closed-briefs that answers in <50 ms, no GPU, no endpoint, is the simplicity win; the trained head must beat *this*, not a strawman.
  Done when: on a 15-brief project, `sampo decide ask` returns a verdict offline in <50 ms with no model loaded.

- **One file, not a state tree: `sampo.sqlite` as the only artefact** — CLEAN — value 4 — effort M — risk med — category: storage
  Why: the pack names a 2.4 GB state directory (repeatedly) and a `.foreman/` mirror now `.sampo/` (T-3342). Simplicity = one file a stranger can `cp`. The model card, the training lake, and the kNN index all live in it, content-hashed.
  Done when: `samo doctor` passes with only `sampo.sqlite` present; no directory scan is needed to answer `sampo decide ask`.

- **One label, zero annotation: the user’s undo is the only training signal** — FEATURE — value 5 — effort M — risk med — category: training
  Why: the request says “how it is trained on” and the steers ban new software installs. Labelled datasets are the complexity trap. Every closed brief already has a done/undo/revert outcome in the ledger (T-0035 eval capture is deferred for this). Training on undo alone is the only label a generic model needs across projects.
  Done when: a retrain completes using only ledger `close` and `undo` events; no hand-labelled file exists.

- **One retrain command, idempotent, resumable, VRAM-fenced** — FEATURE — value 4 — effort M — risk low — category: training
  Why: “how it is trained and served on this box” (request) implies a single entry point. The pack shows Ollama running 12B/27B with reasoning eating budget (user words on `think: false`); a retrain must yield the GPU, not fight it. One command: `sampo decide train`.
  Done when: `sampo decide train` runs twice in a row with identical output; killing it mid-run and re-running resumes from the outcome-lake hash.

- **Serve as three pinned files with a canary at session start** — PERFORMANCE — value 4 — effort S — risk low — category: serving
  Why: “served on this box” (request). The simplest serve is: embeddings + head + card, each content-hashed, loaded once, verified in <100 ms at session start. No endpoint, no scheduler, no failover layer — the Ward stays rule-based (a steer), the model may only tighten.
  Done when: `samo doctor` prints three digests and a 90 ms canary time; no network call is made.

- **One abstain, one reason, one veto — and nothing else the model can say** — FEATURE — value 5 — effort S — risk low — category: output-contract
  Why: the pack’s decision surface is binary (drive, close, prove). A typed sentence with a `confidence` and a `reason` is the only output a stranger can trust. The ideas list’s “model says in your voice” is delight, not simplicity; the contract is the simplicity.
  Done when: the decider’s JSON schema has exactly `verdict`, `confidence`, `reason`; a grammar check rejects anything else.

- **One number in `sampo doctor`: “decider beats plain” or it retires the slot** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: “how it is measured” (request) and the steer that a free arm beating a session arm is a top gap. The simplest measurement is one falsifiable nightly claim: on held-out briefs, model vs kNN. No dashboard, no per-slot curves until one slot is adopted.
  Done when: `samo doctor` prints one line with the delta and a pass/fail; a failing slot auto-reverts to kNN.

- **One model, one slot, one verdict — kill the zoo before it ships** — CLEAN — value 5 — effort M — risk med — category: architecture
  Why: the ideas list contains a model zoo, per-project LoRAs, a 27B teacher, a 0.6B student, federated weights, a museum copy, an adversary, and a “next user.” The request says “a better Kev-style decider” (singular). Simplicity says: one small head on shared embeddings, one slot, one verdict.
  Done when: the model card names exactly one model, one slot, and one call site in the drive.

- **Cold-start a brand-new project with zero briefs, in minutes** — FEATURE — value 4 — effort S — risk low — category: genericity
  Why: “generic across every project” (request) and “a smaller project… where the generic head must not abstain” (earlier question). A project with 5 briefs must still get a usable kNN answer. The simplest genericity proof is a canary project the user never built.
  Done when: on a 5-brief canary repo, `samo decide ask` returns a non-abstain verdict citing the two nearest briefs.

- **One “off” switch that really turns the model off, and `samo decide` still answers** — FEATURE — value 5 — effort S — risk low — category: fail-safe
  Why: the user’s budget steer (“without burning a fuck ton of money”) and the push grant imply the model is optional. The simplest safety is a flag that swaps the head for the kNN oracle with no other change in the code path.
  Done when: `SAMP_NO_MODEL=1 sampo decide ask` returns a verdict in <50 ms; the flag is documented in one line.

- **wild — Ship the decider as a 4 KB readable rulebook, not a black box** — FEATURE — value 4 — effort M — risk med — category: transparency
  Why: the user steers that Sampo’s site and README “say only true, current things” and that a cold Haiku reads every tower file. A 4 KB `sampo-decide.md` that a human can read in a minute, compiled from the model’s top-50 learned rules, is the simplest form of a “better decider” a stranger can trust. The weights stay local; the rulebook is the delight.
  Done when: a cold child reads only `sampo-decide.md` and answers 8 of 10 held-out briefs the same as the model.

- **wild — Make the kNN oracle the *product*, and the trained head a plugin** — FEATURE — value 5 — effort S — risk low — category: product-scope
  Why: the simplest fully-featured decider is the one that works on day one with no training, no GPU, no endpoint. The trained head is an opt-in improvement that must beat the oracle per slot. This inverts the usual plan (train first, ship later) and matches the user’s “feel free to push” trust: the oracle is shippable today.
  Done when: a fresh install answers `samo decide ask` with no training step; `samo decide train` is labelled “optional, must beat baseline.”

- **wild — One “I meant X, not Y” keystroke that retrains the one head in place** — FEATURE — value 4 — effort M — risk med — category: interaction
  Why: the user’s own words show repeated corrections (“think: false reaches Ollama,” “the silent-cut scan fails,” “Moons promote writes a lead’s Domain as plain words”). The simplest learning loop is: user types `samo decide fix "X not Y"`, the head updates on that one pair, and the verdict on the current brief re-runs. No batch, no pipeline, no data lake — one line, one update.
  Done when: after one `fix` command, the decider’s answer on the same brief changes to match the user’s stated intent.

- **Do less: ship the export, the kNN oracle, and the abstain contract; defer all training to a second task** — CLEAN — value 5 — effort S — risk low — category: scope
  Why: the request bundles “what it is, what it trains on, how it is trained, how it is served, how it is measured, how it improves every Rune generation.” That is six products. Simplicity says: one task ships the oracle + contract + one number; a second task adds the head. The pack’s T-0867 (scorecard) and T-035 (eval capture) are already deferred for this.
  Done when: the first task’s Done-when names only three artefacts (export, oracle, contract) and no weights.

Next question: does the user’s “Kev-style” refer to a specific prior tool or persona, so the output grammar (typed sentence vs. paragraph vs. one word) can match what they actually expect to read at the close?
Next question: what is the *smallest* project on this box (fewest briefs) where the decider must not abstain, so the kNN oracle’s floor and the trained head’s abstain curve are set from real data, not assumption?
