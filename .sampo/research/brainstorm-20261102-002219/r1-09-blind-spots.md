# Brainstorm — lens: blind spots

**Earlier questions my lens can answer**
- **Harness dependence:** the cells' probes quietly depend on Claude Code wherever they read hook events or session baton files. Assumption: the pack doesn't show non-Claude probes.
- **Too little history to backtest:** Goal-to-finish has few closed goals, so most cells can only be planted and not measured. They should be labelled that way.
- **Unread outputs:** a goal's contents list is read only by `fm next`. A wrong or padded list would go unnoticed.

The missed asks fall into six classes: a gauge omitting a cost (T-2533), a missing control arm (T-2534), a red number that can't name its cause (T-2535), an installed thing nobody watches (T-2542), a model fed its own output (T-2554), and an artifact with no precondition (T-2546/2547). The ideas below ask each question of the Goal capability.

- **Watch the goal baton for liveness** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: T-2542 (timers) went unwatched until it cost a task. Assumption: a goal with no progress event for days is currently silent.
  Done when: a fixture goal with no event for 3 days makes `fm doctor` WARN with its last-progress age.

- **Flag goals that finish by shrinking** — FIX — value 5 — effort M — risk low — category: done-detection
  Why: the capability promises it "knows when it's actually done rather than merely stopped". A gauge that counts rows left undercounts if rows were deleted or reworded. Assumption: no check compares against the original contents.
  Done when: a goal whose contents lost 30% of its rows since creation can't report finished without a recorded reason per removed row.

- **Tag every contents row by origin** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: T-2554 showed self-authored inputs polluting a model. Foreman-filed rows can pad a "finished" count in the same way.
  Done when: `fm goal` shows user-asked and Foreman-added rows separately, and the done percentage is computed from both counts.

- **Add a free-arm control for plan completeness** — FEATURE — value 5 — effort M — risk med — category: measurement
  Why: T-2534 added a guard-only arm because no control existed. Goal has no equivalent. A tool-less child writing a best-in-class checklist from the vague goal gives a baseline recall for the session's plan.
  Done when: `fm exam` prints plan recall for the foreman, free and plain arms on 3 vague-goal scenarios.

- **Refuse contents rows with no grounding line** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: T-2547 did this for Missions and the cells are the same class. Assumption: goal contents rows are accepted without grounding today.
  Done when: `fm goal add` without a code reference or a recorded "gap" reason exits non-zero, and a test covers it.

- **Match each row to MASTER.md before filing it** — FEATURE — value 4 — effort S — risk low — category: duplicates
  Why: T-2546 exists because asks restated built features. A decomposed goal restates them in bulk, and the lessons say most of #2, #3, #11 and #12 was already built.
  Done when: a goal row restating a MASTER clause is stored as "existing" with the task id, and not as a new task.

- **Name the stage behind a stalled goal** — FEATURE — value 3 — effort M — risk low — category: attribution
  Why: T-2535 made a red ratchet name its commit. A stalled goal shows only "no progress".
  Done when: `fm goal why` names the last advancing event and the first blocked row, with the blocker's kind.

- **Mark each cell with its backtest class** — CLEAN — value 3 — effort S — risk low — category: coverage honesty
  Why: the pack's open question on how many cells have too few events. A cell that can only be planted shouldn't read as a measured one.
  Done when: each of the 58 cells carries `measured`, `planted` or `unreached`, and the sweep counts the three separately.

- **Test goal resume at every kill point** — PERFORMANCE — value 4 — effort M — risk med — category: crash safety
  Why: the capability claims it survives crashes and compactions, and the pack shows state, baton and repo disagreeing after a kill. Assumption: kills are tested at few boundaries.
  Done when: a test kills the session at each write boundary of a goal update and resume restores the same contents hash.

- **Wild: dead-goal séance** — FEATURE — value 3 — effort M — risk low — category: delight
  Why (wild): goals untouched for 14 days get one card, "still wanted?". It lists what changed in the repo since and offers keep, shrink or drop. The standing rule against killing ideas means a drop needs its reason recorded.
  Done when: a fixture 14-day-idle goal produces a card, and each answer updates the goal with a reason.

- **Wild: vague-goal fuzzer in the night tick** — FEATURE — value 4 — effort L — risk med — category: exam
  Why (wild): a tool-less child invents vague goals nightly. Foreman decomposes each one, and the result is scored against a separate child's held-out best-in-class list.
  Done when: the nightly digest names one goal class (for example "infra" or "docs") where plan recall trails the free arm.

- **Wild: goal autopsy letter** — FEATURE — value 3 — effort M — risk low — category: done-detection
  Why (wild): when a goal closes, a cold child reads only the user's original words and the final repo state. It writes what a stranger would say is still missing, which tests "knows when it's done" from outside.
  Done when: closing a goal stores an autopsy file, and the finish receipt shows its count of missing items.

**Next question:** Which numbers Foreman shows about a goal (percent done, rows left, days remaining) have no producing command a stranger could re-run?
**Next question:** Which of the 58 cells would nobody notice if its cited path stopped firing, because no session reads its output?
