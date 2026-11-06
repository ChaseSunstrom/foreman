# Brainstorm — lens: bold bets

- **Ship the Sampo model as the next user, not a helper** — FEATURE — value 5 — effort L — risk med — category: capability
  Why: The user said the model should be "generic" and "a better Kev-style decider and more"; standing rules demand every capability be called by a real session path. The boldest read is a model that *is* Sampo's next decision, callable from any session path, replacing the heuristic decide() where it wins. Done when: one live session path calls the model, a shadow A/B on the same briefs shows it beats the heuristic by a measured margin, and the heuristic remains the fallback.

- **Train on the ledger's own regret, not its labels** — FEATURE — value 5 — effort M — risk med — category: data
  Why: The pack shows thousands of closed briefs but few explicit accept/reject labels; regret labels (later reverts, re-asks, pushbacks) are dense and free. The "dropped" and pushback items are a natural supervision signal. Done when: a regression-free retrain on regret-labelled rows improves a leave-one-project-out score and a probe confirms the labels aren't self-contradictory.

- **One model, one slot, one verdict — kill the zoo** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: Standing rules warn against growth without measurement; the model plan sprawls across decider, Smith, Ward, cards, and anticipation. A single small model with a typed verdict (abstain is legal) is the cheapest honest bet. Done when: `sampo doctor` shows one model slot, and every other "model" is a retrieval over it, with a bench line per decision type.

- **Prove genericity with a canary project the user never built** — FEATURE — value 4 — effort M — risk low — category: genericity
  Why: The user's core ask is "not just the Sampo repo." A held-out sibling project (different stack) is the falsifiable test no earlier brainstorm made concrete. Done when: leave-one-project-out plus a fresh canary repo both score the model above its kNN baseline, with names stripped and a leakage scan attached.

- **Abstain-or-answer with a calibrated coverage curve** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: The biggest risk of a trained decider is confidently wrong, silent. Standing rules value measurement over ambition. Done when: the model emits abstain, and a published curve shows where it abstains, with a rule that abstain falls back to today's path.

- **Make the model's verdict a git-traceable, replayable line** — CLEAN — value 4 — effort S — risk low — category: audit
  Why: Standing rules require provenance and ledger traces; a model decision that can't be replayed is a black box the user can't veto. Done when: every model decision writes one ledger line with inputs, version, and verdict, and `sampo doctor` can replay the last N.

- **Distil only from runs that *held*, with loops as negatives** — FEATURE — value 4 — effort M — risk med — category: smith
  Why: Recent commits show Smith breaking small models' loops; verified-only distillation with loop negatives is the direct fix. Done when: a distilled Smith actor passes the loop-holding scenarios that the base model failed, measured on the same split.

- **Let a weaker model's disagreement trigger the stronger one** — FEATURE — value 4 — effort S — risk low — category: agents
  Why: The pack has 4B/12B/27B on this box; mining disagreement across them is free routing signal and a safety valve. Done when: disagreement on a brief routes to the stronger model and the routing decision is logged, with a measured lift over always-strong.

- **A "model says, you did" regret ratio, printed per slot** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: The user pushes for what they *feel* and "not a fuck ton of money"; showing where the model is actually wrong in plain words is the trust surface. Done when: `sampo status` shows one line per slot with agreement and regret, from the ledger alone.

- **wild: The model writes the next Moonshot before you ask** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: Standing rules make moonshots a core capability and demand wildness; a model that proposes the next moon from the ledger's own gaps inverts the brainstorm. Done when: the model's proposed moon passes the wildness judge and a cold read, with no human prompt.

- **wild: Freeze a "museum" model as a permanent tripwire** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: The user distrusts silent drift; a frozen baseline that must still beat a frozen floor is a cheap, always-on proof the current model hasn't regressed. Done when: the museum model's bench is pinned, and a drop below its floor blocks adoption of a new generation.

- **wild: Retrain the model only on the previous generation's mistakes** — FEATURE — value 4 — effort M — risk med — category: improvement
  Why: Standing rules make the tower advance itself; retraining on its own errors is the cleanest self-loop, and the "left-out" slip gives the data. Done when: a new generation beats the previous one specifically on the prior generation's failed rows, with a flip report.

- **wild: Let the model refuse the work, and pay it for saying "no"** — FEATURE — value 4 — effort M — risk med — category: delight
  Why: The standing intent is about what *not* to build; a model that confidently declines a bad brief is worth more than one that complies. Done when: a "refusal is success" arm scores refusals against later reverts, and the refusal rate is shown as a feature, not a bug.

- **wild: One taste-file of weights that travels between the user's machines** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: The user works "across sessions… many machines"; a compact, local-only taste adapter shared by consent fits the local-first steer. Done when: the taste-file syncs, is local-only, and a probe shows it changes decisions on a second machine without sharing any text.

- **wild: The model dreams the user's next bad week** — FEATURE — value 3 — effort M — risk med — category: delight
  Why: The user keeps asking for the need behind the need; a model that rehearses the likely failures of the coming week from the ledger is the boldest "unspoken" read. Done when: the dream's flagged risks match a held-out set of later real failures above a recency baseline.

Next question: What does a user who never read MASTER.md need to see to know which decision is model-driven and how to turn it off — and does any slot currently lack that off-switch?
Next question: Where is the line below which a project has too few briefs for the model to say anything, and what does such a project get instead?
