# Brainstorm — lens: approaches

**Questions left earlier (what this lens can answer):**
- *Which cells are really one capability counted under several stages?* Assumption: most of the 58 differ only by stage column while one predictor serves them. A set-cover over probes (idea 2) answers it with a number instead of a guess.
- *Does the sweep re-verify a filled cell?* Assumption: it only checks that the cited file exists. Ideas 3 and 8 add the behaviour check.

- **Race four predictor approaches on the asked stream** — FEATURE — value 5 — effort M — risk low — category: anticipation
  Why: the Missions 3-5 lesson says a heuristic ships only if a backtest on real history decides it, and T-2546's matcher met no bar. Race queue-order, verb n-gram, nearest past ask via `fm recall`, and a Haiku few-shot, all on a walk-forward split. Each cell then names its winning approach and hit@3.
  Done when: `fm foresight race` prints hit@3 and cost per approach per request kind, and the cell text cites the winner by name.

- **Cover the 58 cells with a minimal probe set** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the grid probably counts one capability under several stages. Build the cell-to-probe incidence matrix and pick probes by greedy set cover. Cells covered by the same probe cite it and add only a stage-specific delta line.
  Done when: `fm genesis sweep` prints "58 cells / N probes" and every cell resolves to a probe id.

- **Fill in a sweep-in-the-loop ratchet** — FEATURE — value 4 — effort S — risk low — category: genesis
  Why: the rule is "no templated or duplicated cell." Write one cell, run the coverage sweep, keep it only if the templated and duplicate counts don't rise, otherwise revert it and retry once with a different approach. This is generate-and-test with the existing sweep as the oracle.
  Done when: the fill log shows an accept or revert per cell, and the final sweep reports 0 empty, 0 templated.

- **Start from the eight missed asks and work backwards** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: the pack lists T-2532 to T-2547, asks no brainstorm predicted. For each, name the cell that would have fired. Cells that catch a miss get it as their grounding line, and misses with no cell become the real gap tasks.
  Done when: each of the eight asks is attached to a cell id or to a filed gap task.

- **Show a read-only Foresight panel in the web UI** — FEATURE — value 4 — effort M — risk med — category: web UI
  Why: the mission's only surface is the web UI, and the pack asks what the user gets if they never open it. The panel renders the ranked predictions, the problem flags with lead time, and the grid status from the JSON `fmforesight` already produces. It adds no new predictor and also states which session path surfaces the same data.
  Done when: a browser check of `index.html` shows the panel with an empty state and a populated state, and the cell names the session path that makes the same line appear in `fm next`.

- **Fill from a fixture history with a planted next ask** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: a cell is only real if it fails when the capability is removed. Each cell gets a planted-history fixture with a known next request, and the probe must fail on the parent of the feature commit. This is the "red-first" rule applied to coverage.
  Done when: every cell's probe is red on the pre-feature tree and green now, recorded in the sweep.

- **Inherit from Initiative with a mandatory delta** — CLEAN — value 3 — effort S — risk med — category: coverage
  Why: do-less approach. Where Anticipation shares a tick, trigger table or lane with #1 or #2, the cell is "inherits row X" plus one required delta sentence about what is Anticipation-specific. An inherited cell with an empty delta is rejected as templated.
  Done when: the linter rejects an inherit cell with no delta, and the inherit count is printed.

- **Plot the learning curve: hit@3 against history length** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: assumption: a new repo has little history, so Anticipation may do nothing there. Replaying the stream at growing prefix lengths finds how many asks it needs before it beats the queue-order baseline. That sets an evidence floor below which it stays silent.
  Done when: `fm foresight curve` prints the break-even history length, and foresight output is suppressed below it.

- **Re-run each cell's cited behaviour, not just its file** — FIX — value 4 — effort M — risk med — category: genesis
  Why: the left-over question about later generations changing a cited file. The sweep runs each cell's probe command and compares the result to a stored expectation. A file that exists but behaves differently turns the cell red.
  Done when: editing a cited function to return `[]` turns exactly its cells red in `fm genesis sweep`.

- **Wild: let a stub user write the cells' complaints** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: wild. A tool-less child that sees only the steers writes one annoyed sentence per surface×stage ("it didn't warn me before I shipped"). Sentences that no cell answers are the gaps, which is cheaper than inventing 58 capabilities.
  Done when: the unanswered complaints are listed and each one is either a filed task or a recorded n/a with a counterexample search.

- **Wild: shuffled-history control arm** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: wild. Run the predictors on the real asked stream and on a shuffled copy. If hit@3 is the same, the predictor is just echoing frequent words and the cell does not count.
  Done when: the race output includes a shuffled-control column and a predictor within noise of it is marked "no signal."

- **Wild: delete `fmforesight` in a scratch copy and diff the exam** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. Cells whose scenarios score the same without the module are n/a by evidence rather than by assertion. This answers the "n/a needs a counterexample search" rule with a measurement.
  Done when: the scratch run produces a per-cell with/without table and the n/a cells cite it.

Next question: Which of the four predictor approaches costs the least per correct hit@3, and is any of them cheaper than doing nothing?
Next question: What does Anticipation show for a repo with fewer than 20 asks, and does the user see silence or a guess?
