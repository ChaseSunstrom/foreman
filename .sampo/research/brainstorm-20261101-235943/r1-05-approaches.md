# Brainstorm — lens: approaches

- **Backtest each cell before writing it** — FEATURE — value 5 — effort M — risk low — category: anticipation
  Why: Lesson from T-2546 (a word-overlap matcher met no bar). Replay `fmforesight` over the "asked" stream and closed tasks. A cell counts only if its predictor beats a trivial "repeat the last request" baseline, with the hit rate printed in the cell. Otherwise the cell is marked "no signal yet" and kept out of the 58.
  Done when: `fm genesis check` rejects a filled Anticipation cell with no backtest line, and a cell whose predictor loses to the baseline is listed as unfilled.

- **Fold the 58 cells into predictor families** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: This answers the open question about duplicates. Anticipation has about five predictors (next request, correction, breakage, machine, usage). The stage columns repeat them. Fill one grounded anchor per family and let the other stages inherit it with a stated condition, so no phrasing is reused.
  Done when: coverage.md lists at most about 8 anchor cells and the rest cite an anchor id, and the templated-cell lint passes.

- **Predict machine breakage from the package log** — FEATURE — value 4 — effort M — risk med — category: machines
  Why: Evidence from T-2529 (a Python without setuptools) and T-2543 (ETXTBSY), on a hardened-kernel Arch box. Read `pacman.log` and recent interpreter/library changes, then warn at session start that "Python or a lib changed since the last green `fm ship`, so run the full check first".
  Done when: a fixture log showing a Python minor bump makes the session-start note name the change, and a log with no change prints nothing.

- **Next-verb Markov table from the event log** — FEATURE — value 3 — effort S — risk low — category: habits
  Why: Assumption: the event log has verb sequences. Use a plain n-gram over `fm` verbs (after `task finish`, `ship` follows X% of the time). It needs no model call, and `fm next` shows it only when confidence is high and it beats the baseline.
  Done when: a backtest reports top-1 accuracy per verb, and `fm next` prints the prediction only above a set threshold.

- **Compute the model of me on demand from transcripts** — FEATURE — value 3 — effort M — risk low — category: privacy
  Why: This is the do-less approach: store no profile. Derive habits from the Claude Code transcript JSONL and Foreman's own ledgers at query time, so there is nothing to go stale or leak. The trade-off is slower queries, which a cache keyed on a transcript hash can offset.
  Done when: deleting the cache and running `fm me` rebuilds the same output, and no new persistent profile file exists.

- **Reuse shell history and git co-change for habits and breakage** — FEATURE — value 3 — effort M — risk med — category: reuse
  Why: Assumption: atuin or the zsh histdb is present. Read shell history and `git log --name-only` co-change counts instead of hand-building detectors, which fits the standing rule to use ecosystem tools first. Predict "files that usually change with this one" at plan time.
  Done when: editing a fixture file with a strong co-change partner prints that partner in the plan note.

- **Mark each cell with its reach path** — FIX — value 4 — effort S — risk low — category: reliability
  Why: The standing rule says every capability needs a real session path, and the pack asks which outputs no session path reads. Add a "called by" column (session start, `fm next`, drive, hook). A cell with no caller stays empty even if a verb exists.
  Done when: the sweep lists cells whose cited verb has no caller in the session-path index.

- **Negative model from the dropped ledger** — FEATURE — value 3 — effort S — risk low — category: precision
  Why: Dropped items such as "captured by mistake", "already built" and "unmeasured" show what not to predict or draft. Suppress speculative drafts that resemble a past drop.
  Done when: a draft matching a dropped-ledger entry is withheld and the withholding is logged with the matched entry.

- **Prefetch context instead of drafting requests** — PERFORMANCE — value 3 — effort M — risk low — category: anticipation
  Why: Assumption: drafting a whole request is the riskiest form of prediction. Pre-run `fm graph blast`, the affected tests and the stack card for the likely next files. This is cheaper and harmless when wrong, and cells for the riskier surfaces can say "prefetch only".
  Done when: the next task on a predicted file starts with a cache hit in the log, and a wrong prediction costs no edits.

- **Wild: stub-user twin written from steers only** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: wild. A tool-less child that sees only the steers and the "asked" stream writes the objection the user would raise against each plan. At finish it is scored against the user's real follow-ups, and a hit rate under 20% mutes it.
  Done when: a plan violating a stored steer gets a twin objection naming that steer in a fixture test.

- **Wild: a cell is a bet with a Brier score** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. Each filled cell states its prediction as a stored bet that the existing `fm outcomes --judgment` settles. A cell with no settled bets after 30 days turns "unproven" on the grid. The grid then shows only anticipation that has actually been tested.
  Done when: `fm outcomes --judgment` groups bets by cell id and the sweep flags cells with no bets.

- **Wild: search for counterexamples to every "n/a"** — SECURITY — value 3 — effort S — risk low — category: wild
  Why: wild. The standing rule says n/a needs a counterexample search. A cheap child tries to write a realistic Anticipation scenario for each n/a cell, and any scenario it writes reopens the cell as a gap.
  Done when: each n/a cell records a search transcript hash, and a planted false n/a gets reopened in a fixture.

- **Re-run each cell's probe every sweep** — CLEAN — value 4 — effort M — risk low — category: coverage rot
  Why: This answers the question about cells going stale. Today the sweep checks that the cited file exists, not that it still behaves as claimed. Store a probe command per cell and run it at each sweep. A probe that fails turns its cell red.
  Done when: renaming a cited function turns its cell red in `fm genesis sweep`.

Next question: Which of Anticipation's predictors have ever changed what the user did next, rather than only being logged?
Next question: What does the user do in the first minute of a session that a prefetch could already have done?
