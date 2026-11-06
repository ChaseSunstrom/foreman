# Brainstorm — lens: blind spots

- **Flag every number that is recorded but never decides** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-2651 found that `--bench` recorded medians but never failed. The class is "an instrument whose output no gate, doctor row or reader consumes". The question a brainstorm should have asked was "which measurements does Foreman store that nothing acts on?" Assumption: other such instruments exist.
  Done when: `fm doctor --records` lists every ledger or JSON field written with no reader outside display, and a planted write-only field shows up in that list.

- **Compress "ideas so far" into a clustered digest with saturation counts** — CLEAN — value 4 — effort M — risk low — category: developer experience
  Why: the pack's dedupe list is thousands of near-duplicate lines. Three of four slate items turned out already built (T-2659), so the real defence is a pack that shows saturated areas, not a flat list. Assumption: brainstormers skim the flat list.
  Done when: the pack builder emits at most 60 cluster lines, each with idea count, the built verb if any, and the drop reasons. A test shows a known-duplicate idea maps to its cluster.

- **Require every "already built" drop to cite a command run** — FIX — value 4 — effort S — risk low — category: reliability
  Why: ideas were dropped as "mostly built" on a reading of the code (fm replay, fm usage --prune), and the dropped ledger records no check. If a drop is wrong, the capability is lost silently.
  Done when: `fm drop --reason built` refuses without `--probe CMD`, stores the probe's exit code and first lines, and `fm doctor` flags drops whose probe now fails.

- **Make each drill fault declare which reader should report first** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the dropped note on task_done removal says the hash chain breaks, so `verify-ledger` and `drill --restore` report first, before `outcomes` and `digest`. Nothing asserts that ordering. Assumption: faults get added faster than anyone checks which detector fires.
  Done when: every `fm drill` fault has an `expect_first:` field. The drill fails if a different reader reports first, or if none reports. A fault with a wrong declaration fails a test.

- **Print the end-of-run receipt on every exit path, from one renderer** — FIX — value 3 — effort S — risk low — category: user value
  Why: yield per dollar first existed only at contract end (T-2655), then was added to the drive end. Ctrl-C, a usage-limit wait and a crash are likely other exit paths with no receipt.
  Done when: a test kills a drive by SIGINT and by crash. Both leave a receipt line with spend, tokens and yield, and the file the renderer wrote is named.

- **Scan writers for swallowed errors and list the ledgers each can lose** — SECURITY — value 4 — effort M — risk low — category: reliability
  Why: the drill showed readers print zero when a record class is missing. The write side has the matching blind spot: `except: pass` around an append means the record never exists. Assumption: such sites exist in `plugin/lib`.
  Done when: `fm doctor` lists every swallowed-exception site on a ledger write path, and each is either fixed to log a degraded-write line or marked deliberate with a reason.

- **Check that every printed "Next:" command parses and resolves** — FIX — value 3 — effort S — risk low — category: developer experience
  Why: T-2653 made every nonzero exit print a Next command. Nothing proves that command is real, since a renamed verb would leave stale advice. Assumption: the strings are hand-written.
  Done when: a test runs each Next string through the verb table in dry-run and fails on an unknown verb or flag.

- **Classify each user ask by blind-spot class and chart recurrence** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: the missed asks T-2650 to T-2659 fall into a few classes: record-only, partial input, already built, missing rate, uncovered exit path. If the classes recur, the next brainstorm should be told which ones are not yet exhausted.
  Done when: `fm asks --classes` prints counts per class from the ask ledger, and a new ask is tagged within the same task.

- **Auto-run the re-grounding pass before a slate reaches the user** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: five of the 19 asks (c13, c16, c17, c21, and the task_done one) were dropped after the user re-grounded them against the code. That is user attention spent on duplicates.
  Done when: each slate item carries a "grounding" line with the matched verb, file and test or "none found". A seeded already-built idea is filtered out before the slate is shown.

- **Wild: a tool-less child predicts the user's next ten asks from the README and recent diffs, then is scored** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: assumption: a stranger model with only the public surface approximates what the user will ask next. The hit rate would measure the brainstorm's blind spots without waiting for a miss.
  Done when: after each batch of asks, `fm asks score` prints the predicted-versus-actual match and the missed classes.

- **Wild: a child writes the DONE-WHEN from the title alone, and the diff to the real one measures ambiguity** — FEATURE — value 3 — effort S — risk low — category: developer experience — wild
  Why: T-2583's criterion contradicted its own example, so wording the user thought was clear was not. A blind rewrite exposes the gap at birth. Assumption: cheap enough on Haiku.
  Done when: filing a task prints a similarity score and flags tasks under a threshold, with the divergent clause quoted.

- **Wild: an anti-pack of the last 30 dropped ideas, each with its drop reason, handed to every brainstormer** — CLEAN — value 3 — effort S — risk low — category: simplicity — wild
  Why: the dropped reasons ("second-order", "mostly built", "value 2 after re-grounding") are the cheapest negative signal and appear nowhere in the pack's idea list. Assumption: brainstormers would avoid the same traps.
  Done when: the pack includes a "dropped and why" section, and over a month the share of slate items dropped for "already built" falls.

Next question: Which Foreman outputs do the user's asks never mention because they were never visible — and what would the user do if one went wrong?
Next question: When a brainstorm idea is filed and later dropped, which part of the pipeline could have caught it earlier, and at what cost?
