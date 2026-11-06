# Brainstorm — lens: simplicity

Lens: simplicity. The pack is enormous (2,381 files, a 2.4 GB state, 1,396 skills, 80 steers, a 10,000-moon funnel, dozens of deferred L-missions) while the user keeps asking for *one* thing: a small, generic, local model that decides and improves every Rune generation. The repeated pushbacks all point the same way — the silent-cut scan, the "no software installs", the "README says only true things", the "do less: ship a data export" idea, the wall of "one verb" ideas already filed. The need behind them is *reducing the surface the user must hold in their head*. So the best decider ideas here are the ones that *subtract*.

- **Collapse the decider to one verb: `sampo decide`** — FEATURE — value 5 — effort S — risk low — category: simplicity
  Why: the request names "a better Kev-style decider and more" as a bundle of five questions (what it does/trains/serves/measures/improves). That's five mental objects. One verb with `sampo decide explain` and `sampo decide train` answers all five; a cold child reading only the README can then say what it is. Matches the filed "one verb" instinct and the user's "generic, not Sampo-specific" ask.
  Done when: `sampo decide` is the only new top-level verb the decider adds, and a tool-less child names what it does from the README alone.

- **Make the model answer in one typed sentence, or abstain** — CLEAN — value 5 — effort S — risk low — category: simplicity
  Why: a classifier that emits free prose forces the user to parse it; a grammar-constrained one-line verdict ("close will hold" / "abort: repeated action") is checkable, ledger-able, and veto-able. Evidence: the user's "explain every model decision in one plain line" and the silent-cut scan both reward bounded output.
  Done when: every model decision renders as ≤1 sentence or the word "abstain", and a schema test rejects free-form output.

- **Default to no model: retrieval-only kNN, model is opt-in** — CLEAN — value 5 — effort M — risk low — category: simplicity
  Why: the strongest "do less" in the pack is "ship a data export and a bench, defer all training". A kNN-over-closed-briefs baseline already answers "what usually follows this ask" with zero weights to serve, schedule, or regress. Training becomes a lever you pull, not a state you maintain. Matches the user's "quick, without burning money" steer.
  Done when: `sampo decide` works end-to-end with no weights file present, and a model only activates after the user opts in.

- **One "off" switch that really turns the model off** — FEATURE — value 5 — effort S — risk low — category: simplicity
  Why: with a new trained decider the user will want to *not* be decided for, per project. A single flag that removes the model from the path and prints what the rules would have done instead removes the whole class of "is Sampo in the way?" anxiety. Directly serves the filed "one off switch that actually turns Sampo off" and the privacy/local-first lens.
  Done when: setting the flag makes `sampo decide` return the rule baseline and the model binary is never invoked (verifiable in the ledger).

- **Kill the decision zoo: one model, one slot, one verdict** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: the "Ideas so far" wall proposes per-slot heads, a model zoo, per-project LoRAs, federated weights, a rulebook, a twin — dozens of artifacts to track. The user asked for "a better Kev-style decider" (singular). Shipping one head on one shared embedding, measured on one bench, is the version a new user can hold. The rest re-earn their place by measured gain (the lean-substance steer).
  Done when: the decider ships as exactly one head on one embedding plus a rule fallback; no second model file exists in the install.

- **Retrain on a content hash, not a calendar** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: a scheduled retrain is a moving target the user must track and a source of surprise. Keying it to "the outcome lake changed enough" means the model only moves when new evidence actually landed, and `sampo decide train` is idempotent and resumable. Evidence: the user's "retrain by a content hash, not a schedule" idea and the "quick, not burning money" steer.
  Done when: two runs with no new closed briefs produce no retrain; a new closed brief triggers at most one.

- **Cut the context the model sees to the one brief it's deciding on** — PERFORMANCE — value 4 — effort M — risk med — category: simplicity
  Why: the pack's own SessionStart injection is so large it triggered a "300-character first prompt" wild idea and a whole lean-substance campaign. Feeding a 0.6–4B decider the full 2.4 GB state or 1,396 skills is both wasteful and incoherent. The decider should see the current brief, its two nearest closed siblings, and the standing intent — nothing else.
  Done when: a token budget table caps the decider's input and a test fails if a full-lake dump ever reaches the prompt.

- **Show the decider as one line in `sampo status`, not a dashboard** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: the user already has a rich web UI and tower; adding a model dashboard multiplies the surfaces to watch. A single status line — "decider: kNN (model off), last abstain 2h, 14-day agreement 82%" — answers "is it working?" without a new page. Matches "one status line for the model's state" and the "show cost in one card" pattern.
  Done when: `sampo status` prints exactly one decider line and no separate model UI is required to check health.

- **Make the user's undo the only label** — FEATURE — value 4 — effort M — risk med — category: simplicity
  Why: labeling 2,900 briefs by hand is the hidden cost of "how it is trained". If the negative label is simply "the user later reverted/undid this decision", training needs no annotation pipeline, no label store, no consent form per row — the behavior the user already produces is the signal. Removes an entire subsystem. Evidence: the filed "use the user's own undo as the only label" and "treat the user's silence as a label".
  Done when: the training set is derivable from the ledger alone with no separate labeling step, and a new undo automatically becomes a negative example.

- **Ship one training command the user will actually run: `sampo decide train`** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: "how it is trained and served on this box" implies a pipeline the user can operate. A single idempotent, VRAM-fenced, resumable command (no separate serve step — the model loads on demand) is the minimum that makes the capability *yours* rather than opaque. Evidence: the user's own request lists training/serving as things *they* want to control, and the "no software installs" steer.
  Done when: one command trains and one command (the same, with `--serve`) runs the model, with no other steps and no manual install.

- **wild — The decider is a rulebook you can read, not a black box** — FEATURE — value 4 — effort M — risk med — category: simplicity
  Why: a user who can't read the weights will distrust a "better decider". Train the tiny head, then *distil its top-20 decision boundaries back into a short readable rule file* the user can edit — the model proposes, the rules are the contract, and the user can see exactly why it said "abstain". This turns a faith problem into an editable one, and is the one capability a fully-featured version still lacks: legibility of *why*.
  Done when: a human can read `decide.rules` and correctly predict the model's verdict on 8 of 10 held-out briefs without running it.

- **wild — `sampo decide` answers the user's *next* question, not just the task** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the pack's "Questions earlier brainstorms left" are all second-order ("when two slots disagree…", "what does a project with <20 briefs get…"). The simplest, highest-leverage decider output is not a per-task verdict but a standing one-line *answer to the question the user is about to ask*, pre-computed at session start from the ledger. It collapses dozens of "what would happen if" back-and-forth exchanges into one line they can read in 10 seconds — the user's own "cap predictions at what the user can check in 10 seconds" steer.
  Done when: at session start one decider line answers the single most-likely pending question, and it is scored against whether the user then asked it.

- **wild — Let the model refuse the work and be paid for saying "no"** — FEATURE — value 3 — effort S — risk med — category: simplicity
  Why: the user's whole discipline layer is about stopping things. The simplest *improvement* to a decider is the permission to say "this brief is already done / this lane is duplicate / this is a repeat" and *stop the work before it costs anything*. That is a capability the rules struggle with (similarity, premise-staleness) and a model handles trivially — and it removes work rather than adding it, which is the purest form of simplicity.
  Done when: on N held-out already-satisfied or duplicate briefs the model abstains-with-reason and the work is not started, with the abstain logged and veto-able.

Next question: what is the user willing to *stop* running to make room for the model — which existing rule or slot would they gladly delete if the decider beat it on holdout, so the model *replaces* rather than *adds* a surface?
Next question: at what brief-count does a project get too little data for the model to say anything useful, and should the simplest answer be "no model below N briefs" rather than a per-project adapter?
