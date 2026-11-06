# Brainstorm — lens: unspoken needs

- **Fill the 58 cells from the user's own correction history, not the grid** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the "asked" stream (T-2532..T-2547) shows the user repeatedly had to ask for things no brainstorm predicted; each missed ask is a real Anticipation cell. Standing rule says a cell counts only if grounded.
  Done when: each filled cell cites a specific "asked" line or ledger incident, and `fm genesis check` rejects any cell with no such citation.

- **Quarantine test-fed captures from the user model** — FIX — value 5 — effort S — risk low — category: data hygiene
  Why: "The first brief" and "The second brief" were captured by mistake from a debugging sample and sit in the user's "asked" list; the model of me is already polluted by Foreman's own test inputs.
  Done when: a capture whose source is a test run or marked dropped-by-mistake never appears in the forecaster's inputs, proven by a fixture.

- **Show "already built" before the ask is finished** — FEATURE — value 5 — effort M — risk med — category: prediction
  Why: three recent drops were "built: the exam's plain arm already is that" (guard-only arm) and "measured: 1 of 22". The user wastes asks on things that exist; T-2546 only does this at capture time.
  Done when: typing a request into `fm capture --dry` prints matching MASTER.md clauses with task ids in under a second, and a backtest on the dropped-as-built ledger hits ≥ 60%.

- **Backtest every predictor walk-forward before it may draft a lane** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: Lessons from Missions 3-5: T-2546's word-overlap matcher met no bar. Standing rule wants a backtest that decides shipping.
  Done when: `fm foresight backtest` prints hit@3 per predictor on the asked stream and a predictor under its floor is refused from drafting.

- **Print one ranked heads-up line in `fm next`** — FEATURE — value 4 — effort S — risk low — category: reach
  Why: question left open: which outputs does no session path read? A forecast nobody sees is unmeasurable; `fm next` is a real session path.
  Done when: `fm next` shows at most one foresight line with a "because", muted after two dismissals, and a test shows the line appears.

- **Predict the user's drop before Foreman files a self-filed task** — FEATURE — value 4 — effort M — risk low — category: restraint
  Why: the dropped ledger (measured-and-dropped library cards, guard-only arm) shows self-filed work the user later killed with evidence.
  Done when: a self-filed candidate that resembles a prior dropped class is held with the matching drop reason, verified on a replay of the dropped list.

- **Reverse-map the dropped-as-built ledger onto cells** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: each dropped-as-built line is a case where anticipation would have saved an ask; they are ready-made grounded cells.
  Done when: every dropped line with a "built:" reason is linked from at least one cell.

- **Re-run each cell's cited behaviour on every sweep** — CLEAN — value 4 — effort M — risk med — category: verification
  Why: open question: does the sweep check the cited file still behaves, or only exists? Later generations can silently change it.
  Done when: a cell whose probe is edited to fail turns the sweep red, shown by a red-first test.

- **Flag open tasks a commit made moot** — FEATURE — value 3 — effort M — risk med — category: queue hygiene
  Why: assumption: with 35+ deferred/blocked items (e.g. T-0034..T-0869) some are already satisfied by later commits like T-2546.
  Done when: on a replay of the queue, at least one item known to be built is flagged with the commit.

- **Wild: Open the session with "what I would have told you if you'd asked"** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild; the dropped-as-built list holds exactly those facts the user had to discover by asking.
  Done when: session start prints up to three such lines from the ledger, each citing its task id.

- **Wild: Shuffled-history control arm for every predictor** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild; without a control, a hit rate could be just the last request repeated.
  Done when: the exam reports each predictor's hit@3 beside its shuffled-history score.

- **Wild: Plant a fake habit and check the forecaster doesn't over-learn it** — FEATURE — value 3 — effort M — risk low — category: robustness
  Why: wild; Foreman's own tests already polluted the "asked" stream once.
  Done when: a fixture history with a planted one-off habit yields no forecast of it.

- **Cap foresight at one line, mute after two dismissals** — FEATURE — value 3 — effort S — risk low — category: restraint
  Why: assumption: unsolicited flags are the fastest way to lose the user's trust; the standing steers value restraint.
  Done when: a third identical flag in a fixture is suppressed.

Next question: Which of the 58 cells would the user actually notice being empty, as measured by a past ask they had to type?
Next question: Does any predictor output reach the user without them opening a verb, and what do they see if the forecaster silently abstains?
