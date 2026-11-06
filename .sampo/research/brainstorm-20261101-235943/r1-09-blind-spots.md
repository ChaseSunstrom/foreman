# Brainstorm — lens: blind spots

- **Beat-check the forecaster itself** — FIX — value 5 — effort S — risk low — category: reliability
  Why: T-2532 and T-2542 both asked for "never silently off" after a component died quietly. The question that would have caught them is "which part of this loop fails with no trace?" Nothing in the pack shows `fmforesight` has a beat, and a dead predictor looks the same as one with nothing to predict.
  Done when: a test that kills the forecast step makes the next session's Watch line and `fm doctor` name it, with the time of its last good run.

- **Check "already built" before any predicted draft is lane-ed** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: T-2546 and the dropped guard-only arm (already at fmexam.py:2893) show the user keeps asking for things that exist. A predictor that drafts a request in a lane would repeat that error at scale. `fmrecall.covered` and the MASTER.md clause match exist but aren't on the prediction path.
  Done when: a predicted request that matches a MASTER.md clause is dropped with the clause and task id logged, in a test.

- **Refuse a predicted draft without a grounding line** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: T-2547 refuses a Mission with more briefs than grounding lines. The question that was missed: "where is a claim counted without evidence?" The same hole applies to speculative drafts, which carry no evidence of need.
  Done when: a draft whose "why predicted" cites no steer, asked line or ledger row is rejected in a unit test.

- **Meter the forecaster's cost in the lean ratchet** — FEATURE — value 4 — effort M — risk low — category: lean
  Why: T-2533 added hook-note chars to the ratchet because that cost was unmetered. Speculative lanes, the forecast note at session start and the nightly tick are also unmetered. Assumption: they aren't counted today.
  Done when: `fm doctor` shows forecast chars injected per session and speculative-lane tokens per week, and the ratchet trips on growth.

- **Name the cause when predictor precision drops** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-2535 names the commit behind each grown metric. The missed question was "when a number gets worse, does it say who did it?" The same applies to hit rate.
  Done when: a drop in hit rate over the last N scored predictions prints the first commit, model change or input shift that fits, checked on a seeded regression.

- **Ablate each forecast source** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: T-2536 files a cleanup candidate per hook feature whose off arm changed nothing. Forecast inputs (asked stream, co-change, open work) have no such test, so none can ever be cut.
  Done when: `fm bench` runs the backtest with one source off per arm and files a candidate for any source whose removal changes no hit.

- **Backtest on the asked stream before any predictor may draft** — FEATURE — value 5 — effort M — risk med — category: anticipation
  Why: the Missions 3-5 lesson says a heuristic needs a named backtest, and T-2546's word-overlap matcher met none. This sets the gate for "may draft a lane".
  Done when: a predictor beating the repeat-last-request baseline on a replay of closed tasks is the only kind a drafting lane accepts, and a test shows a failing one muted.

- **Triage the 58 cells into one capability list before writing prose** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: this answers the pack's question on duplicate cells. Run a pass that tags each cell existing, gap or n/a, citing a file or a failed counterexample search, and fill only what is left.
  Done when: every cell has a tag and a resolvable citation, and the count of distinct capabilities is printed beside 58.

- **Re-check cited files still behave as claimed** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: the pack asks whether the sweep checks behaviour or only existence. Each cell gets a one-line probe, run at sweep time. A probe that fails turns the cell red.
  Done when: deleting the cited function in a scratch copy turns its cell red in the sweep.

- **Read dropped-as-built asks at session start** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the guard-only arm and the two "captured by mistake" briefs were dropped as already built or accidental. The class "things the user keeps re-asking" is a signal for the forecaster.
  Done when: a request matching a dropped-as-built item prints the earlier answer and task id, in a test.

- **Wild: A ghost-user child writes the next ask blind** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild. A tool-less child sees only the steers and the changelog and writes the user's next three asks. These are scored against what arrives, and each miss becomes a regression probe.
  Done when: the nightly run stores three predictions and scores them after the next three real asks.

- **Wild: "What I would have told you" card on resume** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. After a break, one card lists problems the forecaster saw coming, each with the user's own earlier words as evidence.
  Done when: a resumed session prints at most three items, each citing a ledger row or steer.

- **Wild: Predict which gate will trip before ship** — FEATURE — value 3 — effort M — risk med — category: reliability
  Why: wild. Many recent asks were gate or ratchet failures found late (T-2535, T-2529). Run the lean ratchet and fm check in a shadow tree against the pending diff before the user types ship.
  Done when: a seeded diff that would trip the ratchet gets a warning before `fm ship`.

- **Wild: Replay the last 20 asks through today's forecaster** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: wild. Walk the "asked" stream in order, predicting each ask from the ones before it, then show a calibration table.
  Done when: `fm foresight replay` prints hits and misses for 20 asks in under a minute.

Next question: Which writes does `fmforesight` make that no session path ever reads, so a nonsense prediction would go unnoticed?
Next question: Which of the 58 cells would a stranger repo with no "asked" history leave empty, and is anticipation then a no-op there?
