# Brainstorm — lens: simplicity

- **Generate the rules copies from one source** — CLEAN — value 4 — effort S — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, the 60-line rules file and the eval copies of the rules, so drift is likely.
  Done when: one canonical rules file exists, the eval copies are produced from it, and `fm docs check` fails if a copy differs.

- **Add a guard fallback to the committed copy** — FIX — value 4 — effort S — risk med
  Why: T-0033. A half-applied guard edit made every write fail closed. Fall back to the last committed guard, not fail-open, when the working copy raises, and print a single-line notice.
  Done when: a test with a syntactically broken working guard still blocks a dangerous command and allows a safe one, and the output names the fallback.

- **Collapse audit output saving into one command** — FEATURE — value 4 — effort S — risk low
  Why: reviewer output files are huge and the agent saves the tail by hand. `fm audit save <lens> <file>` would keep only the findings block and the verdict and record them.
  Done when: running it on a 5,000-line reviewer file stores under 100 lines, the done gate reads it, and a file with no findings block is rejected.

- **Replace the guard's text heuristics with parsed-command checks** — FIX — value 4 — effort M — risk med
  Why: the guard blocked the agent's own legitimate edits (quoted paths, "claude plugin" strings). Tokenizing with `shlex` and matching on the command and its arguments, not on raw substrings, removes a class of false positives.
  Done when: a corpus of at least 30 legitimate commands, including quoted paths and heredocs, passes, and every existing block test still passes.

- **Give T-0032 a reason field, not a new status** — FIX — value 2 — effort S — risk low
  Why: a request finished inside another task only has "dropped". Keep the status set unchanged and add `--reason done-elsewhere:T-00NN` to drop.
  Done when: `fm queue drop --reason done-elsewhere:T-0018` records the pointer and `fm status` shows "done in T-0018".

- **Make `fm audit prep --note` repeatable and the only extra input** — FEATURE — value 3 — effort S — risk low
  Why: T-0031. The agent hand-wrote briefs to add threat models. One `--note` flag appended verbatim to every lens brief covers it without a template system.
  Done when: `prep --note "threat: X"` puts that line in all five lens briefs, and the output is unchanged without the flag.

- **Delete dormant code paths** — CLEAN — value 3 — effort S — risk low
  Why: the TaskCompleted gate is dormant on current models, and ~6,700 lines of stdlib code means dead branches add cost. Assumption: coverage shows nothing else depends on it.
  Done when: the TaskCompleted handler and its tests are removed or moved to a documented optional file, all tests pass, and the hook count in `fm doctor` matches the docs.

- **Show umbrella progress as child rounds in the statusline** — FEATURE — value 3 — effort M — risk low
  Why: T-0018 shows "step 3/6" and hides which round is running. Assumption: rounds can be recorded as named steps.
  Done when: the statusline for a task with named steps shows "round 4 of 6: <name>", and tasks without names look the same as now.
