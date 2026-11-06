# Brainstorm — lens: deepen: briefs

- **Brief Exam Card (outcome + live-state + blind author + parent-differs, one object)** — FEATURE — value 5 — effort M — risk med — category: briefs
  Why: the carried gaps name outcome measure and live-state reading in every Exam; the listed ideas (blind authoring, today's-value, parent-commit difference, stamping) are each one field of the same record. Assumption: briefs currently hold the Exam as free text.
  Done when: `fm brief check` rejects a brief whose Exam lacks any of the five fields (measure, today's value, parent-commit value, live reading with stamp, author) and accepts a complete one.

- **Run the Exam on the parent commit at filing time** — FEATURE — value 5 — effort M — risk med — category: briefs
  Why: a measure that reads the same before and after the change can't show the change worked; the "reads differently on the parent" idea becomes a mechanical check, not a promise. Assumption: a throwaway worktree of HEAD is cheap to make.
  Done when: filing a brief whose measure returns the same value on the parent and on a planted-fix branch is refused with both values shown.

- **Mutate the fix to prove the measure notices** — FEATURE — value 4 — effort M — risk med — category: briefs
  Why: "reads differently on the parent" proves sensitivity to the change; a mutation (revert one hunk) proves it for the real fix, closing the gap that the user must otherwise trust the measure. Assumption: reverting hunks is automatable for small diffs.
  Done when: for a closed task, reverting its diff makes its recorded outcome measure flip back, and the receipt says so.

- **Stamp live-state readings with a replayable provenance block** — SECURITY — value 4 — effort S — risk low — category: briefs
  Why: the stamp idea (state dir, uid, home, host, checkout HEAD, time) combined with the open question about recovery paths tested only by their writer. Assumption: readings are currently unlabeled output.
  Done when: a reading pasted into a receipt shows all six stamp fields, and `fm doctor` flags a reading whose stamp differs from the current environment as "stale or foreign".

- **Score blind-authored measures against the brief writer's own** — FEATURE — value 4 — effort M — risk low — category: briefs
  Why: blind authoring only matters if it differs; run both measures on parent and fix and record which separated them. Fits the standing rule on signals Foreman didn't author. Assumption: a tool-less child can write a measure from the brief's goal alone.
  Done when: `fm outcomes` prints, per brief, whether the blind and the writer's measure each separated parent from fix, with counts over all briefs.

- **File unmeasurable outcomes as dated bets with a revisit** — FEATURE — value 4 — effort S — risk low — category: briefs
  Why: when no measure exists the brief currently either fakes one or stalls; a bet carries a date, a proxy and a named future reading, and `fm next` surfaces it when due. Assumption: such briefs exist today.
  Done when: a brief marked `bet` with date D appears in `fm next` on D with its proxy reading, and an overdue one turns up in the sweep.

- **Show the left-out list on every brief** — FEATURE — value 4 — effort S — risk low — category: briefs
  Why: the Mission is "says what it left out"; a brief needs a "Not covered" line (neighbours, surfaces, stages) checked against coverage.md cells. Assumption: the left-out scan already exists for maps (the "N left out" in the map).
  Done when: a brief without a Not-covered line, or whose line names no coverage.md cell, fails `fm brief check`.

- **Auto-demote briefs whose today's value already meets the target** — CLEAN — value 3 — effort S — risk low — category: briefs
  Why: a required today's-value exposes briefs whose premise is already met (the dropped T-… "premise already met" case in the user's words). Assumption: the target is numeric.
  Done when: a brief whose today's value satisfies its goal is filed as dropped with the reading quoted, not queued.

- **Brief lineage: link each brief to the prior briefs it superseded or repeated** — FEATURE — value 3 — effort M — risk low — category: briefs
  Why: gen-3 repeats (kill-script sample lines, ship asks, lineage lines) show the same class of gap refiled; a similarity check against closed briefs says "this was T-2724's class". Assumption: briefs are text searchable.
  Done when: filing a brief whose class matches a closed one prints that task id and asks for the difference.

- **Wild: Send a pre-mortem postcard dated 30 days out** — FEATURE — value 3 — effort S — risk low — category: briefs (wild)
  Why: each brief gets a short note from its imagined failure ("it passed but nobody called it"), written at filing, then re-read at day 30 next to the live reading. Assumption: dated entries can be surfaced by `fm next`.
  Done when: day 30 shows the postcard beside the current outcome measure reading, and the user's mark (right/wrong/not yet) is stored.

- **Wild: Brief adversary — a cold child tries to satisfy the Exam without doing the work** — SECURITY — value 4 — effort M — risk med — category: briefs (wild)
  Why: metric-gaming is a standing concern; a tool-less child proposes the cheapest hack that turns the measure green, and a hit refuses the brief. Assumption: such a child can be run cheaply on Haiku.
  Done when: a seeded brief with a gameable measure (e.g. counts lines) is refused with the hack named, and an ungameable one passes.

- **Wild: Brief half-life — an Exam's live reading re-runs monthly and grades the brief retroactively** — FEATURE — value 4 — effort M — risk low — category: briefs (wild)
  Why: closes the loop from "closed" to "still true"; ties to outcome survival as a signal Foreman didn't author. Assumption: measures are re-runnable commands.
  Done when: a closed task's measure re-runs at 30 days, and `fm outcomes` shows survived/regressed with the reading.

Next question: Which briefs' Exam measures are re-runnable by a cold process today, and which depend on session state that won't exist then?
Next question: When a measure is gameable, does the cold reader or the builder find out first, and what does each cost?
