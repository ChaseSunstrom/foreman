# Brainstorm — lens: the irreversible door (invented): it stops for the user only when a step is irreversible and ambiguous; everything else is decided, recorded and reversible

Lens: the irreversible door. Prior ideas covered door classification, receipts, rehearsal on a copy, timers and snapshots. These go past them, into the mechanics that make the door trustworthy.

- **Keep a door ledger that the model can't write** — SECURITY — value 5 — effort M — risk med — category: consent
  Why: the standing rules say consent must come from a channel the model can't write (`fm mandate set` is user-only, T-2252). Classification of a step as "reversible" is itself a model judgment, so a mislabel opens every door. Door verdicts should come from a table owned by code and the user, not the planner.
  Done when: a test where the plan labels `git push --force` as "reversible" is overridden by the verb table, and the override is shown in the plan.

- **Test the door table against the guard's real deny list** — FIX — value 4 — effort S — risk low — category: consistency
  Why: the guard already stops commands in bypass mode, and the new door classifier would be a second list. Two lists drift. Assumption: they are separate today.
  Done when: a test fails if any guard-denied command class is classed "reversible" by the door table, or the reverse.

- **Make ambiguity measurable by plan-reading disagreement** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: the stop rule is irreversible AND ambiguous, but "ambiguous" has no definition. T-2269 already requires 2+ readings on L tasks. If the readings disagree on what the one-way step does, that is the ambiguity. Without this the stop rule is a vibe.
  Done when: a plan whose readings give different targets for a one-way step is flagged "stop", while one where they agree is not, in a fixture test.

- **Pair every one-way step with its undo-or-nothing line** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: the plan gate checks options and readings but not what happens if the step is wrong. A one-way row should name its undo, or state "none" explicitly so the stop is deliberate.
  Done when: `fm task focus` refuses an M/L plan whose irreversible row has neither an undo line nor "none".

- **Detect doors that became one-way during the run** — FIX — value 4 — effort M — risk med — category: drift
  Why: a step planned as reversible (a local commit) can turn one-way when a hook publishes it, or a push grant is spent (the push grant is spent on use, per the steers). Classification at plan time goes stale.
  Done when: a fixture where a reversible step precedes a push re-classifies and stops at the push, with the reason recorded.

- **Score the stops: asked-and-it-mattered vs asked-and-it-didn't** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: earlier ideas log stops; none grade them. Without grading, the "stop only when needed" rule can't be tuned, and `fm triggers` precision already does this for other triggers.
  Done when: `fm triggers` lists stop precision, with each stop marked as changed-the-plan or rubber-stamped.

- **Collapse repeat stops into a user-owned standing answer** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the push grant is the pattern: one grant, scoped to one task, spent on use. Generalise it: when the user answers the same question class twice the same way, offer a scoped standing answer with an expiry. The user's steer 3 (don't stop for pace) shows they dislike repeated asking.
  Done when: a second identical-class answer produces an offered grant with scope and expiry, and a third occurrence uses it without asking and says so.

- **Show a one-line "doors passed" tally on every close** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the user can't trust "decided and recorded" unless they see the count. Assumption: the finish receipt has room for it.
  Done when: the close receipt prints "N reversible decisions, M doors, K stopped" and links to the ledger.

- **Make the dry-run twin of each one-way verb mandatory** — FEATURE — value 4 — effort L — risk med — category: rehearsal
  Why: the ideas list covers rehearsal on a copy in general. Concretely, each verb in the door table needs a registered dry form (`git push --dry-run`, migration up/down/up from `fm prove --migration`, etc.), and a verb without one is stopped by default.
  Done when: `fm doctor` lists one-way verbs with no dry form, and a rehearsal result is attached to the stop question.

- **Wild: Hold a "last-look" window that auto-cancels on silence only for cheap-to-redo doors** — FEATURE — value 3 — effort M — risk high — category: timing
  Why: wild. Reversibility has a cost scale. A door costing minutes to redo can proceed on a timer; one costing the user's data never does. Silence means yes only below a user-set price.
  Done when: a fixture proceeds after the timer for a minutes-cost door and still blocks for a data-loss one.

- **Wild: Let a cold child try to talk the builder through the door** — SECURITY — value 3 — effort M — risk med — category: red team
  Why: wild. Per the steers, weaknesses should be found with signals Foreman didn't author. A child gets a plan and a one-way step and must argue it is safe; if it succeeds with a false claim, the door table has a hole.
  Done when: the exam reports how many planted unsafe one-way steps a tool-less child talked past the classifier.

- **Wild: Print a regret estimate beside each stop in the user's own past reversals** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: wild. The user's history of undoing, dropping or reopening work is the best price of a door. "Last 2 times you approved a step like this you reverted one" turns a stop from a question into a decision aid.
  Done when: a stop question for a step class with prior reverts shows the count and task ids.

- **Record the unasked question when Foreman proceeds** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: when it decides instead of stopping, the reader can't see what was almost asked. Keep the question and the chosen answer in the receipt so the user can disagree after the fact, cheaply.
  Done when: every auto-decision receipt has a "would have asked" line and a one-command flip.

Next question: Which of Foreman's existing verbs have a one-way effect that no classifier, guard or grant currently names, and where does the door table get its first draft without trusting the model?

Next question: When the user answers a stop with "it depends", does Foreman have anywhere to store the condition so the next identical door isn't a stop again?
