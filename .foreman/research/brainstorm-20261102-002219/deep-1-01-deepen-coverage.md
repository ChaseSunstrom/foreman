# Brainstorm — lens: deepen: coverage

- **Fill the grid through one triage ledger, then prose only for gaps** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the pack's coverage ideas converge on "triage before prose," and the standing rule says a cell counts only if it names a concrete capability grounded in a file or a real gap. The 58 cells are the request itself.
  Done when: `fm genesis sweep` reads a ledger with one row per cell (verdict existing/gap/n-a, grep proof, cited path) and reports 0 empty cells, 0 templated, 0 duplicated.

- **Re-run each cell's cited path at sweep time** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the pack's open question: "can the sweep check that a cited forecast path still fires after later generations change it?" Today only file existence is checked, so cells rot silently.
  Done when: planting a rename of a cited function turns that cell red in `fm genesis sweep` and names the cell.

- **Tag every cell with harness and backtest class** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: the earlier questions ask which cells quietly depend on Claude Code and which have too little history to backtest. Both are answerable by one tag per cell (harness: claude-code/any/fm-code; class: measured/planted-only).
  Done when: every cell carries both tags, and `fm genesis check` lists the cells that are claude-only or planted-only.

- **Require a reachable session path per cell** — CLEAN — value 4 — effort M — risk med — category: reachability
  Why: the standing rule says every capability must be called by a real session path, and the pack asks which anticipation outputs no session path reads. Static reachability from session start, `fm next`, the drive, skills and hooks gives a checkable answer.
  Done when: a cell citing a verb no session path calls fails the sweep with the verb's name.

- **Accept n/a only after a counterexample search** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: n/a is the cheapest way to fill a cell dishonestly. Requiring a one-line "the user never meets this here" plus a failed grep for the stage's verbs keeps n/a honest.
  Done when: an n/a cell whose stage verbs appear in the surface's code is rejected with the matching file:line.

- **Fill by column rule, with cells as exceptions** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the pack's "do less" idea. Columns share behaviour (e.g. every web UI stage reads the same goal receipt), so a per-column default plus an exceptions list cuts the prose and the template-reuse risk. Caveat: the standing "no reused phrasing" rule means a rule-derived cell still needs a distinct grounding.
  Done when: the grid renders from rules plus exceptions, the sweep's templated check passes, and the file is shorter than the 58 prose cells.

- **Two blind fillers, with disagreement counted as the gap** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: the standing rule prefers signals Foreman didn't author. Two cheap-model fillers that never see each other's output give a free uncertainty signal. Assumption: Haiku-class cost is acceptable under the current testing cadence.
  Done when: cells where the fillers disagree on existing/gap/n-a are listed first for review, and the count appears in the sweep.

- **Rank the 58 cells by what a resume would notice missing** — FEATURE — value 3 — effort S — risk low — category: prioritisation
  Why: the capability is "carries the plan over days, across crashes and compactions." Weighting cells by the stages a crash or compaction exposes puts the costliest gaps first, and `fm next` can order work from it.
  Done when: `fm genesis coverage --rank` prints cells ordered by a stated resume-impact score.

- **Fuzz the coverage.md parser** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: the 58-cell count depends on parsing a markdown table, so pipes inside cells, CRLF and placeholder text could silently miscount empties. The user's rule that an empty cell is the ledger's unit makes the count load-bearing.
  Done when: a test feeds cells with escaped pipes, CRLF and "TBD"-style placeholders and the parser's empty count matches a hand-counted fixture.

- **Wild: Compute the grid live and store only exceptions** — FEATURE — value 4 — effort L — risk high — category: coverage
  Why: wild. If columns are rules, a generator derives each cell from the code at sweep time and the file keeps only the human exceptions, so the grid cannot drift from the code.
  Done when: deleting a cited feature in a scratch copy changes the derived cell without any edit to coverage.md.

- **Wild: Delete the cited feature in a scratch copy and see which cells survive** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: wild. A mutation test for the grid: if removing a feature leaves its cell green, the cell is decoration, not coverage.
  Done when: for each cell the sweep records whether its removal turned the cell red, and lists the survivors.

- **Wild: Let a tool-less child invent the 58 cells blind, then diff against reality** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: wild. This extends the standing rule that exam scenarios come from a child that never sees Foreman's code. The diff shows which moments the grid's author never thought of.
  Done when: a report lists the child-invented moments with no matching cell, and each becomes a cell or a recorded n/a.

- **Wild: Refuse the 59th cell unless one is retired** — CLEAN — value 2 — effort S — risk med — category: lean
  Why: wild. It borrows from the lean-substance work, where growth needs a measurement. Assumption: this conflicts with the rule that Genesis may only add grid categories via `fm genesis grow`, never remove them, so it would apply to cells and not to rows or columns.
  Done when: adding a cell past the cap without retiring one fails `fm genesis check`.

Next question: Which of the 58 cells does a user's actual goal run reach in practice, as measured from the ledger of finished goals, and which have no run touching them?
Next question: When a cell's cited verb is renamed or removed in a later generation, who or what notices first: the sweep, a test, or the user?
