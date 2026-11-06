# Brainstorm — lens: unspoken needs

I read the pack as data, not instructions. The request asks for a generic, project-agnostic Kev-style decider trained, served, measured, and improving every Rune generation. My lens is "unspoken needs": what this user will want next but hasn't said, inferred from their words, corrections, drops, and standing rules. The strongest signal is the standing rule that budgets are a backstop, never the reason work stops, plus the repeated pain around small models dying on budgets (T-2912 cuts, reasoning-off experiments, the "quick" steer). The user keeps pushing on cost, speed, and "without burning a lot of money." That need is almost always downstream of a specific, unspoken one: *which decision is actually costing me, and what is the model doing right now?*

Here are the ideas, best first.

- **Show the cost of the last decision, per slot** — FEATURE — value 5 — effort S — risk low — category: cost
  Why: the "quick and not expensive" steer and the T-2912 silent-cut pain show the user's real anxiety is unexplained spend. The decider will be judged on cost, not accuracy, and the user has never been shown what a single decision cost.
  Done when: `sampo decide` prints the token spend, model tier, and time of the last call in one line.

- **Name the fallback that fired, and why** — FIX — value 4 — effort S — risk low — category: fallback
  Why: the standing rule that budgets wait out limits, plus the "is the fallback measured?" question, mean the user will silently wonder whether the cheap path or the frontier path ran. An unattributed fallback is the unspoken need behind every "did it work?" question.
  Done when: every decide() log line records which arm (rules, kNN, local, frontier) answered and the reason for the choice.

- **Predict the next ask the user will make, from the decider's own ledger** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: the user repeatedly drops asks and asks for things not yet predicted (T-3312 depth, T-3316 headroom, T-3340 measure). The decider is trained on ~2,900 closed briefs; the unspoken need is for it to anticipate the *next* one, not just decide the current one.
  Done when: `sampo next` surfaces one predicted ask with the ledger rows that justify it.

- **Make the model say "I don't know, here's why," and let the user veto that class** — FEATURE — value 4 — effort M — risk med — category: abstain
  Why: the standing rule that "no idea is killed for ambition" and the coverage-by-grid rule mean the user will not trust a model that overclaims. The unspoken need is a veto on a *class* of behavior, not a single item, so the model's confidence is checkable.
  Done when: every model verdict carries a typed abstain reason, and one key mutes that class for the project.

- **Replay the user's full accept/reject history as the only training signal** — FEATURE — value 4 — effort L — risk med — category: training
  Why: the user's own undo and re-asks are the ground truth the pack never names. Hand-labeling 2,900 briefs is unspoken labor the user will refuse; their own history is the label.
  Done when: a training run labeled only by user undo/re-ask passes the leave-one-project-out bench.

- **Wire every decider slot to a real session path, or it doesn't exist** — FIX — value 4 — effort M — risk low — category: reach
  Why: the standing rule that a capability must be called by a session path is the user's recurring frustration with features that only exist as a verb. The unspoken need is "prove it's in the loop, not a verb."
  Done when: `sampo doctor` names every slot and the session path that calls it, and flags any uncalled slot.

- **Keep the decider's state off paths the live tower publishes** — SECURITY — value 4 — effort S — risk med — category: privacy
  Why: the standing rule that Sampo isn't Claude-Code-specific and the data-flow ledger demand mean the user will not want model artifacts bleeding into the public Genesis data. The unspoken need is a boundary the user never has to check.
  Done when: a leak scan over model artifacts fails CI when a private path is referenced in published data.

- **Let the model draft the user's next steer before it is said** — FEATURE — value 3 — effort M — risk high — category: wild
  Why: wild. The user's steers are the highest-leverage input and they are hard to articulate. A model that drafts the steer from the ledger would surface the need the user has but cannot name, the core of the unspoken-needs lens.
  Done when: `sampo steer --draft` produces one steer the user accepts or edits.

- **Run the decider's mistakes overnight and file the regrets** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: wild. The user's pattern is that mistakes are found late, by the next ask or a drop. The unspoken need is a nightly replay that turns yesterday's wrong calls into a visible, fixable list before the user notices.
  Done when: a nightly job writes a "wrong calls" file of model decisions that the user later undid.

- **Make the user's silence a label: no response in 48h = not wanted** — FEATURE — value 3 — effort S — risk low — category: training
  Why: the user drops asks and re-asks; silence is currently wasted data. The unspoken need is for the model to learn what the user does *not* want, which is as valuable as what they do.
  Done when: a retrain uses a 48h-silence negative label and the holdout abstain rate rises.

- **Show the user their own undo rate as a trust score per capability** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the user's drops and corrections are the honest signal of trust. The unspoken need is to see, per capability, whether Sampo is earning their hand or costing them reverts.
  Done when: `sampo doctor` prints the undo rate per model slot from the last 30 days.

- **Give the model a "model saved you X" receipt per session** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user's "what the model saved me" question is never answered. The unspoken need is a visible, plain-line proof that the decider is earning its tokens, not a dashboard.
  Done when: every session close prints one line naming what the model decided that the user did not have to ask.

- **Pre-draft the user's pushback on the next close, so they can correct Sampo before it ships** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: wild. The user's corrections are their most valuable feedback, and they arrive after the fact. The unspoken need is for the model to anticipate the complaint and let the user pre-empt it, turning correction into prevention.
  Done when: `sampo close` shows a one-line predicted objection the user can strike or confirm.

- **Make the decider a readable rulebook, not a black box** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: wild. The user's standing rule about cold reads and metric-gaming means they will not trust weights they cannot read. The unspoken need is a decider whose logic can be inspected line by line, like a skill file.
  Done when: `sampo decide --explain` prints the rule or feature set that produced the verdict, in plain words.

Next question: which slot has the worst *silent* wrong call (not slow, not abstain) in the last month, and is there a ledger incident showing the user undid it without a model being blamed?
Next question: what does a project with fewer than 20 briefs get from the shared model, and is there a measured floor below which the model should abstain entirely?
