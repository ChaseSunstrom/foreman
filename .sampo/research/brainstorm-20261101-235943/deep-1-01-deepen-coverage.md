# Brainstorm — lens: deepen: coverage

- **Compile the 58 cells into one executable predictor-family table** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the earlier ideas repeatedly say "collapse into predictor families"; the standing rule says templated cells don't count. A table (family → signal source → fmforesight symbol → session path → backtest) makes the cells rows of data that code reads, not prose. Assumption: most of the 58 reduce to under 10 families.
  Done when: `fm genesis check` loads the table, every one of the 58 cells maps to a family row or a recorded n/a with a counterexample search result, and the count of distinct families is printed.

- **Make the sweep re-run each cell's probe, not just resolve its file** — FEATURE — value 5 — effort M — risk low — category: sweep
  Why: the pack's open question is whether the sweep checks that a cited file still behaves as claimed after later generations. T-2547 only checks grounding lines exist. Assumption: a probe is a one-line command with an expected output.
  Done when: changing a cited function so its behaviour breaks turns the sweep red naming the cell, with the probe's output quoted.

- **Backtest each family on real history before it fills a cell** — FEATURE — value 5 — effort M — risk med — category: backtest
  Why: the Missions 3-5 lesson says to name the backtest that decides whether a heuristic ships (T-2546's word-overlap matcher met no bar). Replay the task and steer history: at time t, predict the next request, score against what was asked.
  Done when: `fm foresight backtest` prints hit rate per family on the recorded asks and a cell is refused if its family is below the stated bar or has fewer than N events.

- **Reverse-map the dropped-as-built ledger onto cells** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the dropped lines (guard arm "already built", fm check interpreter, stack cards) show Foreman keeps re-proposing built things; each is proof a cell is already covered by an existing path. Assumption: the ledger names the file in most entries.
  Done when: each dropped-as-built entry is attached to at least one cell as its existing-path citation, and the number of empty cells falls by the count of matches, listed.

- **Seed cells from the eight missed asks** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: T-2532, 2533, 2534, 2535, 2536, 2542, 2546 and 2547 are asks the user had to make unprompted. Each belongs to a stage (flag problems before they happen, draft on spec) with no predictor; the cells they fall in are the true gaps.
  Done when: each of the eight is mapped to a cell and a predictor that, run on the history before that task, would have raised the issue; those that wouldn't are filed as tasks.

- **Run the n/a counterexample search as a gate on every n/a** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: the pack asks which cells would stay empty under the rule. Assumption: the rule is stated but not enforced in code.
  Done when: `fm genesis put` refuses an n/a cell with no searched counterexample query recorded, and the n/a list is printed with each search's result.

- **Expire n/a rulings when a new capability lands** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: the standing rule says every Seed retries items a new capability may unblock; n/a cells are the same kind of item.
  Done when: adding a capability to frame.md through `fm genesis grow` reopens the n/a cells in its row, and the sweep lists them as pending.

- **Rank the empty cells by minutes lost from the ledger** — FEATURE — value 4 — effort M — risk med — category: prioritisation
  Why: the grid has no order but row order, while the ledger and `fm friction` hold real costs. Assumption: friction rows can be tied to stages by keyword and task kind.
  Done when: the Seed's cell list is sorted by recorded cost and names the top five with the figures behind them.

- **Cover cells via a set-cover over MASTER.md module clauses** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: T-2546 already matches requests to those clauses, so a clause that covers several cells is the smallest probe set the open question asks for. Assumption: clauses carry task ids.
  Done when: a greedy set-cover prints the fewest clauses covering all non-n/a cells and the sweep uses that as the probe list.

- **Check that every filled cell's output is read by a session path** — FEATURE — value 5 — effort M — risk med — category: reach
  Why: the standing reach rule and the open question about deliberation outputs nobody reads. A prediction that is only a file is not anticipation.
  Done when: the sweep reports, per cell, the session path (session start, fm next, the drive, a hook) that reads its output, and fails any cell with none.

- **Wild: Let a stub user file the complaints a cell should prevent** — FEATURE — value 3 — effort L — risk med — category: coverage
  Why: wild. A tool-less child plays the user from the steers alone (never seeing Foreman's code) and writes the next three complaints per stage; a cell counts only if a predictor would have raised each before it was made.
  Done when: a run yields complaints per cell and the sweep prints the share of them that fmforesight flags in a dry run.

- **Wild: Compute the grid live and store only exceptions** — CLEAN — value 4 — effort L — risk high — category: coverage
  Why: wild. Instead of a 58-cell prose grid, derive coverage from the predictor table, probes and session-path reads at sweep time; coverage.md then lists only the n/a rulings and known gaps, so it cannot go stale or templated.
  Done when: deleting coverage.md's filled rows changes no sweep result, and the sweep regenerates the grid from code.

- **Wild: Let filler children bid by confidence and leave low bids as gaps** — FEATURE — value 3 — effort M — risk med — category: coverage
  Why: wild. Several tool-less children propose a fill for each cell with a stated confidence; disagreement or low confidence leaves the cell open, so honest gaps surface instead of confident filler text.
  Done when: each cell records the number of bids and their spread, and a cell with a spread over the threshold is reported as a gap rather than filled.

- **Settle a cell's conflicting fills with a blind second filler** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: the cold-read rule already uses Haiku then Sonnet, but only for pass/fail; a second independent fill compared with the first catches the templated phrasing the rule forbids.
  Done when: two fills per cell are compared, and a pair with matching wording is flagged as templated and sent back.

Next question: Which of the 58 cells does the existing history have too few events to backtest, so that a probe could only be planted and not measured?
Next question: Does `fmforesight` have a public interface a cell can cite, or are its predictors only reachable through other modules that would break the citation?
