# Brainstorm — lens: bold bets

- **Replace the 58 cells with one executable predictor-family table** — CLEAN — value 5 — effort M — risk med — category: coverage
  Why: the earlier open question asks which cells are one capability counted under several stages. Assumption: roughly 8–10 families (next-ask, correction shape, drop, machine breakage, ship-red, conflict, cost/limit, staleness) cover all 58. Each family row carries a probe, a reach path and the cells it stamps. This makes "fill 58" an honest ~10 probes.
  Done when: `fm genesis check` reads the table, lists every one of the 58 cells under a family, and fails if any cell has no family, no probe or no named session path.

- **Backtest-gate every predictor on the asked stream** — FEATURE — value 5 — effort M — risk low — category: forecasting
  Why: lesson from T-2546, where a word-overlap matcher met no bar. Assumption: the "asked" stream holds enough history for a walk-forward replay. A predictor may draft or flag only if hit@3 beats a dumb baseline (last request, weekday-hour) on held-out later months.
  Done when: `fm foresight backtest` prints per-predictor hit@3 against the baseline, and a predictor below the bar is refused by the drafting path.

- **Feed `fm next` one ranked heads-up row from foresight** — FEATURE — value 5 — effort S — risk low — category: reach
  Why: the pack's open questions ask which outputs no session path reads. Assumption: `fm next` already runs every session. One line (the next ask, a likely-red ship, or a machine ETA) with a "because" and a mute after two dismissals, with no new verb.
  Done when: a fixture session shows exactly one foresight row in `fm next`, and two dismissals of its signature silence it.

- **Make foresight stateless and resolvable** — CLEAN — value 4 — effort M — risk med — category: ledger
  Why: assumption: stored predictions drift from their sources. Compute from the existing ledgers (asked, dropped, outcomes, transcripts) and keep only a small resolution log marking each forecast hit, miss, expired or abstained. A purge cannot silently empty it.
  Done when: deleting the foresight state directory and re-running reproduces the same forecasts, and every logged forecast ends in one of the four resolutions.

- **Strip test and mistaken captures from the user model** — FIX — value 4 — effort S — risk low — category: data hygiene
  Why: the pack shows "The first brief" and "The second brief" were captured by mistake from T-2547's test. They are already in the dropped list. The model of me must not learn from them, or from anything Foreman wrote itself.
  Done when: a fixture with those two lines plus a dropped-as-built item yields zero model-of-me records from them, and each record carries an origin tag.

- **Check "already built" as the user types** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: several dropped items (the guard-only exam arm, T-0963) were already built, and T-2546 added the check only at capture. Assumption: matching can run in the prompt hook against MASTER.md clauses and the dropped ledger. It prints "this looks built at <path>" before work starts.
  Done when: a replay of the dropped-as-built asks triggers the note on at least a stated fraction, with zero hits on a control set of genuinely new asks.

- **Plant a known next-ask in a fixture history** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the sweep checks only that a cell's cited file exists, not that it behaves. Plant a habit in a synthetic history, a shuffled-history control arm and a fake habit that must not be over-learned. Each family must find the planted ask and fail on the control.
  Done when: the probe passes on the planted history, scores near chance on the shuffled control, and fails if the predictor over-learns the fake habit.

- **Predict the user's drop before Foreman files a self-filed task** — FEATURE — value 4 — effort M — risk med — category: initiative
  Why: the dropped ledger shows several self-filed tasks measured as not worth doing (the stack cards, the interpreter-specific baseline). Assumption: class-level drop rates from that ledger predict the next drop. A self-filed task whose class was dropped twice goes to a held list with the reason shown.
  Done when: a replay shows at least one of the dropped examples held instead of filed, and held items show their drop-class evidence.

- **Forecast machine runway with an ETA** — FEATURE — value 3 — effort M — risk low — category: machine model
  Why: the environment is tmpfs under `/run/user`, and the pack mentions a tmpfs children cap, so lanes can exhaust it. Read free space and the fill rate from the lane history, then warn "tmpfs full in ~N lanes" before spawning parallel builders.
  Done when: a fixture with a shrinking tmpfs makes `fm next` or the lane spawner warn before it fills, and refuse past a threshold.

- **Show a read-only Foresight card on the web UI Today page** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: web UI is the only surface in this mission. Assumption: nothing there shows foresight. The card shows the current heads-up, the last 20 forecasts resolved, hit rate by family, and an "as of" age with a stale banner. A dismiss button writes the same mute as the CLI.
  Done when: a screenshot test shows the card in empty, loading, stale and populated states, and dismiss changes the CLI output.

- **Wild: Time-machine replay of the forecaster** — FEATURE — value 4 — effort L — risk low — category: eval — wild
  Why: assumption: git history plus the asked stream let us check out each past date and ask "what would you have predicted?". The scorer reads what the user actually asked next. It yields a learning curve of hit@3 against history length.
  Done when: `fm foresight timemachine` outputs a dated hit-rate series over at least 20 past points, and the series is reproducible.

- **Wild: Write tomorrow's first-request stub tonight as a title-only task** — FEATURE — value 3 — effort M — risk low — category: speculative drafts — wild
  Why: assumption: the user's habits are regular enough that a title-only deferred stub costs no tokens. In the morning the stub is scored on whether the first real ask matched it, and an overlap is adopted. Unmatched stubs expire.
  Done when: after a fixture night, a matching first ask adopts the stub and a non-matching one leaves it expired and counted as a miss.

- **Wild: Hold a "contradiction court" between standing steers and recent behaviour** — FEATURE — value 3 — effort M — risk med — category: user model — wild
  Why: the steers list is long (28 or more) and some assume a live session or have ended conditions. If the user has done the opposite three times, propose retiring or restating the steer, never auto-remove it.
  Done when: a fixture steer contradicted three times appears in a weekly card with its evidence, and nothing changes without a yes.

Next question: Of the forecasts the user would actually read, which one sentence earns the user's attention at session start, and what does the exam say happens to their words-per-landed-task when it appears?
Next question: Which predictors are only valid on Claude transcripts, and what do codex, gemini, opencode and `fm code` sessions contribute to the model of me?
