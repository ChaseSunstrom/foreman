# Brainstorm — lens: approaches

- **Score a recency baseline first** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the user's asks are mostly Foreman-filed brainstorm items (c14–c24, "asked: FEATURE: …"), so a naive predictor like "next ask = highest-value deferred item in the last-touched category" may already match most of them. Every fancier approach needs this null to beat.
  Done when: `fm anticipate --backtest` replays the last 60 days of asks and prints the hit rate of "last category + next-highest value" against actual next asks, with n shown.

- **Mine ask-sequence n-grams from the ledgers** — FEATURE — value 5 — effort M — risk low — category: prediction
  Why: asks arrive in runs (the c14→c24 run; Mission 5→6→7 gen-3 asks; "fix, then sibling sweep"). Zero-token bigram/trigram over ask kind, category and verb touched.
  Done when: a test feeds a fixed ask history and the predictor ranks the known successor in its top 3, and the same test fails with shuffled order.

- **Predict by task-kind follow-up table** — FEATURE — value 4 — effort S — risk low — category: do-less
  Why: the "Do less" approach is a static table, e.g. after FIX → sibling sweep, after a new verb → help string, MASTER.md, site, session path ("every capability needs a real session path" steer). It needs no model and is auditable.
  Done when: `fm task finish` prints at most 3 follow-ups from a table keyed by TYPE and files touched, and a test pins each row.

- **Treat drops as negative evidence** — FEATURE — value 4 — effort M — risk low — category: prediction
  Why: the "dropped" lines (re-grounded to value 2, already built via `fm usage --prune`) show the user kills "mostly built" and "second-order" ideas. Predicting what they will drop is cheaper and more valuable than predicting what they will ask for.
  Done when: before a slate is shown, items matching a past drop's reason class are flagged "likely drop: <reason>", and a backtest on past slates reports precision against actual drops.

- **Fire anticipation from external events, not history** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: blocked tasks (T-0335/36/37, T-0418, T-0325) wait on outside facts such as host releases, packages and installed versions. A probe that wakes a task when its blocker flips predicts "you'll want this now" with no user model.
  Done when: a fake host-version bump in a fixture moves T-0418 from blocked to the `fm next` offer with the reason line "blocker cleared: <probe>".

- **Pre-draft the top predicted ask during idle quota** — FEATURE — value 3 — effort L — risk med — category: speculative work
  Why: the standing steer says not to stop for pace and to wait out limits. Idle windows could produce a lane branch, unmerged and labelled speculative, for the top predicted item. Trade-off: the spend is wasted on a miss, so gate it on the baseline hit rate.
  Done when: a drafted branch exists only when the backtest hit rate for that category exceeds a configured bar, and a miss is discarded with its cost recorded in the receipt.

- **Turn every "Next question" into a scored forecast** — FEATURE — value 4 — effort S — risk low — category: feedback loop
  Why: each brainstorm ends with Next question lines, and "what earlier brainstorms missed" lists T-2659…T-2677. Those misses are prediction failures, never scored.
  Done when: each Next question is stored with an id, and `fm doctor` reports how many were later asked, dropped, or are still unasked, within 30 days.

- **Run a cold child that tries to be surprised** — FEATURE — value 3 — effort M — risk low — category: adversarial check
  Why: a tool-less child is given the predictor's output plus the last 20 closed titles and asked only for "what would the user ask that this list lacks". It is the approaches-lens counterpart to the grid lens and uses a signal Foreman didn't author.
  Done when: its output is scored against the next 10 real asks, and the arm is kept only if it adds hits beyond the n-gram predictor.

- **Reuse the host's own history** — FEATURE — value 3 — effort M — risk med — category: reuse
  Why: Claude Code transcripts hold the user's unfiltered phrasing, including corrections. Mining these for "also", "again" and "I told you" is the existing repeat-correction idea applied to prediction.
  Done when: a fixture transcript with 3 repeated corrections yields one predicted-ask card naming the class, and a transcript with none yields nothing.

- **Wild: sell the prediction back as a bet** — FEATURE — value 2 — effort M — risk low — category: wild
  Why: assumption: showing the user "I bet you ask X next (62%)" and settling it on their next message gives free calibration data and a small moment of delight.
  Done when: the bet appears on the finish card, settles on the next ask, and a calibration plot reads from the settled rows.

- **Wild: replay the user's week and predict only the gaps** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: assumption: gaps in cadence (a Monday with no ask after a Friday run) are more telling than content, and the "while you were away" card could rank by expected-ask-time, not recency.
  Done when: `fm anticipate --gaps` lists expected-but-missing asks for the last 14 days, and a test with a planted gap names it.

- **Wild: let the predictor retire itself** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: the standing lean steers want measured value. An anticipation feature whose hit rate sits at or below the recency baseline for 30 days should shut itself off and say so.
  Done when: a fixture where the predictor underperforms the baseline flips the feature to off, and `fm doctor` prints one line with the reason.

- **Count what the user types after Foreman's last output** — FEATURE — value 3 — effort S — risk low — category: ground truth
  Why: ground truth for every approach above is the user's next message. Pairing each finish card with the following user message in one place, tagged "predicted, partly predicted, or surprise", gives one dataset shared by all predictors.
  Done when: a ledger of (finish, next-ask, label) rows exists and a test labels three planted pairs correctly.

Next question: which of the user's asks in the last 60 days were genuinely unpredictable from the ledger alone, and what did they share?
Next question: does the user read a predicted-ask card at all, or does it join the notes they already skip?
