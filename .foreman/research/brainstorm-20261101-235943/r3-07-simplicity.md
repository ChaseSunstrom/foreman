# Brainstorm — lens: simplicity

- **Collapse the 58 cells into one predictor-family table** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the pack's open question says many cells are one capability counted under several stages; the "no templated cells" steer penalises 58 near-identical sentences. Assumption: roughly 6–8 families (next-ask, correction shape, problem flag, machine breakage, drop prediction, user-model input hygiene) cover them.
  Done when: coverage.md has one row per family, and each former empty cell resolves to a family id plus a surface-by-stage tag. `fm genesis check` reports zero empty cells and zero templated cells.

- **Show the forecast as a ranked row in `fm next`, add no new verb** — FEATURE — value 5 — effort S — risk low — category: reach
  Why: the standing reach rule says every capability must be called by a real session path. The pack's earlier ideas keep adding pages and verbs. Assumption: `fm next` already renders ranked rows that can carry one more source.
  Done when: with a seeded history, `fm next` prints one "likely next" line with a one-line "because". `fm genesis check` reach names no Anticipation verb that lacks a session path.

- **Strip test and debug captures from the user model's input** — FIX — value 5 — effort S — risk low — category: hygiene
  Why: the dropped ledger shows "The first brief" and "The second brief" captured by mistake from T-2547's test debugging. The "asked" stream above includes them, so the model of the user learns from Foreman's own fixtures.
  Done when: a red-first test feeds `fm intake` a sample line under a test marker and an `asked` row for it never reaches fmforesight's input. Previously-dropped-by-mistake rows are excluded.

- **Predict by grep alone: nearest past ask through `fm recall`, no learning** — FEATURE — value 4 — effort S — risk low — category: baseline
  Why: T-2546's word-overlap matcher met no bar, and `fmrecall.covered` already exists. Doing less sets the baseline every cleverer predictor must beat. Assumption: nearest-neighbour over the asked stream is cheap to compute.
  Done when: a walk-forward backtest on the real asked stream prints the grep baseline's hit@3. Any later predictor is refused unless it beats that number.

- **Gate every predictor on a walk-forward backtest before it may draft** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the Missions 3–5 lesson says "name the backtest that decides whether it ships". The only evidence of a matcher failing is T-2546.
  Done when: `fm foresight backtest` replays the asked stream in order and reports hit@3 and abstain rate. A predictor below the grep baseline cannot create a lane, shown by a failing test.

- **Resolve every prediction to hit, miss, abstained or expired** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the earlier question "which outputs does no session path read" implies silent dead outputs. An unresolved forecast can neither be scored nor deleted.
  Done when: each forecast row has a terminal state within 14 days, and `fm doctor` shows counts per state. A forecaster that returns nothing prints "abstained", never an empty list.

- **Cap foresight at one line and mute a signature after two dismissals** — FEATURE — value 4 — effort S — risk low — category: restraint
  Why: this is the simplest defence against nagging, and the steers already stress attention cost. Assumption: dismissals are recorded somewhere readable (the dropped ledger is the model).
  Done when: a test dismisses the same signature twice and sees it vanish from `fm next` and the SessionStart note. A third distinct flag in one session is not printed.

- **Delete forecasts nobody read** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the open question "which deliberation outputs does no session path read" applies to fmforesight too. The lean steer requires each addition to be measured or wait.
  Done when: the sweep lists every fmforesight output with a reader path, and an output with none for 30 days turns up as a deletion candidate task.

- **Re-run each cell's cited behaviour, not just its file** — SECURITY — value 4 — effort M — risk med — category: coverage rot
  Why: the open question asks whether the sweep verifies that a cited file still behaves as claimed. Today it only checks that the file exists. Assumption: each family can name one command with an exit code.
  Done when: the sweep runs one probe command per family. Reverting the cited function in a scratch copy turns that family red.

- **Park a predicted ask as a title-only deferred task, spend tokens only on a yes** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: draft-in-a-lane spends tokens on guesses. A title costs nothing and supports "again" or "yes" later. Assumption: the deferred state already hides tasks from the drive.
  Done when: a prediction creates a deferred task tagged `predicted` that `fm drive` never starts. Accepting it triggers the first lane spawn, and lapsing it deletes the task.

- **Wild: add a shuffled-history control arm to every predictor** — FEATURE — value 4 — effort M — risk low — category: honesty (wild)
  Why: the standing rule demands signals Foreman didn't author, and a predictor that beats a shuffled history only by chance is theatre.
  Done when: the backtest prints real hit@3 beside shuffled hit@3, and a predictor within noise of the shuffle is marked "no signal".

- **Wild: delete `fmforesight` in a scratch copy and diff the exam** — CLEAN — value 4 — effort M — risk low — category: subtraction (wild)
  Why: the lean steers say growth needs a measurement. Removing the module is the cleanest test of what it earns.
  Done when: a recorded run compares exam and outcome numbers with and without it. If there is no difference, a subtraction task is filed with the numbers.

- **Wild: let a stub-user twin, written only from steers, complain about each cell** — FEATURE — value 3 — effort M — risk med — category: blind check (wild)
  Why: it uses an input Foreman did not author. A tool-less child that reads the steers can say which cells nobody would miss.
  Done when: the child's complaint per cell is stored, and cells it calls pointless are flagged for n/a with a counterexample search.

- **Run the sweep's n/a counterexample search before accepting any n/a** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: the earlier question asks which cells would stay empty under the standing rule; simplifying the grid shouldn't smuggle in n/a as a shortcut.
  Done when: each n/a cell cites a grep or run that found no counterexample, and a planted counterexample flips the cell to red.

Next question: Which of the six predictor families has a real, non-Foreman-authored history long enough to backtest, and which should be dropped for lack of data?
Next question: If `fm next` is the only reach path, what does a user who never runs it get from Anticipation?
