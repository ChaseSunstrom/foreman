# Brainstorm — lens: blind spots

Answers to earlier questions, from this lens:
- **Outputs the user would only miss after it cost a task:** anything that fails silently and is read by no session path. That means timers, prefetch drafts, sealed predictions and cell probes.
- **Cells that depend on one harness:** any cell citing a hook note or the SessionStart injection. Hookless harnesses never run those paths.

Each missed ask (T-2533 to T-2554) maps to a question nobody asked. I put each question to the whole project below.

- **Add a gauge-omission line to every number** — FEATURE — value 5 — effort M — risk low — category: gauges
  Why: T-2533 (hook notes missing from the lean ratchet) asked "what does this gauge leave out?". Asked of the whole project, it also covers the doctor gauges, the lean ratchet and the exam denominators. Assumption: the gauges are defined in several places.
  Done when: `fm doctor --json` gives every numeric gauge an `omits` list. A test deletes one and fails.

- **Require a control arm for each measured capability** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: T-2534 (guard-only arm) and the steer on free arms both show that a capability measured without a stripped-down comparison lets the weight pass as value. The question is "what is the do-nothing arm for this?".
  Done when: `fm exam scorecard` marks any capability with no control arm as "uncontrolled" and does not rank it.

- **Name the cause when any ratchet or gate trips** — FEATURE — value 4 — effort M — risk low — category: diagnosis
  Why: T-2535 asked for a commit name on the lean ratchet. The same question applies to the sweep, the proof gates and the hook-latency check: a trip that says only "red" is the same gap.
  Done when: every trip message in a fixture run names a commit, file or input. A lint fails any trip that lacks one.

- **Add a liveness row for every unattended path** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: T-2542 (timers known alive) came after silence went unnoticed. The class also includes the night tick, ci-watch, the genesis live publish, prefetch and the hook fallback. Assumption: these are not all in one inventory today.
  Done when: `fm doctor` prints last-proof-of-life for each unattended path. A killed fixture path turns WARN within three intervals.

- **Run an "is this already built?" check at every filing point** — FEATURE — value 4 — effort S — risk low — category: duplicates
  Why: T-2546 covered capture and task new. Self-filed sweep fixes, discovered items, genesis briefs and brainstorm output also file without it, and the dropped ledger shows many false alarms.
  Done when: all five filers print covered-by clauses. A test files a known-built item through each and sees the match.

- **Tag each learner's inputs with their origin and add a taint test** — SECURITY — value 5 — effort M — risk med — category: contamination
  Why: T-2554 found test-fed captures inside the user model. The question is "which inputs to each learner did Foreman or a test author?". That covers bets, outcomes, lessons, the friction ledger and recall.
  Done when: a fixture seeded with Foreman-authored rows in every learner's source leaves every learner's output unchanged.

- **Make test runs unable to write the real state dir** — FIX — value 4 — effort S — risk low — category: test isolation
  Why: the dropped "captured by mistake" briefs came from tests feeding fm intake. Assumption: tests can reach the real state dir through an env default.
  Done when: a suite run with the state dir read-only passes, and a write attempt aborts the suite.

- **Probe every cell's path for gaps like a missing refusal** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: T-2547 shows the missing piece was a refusal at the writer. Ask of the 58 cells: "what does the writer allow that the reader needs to reject?". The probe feeds each cell's writer an empty, templated, ungrounded or truncated input.
  Done when: each cell's writer rejects its bad fixture. The sweep lists the writers that don't.

- **Produce a ranked list of what the user types to verify Foreman** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user's asks are mostly checks ("does it show X?"). Each repeated check is a missing output. Assumption: shell and session history record these.
  Done when: `fm friction` lists the top five verification commands. The ones that repeat get a doctor row.

- **Check that cell citations are reachable** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: cell citations name files, but earlier questions ask whether a path is ever called. Reachability from an entry point is the real check.
  Done when: the sweep follows a cited symbol back to a hook, verb or skill. It marks the unreachable ones "orphan", and a planted orphan fails the sweep.

- **Wild: plant known blind spots in a fixture project and score the brainstorm** — FEATURE — value 4 — effort L — risk med — category: meta
  Why: wild. Today a blind spot is found only when the user asks for it. Seed ten known gaps into a fixture project, run the brainstorm, and score recall.
  Done when: `fm ideas --selftest` reports recall of planted gaps, and a drop of more than 20% fails.

- **Wild: have a child predict the next verification ask from the closing diff** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild. A tool-less child that sees only the diff writes the follow-up the user will make, then checks it against the real next ask. Misses become probes.
  Done when: each closed task stores a predicted follow-up. A scored hit rate appears in `fm outcomes`.

- **Wild: switch one quiet output off per day and see whether anyone notices** — FEATURE — value 3 — effort M — risk med — category: unread outputs
  Why: wild. It answers whether the user would only miss an output after it cost a task. Unnoticed ones become deletion candidates and noticed ones get a liveness row.
  Done when: a rotation log records the output, the day and whether any session or user reaction followed.

- **Publish a producer/consumer pair check for generated artifacts** — CLEAN — value 3 — effort S — risk low — category: consistency
  Why: lists such as KIND_WORDS and BEYOND have a hidden reader. One pair mismatch (the test_exam and fmgenesis case) cost a brief.
  Done when: a lint compares each generated list with its readers. A planted count mismatch fails it.

Next question: which of Foreman's own learners has never been tested with a deliberately poisoned input?
Next question: which gauge does the user trust enough to act on, and has it ever been checked against ground truth?
