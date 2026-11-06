# Brainstorm — lens: the forecaster (invented): it predicts the next request and the next breakage, drafts the first on spec in a lane, flags the second, and every prediction is scored

- **Add a calibration chart to fm doctor for every predictor** — FEATURE — value 4 — effort S — risk low — category: forecasting
  Why: T-2290 scores active-minute predictions at close, and the ideas so far list "calibration chart" only for requests. Assumption: minutes, attempts, trigger precision and model-router picks each log a predicted value and an outcome. Plot predicted vs actual per predictor so one that is systematically wrong is visible.
  Done when: `fm doctor` prints one row per predictor with n, hit rate and bias, and a test with a seeded biased predictor shows the row flagged.

- **Predict the follow-up edit to a just-closed task** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: the "asked" stream is full of corrections of a task Foreman just built (T-2285 after plan gate, T-2289 after T-2259, T-2326 after the site). Closing a task X predicts a "X, but for the sibling case" request from co-change history and past follow-ups, then adds it to the close receipt as a one-line guess.
  Done when: on a replay of the last 50 closed tasks, the guess names the next same-area task for at least a stated fraction, and the number appears in the scorecard.

- **Back-test every predictor on a rolling replay before it may draft a lane** — FEATURE — value 5 — effort M — risk low — category: forecasting
  Why: the speculative-lane ideas assume precision, but nothing shows a predictor earns the right to spend. Assumption: events and closed tasks are replayable by timestamp. Replay the history, feed each predictor only data from before each request, and compare it with "repeat the last request" and "most common kind".
  Done when: `fm foresight backtest` prints each predictor against both baselines, and a predictor under baseline is muted automatically in a test.

- **Predict the user's correction before delivery, from the pattern of the correction itself** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: many asks are corrections of a gate or scope the first version missed (T-2285 flag-led options, T-2289 scratch folder, T-2327 steers turned into checks). Assumption: "asked" lines can be grouped by the phrase "misses X" or "also Y". Before close, the forecaster lists the 3 nearest past corrections to this diff's shape and checks whether each class was handled.
  Done when: closing a task whose diff touches a parser prints the nearest past correction classes, and a test fixture reproduces the T-2285 miss being named.

- **Forecast tomorrow's red ship from today's open lanes** — PERFORMANCE — value 3 — effort M — risk low — category: breakage
  Why: "Ship red after T-2072" and the duplicated "Baseline red" tasks show reds are found at ship, late. Assumption: lane branches can be test-merged cheaply. Nightly, merge-simulate the open lanes pairwise in a scratch worktree and flag the pair that goes red before the user merges either.
  Done when: two lanes planted with a conflicting always-on-budget change get flagged by the nightly run, with the pair named.

- **Learn the user's idle-time return pattern and time speculative drafts to it** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: speculative lanes burn budget ($0/$200 now) and are wasted if the user returns to a different topic. Assumption: event timestamps show a day rhythm. Start drafts shortly before the typical first request of the day, not overnight at random.
  Done when: the foresight schedule shows a start window derived from the last 14 days, and a test with synthetic timestamps moves the window.

- **Mark each prediction as adopted, edited, ignored or contradicted** — FEATURE — value 4 — effort S — risk low — category: scoring
  Why: "scored" currently means hit or miss, but a draft the user edits by two lines is worth far more than a miss. Record the overlap between the draft and the real task, and let the router learn from the partial credit.
  Done when: a draft with half its rows reused scores 0.5 in `fm foresight`, and the score shows in the prediction list.

- **Put an expiry on every drafted lane and delete it unmerged** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: T-2289 shows lane cleanup already has sharp edges, and the standing rule says to keep context small and lean. Speculative drafts left around would grow the same debt. Every draft lane gets a TTL, a disposition record and no merge path.
  Done when: a draft older than its TTL is removed by `fm foresight sweep` and recorded as expired, and a test shows it cannot be merged.

- **Predict which steer a new feature will violate, from the steer list itself** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the 20+ standing steers are each enforced by a separate check (T-2327), and new work (T-2252 guard words) keeps landing right next to them. Assumption: a cheap model can match a plan's scope to steer text. At plan time, list the 3 steers most likely to be touched and run their checks on the plan's file list.
  Done when: a plan touching the exam's session arms names the 2026-10-31 steer #1, and its check runs before the first edit.

- **Wild: Keep a prediction book with the user's bets** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The user can type `fm bet "next I'll ask for X"`, and Foreman's forecast and theirs are scored side by side. Over time it shows who knows the project's direction better, and each side gets a streak.
  Done when: a bet is stored, scored at the next request and shown with Foreman's guess on the same line.

- **Wild: Run a ghost-user lane that attempts the predicted request blind and reports its first question** — FEATURE — value 4 — effort L — risk med — category: anticipation
  Why: wild. The first question a draft has to ask is exactly the clarification the real request will lack. Capture it ahead of time and offer it as the interview's pre-filled answer from past steers.
  Done when: a draft's first blocking question appears on the predicted goal card, and a test shows it is answered from a recorded steer.

- **Wild: Publish a "what Foreman got wrong about me" page with the worst misses** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. Showing the biggest forecast misses with the signal that fooled it builds credibility, and it is a place to fix the model. Assumption: the user would accept a local-only page.
  Done when: `fm foresight misses` writes a page listing the 10 worst misses with predicted, actual and the feature that misled.

- **Combine the forecasts into one morning card with a veto key** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the ideas above create several outputs: request guesses, red-ship warnings, lane drafts, a cost forecast. Merge them into one card that ranks by minutes saved, and let the user veto a class with a word.
  Done when: the first prompt of the day shows at most 5 lines, each with a veto key, and a vetoed class stops appearing.

Next question: Which of Foreman's predictors has never been run against history it did not train on, and what does the plain "same as last time" baseline score there?
Next question: When a speculative draft was right but the user phrased it differently, how does scoring recognise the match without a model grading its own work?
