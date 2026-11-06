# Brainstorm — lens: approaches

- **Extrapolate numbered series in the user's asks** — FEATURE — value 4 — effort S — risk low — category: prediction
  Why: the recent asks are literal series: "Mission 5", "Mission 6", "Mission 7"; "M-01 to M-20"; c13…c24 from one slate. The next element is deterministic and needs no model or learned table.
  Done when: a test feeding the asks "Mission 5/6/7" and "c22/c23/c24" makes `fm anticipate` print "Mission 8" and "c25" with the matched series as evidence, and print nothing for an unnumbered ask.

- **Log the show-probability of every anticipation for offline evaluation** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the pack proposes dozens of predictors (n-grams, TF-IDF, bandit, event rules) and Foreman cannot run them all live. Logging the probability that each candidate was shown lets any new predictor be scored on past data with inverse-propensity weighting, with no deployment. Assumption: the user's accept and ignore signals are logged per show.
  Done when: `fm anticipate --eval NAME` prints an estimated hit rate with a confidence interval for a predictor that was never shown, and a synthetic ledger with a known hit rate is recovered within the interval.

- **Fit every anticipation window and half-life by backtest on the user's own history** — FIX — value 3 — effort S — risk low — category: calibration
  Why: the open question "which numeric defaults were picked without ever being run against the user's history" applies directly. Any predictor's recency window or decay is a guess until a grid search over the real ledger sets it.
  Done when: each anticipation constant lives in one table with a `fitted_on` date and score, and a test fails if a constant has no fit record.

- **Detect new vocabulary in the user's recent messages that no verb or MASTER.md clause covers** — FEATURE — value 3 — effort S — risk low — category: prediction
  Why: terms like "grid lens", "canary", "moonshot" and "steer-expansion" each appeared in the user's words and became a Mission later. A term first seen in the last 7 days, repeated, and absent from MASTER.md is a cheap leading indicator. Assumption: stemmed unigrams and bigrams are enough.
  Done when: replaying the ledger up to the day before "canary" first appears, then the day after, lists "canary" as uncovered; a term already in MASTER.md never appears.

- **Show a prediction only when a conformal set has size one** — FEATURE — value 3 — effort M — risk med — category: prediction
  Why: earlier ideas mute a predictor only after it loses to a baseline. A calibration split gives a coverage guarantee per kind, so the system says nothing when it cannot be right at the chosen rate. Trade-off: it needs enough history to calibrate and will mostly abstain early on.
  Done when: on a held-out ledger slice, shown predictions hit at the target rate (for example 80%) within sampling error, and with fewer than N samples the output is the "can't read you yet" state.

- **Make `fm anticipate` a stateless pure function over the ledgers** — CLEAN — value 3 — effort S — risk low — category: do-less
  Why: several ideas above fight staleness (epoch binding, card age, Stop-time precompute). Computing at read time in under 50 ms removes the whole class, at the cost of repeated work on large ledgers. This is the baseline any cached design must beat.
  Done when: the verb writes no file, its output is identical on two runs over the same ledgers, and a bench keeps it under 50 ms on a 10× ledger.

- **Use zlib compression distance as the nearest-neighbour finder for asks** — FEATURE — value 2 — effort S — risk low — category: reuse
  Why: it needs no TF-IDF index, no vocabulary file and no third-party code, so there is nothing to go stale. Using stdlib zlib fits the standing "works with no extra tooling" rule. Trade-off: it is weaker on short asks, and a backtest decides it.
  Done when: on the leave-one-out ask set it ranks the true follow-up in the top 5 at least as often as the TF-IDF baseline, or the idea is dropped with the numbers recorded.

- **Replay the first 100 historical asks through today's Foreman to measure the pre-emption rate** — FEATURE — value 3 — effort M — risk low — category: measurement — wild
  Why: assumption: many early asks (output caps, "N left out", next-command-on-error) are now answered by shipped features. A canary grep plus a cold child can say, per old ask, "a verb or gauge now covers this". The fraction tells the user whether anticipation has been working at all.
  Done when: `fm anticipate --time-machine` prints covered / uncovered counts over the first 100 asks, each with a quoted command or file as proof.

- **Write a prospective receipt for each filed task and score it at close** — FEATURE — value 3 — effort M — risk low — category: forecasting — wild
  Why: the pack has cost forecasts and scored estimates but no prediction of the receipt itself (files touched, lines, commit subject). A diverging receipt shows scope surprise before the user has to ask "why did that touch X?".
  Done when: every task has a `predicted_receipt` line at filing, and `fm task finish` prints the diff between it and the actual receipt.

- **Write tomorrow's expected ledger in the real schema and diff it against the actual one** — FEATURE — value 2 — effort L — risk med — category: forecasting — wild
  Why: because the forecast uses the real record format, digest, outcomes and cost readers run on it unchanged. The surprise map is then an ordinary ledger diff instead of a new gauge. Assumption: the existing readers tolerate a flagged "expected" author class.
  Done when: `fm digest --expected` and `fm digest` run on the two files, and a day with a planted unplanned close shows exactly that close as the difference.

- **Run a weekly tournament of three shadow predictors and let the held-out week choose the live one** — FEATURE — value 2 — effort M — risk med — category: prediction — wild
  Why: a single predictor is a bet on one theory (series, follow-up table, nearest neighbour). Running all three silently, scored on the next week's real asks, replaces the choice with data and keeps the loser available for a rematch.
  Done when: the ledger holds a weekly record naming each predictor's hits and the winner, and a forced-loss fixture swaps the live predictor.

Next question: which of the user's asks were typed by them and which were filed by Foreman (Missions, slate items), and do the anticipation scores change once only the typed ones count?
Next question: when an anticipation was shown and the user ignored it, how would Foreman tell "wrong" from "right but not now"?
