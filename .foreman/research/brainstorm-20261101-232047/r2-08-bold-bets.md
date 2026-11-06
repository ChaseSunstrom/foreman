# Brainstorm — lens: bold bets

- **Compile the 58 cells from a deliberation trace corpus** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: the grid rule demands each cell name a concrete grounded capability, and earlier ideas fill by prose or probe. Bold version: replay the last N closed tasks through the plan gate, record which readings, options, races and stops each one actually used, and emit coverage.md cells from those traces. Cells with no trace stay empty and become the task list. Assumption: closed tasks carry enough plan text to extract this.
  Done when: `fm genesis coverage` regenerates the Exhaustive-thinking row from traces only, and every filled cell cites a task id and a file path.

- **Run a blind rival planner and show only the disagreement** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: Foreman's plan gate counts text shape, but one model still writes both options and judge. A different-family child reads only the request and repo, and the plan shows the diff of readings and approaches. Disagreement becomes the ambiguity signal for stopping. Assumption: a second planner is affordable for M and L tasks only.
  Done when: `fm plan --rival` on a fixture request with two valid readings prints both and the first plan cannot be accepted until the user or a rule picks one.

- **Gate irreversible steps on a door ledger the model can't write** — SECURITY — value 5 — effort M — risk med — category: safety
  Why: a standing steer says to ask only for irreversible-and-ambiguous steps, and the guard already knows destructive verbs. Derive door class from effect, require a named undo line or "no undo", and write every auto-decision receipt to a file outside the model's write path, with `fm undo N`.
  Done when: a planted two-way fork proceeds with a receipt, a planted one-way ambiguous fork stops with one question, and `fm undo 1` restores the pre-state.

- **Pre-register every confidence and score it at close** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: existing ship bets and plan percentages are scored separately. Unify into one write-once table keyed by evidence class, show a reliability table in `fm doctor`, and cap stated confidence by the strongest evidence present. Assumption: enough bets exist by now to fill buckets.
  Done when: `fm doctor` prints per-evidence-class reliability and a plan claiming 90% on prose-only evidence is capped with a named reason.

- **Judge races by minimax regret across readings** — FEATURE — value 4 — effort L — risk med — category: decision
  Why: races pick by first pass, but readings of the request may disagree. Run each finalist against tests derived from every live reading, pick the one with the least worst-case regret, and report how fragile the pick is.
  Done when: on a two-reading fixture, the picker chooses the candidate passing both readings' checks over one that only wins one, and prints a fragility score.

- **Backtest every gate threshold on closed tasks before enforcing it** — PERFORMANCE — value 4 — effort M — risk low — category: gates
  Why: gates are tuned by feel. Make each a named knob with a shadow mode, replay finished tasks, and refuse to enforce a knob whose counter-metric (refusal rate, reopen rate) worsens.
  Done when: a candidate threshold runs in shadow on 30 closed tasks and `fm doctor` shows would-have-refused count beside reopen outcomes.

- **Add a trap exam kind where the obvious fix is wrong** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: exhaustive thinking only earns its cost when first instinct loses. A tool-less child authors repos whose natural fix breaks a hidden sibling; score foreman vs plain on them.
  Done when: `fm exam run --kind trap` reports foreman and plain pass rates on at least 6 child-authored scenarios.

- **Ground every idea against built features before it is shown** — CLEAN — value 4 — effort S — risk low — category: brainstorm
  Why: the Lesson from Missions 3 and 4 says most ideas were already built, and this pack's idea list is hundreds of near-duplicates. Check each idea against MASTER.md and the verb index first.
  Done when: a brainstorm run drops ideas whose title matches an existing verb and prints the dropped count with the matching verb.

- **Require a falsifier beside every low-confidence assumption** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: assumptions are listed but untested. The gate refuses a plan whose sub-70% assumption has no command that would show it false.
  Done when: a plan with an unfalsified low-confidence assumption is refused, naming the line, and passes once a command is added.

- **Model-check the task state machine by bounded exhaustive search** — FIX — value 4 — effort M — risk low — category: reliability
  Why: recent commits (T-2540, T-2526, T-2525) show repeated premise bugs in task-state edge cases. Enumerate states times verbs and assert no illegal transition or silent no-op.
  Done when: a test enumerates every (state, verb) pair and fails on a planted illegal transition.

- **Wild: Hold a nightly dojo that re-derives old fixes from scratch** — FEATURE — value 3 — effort L — risk med — category: learning
  Why: wild. A lane re-solves closed FIX tasks blind from the original ask; where its fix differs and survives the same tests, the difference is filed as a candidate lesson.
  Done when: a nightly tick produces a digest line with N re-derived, M differed, and one lesson draft.

- **Wild: Let a stubborn-reader child argue each coverage cell false** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: wild. A blind child tries to show the cited file doesn't do what the cell claims; cells it breaks go back to empty.
  Done when: a cell citing a deleted function is flipped to empty by the child in a fixture run.

- **Wild: Pre-mortem the plan with a child told it already failed** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild. Cheap Haiku call writes the most likely cause of failure; the plan must answer it with a step or a falsifier.
  Done when: `fm plan` on an L fixture includes a pre-mortem line and refuses acceptance when it is unanswered.

- **Wild: Draw the deliberation as a funnel in the web UI** — FEATURE — value 3 — effort M — risk low — category: UI
  Why: wild. Readings narrow to options, options to a race, race to a pick, with the runner-up and flip condition visible; no ceremony shown for S tasks.
  Done when: the web UI task page renders the funnel for a task with a race and an empty-state line for an S task.

Next question: Which Exhaustive-thinking cells does a real session path (the plan gate, fm next, the drive) already exercise, so the 58 empties split into "existing path" versus true gaps?
Next question: Does the plan-time deliberation ever change the outcome on tasks the user later reopens, and where is that recorded?
