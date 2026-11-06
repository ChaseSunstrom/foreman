# Brainstorm — lens: simplicity

- **Make a goal a tag on tasks, not a second structure** — CLEAN — value 4 — effort M — risk med — category: goal model
  Why: assumption: goal contents, the task queue and the baton each hold plan state, and the pack shows reconcile and drift ideas piling up around that overlap. Fewer stores means fewer cells that need a probe.
  Done when: `fm goal` status is computed from tasks carrying the goal tag, and a kill-and-resume test passes with the separate contents file deleted.

- **Define "done" as one exit code** — FEATURE — value 5 — effort M — risk low — category: done detection
  Why: assumption: "knows when it's actually done rather than merely stopped" is the core of #4. A single `done-check` command that exits 0 is the smallest honest oracle.
  Done when: closing a goal runs the command, and a goal whose command exits non-zero refuses to close.

- **Give every stop one reason from a five-value list** — FEATURE — value 4 — effort S — risk low — category: done detection
  Why: assumption: "done" versus "merely stopped" is untested without a typed reason. The values are done, usage-limit, crash, blocked-on-user and abandoned.
  Done when: each goal exit writes one value, and `fm status` prints it. A test feeds each of the five paths and checks the value.

- **Fill the 58 cells with one default per column plus a short exceptions list** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the grid is surfaces by stages, and the web UI column is the only surface the pack names. Most cells in a column share one behaviour, so writing the default once and the deviations as rows avoids templated cells.
  Done when: the sweep reports zero empty cells for #4 and its templating linter passes. Every exception row cites a file.

- **Mark a cell n/a only with the sentence "the user never meets this here"** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: assumption: surfaces such as notifications or the car likely don't touch goal planning. A fixed reason shape keeps n/a cheap and lets the counterexample search match one pattern.
  Done when: every n/a cell for #4 has that shape and a recorded counterexample search. The linter rejects any other wording.

- **Show progress as "n of m rows with evidence", with no percent** — CLEAN — value 3 — effort S — risk low — category: progress display
  Why: assumption: a stored percent drifts when rows are added, and the pack lists scope-growth and backward-bar ideas that all try to patch that drift. Dropping the percent removes the problem.
  Done when: no percent field exists in goal state, and the count changes correctly after a row is added.

- **Plan only the next wave in detail** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: assumption: decomposing the whole finished version up front creates 50-plus rows that go stale across days and compactions. The later parts stay as one-line titles.
  Done when: a goal's contents show at most 12 rows with detail, and the next wave expands from the repo on resume.

- **Resume prints a fixed ten lines read from files only** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: crashes and compactions are named in the capability text, and a bounded resume works for every harness because it needs no hooks.
  Done when: after a kill, resume output is at most 10 lines and identical when run twice. A test covers a torn journal record.

- **Pay for each new goal verb with a removal** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: the lean steers (T-2503) require growth to be justified, and goal work is the likeliest place for verb sprawl. This is the cheapest enforcement.
  Done when: `fm task finish` on a task adding a goal verb fails unless a removal or a merge into an existing verb is named.

- **Wild: Make the goal one sentence plus a falsifier** — FEATURE — value 3 — effort M — risk med — category: goal model
  Why: wild. Everything else is derived from "finished when X holds", and a sentence the user can edit is simpler than any contents table.
  Done when: a goal created from one sentence yields a runnable falsifier command, and rows appear only after the first wave starts.

- **Wild: Delete the goal file and rebuild it from git, tasks and the ledger** — FEATURE — value 3 — effort L — risk med — category: crash safety
  Why: wild. If state can always be rebuilt, there is nothing to corrupt, and the recovery drill becomes the probe for every resume cell.
  Done when: removing the goal file and running `fm goal rebuild` gives a status identical to before, in a test.

- **Wild: Let the sweep fail any cell longer than one line** — CLEAN — value 2 — effort S — risk low — category: coverage
  Why: wild. A hard length cap makes padding visible, and the pack's templating concern is mostly long near-duplicate prose.
  Done when: the linter rejects a cell above 140 characters or without one resolvable file reference.

- **Close a goal with a three-line receipt** — FEATURE — value 3 — effort S — risk low — category: finish
  Why: assumption: the user wants proof it's finished, not a report. The receipt gives what changed, the done-check output and the user-only items.
  Done when: the closing output has exactly those three parts. User-only items stay empty when there are none.

Next question: Which of the 58 cells would still be needed if the goal were just a tag on tasks plus one done-check?
Next question: What is the smallest set of goal verbs and files that survives a kill at any point, and which current ones fall outside it?
