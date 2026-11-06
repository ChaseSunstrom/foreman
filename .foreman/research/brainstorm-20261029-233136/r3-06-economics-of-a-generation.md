# Brainstorm — lens: economics of a generation

- **Stop on the knee of the curve, not the budget** — FEATURE — value 5 — effort M — risk low — category: stopping rule
  Why: the pack lists budget caps and "stop early once marginal gain falls off" separately, but nothing defines the rule. Assumption: `exam.jsonl` scores arrive per scenario, so a running closed-per-dollar slope can be computed between stages.
  Done when: on a fixture tower where scenarios 1–6 close at $1 each and 7–9 cost $6 each, `fm genesis run` halts after 6 and writes "stopped: marginal $/scenario 6× the running mean" into the generation's status.

- **Price the generation before it starts, then hold to the quote** — FEATURE — value 5 — effort M — risk low — category: forecast
  Why: the pack proposes quoting and calibrating forecasts, but no one has made the quote a precondition. Assumption: the child-call count per stage is predictable from the mission count and the exam size.
  Done when: `fm genesis plan` prints a low/expected/high USD and wall-clock range per stage, and `status` shows actual against quote, flagging any stage over 1.5× its high.

- **Price a rewrite by marginal scenarios per dollar over its parent** — FEATURE — value 5 — effort S — risk low — category: selection
  Why: the current rule is "closes more exam scenarios than its parent". A rewrite that ties at 3× the cost still passes on a tie-break or a one-scenario edge. Assumption: both arms' cost is logged in `exam.jsonl`.
  Done when: a fixture rewrite that closes +1 scenario at 3× cost loses selection, and lineage.md records "lost: +1 scenario for +$4.20 (threshold $1.50/scenario)".

- **Run the cheap screen first, full exam only on survivors** — PERFORMANCE — value 4 — effort M — risk med — category: cost cut
  Why: the exam has at least 9 scenarios per capability and plain-Claude arms are expensive. Assumption: a 3-scenario cheap subset (the oracle/empty/finders arms need no session) predicts the full result well enough to drop obvious losers.
  Done when: on 5 past rewrites, the screen rejects every loser that the full exam rejected, and total exam spend drops at least 30%. The screen's false-reject count is reported.

- **Pause on a usage limit and resume at the reset** — FIX — value 4 — effort M — risk low — category: quota
  Why: the request says a week of usage on one project is a failure mode. Assumption: the harness exposes a rate-limit signal or reset time on a capped child.
  Done when: a simulated limit mid-generation writes a journal entry with the resume time, the tower sleeps without polling, and the next run continues from the same step with no repeated child calls.

- **Reuse any stage whose inputs are unchanged** — PERFORMANCE — value 4 — effort M — risk low — category: caching
  Why: each generation re-runs Seed, missions and exams even when a parent's artifacts are identical. Assumption: stage inputs can be hashed (gen-0, parent doc, exam keys, model ID).
  Done when: a second generation that changes only one mission re-runs only that mission's brief, critique and exam, and `status` shows "reused 6/7 stages, saved ≈$X".

- **Charge auto-start for what the last auto-start produced** — SECURITY — value 4 — effort S — risk low — category: spend guard
  Why: the pack proposes auto-start when the queue runs dry, so a quiet project could burn money in a loop. Assumption: closed scenarios and cost per tower are recorded.
  Done when: after an auto-started tower that closed 0 scenarios, the next auto-start proposal is suppressed until the user acts, and the reason cites the previous tower's cost and yield.

- **Report the user's own time as a cost** — FEATURE — value 4 — effort S — risk low — category: user attention
  Why: the user's habit of terse steers suggests approvals are the scarce resource, not dollars. Assumption: each question card or approval can be counted from the tower journal.
  Done when: the generation receipt shows "$X, Y min wall-clock, Z asks to you", and a generation that asked for more than N approvals is flagged for batching.

- **Rank the not-yet ledger by expected value per retry dollar** — FEATURE — value 4 — effort M — risk low — category: retry economics
  Why: the ledger is retried every generation, so a blocked item that fails the same way each time wastes a retry. Assumption: each entry stores attempts, cost per attempt and blocker class.
  Done when: with a $2 retry budget on a fixture ledger of 6 entries, only the top-ranked entries run, and an entry that failed twice with the same blocker is skipped unless its blocker changed.

- **Show the cost-per-closed-scenario curve against plain Claude** — FEATURE — value 3 — effort M — risk low — category: reporting
  Why: the exam already has foreman and plain session arms with cost. Nothing shows whether Genesis beats a plain session per dollar. Assumption: the site tower page can render a chart from the exported JSON.
  Done when: the Genesis page plots cumulative USD against scenarios closed for each generation and a plain-Claude baseline line, from `exam.jsonl` alone.

- **Wild: Let generations bid for budget** — FEATURE — value 3 — effort L — risk med — category: allocation
  Why: wild. Each mission submits a one-line bid ("expect +3 scenarios for $4"), and the orchestrator funds the best ratios first, then scores bids against actuals so honest bidders get more room next time.
  Done when: on a fixture with three missions, the funding order matches bid ratios, and a mission that overbid by 2× gets a smaller allotment in the next generation.

- **Wild: Quote the tower like a contractor and refund the overrun to a rainy-day fund** — FEATURE — value 3 — effort M — risk low — category: budgeting
  Why: wild. Underspend from a generation that stops early goes into a fund the not-yet retries and the held-out rotation can draw on, so saving in one place buys depth in another.
  Done when: a tower that finishes $3 under its quote shows a $3 fund balance, and a later not-yet retry draws from it with the balance decremented in `status`.

- **Wild: Run a cheap-model twin tower and spend big only where it diverges** — PERFORMANCE — value 4 — effort L — risk med — category: model routing
  Why: wild. A small-model tower runs the whole sequence first. The expensive model re-runs only the stages where the twin's selection or drift verdict differs from a quick sanity check, or the twin's confidence is low.
  Done when: on three fixture projects, total spend falls at least 40% against the all-large run while the final selections match in at least 2 of 3. Mismatches are listed.

- **Wild: Sell the salvage of a failed generation** — FEATURE — value 3 — effort M — risk low — category: waste recovery
  Why: wild. When a generation is aborted or loses selection, its passing scenarios, briefs and critiques are filed as reusable parts, so the sunk cost is credited back toward the next attempt.
  Done when: after a losing rewrite, `fm genesis status` lists the salvaged items with their original cost, and the next generation's quote subtracts the reuse.

Next question: What does one closed scenario actually save the user — in minutes of their own work or regressions avoided — so that "cost per closed scenario" has a break-even to compare against?
Next question: How much of a generation's spend is the plain-Claude comparison arm, and would a sampled or cached baseline change any selection decision?
