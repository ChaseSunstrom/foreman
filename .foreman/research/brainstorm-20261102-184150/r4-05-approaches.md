# Brainstorm — lens: approaches

- **Settle each dissent by whether the next Seed re-raises it** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: the carried gap is "dissents scored against outcomes". Scoring needs no model if the next generation's Seed or pack is the judge: a dissent that comes back has survived, and one that never does has not. Assumption: re-raise is a text or cell-id match that a zero-token check can do.
  Done when: a test feeds a planted dissent and a Seed that quotes its cell id, and the scorer marks it "re-raised" in one case and "unseen" in the other.

- **File each dissent as a sleeping task with a wake predicate** — FEATURE — value 3 — effort M — risk low — category: dissent
  Why: assumption: the existing deferred-task machinery already wakes tasks on evidence (T-0217 and the "wake deferred tasks" ideas). A dissent stored as a task gets an owner, an age and a closing event for free. The cost is more queue clutter, so a cap is needed.
  Done when: `fm task new` on a dissent produces a deferred task carrying a `wake:` line, and a fixture event flips it to open.

- **Rank dissents by correlation, not by hit or miss** — FEATURE — value 2 — effort S — risk med — category: dissent
  Why: assumption: a Mission files 5–15 briefs, so a binary dissent score is almost always noise. Comparing a dissenting lens's ordering of briefs with the order they survived (Kendall tau) uses the same data and says which lens predicts survival.
  Done when: a fixture with 6 briefs and known survival returns the expected tau for two lenses, and "n too small" below 5 briefs.

- **Put the Exam in a trailer on the closing commit** — FEATURE — value 4 — effort S — risk low — category: exam
  Why: the earlier question "which Exam measures are re-runnable by a cold process" is answered if the outcome and live reading live in git, not in session state. `git log --format=%(trailers)` then reads them in any clone.
  Done when: `fm task finish` writes `Exam-outcome:` and `Exam-live:` trailers, and a script in a fresh clone parses them and runs the live command.

- **Draft the Exam at pickup and file only the claim** — CLEAN — value 3 — effort S — risk med — category: exam
  Why: doing less. A reading written at filing describes a world that is days old by the time the brief is built. Filing the claim and a "needs Exam" flag, with the Exam written at pickup against current state, removes the stale-reading class.
  Done when: a brief filed without an Exam is accepted. `fm task start` on it refuses until `outcome:` and `live:` lines exist.

- **Give each Exam a before/after pair of golden `--json` outputs** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: for "what is a live-state reading" this is the unconventional answer. Store a real pair of outputs from a comparable past close, and have the Exam say "same keys move the same way". It is easy to author and easy to check, but only suits capabilities that already have `--json`.
  Done when: one gen-3 brief's Exam is rewritten as a fixture pair, and the checker fails when the key does not move.

- **Borrow the reading from the nearest closed brief and change only the threshold** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: assumption: closed briefs in the same coverage.md row already carry working readings. Copying one costs less than authoring one and has already been shown to run.
  Done when: filing a brief in a row with a prior Exam pre-fills `live:` from it, and the filer edits only the number.

- **Build the grid's rows from the call graph the request touches** — FEATURE — value 3 — effort M — risk med — category: grid
  Why: now the grid comes from the lens children's judgement. Importing from the request's nouns and listing the verbs, hooks and skills reachable from there gives a zero-token floor of rows. Any row with no cell and no n/a is "left out" by construction.
  Done when: the Mission page lists a row for each reachable module, and a test with a planted unreferenced module shows it as an empty row.

- **Print a readings-taken ratio as the last line of a Mission** — FEATURE — value 3 — effort S — risk low — category: left-out
  Why: doing less than a full left-out receipt. "Exams with a reading taken: 7 of 9; 2 could not run (reason)" costs one computed line and tells the user how far to trust the rest, without a new store.
  Done when: closing a Mission with one unreadable Exam prints "8 of 9" and names the one that failed.

- **Hand a hindsight child the ledger from 14 days later** (wild) — FEATURE — value 4 — effort M — risk med — category: dissent
  Why: wild. A tool-less child reads only the Mission page and the 14-days-later ledger slice, and writes what the Mission missed. Its list is an outcome-based left-out receipt, written by something that never saw the plan.
  Done when: the child's list for one gen-3 Mission is produced and diffed against that Mission's own left-out list, with the overlap reported.

- **Keep left-out cells as files the user can delete or promote** (wild) — FEATURE — value 3 — effort S — risk low — category: left-out
  Why: wild. One file per left-out cell in `left-out/`. Deleting one means "don't care" and is recorded as an explicit drop. Moving one into `queue/` files the task. The user already edits files to reply, so this needs no new UI.
  Done when: `rm left-out/c07.md` writes a drop record with a reason of "user deleted", and `mv` into `queue/` files a task.

- **Show a one-glyph Exam forecast in the status line** (wild) — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A sun, cloud or fog glyph shows the share of open briefs whose reading is fresh, stale or unreadable. It makes the "stale" and "can't read" states visible without opening a page.
  Done when: the status line shows the fog glyph when a reading is unreadable, and the glyph is covered by a test.

- **Check each "not built" claim against the host CLI's own help and tool list** — FEATURE — value 2 — effort S — risk low — category: canary
  Why: the canary gap is "near the idea". The parser's did-you-mean already probes verbs, but the host's tool and flag surface is another place where the thing may already exist. Assumption: that surface can be listed cheaply and offline.
  Done when: a brief claiming "not built" for a capability the host already offers shows that host entry as a canary hit.

Next question: which gen-3 briefs would pass their own Exam on the parent commit, and does that count change which approach above is cheapest?
Next question: of dissent signals available without a model (re-raise, survival, wake events), which has enough volume in one generation to score anything?
