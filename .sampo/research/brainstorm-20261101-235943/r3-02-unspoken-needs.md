# Brainstorm — lens: unspoken needs

- **Tell the user which cells are really one capability before filling any** — CLEAN — value 5 — effort S — risk low — category: coverage triage
  Why: The user keeps pushing "coverage must be real, no templated cells", and the first open question asks which of the 58 are one capability counted under several stages. The need behind it is to stop reading 58 near-identical lines. Assumption: many cells collapse to maybe 8–12 predictor families.
  Done when: a table maps each of the 58 cells to a family id, and `fm genesis check` fails if a cell cites no family.

- **Make every cell name the session path that reads it** — FEATURE — value 5 — effort M — risk low — category: reach
  Why: Standing rule says every capability must be called by a real session path (start, `fm next`, drive, hook). The user will next ask "who calls this?" for each cell, since they did for #1 and #2.
  Done when: a cell without a `reach:` path to a named caller is counted empty by the sweep.

- **Strip Foreman-authored and mistaken captures from the user model** — FIX — value 5 — effort S — risk low — category: data hygiene
  Why: The dropped ledger shows "The first brief" and "The second brief" were captured by mistake from a test of T-2547. A model of the user trained on that learns noise. Unspoken need: trust that the forecast reflects them.
  Done when: a test feeds a captured-by-mistake line to the intake and `fmforesight` input excludes it, with the origin tag shown.

- **Backtest every predictor walk-forward before it may draft a lane** — FEATURE — value 5 — effort M — risk med — category: forecasting
  Why: The lesson from T-2546 (the word-overlap matcher met no bar) says heuristics need a backtest. The user will otherwise find drafts that were never right. Assumption: the asked stream has enough rows for hit@3.
  Done when: `fm foresight backtest` prints hit@3 against a "repeat the last request" baseline, and a predictor under baseline cannot draft.

- **Resolve every prediction to hit, miss, expired or abstained** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: Questions left ask which outputs no session path reads. An empty forecast is currently indistinguishable from a dead one.
  Done when: each forecast row carries a resolution, and `fm doctor` shows abstain versus failed counts.

- **Print one ranked heads-up line in `fm next`, not a new verb** — FEATURE — value 4 — effort S — risk low — category: delivery
  Why: Lean rules (T-2503) and the user's repeated "pay for a verb with a deletion" steers imply anticipation should ride an existing path. The user will not run a new verb to find out.
  Done when: `fm next` output includes at most one foresight line with a "because", muted after two dismissals.

- **Re-run each cell's cited behaviour on every sweep, not just file existence** — FIX — value 4 — effort M — risk med — category: coverage rot
  Why: An open question asks whether the sweep verifies a cited file still behaves as claimed. Later generations will change files under filled cells.
  Done when: deleting a cited function in a scratch copy turns its cell red in the sweep.

- **Tell the user "already built" at the moment they type the ask** — FEATURE — value 4 — effort M — risk low — category: duplicate prevention
  Why: Dropped-as-built items (guard-only exam arm, T-2534) cost the user a full ask each. T-2546 only checks at capture time, after the ask is made.
  Done when: a draft ask matching a MASTER.md clause prints the clause and task id in the same turn.

- **Predict which self-filed task the user will drop, before filing it** — FEATURE — value 4 — effort M — risk med — category: filing precision
  Why: Several dropped rows are Foreman-filed (measured: 1 of 22 baselines; 5 of 1219 cards). The user is paying attention to reject them.
  Done when: a backtest on the dropped ledger shows the filter would have held back at least half of past drops at no more than one wrongly held keeper.

- **Show a read-only Foresight panel with last-seen age and a stale banner** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: The web UI is the only surface in the mission, and a panel nobody opens is the failure the user fears (reach). Assumption: it reads the same ledger as `fm next`.
  Done when: the page renders each forecast with its resolution and "as of" stamp, and an empty state names why it is empty.

- **Wild: Run a shuffled-history control arm beside every predictor** — FEATURE — value 4 — effort M — risk low — category: validation
  Why: wild. The user distrusts signals Foreman authored. A predictor that beats shuffled history proves it learned order rather than vocabulary.
  Done when: the exam prints real hit@3 beside shuffled hit@3, and a predictor within noise of the control is muted.

- **Wild: Open resume with "things I would have told you if you'd asked"** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The dropped-as-built list shows the user repeatedly rediscovering things already done; surfacing them once a session turns those into gifts.
  Done when: session start prints at most three lines drawn from the dropped-as-built ledger, none repeated within seven days.

- **Wild: Replay the forecaster at each past commit date (time machine)** — FEATURE — value 3 — effort L — risk med — category: evaluation
  Why: wild. It gives a honest learning curve of hit@3 against history length without waiting weeks of live use.
  Done when: `fm foresight replay --since DATE` outputs a per-date hit@3 series from only data available on each date.

Next question: Which of the user's steers have since been contradicted by their own later behaviour, and would a forecaster flag that or keep obeying the stale one?
Next question: What does the user do in the first minute after a Foreman hit that they would rather not do, and can a forecast remove that step?
