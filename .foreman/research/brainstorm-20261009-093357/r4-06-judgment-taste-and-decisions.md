# Brainstorm — lens: judgment, taste and decisions

- **Route every fork through one judgment call** — FEATURE — value 5 — effort L — risk med — category: judgment core
  Why: the pack lists many separate pieces (precedence order, precedent file, stakes pricing, vetoes, decisions, asks ledger) but no single place where a fork gets decided. Assumption: today each skill improvises its own ask-or-proceed call.
  Done when: `fm judge <fork>` returns proceed/ask/defer/refuse plus a basis that cites the user quote, veto, precedent or stakes class. A fixture of 20 past forks reproduces the recorded user outcome for at least 17.

- **Surface the implicit decisions in every diff** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: assumption: builders make unrequested design choices (new dependency, abstraction, public name, config key) that nobody reviews. The existing drift ideas compare diff to brief, not choices to the user's say.
  Done when: closing a task lists each added dependency, public symbol and config key not named in the brief as a "calls I made". A test diff adding a new dep with an unmentioned name shows up in the list.

- **Make every decision flippable with a prepared runner-up** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: decisions already have revisit triggers. When one fires, flipping it means replanning from scratch. Assumption: the runner-up's switching cost is known at decision time and can be recorded.
  Done when: `fm decide --flip D-n` lists the runner-up's recorded steps and the files affected, and creates the follow-up task. A decision recorded without a runner-up is rejected for M/L tasks.

- **Learn taste from the user's overwrites of agent code** — FEATURE — value 5 — effort M — risk med — category: taste
  Why: the first brainstorm planned a taste model, and T-0439 holds the "Taste model and user portrait" idea. Its strongest signal is untapped: lines the user rewrites after the agent wrote them. The pack has "tell the user's edits from the agent's" as an idea but no consumer.
  Done when: after the user edits a file in a Foreman-finished task, `fm taste` proposes a candidate rule with the before/after hunk as its example. Rejecting it records a veto.

- **Promote taste inferences only after three unlike cases** — FEATURE — value 4 — effort S — risk low — category: taste
  Why: the user dropped YAGNI-style over-generalisation before (the `fm task new … && <edit>` guard loosening). A taste model that generalises from one steer will over-fit. Assumption: inferred rules currently apply after one occurrence.
  Done when: a candidate stays "probation" and only advises until three cases in different files or tasks confirm it. A test with two same-file cases leaves it in probation.

- **Audit nuisance controls for a quiet-until-it-matters threshold** — CLEAN — value 4 — effort M — risk low — category: proportionality
  Why: the user steered "budget/pace limits shouldn't block anything until 75% usage" and rejected hard caps on subagents. The same pattern probably holds for other gates and limits. Assumption: other limits still act early.
  Done when: `fm doctor` lists every blocking limit with its activation threshold and the number of times it fired below that threshold in the last 30 days. Any limit lacking a declared threshold is flagged.

- **Judge whether a mid-task message preempts the task** — FEATURE — value 4 — effort M — risk med — category: intake judgment
  Why: Foreman captures new requests instead of chasing them, which is right most of the time. A "prod is down" message and a "someday" message look the same to it. Assumption: there is no urgency class today.
  Done when: capture tags each mid-task message as steer, preempt or later using wording and the open task's state. A test set with an "it's on fire" message pauses the task with a resume point, and a casual idea does not.

- **Arbitrate between the user's preference and the repo's convention** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: assumption: builders follow whichever instruction is nearer, and the user never learns the two disagreed. The precedence idea covers the user's own words, not the repo's.
  Done when: when a request contradicts a convention that `fm map` detected, the brief records a one-line conflict and the winner, and that winner is reused for the same area afterwards.

- **Re-rank audit findings by what this user acts on** — FEATURE — value 4 — effort M — risk low — category: review judgment
  Why: T-0034 (audit run) is deferred, and review packets are ranked by risk and reader time. The user's history of fixing versus waving off each lens's findings isn't used. Assumption: ledger records which findings led to edits.
  Done when: the findings list shows a "likely to matter to you" score per finding, and a replay over past audits ranks acted-on findings above waved-off ones at least 70% of the time.

- **Wild: Pre-write the apology before any one-way call** — FEATURE — value 3 — effort S — risk low — category: irreversible calls
  Why: wild; assumption: if the model can't write the two-sentence "I got this wrong because…" in plain words, it doesn't understand the risk well enough to proceed.
  Done when: one-way-door forks need an apology line in the decision record. An empty or generic line ("something went wrong") fails the gate.

- **Wild: Record a gut call before deliberating, and score it** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild; the pack has deliberation spend and passes ranked by yield, but no baseline of what the first instinct would have chosen. A cheap pre-deliberation answer shows where analysis never changed the outcome.
  Done when: each M/L plan logs a one-line gut pick before the passes run, and `fm friction` reports how often deliberation overturned it and whether the overturned picks did better.

- **Wild: Seat a conscience critic who needs a user quote or stays silent** — FEATURE — value 4 — effort M — risk med — category: taste critic
  Why: wild; critics in the list (devil's advocate, ex-user persona) can speak from opinion. This one may object only by quoting the user's own message, a veto or a decision. Fewer objections, each checkable.
  Done when: every critic objection links a quote that mechanically matches the ledger. A fixture objection with an invented quote is dropped, and objections with a real quote appear in the plan review.
