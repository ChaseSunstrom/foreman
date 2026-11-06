# Brainstorm — lens: user value

- **Show "what I stopped doing" after each model adoption** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: User's words: "measure what the user feels" and "tell the user what the model changed in plain words." Every adopt decision needs a human-readable diff: which routine asks it now answers, which stalls it removes, which cost it saves — one sentence, one number.
  Done when: `sampo model adopt SLOT` prints a "you no longer have to…" line with a 30-day projected minutes-saved, verified against the ledger.

- **Pre-draft the user's pushback on the next close** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: User steers: "I don't want to just cap the cost… I want it to still get done without burning a fuck ton of money, and quick" and "never interrupt the user mid-run." The model's job isn't just to decide — it's to surface the objection before it's voiced, so the close ships once.
  Done when: on `sampo task prove`, a one-line "you might say: …" card appears, and 4 of 10 real closes match a user's next message within 30 days.

- **Print "the one thing I'd ask you if I could" at session close** — FEATURE — value 4 — effort S — risk low — category: unspoken needs
  Why: User's standing rule: "never block on the user for a question about rules, gates or process." But the model *does* know what it can't do alone. One honest line beats a silent miss.
  Done when: every session close prints at most one unresolvable question, and the next pack's "missed asks" includes it.

- **Make the model's abstain a first-class receipt** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: User's words: "show which slots use a model, with a user veto" and "make every model abstain." A silent fallback erodes trust; a named abstain with the reason ("3 nearest briefs disagree") is a feature.
  Done when: every model slot prints `abstain: <reason>` in the close line, and `sampo doctor` shows a per-slot abstain rate.

- **Predict "you'll re-ask this in 6 days"** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: User's words: "learn the user's accept/reject history as an interruption filter" and the repeated "left out" slips. The model should predict which closes the user will reopen, and say so up front.
  Done when: on close, a "you might ask again about: X" line appears, scored against the user's actual re-asks over 30 days.

- **Turn each repeated correction into a one-line steer candidate** — FEATURE — value 5 — effort M — risk low — category: unspoken needs
  Why: User's standing rule: "every user steer becomes a standing rule plus an automatic check." The model should mine its own ledger for corrections the user made 3+ times and offer the steer draft, not wait for it.
  Done when: `sampo learn` lists top 3 repeated corrections with a one-line steer proposal, and one lands per generation.

- **Show "Sampo saved you X this week" in the morning card** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: User's words: "measure what the user feels" and "print a measured 'minutes returned' receipt." The model's value must be visible in plain words, not a dashboard.
  Done when: the morning card has a "saved you: N tasks, M minutes" line, computed from the ledger, with a link to the receipts.

- **Let the user veto a *class* of model decisions, not just one** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: User's words: "show which slots use a model, with a user veto." A single-item veto is too fine-grained; "I don't want the model deciding which tests to run" is the real unit.
  Done when: `sampo model veto CLASS` disables an entire slot family, and the next close shows the rules fallback in use.

- **Draft the "I'll be annoyed if…" line at intake** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: User's words: "hold a 'wrong-done' recording when a user says it was not done" and "turn each pushback into a probe." The model should infer the user's frustration trigger at intake and make it a clause.
  Done when: at `sampo task add`, a "you'll be annoyed if: …" line is suggested, and it becomes a done-clause.

- **Wild: the model writes the next Moonshot before you ask** — FEATURE — value 4 — effort L — risk med — category: wild
  Why: User's words: "Moonshots must be wild" and "no idea is killed for ambition." The model, trained on the user's own accept/reject history, should propose the next wild idea unattended, not wait for a brainstorm.
  Done when: once per generation, the model files a Moonshot brief with a wildness score ≥ 4, and the user's next pack includes it.

- **Wild: replay the user's last 30 days through the free arm and print the counterfactual** — FEATURE — value 5 — effort M — risk low — category: wild
  Why: User's words: "measure what the user feels" and "foreman vs plain on the same held-out scenarios." The model should show what would have happened *without* it, so the user knows the value.
  Done when: `sampo replay --days 30` prints "without the model: N tasks would have stalled, M re-asks, X minutes lost" and the user can compare.

- **Wild: train a "user twin" that drafts steers before they're said** — FEATURE — value 4 — effort L — risk high — category: wild
  Why: User's words: "learn the user's accept/reject taste to pre-rank moons and pre-answer asks" and "the model that reads the user's frustration." The model should draft the steer the user would have given, so the user confirms instead of correcting.
  Done when: on close, a "you might steer: …" line appears, and 3 of 10 match a user's actual steer within 30 days.

Next question: what does a "saved you" number look like when the model abstained, and does the user still count it as value?  
Next question: which model slot's abstain rate is highest, and is it a signal the model is too cautious or the data is too sparse?
