# Brainstorm — lens: bold bets

- **Pair every Exam with a good world and a bad world** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the carried gap is "every brief's Exam names an outcome measure and a live-state reading". The list has parent-differs, positive controls and hermetic cold shells, but they are separate ideas. Folding them into one pair of miniature ledger fixtures means the reading runs on a world where the outcome holds and one where it doesn't. The Exam is accepted only if the two readings differ.
  Done when: a brief whose reading is identical on both fixtures is refused at filing, with a test using a planted constant-output reading.

- **Compile the request into a typed IR with lint passes** — FEATURE — value 5 — effort L — risk med — category: thinking
  Why: the clause tracing, grid, canaries and left-out lists are all manual. Instead, parse the request into clauses, nouns, constraints and non-goals once. Every later step becomes a pass over that IR with compiler-style diagnostics: undefined reference (a noun no brief names), unused clause, dead brief, shadowed non-goal. assumption: clause extraction is reliable enough for a tool-less child to produce it and a zero-token checker to validate it.
  Done when: a planted request with one clause that no brief covers makes the lint print `unused clause`, and the clause appears in the left-out slip.

- **Calibrate breadth against realized footprint** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: nothing so far measures exhaustiveness against ground truth that Foreman didn't author. Closed tasks record the files actually touched. Compare each past request's planned grid with the footprint that eventually landed, then show at intake "requests of this shape grew from 4 files to 11". assumption: task→commit→file links are in the ledgers.
  Done when: `fm` prints a historical growth ratio for a new request, and a backtest over the last 30 closed Missions shows the ratio's sign was right more often than a flat guess.

- **Allocate lens budget to grid cells with a bandit** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: the packs are about 3,000 lines of "ideas so far" and every lens re-reads them all. Start with one cheap pass per cell, then spend further lens calls only on cells whose answers vary between runs or whose canary hit-rate is low. The pack stays small and the money goes where the uncertainty is.
  Done when: on a replayed Mission, the new-idea count per dollar is at least equal to the flat fan-out's, with a smaller total spend.

- **Enumerate scenarios from the grid axes, pruned by constraints** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: the list has pairwise covering and decision tables, but no way to rule out impossible combinations. Take the recorded n/a cells as constraints, enumerate surface × actor × failure × state by brute force in the stdlib, drop the infeasible ones, and report concrete combinations that no brief's tags cover.
  Done when: a planted uncovered feasible combination appears in the output, and an n/a-excluded one does not.

- **Have two authors derive each Exam command** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: a lens child writes a shell command that later runs at close, on text derived from the pack, which holds pasted material. A second child sees only the outcome sentence and writes its own reading. The brief files only if the two agree on the files and keys they read. A tampered pack that makes the first child emit an odd command then fails visibly.
  Done when: a planted pack line that tells the child to read `~/.ssh` makes the filing refuse the brief.

- **Break the Mission early when grounding yield collapses** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: gen-3 briefs were repeatedly dropped as "premise already met". If the first five canaries show more than half of the claims already built, the rest of the fan-out is probably rediscovery. Stop, print the hit-rate, and offer the narrower question.
  Done when: replaying the T-2702 and fm-next Missions trips the breaker, and the count of dropped briefs falls.

- **Fast-lane a re-ask that cites its left-out slip** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user's own words show repeated asks that an earlier Mission left out. When intake sees a request matching a recorded left-out cell, it files the brief with a one-line "left out on <date> for <reason>", jumps it up the queue, and counts a miss against that Mission's exhaustiveness record. assumption: left-out cells carry stable ids, as the earlier idea "Give every cell a permanent id" proposes.
  Done when: filing an ask that matches a recorded cell prints the cell id and date, and a miss is counted.

- **Reconstruct the request from the Exams alone** — FEATURE — value 4 — effort S — risk low — category: validity
  Why: the measures should be checkable against the ask. A tool-less child reads only the Exam lines and writes the request they imply. Compare it to the real one, and a large mismatch means the Exams measure something else. This differs from reverse-intake of whole briefs because it isolates the measure.
  Done when: a Mission with a planted off-topic Exam scores below the threshold, and a good one scores above it.

- **Wild: Let the user run a Mission in "I'll disagree" mode** — FEATURE — value 3 — effort M — risk med — category: dissent
  Why: dissents are scored against outcomes that arrive late. Let the user stake a one-word bet ("cell 4 matters") against the Mission's ranking. The settled dissent is graded the same way as an in-house one, so there is a user-authored signal Foreman didn't write. wild
  Done when: a recorded user bet appears in `fm outcomes` and is settled at +14 days.

- **Wild: Keep a "twenty years later" Mission page** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: it forces a different failure class than the usual grid axes: what breaks only after the repo has 10× the files, the ledger 10× the lines, and the original author is gone. A child writes it as a short retrospective, and each failure it names becomes a candidate cell. assumption: a story prompt reaches cells that a checklist doesn't. wild
  Done when: on one past Mission, the retrospective names at least one cell absent from the grid that a later user ask confirmed.

- **Wild: Hold a monthly "remove a Mission" drill** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: pick a past Mission at random, revert its additions in a scratch copy, and run the Exam readings. If the outcome measures don't move, the Mission added no outcome and its exhaustiveness work was theatre. This puts the question "did exhaustive thinking cause anything" on measured ground. wild
  Done when: the drill reports, for one Mission, the readings with and without it, and flags a no-change one.

- **Mark where the answer came from on every summary** — FIX — value 3 — effort S — risk low — category: honesty
  Why: this is a second-order fix to "report the dimensions each summary collapsed". A Mission's headline numbers (brief count, cells filled) say which source produced each one: the ledger, a cold child, or an estimate.
  Done when: each Mission-page figure carries a source tag, and a test fails on an untagged number.

Next question: How many of the ~3,000 "ideas so far" lines would a mechanical dedupe against the catalogue remove, and does the pack's size now push brainstormers toward rediscovery rather than new ideas?
Next question: Which of the carried gaps (dissent scores, canaries, Exam readings) has a consumer that actually changes a decision, and which only produces a number?
