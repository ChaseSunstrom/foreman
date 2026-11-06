# Brainstorm — lens: bold bets

Answer to the open question my lens can reach: most of the 58 cells collapse into three predictors (ask-series, signal→reaction, machine/problem flags). A cell counts only if it names the session path that reads that predictor's output.

- **Track user words per landed task as Anticipation's north star** — FEATURE — value 5 — effort M — risk low — category: metrics
  Why: the pack's hit-rate and lead-time ideas score guesses, not the point of the capability, which is the user typing less. Assumption: transcripts give word counts per task from capture to close.
  Done when: `fm doctor` prints median user words per closed task, 4-week rolling, split by task kind, and a test on fixture transcripts reproduces the number.

- **Mine ask-to-ask transformation operators** — FEATURE — value 4 — effort M — risk med — category: prediction
  Why: the asked stream shows chains where each ask transforms the last (bets → bets carry their harness → interim reads, plan percent → interim calibration → settle without a session). Learn the operators (add a dimension, make it unattended, add a test, split per harness) instead of the topics. Backtest per the Missions 3-5 lesson.
  Done when: a walk-forward backtest on the asked stream reports operator-guess top-3 hit rate versus last-ask-repeat, and the predictor ships only if it beats the baseline.

- **Build a signal→reaction latency table** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: for each signal (red CI, dependency release, deferred revisit date, ship gate failure), measure how long the user takes to react, or whether they ever do. Pre-brief the fast-reacted signals and silence the never-reacted ones. Evidence: `ci-watch` and the nightly digest exist, but nothing learns which signals the user cares about.
  Done when: `fm foresight signals` lists each signal with its median latency and ignore rate from the ledgers, and a never-reacted signal stops appearing in the session start note.

- **Run champion/challenger forecasters in shadow** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: backtests are offline and one-off. Running challenger predictors silently beside the live one, with online scoring, lets the best one earn promotion. Assumption: predictor outputs can be logged without adding hook cost.
  Done when: two predictors score against the same real asks for 14 days and a promotion verdict is written with both Brier scores.

- **Detect steers the user's behaviour now contradicts** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: about 30 standing steers are in force, some tied to a moment ("pause long-horizon runs now", "finish round 1 first"). The existing "lift a steer at its end condition" idea needs an observed end, but drift shows up earlier in what the user stops enforcing.
  Done when: a card names a steer with 0 enforcement or corrections in 30 days beside a contrary action, offering retire or keep, and the user's answer is stored.

- **Graduate recurring ask classes to accept-by-default** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: speculative drafts cost review attention even when they are right. After N consecutive drafts of a class are adopted unedited, the class moves from draft to filed-and-started, with a one-line undo; a miss demotes it.
  Done when: a fixture class reaches graduation after 5 unedited adoptions and demotes on the first edit or drop, with the transitions logged.

- **Detect when an arc has ended** — FEATURE — value 3 — effort S — risk low — category: queue hygiene
  Why: the asked stream runs in arcs (calibration, lean, proof). Once the user stops asking in an arc and the open items in it are Foreman-filed, those items are probably stale. Evidence: many "Later from T-07xx" bundles sit deferred.
  Done when: `fm next` marks an arc quiet after 21 days with no user ask and lists its open items for one batched keep/drop.

- **Forecast Foreman's own failures for the day** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: from friction counts, hook errors and flaky-test ledgers, post "likely to go wrong today: X" and score it at day's end.
  Done when: the session start note carries one self-forecast line and a nightly job records hit or miss.

- **Wild: Write a weekly letter of predicted asks that the user strikes through** — FEATURE — value 3 — effort S — risk low — category: labels
  Why: assumption: striking a line is cheaper than a click-through feedback form and gives clean hit/miss labels. Each letter line is a drafted ask in the user's voice.
  Done when: striking a line in the letter file records a dismissal against its predictor, and an unstruck line older than 7 days counts as an unreviewed miss.

- **Wild: Keep a "thesis of the user" and watch it drift** — FEATURE — value 3 — effort M — risk med — category: strategic model
  Why: assumption: a tool-less child can read only the last 3 days of the user's words and write 5 lines on what they are trying to make Foreman become, then be compared with the previous thesis. A change in thesis is a strategy change, which no per-ask predictor sees.
  Done when: `fm foresight thesis` shows this week's lines beside last week's, and a planted shift in fixture asks changes the thesis lines.

- **Wild: Pre-write tomorrow's drafts as title-only stubs scored at wake** — FEATURE — value 3 — effort S — risk low — category: speculative drafts
  Why: assumption: stubs are close to free, and scoring them at wake gives a morning "yes" sheet from yesterday's evidence.
  Done when: a nightly tick writes at most 3 stubs with grounding lines, and `fm next` shows each beside its overnight hit or miss.

- **Wild: Compute a "regret of silence" score** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: assumption: anticipation fails by flooding or by saying nothing, and only the first is measured. Whenever a real ask had a matching signal in the ledgers that Foreman did not surface, count it as regret.
  Done when: `fm doctor` shows silent-miss count beside flag count, and a planted fixture signal that went unflagged is counted.

Next question: Which predictor's output is read by no session path today, and what does the user lose if each of the three predictor families stays silent for a week?
Next question: What does the user do in the first 60 seconds after a Foreman-filed draft appears, and does anything measure whether they read it?
