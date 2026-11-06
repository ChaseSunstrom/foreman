# Brainstorm — lens: bold bets

**Answers to the questions left earlier, where this lens can:**
- A filled cell's citation is only checked for existence (the pack names no behaviour check). So a later generation can change a cited file and the cell stays "filled". Ideas 1 and 2 close this.
- Anticipation outputs (next-ask drafts, forecasts, bets) are the likeliest ones with no session reader. Idea 3 checks it mechanically.

**Ideas, best first**

- **Gate every cell on retrodiction** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the Missions 3-5 lesson says to name the backtest that decides whether a heuristic ships, and T-2546's matcher met no bar. Cells currently count on grounding prose.
  Done when: `fm genesis check` prints a retrodiction row per cell (the past ledger event a leave-one-out replay would have predicted, versus the "repeat last" baseline), and a cell with no row is listed as unproven and excluded from the count.

- **Measure problem-flag cells in warning lead time** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the "flags problems before they happen" half has no unit. Planted faults would give one: a dead timer, a stale map, a full tmpfs.
  Done when: a new exam kind plants N faults in a fixture and reports minutes of warning before each one bites. Every problem-class cell cites one such fault.

- **Fail on predictor outputs nothing reads** — CLEAN — value 4 — effort S — risk low — category: reach
  Why: the standing reach rule requires a session path for every capability. The pack's own question asks which outputs have none.
  Done when: a fixture predictor field that no session path reads turns `fm genesis check` red and names the field.

- **Forecast machine exhaustion with an ETA** — FEATURE — value 4 — effort M — risk low — category: machines
  Why: the children dir sits on `/run/user/1000` (tmpfs). T-2543 hit ETXTBSY, T-2529 a missing setuptools, T-2542 a silent dead timer. The "machines" part of the model is only reactive.
  Done when: a fixture state-dir growth series makes `fm doctor` print "fills in ~N h at the current rate", and a flat series prints nothing.

- **Predict the user's drop before filing** — FEATURE — value 4 — effort M — risk med — category: dropped ledger
  Why: three of the five recent drops were "already built", "captured by mistake" or "measured: not worth it". Each cost a task that could have been caught at birth. T-2546 covers only the "built" case.
  Done when: a replay over the dropped ledger gives a recorded precision and recall, and the filter is armed only above a stated bar (otherwise it stays advisory).

- **Show the predicted next ask as ghost text in the foreman-ui prompt** — FEATURE — value 4 — effort M — risk med — category: web/pane
  Why: the user's asks are rigidly shaped (`FEATURE: … DONE-WHEN`). The foreman-ui mod already owns the prompt area, so a draft can sit where they type.
  Done when: with a fixture ledger the prompt shows the draft, Tab inserts it, and Esc logs a miss that the predictor's score reads.

- **Project the user model into every harness's first message** — FEATURE — value 3 — effort M — risk low — category: harnesses
  Why: the standing rule says Foreman isn't Claude-specific, T-0335 shows non-Claude grants blocked, and the anticipation model must not live only in hooks.
  Done when: a codex or opencode session's first turn contains the same top steers and predicted-next line as Claude's, checked by a fixture diff.

- **Let the user model forget** — FEATURE — value 3 — effort S — risk low — category: privacy/decay
  Why: assumption: habits stale out. A model of "me" that never decays will confidently predict last quarter's user.
  Done when: a habit with no new observation in 60 days drops out of predictions, and `fm me` lists each fact with its source and a one-key forget.

- **Ration anticipation flags by expected loss** — FEATURE — value 3 — effort M — risk med — category: attention
  Why: assumption: ten correct flags a day train the user to ignore all of them. The "attention asked" idea counts the cost but never ranks flags against it.
  Done when: with five fixture flags and a budget of two, only the two with the highest expected loss avoided surface, and the rest go to a digest line.

- **Wild: run a prediction market among cheap lanes** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild. Several cheap-model predictors bet a bankroll on the user's next ask, and settlement is the real ask. Prices give a calibrated confidence, and broke predictors are muted.
  Done when: after 20 settled asks, the market price has a lower Brier score than the best single predictor on the same replay (or the result is reported honestly as not).

- **Wild: build an option book of pre-made stubs** — FEATURE — value 3 — effort M — risk med — category: speculative lanes
  Why: wild. For the top 3 predicted asks Foreman pre-builds only a red test and a stub, under a hard cost cap, and each expires unexercised. Payoff is measured as minutes saved when exercised.
  Done when: `fm status` shows each option's cost, expiry and exercise rate, and a user-typed ask that matches an option starts from its stub.

- **Wild: compare the dream diff with the real diff** — FEATURE — value 3 — effort L — risk high — category: taste learning
  Why: wild. Overnight, a scratch tree attempts the predicted ask. When the real ask arrives, the delta between the dream diff and the real one is recorded as taste data (what the user wanted that Foreman didn't guess).
  Done when: a fixture pair produces a recorded delta, and the next prediction cites it.

- **Wild: print one "you'll wish you'd known by Friday" line at session start** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A single forecast sentence per week, scored on Friday against what actually happened, with the running hit rate shown beside it.
  Done when: the line appears once per session, Friday's score is stored, and the hit rate is printed.

- **Transfer the user's first-hour priors to a new repo** — FEATURE — value 3 — effort M — risk med — category: projects
  Why: assumption: the "my projects" part of the model is per-repo only. The gates, stacks and rules the user adds to every new repo are a cross-project habit.
  Done when: on a fresh fixture repo with the same stack, `fm` pre-briefs the top 3 habitual setup steps, and a decline is recorded.

Next question: Which of the 58 cells can be probed on a replayed ledger, and which can only be judged live, so the retrodiction gate would leave them unproven by design?
Next question: What does the user do in the five minutes after a prediction is shown and ignored, and does any signal Foreman already records distinguish "ignored" from "unseen"?
