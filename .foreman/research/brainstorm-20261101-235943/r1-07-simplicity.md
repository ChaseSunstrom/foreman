# Brainstorm — lens: simplicity

Answering the earlier questions my lens can: many of the 58 cells are one forecast kind seen from different surfaces and stages, so the smallest probe set is one per kind (repeat, follow-up, wait-release, drift) run on each surface. Nothing in the pack shows a read path for fmforesight output beyond the session start note, which is what ideas 2 and 5 test.

- **Show the forecast as a ranked row in fm next, not a new verb** — CLEAN — value 4 — effort S — risk low — category: surface
  Why: assumption: fm next is already the session path the user meets (the standing rule says a capability must be called by one). A separate `fm foresight` verb would exist only as a verb.
  Done when: `fm next` prints a row tagged `predicted` with its evidence count, and no new top-level verb is added to the verb list.

- **Give foresight a slot, not an addition** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the lean ratchet fails on injected-context growth (T-2503/2504), and the SessionStart note is the only reach path. Assumption: one existing note line is lower-value.
  Done when: the SessionStart note's byte count is no greater with foresight on than with it off, and the line it replaced is named in the task.

- **Stay silent below an evidence floor** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: T-2546's word-overlap matcher met no bar. A predictor with few history rows is the likeliest to be wrong and to look confident.
  Done when: a project with fewer than N closed tasks yields no forecast row and prints `foresight: not enough history (k of N)`, under a test.

- **Make fmforesight stateless over the ledgers that already exist** — CLEAN — value 3 — effort M — risk med — category: architecture
  Why: the asked stream, fm outcomes and fm friction already hold the history. A private store would be a second copy to drift.
  Done when: deleting foresight's own state file changes no forecast, because every row is recomputed from the ledgers.

- **Put a read receipt on every foresight output and delete the unread** — CLEAN — value 4 — effort M — risk low — category: reach
  Why: an earlier brainstorm asked which deliberation outputs no session path reads. The standing reach rule makes an unread output a liability.
  Done when: each output type logs when it was shown or read, and `fm doctor` lists any type with zero reads in 30 days, naming it as a deletion candidate.

- **Diff `fm doctor` snapshots per host to flag drift before it bites** — FEATURE — value 4 — effort M — risk low — category: machines
  Why: T-2529 (no setuptools) and T-2543 (ETXTBSY) were machine-specific breaks. The gen-0 text asks for a model of "my machines" and flags before things happen.
  Done when: after the interpreter or a tool version changes between two snapshots, the next session start names the change and the check it affects.

- **Park a predicted ask as a title-only deferred task, spend tokens only on a yes** — FEATURE — value 3 — effort S — risk low — category: drafting
  Why: a drafted lane costs tokens on a guess. A title costs nothing and still gives `fm next` something to rank. Assumption: the title alone is useful to the user.
  Done when: a forecast creates a deferred task with a `predicted` origin and no lane. `fm accept ID` starts the draft, and an unaccepted one expires unmerged.

- **Cap live forecasts at three per project** — FEATURE — value 2 — effort S — risk low — category: attention
  Why: the user's queue already holds about 30 deferred items. A fourth guess adds noise, not information.
  Done when: a test with five candidates shows only the top three, and the rest are dropped without being filed.

- **Exclude test-run captures from fm intake** — FIX — value 3 — effort S — risk low — category: data hygiene
  Why: two items were dropped as "captured by mistake: a sample line fed to fm intake while debugging T-2547's test". Any model of the user's requests would learn from that noise.
  Done when: a test calling fm intake under the test flag writes nothing to the asked stream.

- **Predict by grep: nearest past ask through fm recall, no learning** — FEATURE — value 3 — effort M — risk med — category: approach — wild
  Why: the cheapest baseline is "the next ask looks like the last similar one". T-2546 shows word overlap failed once, so this ships only with a backtest line on the real asked stream.
  Done when: a recorded backtest compares it with the queue-head baseline, and it ships only if it wins on at least one task kind.

- **Add a weekday-and-hour seasonality predictor as a one-line baseline** — FEATURE — value 2 — effort S — risk low — category: baseline — wild
  Why: assumption: habits repeat by day (release Fridays, cleanup Mondays). It is nearly free to try and sets the bar every smarter predictor must beat.
  Done when: its hit rate sits in the prediction ledger beside the other predictors, and `fm doctor` marks any predictor that loses to it.

- **Forecast only "skip": name the queue item the user is about to drop** — FEATURE — value 3 — effort M — risk med — category: queue — wild
  Why: the pack shows many drops (built already, captured by mistake, measured not worth it). Predicting a drop saves the user a decision and costs no build.
  Done when: for an old deferred item that resembles prior drops, `fm next` shows `likely drop: reason`, and the user's accept or reject is logged.

Next question: Which forecast kind could be deleted outright with no change in the user's next-day behaviour, and what experiment would show it?
Next question: Does any cell's filled citation point at code that only runs when the user opens the web UI, and so never reaches a user who doesn't?
