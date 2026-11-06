# Brainstorm — lens: simplicity

- **Collapse the 58 cells into one predictor-family table** — CLEAN — value 5 — effort S — risk low — category: coverage
  Why: "Which of the 58 cells are really one capability counted under several stages" is an open question, and the pack's earlier ideas keep proposing family-level fills. Standing rule says templated cells don't count. Anticipation is really about 4–5 families (next request, correction shape, breakage on this machine, problem flag, skip/drop). One table of families × stages, each cell a file reference, makes most cells "same family, cited once".
  Done when: the table has ≤8 family rows, every grid cell resolves to a family row plus a file path, and the templating linter passes with zero duplicates.

- **Read forecasts from `fm next`, add no new verb** — FEATURE — value 5 — effort S — risk low — category: reach
  Why: the standing rule requires a real session path to call each capability. The reach check fails for verbs only the user types. Putting one ranked "likely next" row in `fm next` and the SessionStart line gives every cell a reach path without a new surface.
  Done when: `fm next` prints at most one forecast row sourced from fmforesight, and `fm genesis check` reach finds no foresight verb unreached.

- **Make fmforesight stateless over existing ledgers** — CLEAN — value 4 — effort M — risk med — category: foresight
  Why: assumption: the asked stream, outcomes, decisions and dropped ledgers already hold everything. A separate model-of-me store adds drift, a place to forget, and a lean-ratchet cost. Compute on demand, store nothing.
  Done when: deleting any foresight cache file changes no output, and a test proves rebuild-from-sources equals the prior result.

- **Strip test captures from the user model's input** — FIX — value 4 — effort S — risk low — category: data hygiene
  Why: dropped ledger: "The first brief" and "The second brief" were captured by mistake from T-2547's test and still appear in the asked stream. They would poison any request predictor.
  Done when: items whose drop reason says "captured by mistake" or that come from a test cwd are excluded, and a red-first test shows the two sample lines absent from the predictor input.

- **Gate every predictor on a walk-forward backtest, with one baseline** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the lessons say T-2546's word-overlap matcher met no bar; the rule is to name the backtest that decides shipping. Baseline is "predict the last request repeated".
  Done when: a predictor that doesn't beat the baseline on the asked stream is reported as "abstained", never drafts a lane, and the report prints hit rate versus baseline.

- **Stay silent below an evidence floor** — FEATURE — value 4 — effort S — risk low — category: restraint
  Why: assumption: flags the user dismisses cost trust more than missed ones. Cap at 3 live forecasts and mute a signature after two dismissals.
  Done when: a test with fewer than N supporting events prints nothing, and a signature dismissed twice never reappears.

- **Mark most cells n/a by rule with a counterexample search** — CLEAN — value 4 — effort S — risk med — category: coverage
  Why: the open question about the "n/a needs a counterexample search" rule. Stages like web UI × predict-skip often have no meaning. A recorded grep that returns empty is cheaper than prose.
  Done when: each n/a cell holds the search command and its empty result, re-run by the sweep.

- **Re-run each cell's citation as a probe every sweep** — FIX — value 4 — effort M — risk low — category: coverage rot
  Why: the open question asks whether the sweep checks that a cited file still behaves as claimed, not just that it exists.
  Done when: breaking a cited function in a scratch copy turns its cell red in the sweep.

- **Park a predicted ask as a title-only deferred task** — FEATURE — value 3 — effort S — risk low — category: drafts
  Why: speculative lanes cost tokens and can be wrong. A title-only deferred row costs nothing and spends tokens only on a yes, with a grounding line (already built? check via fmrecall.covered).
  Done when: a forecast creates a deferred task carrying a grounding line and an expiry, and no lane starts until the user accepts.

- **Wild: Predict by grep alone** — FEATURE — value 3 — effort S — risk low — category: baseline
  Why: wild. A zero-learning predictor (nearest past ask via `fm recall`) may match a heavier one. Its score sets the bar for everything else.
  Done when: the baseline's hit rate on the asked stream is recorded beside every other predictor.

- **Wild: A shuffled-history control arm** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: wild. Run the forecaster on a shuffled stream. If it still "hits", the hit rate is an artefact.
  Done when: the control's hit rate is printed and the real predictor must beat it by a stated margin.

- **Wild: Refuse the 59th verb unless one is retired** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: wild. Anticipation tends to add verbs; the lean ratchet rewards subtraction.
  Done when: `fm task finish` fails a task that adds a verb with no recorded retirement.

- **Delete forecasts nobody read** — CLEAN — value 3 — effort S — risk low — category: observability
  Why: the open question about deliberation outputs no session path reads. Stamp each forecast with a read receipt and prune unread ones after 14 days.
  Done when: an unread forecast older than 14 days is removed and counted in `fm doctor`.

Next question: Which of the five predictor families actually beats "repeat the last request" on the real asked stream, and does any beat it by more than the noise?
Next question: If foresight were deleted tomorrow, what would the user notice within a week, and which cells would still be defensible?
