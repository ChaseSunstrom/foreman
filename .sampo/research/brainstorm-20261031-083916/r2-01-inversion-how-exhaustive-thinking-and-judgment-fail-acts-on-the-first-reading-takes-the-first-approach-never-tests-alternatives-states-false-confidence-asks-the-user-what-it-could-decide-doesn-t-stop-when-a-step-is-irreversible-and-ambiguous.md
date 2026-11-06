# Brainstorm — lens: inversion: how exhaustive thinking and judgment fail: acts on the first reading, takes the first approach, never tests alternatives, states false confidence, asks the user what it could decide, doesn't stop when a step is irreversible and ambiguous

- **Replay the failure modes as a fixture suite** — FEATURE — value 5 — effort M — risk low — category: testing
  Why: the pack lists the failure modes (first reading, first approach, false confidence, needless asking, irreversible-ambiguous run-through) but shows no scenarios that provoke each one. Mission 5 builds the gates (T-2269, T-2271, T-2277) without a test that the failures they target actually occur without them.
  Done when: `fm exam` has five inversion scenarios, one per failure mode, where the plain arm fails and the gated arm passes, and the report names which gate caught each.

- **Catch the paraphrased plan gate pass** — FIX — value 4 — effort S — risk low — category: plan gate
  Why: T-2285 shows the gate miscounts options (flag-led text). The opposite miss is likelier: three options that are one idea reworded pass the count. The earlier idea "fail the plan when options are one idea in three costumes" is unbuilt, and this one makes it concrete with a free check (shared-token overlap of the option's verb and target path).
  Done when: a plan whose three options share their main verb and scope paths is refused with the pair named, and a plan with three distinct mechanisms passes.

- **Pin the user's words in the plan and diff readings against them** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: first-reading lock-in is the lens's first failure; the pack has the user's verbatim asks, but L plans only need "2+ readings" by count. Assumption: readings often differ only in wording.
  Done when: each reading lists the user-word span it relies on, and a reading whose spans fully overlap another's is rejected as a duplicate.

- **Make a stop-and-ask prove it could not decide** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: the Mission says to stop only when irreversible and ambiguous; the pack shows `fm ask` exists and earlier ideas classify stops, but no gate rejects an ask that skipped the check. Dropped items show Foreman asking about things it could settle (T-2285-type clarifications).
  Done when: `fm ask` requires a reversibility tag and the two readings in conflict; an ask with a reversible tag is auto-answered with the default and logged with its undo.

- **Block irreversible steps whose confidence rests on one reading** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: the guard already stops dangerous commands but not an ambiguous plan step. Mission 5 wants a stop on irreversible plus ambiguous; nothing joins the guard's verb table to the plan's readings.
  Done when: a plan step flagged irreversible (migration, publish, force-push, delete) under a plan with 2+ unreconciled readings makes `fm task focus` refuse with the one question to answer.

- **Run the race when the cheap verify exists, not only after 3 failures** — PERFORMANCE — value 4 — effort M — risk med — category: lanes
  Why: T-2271 races the runner-up only after 3 failed runs; the first-approach failure is paid for three times. Assumption: for S/M tasks with a ≤30s verify, an up-front race is cheaper than three failures.
  Done when: an S/M task with a named alternative and a verify under 30s races at focus, and the ledger shows total minutes against the stuck-ladder path on a replayed task set.

- **Cap stated confidence by evidence kind** — FIX — value 4 — effort S — risk low — category: calibration
  Why: the user's own-words list shows "Unproven rollup" for typed or inconclusive evidence; a plan can still say "high" confidence on it. Assumption: confidence is free text today.
  Done when: a done claim resting on typed evidence cannot record confidence above "medium", and the finish receipt shows the cap and its reason.

- **Fail the plan when a low-confidence assumption has no falsifier** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: the gate already requires a research note or spike for a low-confidence assumption; it does not require saying what observation would prove it wrong, so a note can be filler.
  Done when: the gate refuses a research note lacking a line beginning "Falsified if:" naming a command or file, and accepts one that has it.

- **Log decide-instead-of-ask receipts and review the regrets** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: "records and decides" is the Mission's promise, and a silent default is its failure case when the user later reverses it. The pack's "what earlier brainstorms missed" list is exactly these reversals (T-2288, T-2290, T-2291 were asks the user had to make).
  Done when: every auto-decision writes one receipt line with an undo command, and `fm decisions` lists those the user later reversed with the rate per question class.

- **Score the blast-radius neighbours against where fixes landed** — PERFORMANCE — value 3 — effort S — risk low — category: blast radius
  Why: T-2277 writes neighbours into Risks once, with no check that they were useful. Assumption: many are noise and train the reader to skip Risks.
  Done when: at close, `fm graph blast` hit-rate (neighbours actually touched or failing) is recorded per task, and a Risks line whose rate is under 10% across 20 tasks is dropped from the template.

- **Wild: Stage a "first-instinct tribunal" before every L plan** — FEATURE — value 3 — effort M — risk med — category: judgment
  Why: wild. A cold Haiku child is given only the user's words and writes the plan it would write in 60 seconds; the real plan is diffed against it, and agreement on all rows is flagged as suspicious sameness, disagreement as the readings to reconcile.
  Done when: an L plan shows a "first-instinct diff" section naming rows only one side has.

- **Wild: Run an inversion canary that plants a trap in the user's request** — FEATURE — value 3 — effort L — risk med — category: testing
  Why: wild. A weekly canary goal has two valid readings and one irreversible step; the pass condition is that the agent stops for exactly that step and decides everything else.
  Done when: the canary report shows one stop at the irreversible step, zero stops elsewhere, and a failing run opens a FIX task.

- **Wild: Print a "regret forecast" next to each approach** — FEATURE — value 3 — effort M — risk high — category: calibration
  Why: wild. Beside each option, show the odds the runner-up would have won, taken from past races of the same tier and type, so a confident choice carries its historical error bar.
  Done when: the plan's Approach shows a "runner-up won N of M similar races" line, and with fewer than 5 races it says "no history" and does not guess.

Next question: Which of Foreman's own stated confidence numbers have ever been compared with how the task actually ended, and where would that comparison live?
Next question: When two gates disagree (plan gate passes, blast radius warns, guard stops), which one does the user see first, and is the order chosen or accidental?
