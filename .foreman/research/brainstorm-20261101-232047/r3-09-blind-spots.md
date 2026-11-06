# Brainstorm — lens: blind spots

Seven of the eight misses ask Foreman to observe itself, not to do more. T-2532 (fallback runs silently), T-2533 and T-2535 (cost and cause of the ratchet), T-2534 and T-2536 (control arms and ablation) and T-2542 (liveness) all fit this. T-2525 is a state the premise test never tried. T-2505 is the meta-ask. So the question a brainstorm should have asked is: for each subsystem, how would you know it is alive, what it costs, why it changed, and whether it earns its place? Applied to deliberation's 58 cells, that gives the ideas below.

**Answers to earlier questions my lens can reach**
- Silent unattended failures (OS kill, logged-out session, expired auth) leave no trace by definition. The next morning the user sees only an old "last ran" time, so absence has to be recorded elsewhere (idea 2).
- Steers that assume an interactive session are the ones using `fm ask`. With nobody present they need a safe default (the ask-class idea, already listed). Idea 1 would show where this is still untested.

**Ideas**

- **Fill a self-observability matrix** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: T-2532/2533/2534/2535/2536/2542 are all one class: subsystem × {alive, cost, cause, control arm}. No grid row asks it.
  Done when: `coverage.md` has a row per deliberation subsystem (plan gate, race, blast, research trigger, ask gate) with four cells, each citing a file or a recorded gap, and the templating lint passes.

- **Show "last proof of life" per deliberation component** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: T-2542 covered timers only. The plan gate, race and blast graph can be dead too (assumption: no per-component liveness exists).
  Done when: killing one component in a scratch copy makes `fm doctor` name it within one run.

- **Diff gate verdicts between the working copy and the committed fallback** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2532 runs hooks from the committed library when the working copy fails. If the older gate judges differently, the fallback silently changes behaviour.
  Done when: a corpus of 30 plans yields identical verdicts on both libraries, or the diff is listed in `fm doctor`.

- **Give each deliberation step a control arm** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: T-2534 and T-2536 show the user wants every feature measured against its absence. The exam has a guard-only arm but none for readings, race or blast radius.
  Done when: `fm exam run --agent` takes a no-race or no-plan-gate arm and the scorecard prints the delta per step.

- **Record the task state each cell's probe ran in** — FIX — value 4 — effort M — risk low — category: coverage
  Why: T-2525 shows a premise tested in only one state (no start commit, open tasks). A cell proved once is not proved everywhere.
  Done when: every cell lists the lifecycle states it was probed in, and `fm genesis check` flags a cell probed in fewer than three.

- **Keep a question deck from every closed miss** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Each missed ask should leave behind the question that would have caught it. Today the lesson is the fix, not the question.
  Done when: closing a FIX with a `caught-by:` line adds it to a deck, and the plan gate shows the deck's matching questions for touched paths.

- **Stamp every budget with the unit the user pays** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: T-2533 found hook notes counted per session while the user pays per reply (assumption: other gauges have the same mismatch).
  Done when: each lean-ratchet row names its measured unit and its paid unit, and any mismatch is listed.

- **Show "as of" age and a stale banner on every web UI panel** — FEATURE — value 4 — effort S — risk low — category: web UI
  Why: The only surface here is the web UI, and the packs show no empty, loading or dead-source state for deliberation panels (assumption).
  Done when: stopping the server leaves the open page showing "stale, 40s" instead of frozen numbers, checked by a screenshot.

- **Measure before filing** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: Four of the five dropped items were decided by a measurement ("1 of 22", "5 of 1219") that could have run at capture time.
  Done when: `fm capture` on a "cut/add X" idea appends a count from the ledger or logs, and a task whose count is zero is held.

- **List everything Foreman leaves outside the repo** — FEATURE — value 4 — effort M — risk low — category: footprint
  Why: T-2542 found installed units nobody inspected, and the standing "leave no trace" claim has no inventory.
  Done when: `fm footprint` prints every unit, hook, settings key and cache directory with its last-touched time, and eject removes exactly that list.

- **Wild: Run an anti-brainstorm** — FEATURE — value 4 — effort M — risk low — category: blind spots
  Why: wild. A tool-less child gets only the list of built features and must write how each could be silently broken. Each answer becomes a cell probe, which catches T-2532-style gaps before the user hits them.
  Done when: one run yields 20 or more failure-first probes and the tower records how many already existed.

- **Wild: Add a scar count to cells** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild. A cell gains a scar when a real miss lands in its area. Cells with none are shown pale as "untested by reality", which makes thin evidence visible.
  Done when: the grid page renders scar counts from the missed-ask list.

- **Wild: Build a blind-spot museum page** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Each missed ask sits beside its catching question and a "would it be caught today?" replay button. This makes the miss trend legible to the user.
  Done when: the page lists all eight T-ids and each replay returns pass or fail.

Next question: Which of Foreman's own measurements (ratchet, exam, outcomes) has a user-visible number whose producer and checker are the same code?
Next question: What does the user have to remember to ask for every generation that Foreman could ask itself once, durably, as a standing probe?
