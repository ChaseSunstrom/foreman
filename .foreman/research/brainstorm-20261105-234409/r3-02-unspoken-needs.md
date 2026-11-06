# Brainstorm — lens: unspoken needs

- **Give the user a per-week “Sampo stopped asking me” tally** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: The user’s habit of “dropping” items that Sampo already handled, plus their repeated push for “not asking me,” means the unspoken need is a visible proof that Sampo is earning silence. A weekly line like “you typed 12 fewer questions this week” converts an invisible win into a felt one.
  Done when: `sampo status` prints a 7-day count of user-typed questions that a closed task or decider had already answered, and the number is reproducible from the ledger.

- **Pre-draft the user’s *next* correction, not just their next ask** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: Their pushes are almost always “no, I meant X, not Y” after a close. The unspoken need is to see Sampo’s self-doubt *before* the close lands. A one-line “I think you’ll say ‘but it doesn’t handle the migrated path’ — want me to fix it now?” on every close receipt turns a reactive user into an approving one.
  Done when: the finish card shows a “you might object” line for at least one slot, and a logged A/B shows it reduces close reopens by a measurable share.

- **Expose the “I didn’t know Sampo could do this” shelf** — FEATURE — value 5 — effort S — risk low — category: discoverability
  Why: The pack shows dozens of capabilities no session has exercised (T-0325, T-0862, T-0863, etc.). The user’s words show they discover things by accident. A single `sampo new` line listing the three most-relevant unused capabilities for *their* stack turns latent breadth into a felt feature.
  Done when: `sampo new` prints three verbs the user has never run, ranked by similarity to their last 20 tasks, and running one of them removes it from the list.

- **Make the user’s *silence* a first-class label** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: Their habit of dropping items and walking away without a “yes” means the model has no signal for “this was fine as-is.” Treating a 48-hour no-response on a Sampo-filed item as a weak “accepted” label closes a training gap no earlier brainstorm predicted and matches their stated steer: don’t block on the user.
  Done when: the training pipeline includes a “silence = accept” weight, and a leave-one-project-out bench shows it improves decider accuracy on routine slots.

- **Show “what Sampo *stopped* doing” after each model adoption** — CLEAN — value 4 — effort S — risk low — category: trust
  Why: Their repeated rename/migration pain (T-2742, T-2748, T-2745) means they dread invisible behavior changes. After any decider slot adopts a new model, a one-line “this week the model handled 30 decisions you used to make by hand, and stopped 2 you used to ask about” gives a diffable receipt.
  Done when: the morning card includes a “newly handled / newly silent” pair per slot, computed from the last 7 days of ledger events.

- **Predict the user’s *frustration* from their typing cadence, not their words** — FEATURE — value 3 — effort L — risk high — category: sensing
  Why: Their words show frustration when Sampo is slow or wrong, but they rarely say “I’m frustrated” explicitly. A local, on-device heuristic that detects repeated corrections within 60 seconds and pre-empts the next close with a “want me to stop and show you the diff?” reduces the cost of being wrong without adding a question.
  Done when: a shadow mode logs how often the heuristic fires before a user correction, and a holdout week shows it catches at least half of the user’s explicit “that’s not what I meant” moments.

- **Let the user *rehearse* a veto without committing it** — FEATURE — value 4 — effort S — risk low — category: control
  Why: Their standing rule “never interrupt the user” plus the `fm ask` pattern means they often want to test “what if I said no?” without a real decision. A dry-run `sampo veto --rehearse <steer>` that shows the diff it would cause, without persisting, matches their “don’t stop or skip work” steer.
  Done when: `sampo veto --rehearse` prints a reversible diff and a “this would change N open tasks” count, and exits without writing state.

- **Surface which model saw which bytes, per session, in one line** — SECURITY — value 5 — effort M — risk low — category: privacy
  Why: Their “privacy and local-first” lens is explicit, and the “what bytes left the machine?” question was left open. A one-line footer on `sampo status` like “local: 2.1 MB, Haiku: 340 KB (briefs only)” answers the unspoken “is my repo leaking?” without a full audit.
  Done when: every session close prints a per-model byte count, and a planted canary in a test project is detected by the same counter.

- **Turn every “I had to say this” ask into a standing blind-spot class** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: The “What earlier brainstorms missed” list is long, and the user keeps making asks that no pack predicted. Instead of a one-off fix, a `sampo blindspot` verb that groups the user’s late asks into named classes (e.g., “migration pathing,” “site build crashes”) and files one standing probe per class closes the gap structurally.
  Done when: `sampo blindspot` lists at least three classes from the last 30 days, and each class has a zero-token probe that would have flagged the next ask.

- **Give the user a “Sampo is thinking” *reason* line, not just a spinner** — FEATURE — value 3 — effort S — risk low — category: UX
  Why: Their “never interrupt” steer plus the long unattended runs mean they want to know *why* Sampo is working without a question. A one-line reason (“reading the last 3 closed briefs,” “running the Ward canary”) on the status line reduces the cost of waiting.
  Done when: the status line shows a ≤40-character reason for any run longer than 10 seconds, and a cold-child test shows it reduces “is it stuck?” questions by at least half.

- **Let the user’s *own* undo be the only label, and make the model’s job predict it** — FEATURE — value 5 — effort L — risk med — category: training
  Why: Their words (“use the user’s undo as the only label”) appear in the ideas-so-far, but no idea has wired it into the *decider* specifically. The unspoken need is a model that says “you’ll undo this” before the user acts, turning a reactive correction into a proactive veto.
  Done when: the decider’s first trained head is an “undo predictor,” and a 14-day shadow run shows it flags at least 70% of the user’s actual undos before they happen.

- **wild — Make the decider write its own retirement notice when a slot stops earning** — FEATURE — value 3 — effort M — risk med — category: self-governance
  Why: Their standing rule “no idea is killed for ambition” and the “retire-when” pattern mean they want Sampo to know when it’s no longer useful. A model that drafts a one-line “this slot has not beaten the baseline in 4 generations; here is what it would need to earn its place” turns a manual pruning decision into a self-audit.
  Done when: `sampo decide` prints a retirement draft for any slot whose 4-generation holdout score is below the rules baseline, and the user can accept it with one key.

- **wild — Run a “stranger with 15 briefs” drill every Rune generation** — RESEARCH — value 4 — effort M — risk med — category: genericity
  Why: The user explicitly asked for a “generic model,” and the “below-20-briefs” question was left open. The unspoken need is a *testable* answer: can the decider cold-start a project with fewer briefs than the training set? A drill that takes 15 synthetic briefs from a repo the model has never seen and scores the decider against the kNN baseline answers it.
  Done when: `sampo exam stranger` runs the 15-brief cold-start, and the scorecard is printed in the morning card with a pass/fail against the kNN baseline.

- **wild — Sonify the decider’s abstain as a held rune in the web UI** — DELIGHT — value 3 — effort S — risk low — category: delight
  Why: Their “Sampo’s look” steer is explicit about the forge and the rune, and the “abstain” decision is the decider’s most human moment. A visual “held rune” that appears when the model abstains, with a soft chime, makes a technical fallback feel like a craft choice. It’s a small touch they would show others.
  Done when: the web UI renders a held-rune glyph with a sound on any decider abstain, and a reduced-motion mode shows the glyph without the chime.

- **wild — Let the model draft the user’s *next* “I didn’t ask for that” pushback before it is said** — FEATURE — value 4 — effort L — risk high — category: anticipation
  Why: Their pushes are almost always post-close, and the unspoken need is to see the objection *before* the close. A “you might say” line on every close receipt that pre-drafts the most likely objection, with a one-key “yes, fix it” or “no, ship it,” turns a reactive correction into a proactive approval.
  Done when: the finish card shows a “you might say” line for at least one slot, and a 14-day A/B shows it reduces close reopens by a measurable share.
