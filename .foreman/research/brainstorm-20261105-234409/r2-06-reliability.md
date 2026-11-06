# Brainstorm — lens: reliability

- **Make every model verdict replayable from its on-disk evidence, or fail the slot** — FIX — value 5 — effort M — risk low — category: reliability
  Why: T-2966/T-2967 show the loop and guard depend on path and state correctness; a decider that "decided" but can't reproduce its call is the same class of bug. The standing rule says a FAIL counts only when it quotes the offending line — the model's own output needs the same quotability.
  Done when: `sampo decider replay <slot> <decision-id>` re-runs the head on the stored inputs and returns a byte-identical verdict, and `fm doctor` lists any slot that can't replay.

- **Give each model slot a typed stall cause with a rules fallback, and log which fallback won** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: The drive already types stops (T-3185 class) and the standing rule is "never block, name it and keep going." If the GPU is busy with the moons funnel (a left-question), a silent model timeout would stall a task or, worse, a wrong one. Today the fallback is implicit.
  Done when: a killed model call leaves a ledger line `slot=decider cause=gpu-busy fallback=rules verdict=<x>` and the next `fm next` names it; no slot ever returns an empty verdict.

- **Pin weights, embeddings and the serving stack by content hash, and verify at session start** — SECURITY — value 4 — effort S — risk low — category: reliability
  Why: "Refuse a model whose serving settings never reached the endpoint" is an existing idea, but a model that *is* reachable with *different* weights than it was benched on is the real failure. The rename already bit by literal-path mismatch (T-2967); a model bit is the same shape.
  Done when: a canary at session start re-runs one fixed probe prompt and diffs the output against the pinned digest; a mismatch flips the slot to rules and prints the mismatch, and `fm doctor` names it.

- **Quarantine training rows whose text came from a tool result or repo file, not the user or a verified close** — SECURITY — value 4 — effort M — risk med — category: reliability
  Why: A left-question asks whether ledger text can attack the trainer and the Ward. The pack shows tool results flowing into the ledger (silent-cut scans, cold reads). A model trained on untrusted text is a stored injection: it fires later, on another project, with no visible prompt.
  Done when: every row in the training lake carries a `source=user|close|tool|repo` tag, and the collector refuses to train on `tool` or `repo` rows unless an explicit project flag overrides it, recorded in the row's manifest.

- **Run the decider in shadow for one full Rune generation before it may vote, gated on a statistical floor** — CLEAN — value 5 — effort M — risk low — category: reliability
  Why: The standing rules already run zero-token arms and a Haiku smoke run and require a cold read before a capability counts. A model that *could* be wrong silently is worse than none; the champion/challenger registry exists in ideas but has no minimum-observation gate. "Add a statistical floor to every adopt decision" is listed but no mechanism.
  Done when: a newly trained slot reports `shadow=true` for at least N decisions (from the bench), and `fm genesis check` refuses to set it live until its holdout margin over the rules arm passes a pre-registered threshold.

- **Hold the model out of the Ward's decision path; the Ward stays rule-based and the model may only tighten** — SECURITY — value 5 — effort S — risk low — category: reliability
  Why: The standing rule is that the guard holds on the real path and undo must stick (T-2967). If a trained risk head can *loosen* a Ward refusal, a single poisoned training row or a drifted embedding becomes an escape route. The ideas already say "keep the Ward rule-based and let a model only tighten it," but nothing enforces direction.
  Done when: the Ward's code path has no model call; a model output that disagrees with a Ward *refusal* is ignored and logged as `advisory-ignored`, and a model output that would *refuse more* is applied and logged.

- **Make "will this close hold?" the first trained head, labelled by the user's own undo, and give it a veto on close** — FEATURE — value 5 — effort M — risk med — category: reliability
  Why: The six false dones and the "false-done detector" are known, but the label source is the weakest link. The standing rule treats the user's undo as ground truth elsewhere ("use the user's own undo as the only label" is listed but not wired). A head that can't veto a close is a dashboard; one that can is a gate.
  Done when: `sampo task finish` calls the head on the close evidence, and a verdict of `will-revert` (calibrated against ≥14 days of undo labels) blocks the close and names the closest historical revert; the user overrides with a one-key `--force` recorded in the ledger.

- **Fence every model-made decision to its declared file set, with a pre-edit canary that fails on any out-of-set write** — SECURITY — value 4 — effort M — risk low — category: reliability
  Why: "Bound the blast radius of a wrong model decision" is an idea without a mechanism. The decider suggests verify commands, pre-fills briefs, ranks the queue — if a wrong suggestion is *acted on*, the blast radius is the files it touched. A canary that checks the diff against the declared set is cheap and catches the worst case.
  Done when: a model-suggested brief carries a `files:` list, and `fm task prove` fails the close if the diff touches any file not in that list, printing the extra file and the model that suggested it.

- **Wild — give the decider a "I'd be wrong, here's the shape" self-report, and train it on its own past mistakes** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: A left-question asks which slot is worst when silently wrong. The pack has no mechanism for a model to flag *its own* uncertainty beyond abstain. The standing rule is "no idea is killed for ambition; a failed spike gets 2+ approaches." A self-report head is the third approach: not a new model, but a trained "confidence-is-calibrated" check on the existing heads, using the regret labels already mined.
  Done when: each head emits a `self-risk` score; a score above threshold routes the decision to the rules fallback and logs `self-risk=high reason=<pattern>`; the pattern is added to the training set on the next retrain, and `fm doctor` prints the self-risk rate per slot.

- **Wild — run a "model autopsy" lane: replay every silent fallback decision from the last 7 days against the rules arm, and file the disagreements** — CLEAN — value 4 — effort S — risk low — category: reliability
  Why: The pack shows silent fallbacks everywhere (Haiku fallback, rules fallback, "could not run" exam readings). If the fallback is the *usual* path, the model's actual behaviour is invisible. The standing rule wants a "model saved you X" receipt; the inverse — "the model was wrong and you didn't know" — is the reliability gap.
  Done when: a nightly lane (`sampo decider autopsy`) replays the last 7 days of model decisions against the rules arm on the same inputs, and files a task for each disagreement where the model was wrong and the rules were right, tagged `model-regret`; the morning card prints the count.

- **Wild — commit a "museum" model: a frozen copy of the first decider, re-run on every close forever, as a tripwire for drift** — CLEAN — value 3 — effort S — risk low — category: reliability
  Why: "Keep a frozen 'museum' model as a permanent tripwire" is listed but not built. The rename showed how easily a path or setting changes silently (T-2967). A frozen model that *should* agree with the live one on stable inputs is the cheapest drift detector: when it disagrees, something in the serving stack, embeddings, or weights changed.
  Done when: the museum model's weights and embeddings are pinned by hash, it runs on every close as a second opinion, and a disagreement > ε prints `drift: museum vs live on <brief-id>` and freezes the live slot to rules until the user re-benches.

- **Make the training pipeline resumable, VRAM-fenced, and idempotent: one command re-trains from the content hash of the outcome lake** — PERFORMANCE — value 4 — effort M — risk low — category: reliability
  Why: "Make training resumable and VRAM-safe" and "retrain by a content hash, not a schedule" are both ideas without a spec. The moons funnel already contends for the GPU (a left-question). A training job that dies mid-epoch, re-runs from scratch, or silently uses stale rows is a reliability failure, not a training failure.
  Done when: `sampo decider train` is idempotent (same hash → no-op), resumes from the last checkpoint on OOM or kill, fences VRAM to the slot's budget (yielding to Ollama and the funnel), and refuses to train on a lake whose hash doesn't match the manifest.

- **Wild — let the user's *undo* be the only label, and make the model's job to predict the undo, not the close** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: The standing rule "use the user's own undo as the only label" is listed but the close-holds verifier is framed as predicting "will this close hold?" — a close the user *didn't* undo is a positive label, but a close the user *did* undo is a negative. The problem: most closes are never undone, so the positive class is noisy (a close can "hold" because the user forgot to undo, not because it was right). Predicting the undo directly, with a long tail, is a cleaner signal.
  Done when: the head's target is `undone-within-30d: 0/1`, the negative class is sampled from the user's actual undo history (not assumed), and the head's precision on the `1` class (i.e., it flags things that *will* be undone) is reported per slot and gates adoption.
