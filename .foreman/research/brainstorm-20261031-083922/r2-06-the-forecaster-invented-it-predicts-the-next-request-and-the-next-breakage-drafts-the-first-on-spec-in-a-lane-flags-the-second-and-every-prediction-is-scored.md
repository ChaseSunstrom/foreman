# Brainstorm — lens: the forecaster (invented): it predicts the next request and the next breakage, drafts the first on spec in a lane, flags the second, and every prediction is scored

- **Score the forecaster against a dumb baseline on every surface** — FEATURE — value 5 — effort M — risk low — category: forecasting
  Why: T-2290 scores predictions of minutes and attempts, but the ideas list only says "mute predictors that lose to the baseline" for the trigger table. No baseline is defined for request prediction, and the user's steer says free arms must beat session arms. Baselines: last request repeated, the oldest open task, the most common kind this week.
  Done when: `fm foresight score` prints, per predictor, hit rate beside the baseline's hit rate for the last 30 days, and a predictor at or below baseline for 2 weeks is marked muted in the output.

- **Predict the next request from the open-work and "asked" streams jointly** — FEATURE — value 5 — effort M — risk med — category: prediction
  Why: The "asked" stream is a run of numbered Mission items (Mission 5 #2, then 6 #5, then 8 #7...) and each one is a follow-on of the previous task's gap; the "Later from T-07xx" bundles show what was set aside. A model on (last closed task's follow-ups, steer-driven next Mission item) would have predicted several of these. Assumption: Mission ordering is parseable from the mission files.
  Done when: replaying the last 20 asked items, the predictor ranks the actual next item in its top 3 at least 8 times, and the result is stored in the ledger.

- **Draft the predicted request as a spec-only lane that never merges** — FEATURE — value 4 — effort M — risk med — category: speculative lanes
  Why: The request says "drafts it on spec in a lane". Make the output a branch holding a failing-first test plus a plan, no source edits, so a wrong guess costs a little and a right guess saves the plan and red step. Gated by the precision floor.
  Done when: a speculative lane produces a task with a plan that passes the plan gate and a red test, the lane has no non-test diffs, and when the user's real request matches (score ≥ threshold) `fm task focus` adopts it.

- **Turn each recurring "what earlier brainstorms missed" ask into a pre-breakage probe** — FEATURE — value 4 — effort M — risk low — category: foresight
  Why: T-2285, T-2288, T-2289 and T-2327 are all one class: a new feature has an edge the plan gate, doctor, or lane rm didn't expect (flag-leading option text, throwaway scratch folders, undeclared enforcement). Classify by "new feature × existing guard that parses or lists it" and have foresight run the guard against the feature's own sample inputs at task finish.
  Done when: finishing a task that adds a verb or parser runs the existing parsers/guards on that task's fixtures, and a seeded flag-leading Approach option is flagged before ship.

- **Forecast "red after ship" from the diff's co-change history** — FEATURE — value 4 — effort M — risk low — category: breakage
  Why: The ship went red after T-2072 on a char budget and a skill-count cap. `fm graph blast` already exists; join it with the lean ratchet footprints so a diff that nears a budget gets a warning before `fm ship`.
  Done when: a diff adding rules text within 5% of the 6,400-char budget makes `fm task finish` print the headroom and the sibling checks likely to fail.

- **Predict which steers will collide with a new feature** — FEATURE — value 4 — effort S — risk low — category: steers
  Why: The 2026-10-31 steers (no skipped work, no exam session arms before the end) were contradicted by features such as `--jobs N` and needed T-2327 after the fact. Match a task's text against stored steer checks at focus time.
  Done when: focusing a task whose title mentions "exam run" prints the steer 1 check that would refuse it, with its id.

- **Keep a prediction ledger the user can read as a calibration chart** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: predictions are scored but only in per-tier lines. A chart of predicted vs actual (minutes, attempts, next request) on the web UI makes trust visible.
  Done when: the web UI page shows a calibration plot with at least 20 points, and an empty state when there are fewer.

- **Warn when the day's forecast hits the usage wall before the queue empties** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: steer 3 says wait out limits; foresight can order the queue so the highest-value tasks run before the wall. Assumption: usage per task is recorded per tier.
  Done when: `fm next` prints "~N tasks fit before the wall" and reorders to put proven-value tasks first.

- **Wild: Hold a prediction court for each speculative lane** — FEATURE — value 3 — effort M — risk med — category: scoring
  Why: wild. After the real request arrives, a cold Haiku child with no access to the draft judges whether the draft matched, quoting both texts, so the hit/miss isn't scored by the code that predicted.
  Done when: each scored prediction stores a judge quote and the judge disagrees with the code score in a logged share of cases.

- **Wild: Pre-write tomorrow's first request as a morning card** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Tonight's forecaster writes one line, "next you'll probably ask: X", with a draft lane link and a one-key accept or discard. Discards feed the score.
  Done when: session start shows the card once and the accept/discard is recorded as a labeled outcome.

- **Wild: Run a canary prediction from a user-twin built only from steers** — FEATURE — value 3 — effort L — risk high — category: user model
  Why: wild. A model with only the stored steers and corrections answers "would the user accept this plan?" before the plan reaches them. Its accuracy is scored against real accept/edit/reject outcomes and it is retired if it can't beat chance.
  Done when: twin verdicts on the last 30 plans are compared with real outcomes and the agreement rate is printed.

- **Forecast which hooks will breach their latency budget next** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: the lean ratchet records hook p50 at each ship; fitting a trend to those rows predicts the ship at which a hook crosses its limit, so the warning lands several ships early.
  Done when: `fm doctor` prints "hook X projected over budget in ~N ships" from at least 5 recorded ships.

Next question: What fraction of the user's requests are follow-ups to the previous task rather than fresh, and does that fraction make a next-request predictor worth its cost?
Next question: Which prediction would the user have wanted to hear aloud before it happened, and which would only have been noise?
