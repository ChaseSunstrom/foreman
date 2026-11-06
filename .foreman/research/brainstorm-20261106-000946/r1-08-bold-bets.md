# Brainstorm — lens: bold bets

- **Bet the whole product on one number: decider beats plain on whole held-out projects, or Sampo retires the slot** — FEATURE — value 5 — effort L — risk high — category: capability map
  Why: the pack's request is a "better Kev-style decider"; the only claim that makes it a discipline layer rather than a helper is that a held-out project passes with it and fails without. The steers (foreman vs plain, held-out, end-of-run exam) already exist as infrastructure. Assumption: held-out whole projects exist on this box.
  Done when: `samo decide --bench` prints one pass/fail per slot per held-out project, and the ship gate fails when any adopted slot regresses below its baseline.

- **The decider is the next user, not a helper** — FEATURE — value 5 — effort M — risk med — category: blind spots
  Why: the user's words ("generic… other things made with sampo", "brainstorm on features the model should have") push past the repo; the deepest unspoken need is a model that *is* the user, so Sampo works on any project the user touches without per-repo setup.
  Done when: a fresh project with 5 closed briefs gets a decider that answers 3 of 4 routine asks the user would have made, with abstain on the fourth.

- **Wild — Bet the Ward on the model, but the model may only *tighten*** — SECURITY — value 5 — effort M — risk high — category: privacy
  Why: T-2967 shows the guard's core protection breaks on a migrated path; a model that learns *what this user never accepts* (undo rate per capability, per steer) turns the Ward from a rule list into a taste model. The steers ("Ward refuses under the Sampo names") demand this stay local and strict.
  Done when: a Ward block carries a model confidence and a "tightened by model" tag, and a "model gone" week shows the rule-based Ward still blocks everything the model blocked.

- **Wild — Federate *regret*, not weights, across the user's own machines** — SECURITY — value 4 — effort L — risk med — category: privacy
  Why: the user steers "manage all of that across sessions… not only one machine"; the pack's fleet part (T-3321) handles claims, not learning. Federating only the user's undo/accept *regret labels* (never text) lets the decider learn across projects without the training lake leaving the machine.
  Done when: two machines on the same user see a combined regret score per slot; a redaction scan proves no brief text crosses.

- **One decision, one typed sentence, or silence — and nothing else the model can say** — CLEAN — value 5 — effort S — risk low — category: capability map
  Why: T-2912's silent-cut scan found 4-file and 10-rule cuts; a constrained grammar for every typed decision (block/close/abstain with a bounded repair) makes the decider's whole output surface auditable and replayable. This is the smallest bet that makes every other slot honest.
  Done when: every model verdict parses against the grammar; a malformed output triggers the rules fallback and is logged with a typed stall cause.

- **Train on *regret*, never on labels — the user's undo is the only ground truth** — FEATURE — value 5 — effort M — risk med — category: approaches
  Why: the user's undo is the pack's strongest signal (T-2967's undo that doesn't stick; the standing rule that the user's pushback is the best data). A self-supervised "next ledger event" target where undo is the positive class means zero hand-labelling and the model's job is literally "predict what I'll undo."
  Done when: a retrain command `samo decide train` produces a model whose "will this close hold?" head scores above the rules baseline on held-out undos.

- **Cold-start a brand-new project by *project fingerprint*, zero-shot, in minutes** — FEATURE — value 4 — effort M — risk low — category: capability map
  Why: "generic across every project" means the first project on a new machine gets nothing; a fingerprint (stack, verb usage, steer density) retrieves the nearest sibling's decider priors without sharing text. This is the capability a best-in-class version has and the pack doesn't show.
  Done when: `samo init` on a fresh repo prints "nearest siblings: X, Y; priors loaded" and the first 3 decider calls abstain less than 50%.

- **Wild — Run the model as an *adversary* in its own exam: the Ward's attacker is the decider** — SECURITY — value 4 — effort L — risk med — category: agents
  Why: the standing rule "weakness-finding uses signals Foreman didn't author" and the Ward's history of over-refusal (pgrep self-match) demand an adversarial arm. A decider that *tries to get past* its own guard and its own close-verifier turns the exam into a zero-sum game where only the strongest rules survive.
  Done when: a nightly `samo exam --adversary` run produces a "Ward survived N attacks" line and files a fix task for each attack that got through.

- **Invert the teacher: let the 0.6–4B student grade the 27B, and promote the student only when it beats the teacher** — PERFORMANCE — value 4 — effort M — risk med — category: approaches
  Why: the pack's uplift work (T-2912, small-model cards) shows local models are the bottleneck; distilling *from* the 27B is the obvious path, but the bet is to make the student the gatekeeper. A 0.6B that grades a 27B run's "did this close hold?" at 90% of the teacher's accuracy, at 1/50 the cost, changes the whole serving economics.
  Done when: a `samo decide --model 0.6b` head on the close-verifier slot scores within 5% of the 27B head on the same held-out set, and the serving cost per close drops 10×.

- **Wild — Ship a frozen "museum" decider as a permanent tripwire: the first model, re-run on every close forever** — PERFORMANCE — value 3 — effort S — risk low — category: capability map
  Why: every retrain risks silent drift; a frozen copy of generation 1's decider, re-run on every close in shadow, catches the moment a newer model's verdicts drift from the original. This is the cheapest possible bet and the pack's "champion/challenger registry" idea, reduced to its minimum.
  Done when: `samo decide --museum` prints a "drift: 3 slots changed verdict vs gen-1" line, and a regression task is filed for any slot with >10% drift.

- **Make "will this close hold?" the first trained head, labelled by the user's own undo, and give it a veto on close** — FEATURE — value 5 — effort M — risk med — category: capability map
  Why: the pack's open work (T-0035 eval capture, T-1231 Foreman beats Claude) all hinge on close quality; the user's undo is the label. This is the single most valuable slot: if the model can say "this close will not hold" *before* the user undoes it, Sampo has earned its tokens.
  Done when: the close-verifier head, called at `samo task finish`, prints "close holds: no (confidence 0.83, 2 similar undos in last 30 days)" and the task stays open.

- **Wild — The decider writes the next Moonshot before you ask, scored wildness 1–5 by the cold reviewer** — FEATURE — value 3 — effort M — risk med — category: delight
  Why: the standing rule "Moonshots must be wild" and the funnel's 10,000-candidate pipeline mean the model's most playful output is the one nobody asked for. A decider that, at night, reads the ledger and drafts one Moonshot in the user's voice, scored by the existing cold reviewer, turns the model into a co-author of the tower's own future.
  Done when: a nightly `samo moon --draft` produces one Moonshot with a wildness score, and the user can accept, reject or edit it with one keystroke.

- **Prove genericity with a redaction and leak scan on every artefact, before any weights leave the machine** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the request is "generic across every project"; the moment a trained model encodes one project's briefs, every other project's decider calls are a privacy leak. A content-hash-pinned, redaction-scanned artefact is the minimum bet that makes "generic" honest.
  Done when: `samo decide --scan` runs on every retrain, and the output is "no project names, no user phrases, N rows quarantined" or the retrain is blocked.

- **Wild — Bet on *predicting the user's next bad week* and pre-stage the fix** — FEATURE — value 4 — effort L — risk high — category: blind spots
  Why: the user's silence and the "what I got wrong about you" confession idea point to a model that learns the user's *rhythm* — the weeks where pushes pile up, undos spike, and Sampo should be quieter. Pre-staging the fix (the one brief the user will re-ask, the one steer they'll re-type) before the bad week starts is the boldest unspoken need.
  Done when: a `samo decide --forecast` line in the morning card says "next week: likely re-ask of X, likely steer re-type of Y; pre-staged" and the user confirms or strikes with one key.

- **Do less: ship the data export, the kNN oracle, and the abstain contract only; defer all training** — CLEAN — value 4 — effort S — risk low — category: approaches
  Why: the pack's 2,900 closed briefs and the existing bge-m3 embeddings mean a retrieval-only decider (kNN over closed briefs, with a calibrated abstain) is buildable in a day and is the honest baseline every trained model must beat. The bet is that the baseline *is* the product until a trained head proves a measured gain.
  Done when: `samo decide --knn` answers 3 of 5 routine asks on a held-out project, abstains on the other 2, and a trained head must beat this score by 10% before it is adopted.
