# Brainstorm — lens: learning from outcomes

- **Build an outcome ledger that joins every decision to its eventual fate** — FEATURE — value 5 — effort M — risk low — category: outcomes
  Why: the pack has lessons, decisions, vetoes, hypotheses, plans and "done" claims in separate stores; the earlier ideas score each in isolation (lesson confidence, regret, rework). Assumption: a single table keyed by task id (approach chosen, agent lane, model, plan passes run, lessons recalled, gate results, later reverts or user corrections, days survived) does not exist yet. It is the substrate every other learning loop needs.
  Done when: `fm outcomes T-xxxx` prints one row per decision made on a finished task with its 7-day and 30-day fate (survived / reverted / corrected / reopened), and a test seeds a revert and sees it attributed to the right decision.

- **Attribute each failure to a pipeline stage** — FEATURE — value 5 — effort M — risk low — category: attribution
  Why: friction digests show blocks, corrections and steers, but not which stage of intake → plan → execute → verify let the problem through. Assumption: corrections are tagged only by symptom. Learning needs "this was a misread at intake" vs "plan missed a step" vs "gate couldn't see it".
  Done when: each correction or reopened task carries a stage label (intake, plan, build, verify, merge, spec-was-ambiguous), and `fm friction` ranks stages by count over the last 30 tasks.

- **Run a counterfactual replay to see whether a pass or agent mattered** — FEATURE — value 4 — effort L — risk med — category: counterfactual
  Why: "Yield-rank planning passes" and "audit which passes change anything" exist as ideas, but they need the cheap mechanism: replay a finished task's brief with one pass or lens removed (using fm bench machinery) and compare plan and outcome. Assumption: fm bench can replay a brief headlessly.
  Done when: `fm ablate T-xxxx --without second-opinion` produces a diff of the resulting plan and gate outcome against the original, and records "changed / unchanged" into the outcome ledger.

- **Hold delayed-feedback checkpoints on every closed task** — FEATURE — value 4 — effort S — risk low — category: follow-up
  Why: the done gate judges at close, but real outcomes arrive later (the user's next message, a revert, a bug filed such as T-0317 "There's new bug feedback"). Assumption: nothing re-visits closed tasks.
  Done when: the drive, on a task closed 3 and 14 days ago, runs a cheap check (revert in git log? file churn? user complaint mentioning its id or files?) and appends a verdict event; a test fakes a revert and sees it flagged.

- **Keep a per-agent-type scorecard from verdicts and later fate** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: fm-builder, reviewer, recon, scout and debugger are fixed roles with no measured record. Assumption: lane results and later reverts can be joined. Score each by first-pass gate rate, reviewer findings that were later vindicated, scout answers later proved wrong.
  Done when: `fm agents scores` lists each agent type and lens with n, hit rate and false-alarm rate, and the dispatcher cites the score when it picks a lane.

- **Learn the real cost of each plan step type** — PERFORMANCE — value 3 — effort M — risk low — category: estimation
  Why: the pack lists estimate/pace ideas but not a learned decomposition model. Assumption: ledger timestamps per step exist. Mining "steps of kind X take Y minutes and fail Z% of the time" lets the planner order and size steps from data instead of guesses.
  Done when: the planning pass prints a predicted duration and failure probability per step drawn from at least 10 similar past steps, and a backtest shows the prediction error on held-out tasks.

- **Convert every user steer into a graded rule candidate with an expiry trial** — FEATURE — value 4 — effort M — risk med — category: preference learning
  Why: the user's steers ("budget limits shouldn't block until 75% usage", "cleanup never got done") arrive as one-off words. Assumption: they become lessons only manually. Propose them as probationary rules for N tasks, and promote only if the steer doesn't recur.
  Done when: a steer creates a probation rule with a counter; after N tasks without a recurrence it becomes permanent, and if the same steer recurs the rule is escalated to a gate.

- **Mine "first-time-right" tasks for what they had in common** — FEATURE — value 3 — effort M — risk low — category: success patterns
  Why: all existing learning is failure-driven (friction, blocks, dead-ends). Success is equally informative: compare briefs, plan shape and recalled lessons between tasks that passed first try and those that needed retries.
  Done when: `fm friction --wins` prints the features that separate the two groups with counts, and flags any that are statistically unremarkable.

- **Wild: Let rejected ideas come back to life when the world changes** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: wild. The brainstorm queue holds hundreds of ideas, dropped ones included. Store each rejection's kill reason as a testable condition (a model release, a dependency change, a usage-pace figure) and re-offer the idea when it flips.
  Done when: a dropped idea with kill reason "needs Codex grants" is re-surfaced by the drive when T-0335 closes.

- **Wild: Keep a "Foreman's track record" page that the model reads before claiming confidence** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: wild. Before the main thread writes "done" or states a confidence, it receives one line of its own historical hit rate for this task type and tier ("FIX M: 82% held after 14 days"). Assumption: calibration ideas exist but not this inline injection.
  Done when: the done-gate output includes the track-record line, and it changes when seeded outcomes change.

- **Wild: Run a "lessons tournament" where lessons compete on held-out tasks** — FEATURE — value 3 — effort L — risk med — category: lessons
  Why: wild. Existing ideas score lessons by recall-then-pass. Instead replay held-out finished tasks with and without each lesson in injected context and keep those that win, retiring the rest.
  Done when: `fm lessons tournament` outputs per-lesson win/loss versus the baseline over at least 10 replays and marks losers for retirement.

- **Wild: Write a one-line "what I'd do differently" at every task close and aggregate them weekly** — FEATURE — value 3 — effort S — risk low — category: retrospectives
  Why: wild. A mandatory forward-looking sentence from the builder, checked next week against whether the same situation recurred and whether the advice was followed — a tiny, cheap loop that makes learning legible to the user.
  Done when: the close-out requires the field, a weekly digest clusters them, and any unfollowed repeated advice is flagged.
