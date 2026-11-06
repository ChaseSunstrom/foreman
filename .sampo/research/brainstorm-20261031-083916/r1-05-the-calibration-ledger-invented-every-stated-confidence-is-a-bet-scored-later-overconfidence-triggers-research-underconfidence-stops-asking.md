# Brainstorm — lens: the calibration ledger (invented): every stated confidence is a bet scored later; overconfidence triggers research, underconfidence stops asking

- **Record a confidence on every assumption and decision, then score it at close**: FEATURE, value 5, effort M, risk low. Category: calibration.
  Why: T-2290 predicts only minutes and attempts, and T-2269 gates "low-confidence assumptions" without any record of whether those confidences were right.
  Done when: `fm calibration` prints a Brier score per tier and kind from at least 10 closed tasks, and a task with an unscored confidence fails `fm check`.

- **Trigger research on overconfidence, not on a keyword**: FEATURE, value 5, effort M, risk med. Category: research trigger.
  Why: the seed row "unsure → research trigger (3)" needs a definition of "unsure". Assumption: a bucket such as "stated ≥90%, missed ≥20%" is a better signal than self-reported doubt.
  Done when: a fixture ledger with an overconfident bucket makes the next plan claim in that bucket require a research note, and a well-calibrated bucket does not.

- **Stop asking the user once a question class is predictable**: FEATURE, value 5, effort M, risk med. Category: underconfidence.
  Why: steer 3 says don't stop for non-blockers, and the Mission 5 text says to stop "only when irreversible and ambiguous". Assumption: past `fm ask` answers like "your call" or "default" show which classes need no asking.
  Done when: a class answered "default" 3 or more times in a row is decided and recorded without asking, and the record names the ledger rows that justified skipping the question.

- **Classify decisions as reversible or not from a verb table**: FEATURE, value 4, effort S, risk low. Category: stop rule.
  Why: the Mission 5 text makes irreversibility the one reason to stop, but nothing in the pack names a classifier. The guard and `fm ship` already know the dangerous verbs (push, migrate, delete).
  Done when: a decision touching an irreversible verb with confidence under the threshold raises one `fm ask`, and the same decision on a reversible verb is decided and logged.

- **Cap a done claim's confidence by its evidence kind**: FIX, value 4, effort S, risk low. Category: verification.
  Why: the unproven rollup counts typed or inconclusive evidence, but the stated confidence beside it isn't tied to that evidence. Assumption: typed evidence should cap confidence at about 0.6 and a run at 0.95.
  Done when: closing a task on typed evidence with a stated 0.95 is refused or auto-lowered, and the unproven rollup shows the capped number.

- **Score the cold-read judges against later outcomes**: FEATURE, value 4, effort M, risk low. Category: judge calibration.
  Why: this answers the left-over question about a model on both sides with no user-owned check. T-2246 makes a FAIL block only when it quotes a charter clause, but nobody scores the PASS/FAIL calls against later reverts or reopens.
  Done when: each cold-read verdict stores a confidence, and `fm calibration --judges` shows hit rates per judge model and per file kind.

- **Learn the racing threshold from the ledger**: PERFORMANCE, value 4, effort M, risk med. Category: race trigger.
  Why: T-2271 races the runner-up after exactly 3 failed runs. Assumption: lower confidence in the primary approach at plan time should race earlier, and high calibrated confidence should race later.
  Done when: a replay over closed tasks shows the learned trigger reaching the winning approach in fewer runs than the fixed 3, or the old rule is kept with the numbers recorded.

- **Spend research only where the expected loss exceeds its cost**: FEATURE, value 4, effort M, risk med. Category: value of information.
  Why: research has a cost in tokens and minutes, which T-2290 already measures. Assumption: research is worth it when (1 − p) × the cost of a miss is greater than the research cost.
  Done when: a low-confidence, high-blast-radius row (from T-2277) triggers a research task, and the same confidence on a one-line S row is decided and logged without one.

- **Let confidence decay when the files it rests on change**: FEATURE, value 3, effort M, risk low. Category: staleness.
  Why: blast radius already records scope paths, and a plan's confidence goes stale after a rebase or a merge into those paths. Assumption: no current check ties the two.
  Done when: changing a file in a task's scope after focus marks that task's assumptions "re-state", and the next plan gate demands a refreshed confidence.

- **Predict whether the user will accept each plan row**: FEATURE, value 3, effort M, risk med. Category: user model.
  Why: this answers the left-over question about the smallest plan edit made after acceptance. Recorded edits and vetoes are a free label set.
  Done when: each row carries a predicted accept probability, and the report shows the hit rate over the last 20 plans.

- **Wild: run a betting market between racing lanes**: FEATURE, value 3, effort M, risk med. Category: race. Each lane's builder, and a cold model that sees only the briefs, bets on which approach wins before the race runs. The bets are scored, which shows whether the stated confidence predicts evidence.
  Done when: a race records the bets, and `fm calibration` reports the win rate of the favourite.

- **Wild: forecast the diff before building**: FEATURE, value 3, effort S, risk low. Category: surprise. The agent predicts the files touched, the test count and the size of the diff at plan time. A large gap at close opens a "what surprised us" note that feeds the next plan's Risks.
  Done when: the close receipt shows the forecast beside the actual diff, and a gap over a threshold creates a note.

- **Wild: a per-model trust card from the ledger that feeds the router**: FEATURE, value 4, effort M, risk med. Category: routing. T-2291 picks a builder model from how past lanes held up. Adding each model's calibration score would let a confident but wrong model get cheaper checks when its numbers are bad and fewer checks when they are good.
  Done when: `fm lane brief` prints the model's calibration next to its pick, and a model with a poor score gets an extra check step.

- **Wild: a user-twin that guesses answers before `fm ask`**: FEATURE, value 4, effort L, risk high. Category: asking. The twin predicts the user's answer to each question, is scored on the real answers, and takes over a class of questions after 20 or more hits at 95% or better. The user can switch it off with one steer.
  Done when: a replay over stored `fm ask` records shows the twin's hit rate by class, and a class below the bar is never auto-answered.

Next question: which of Foreman's recorded numbers (minutes predicted, attempts, held-rate, Brier) is already being used to change behaviour, and which only gets displayed?
Next question: when a stated confidence is wrong, does Foreman currently know whether the cause was a missing fact, a changed mind or a flaky check?
