# Brainstorm — lens: user value

- **Show the plan as a one-screen decision card at accept** — FEATURE — value 5 — effort M — risk low — category: plan UX
  Why: the pack lists dozens of deliberation checks (readings, options, falsifier, door class, depth) but the user only ever sees refusal text; assumption: the user can't tell whether thinking happened without reading the plan prose.
  Done when: `fm task plan --accept` prints a card with readings, chosen approach, runner-up, blast radius ("unknown" when unknown), depth reason and one falsifier, in ≤15 lines, covered by a test.

- **Ground every coverage-cell fill against the repo first** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the Mission 3/4 lesson says most ideas were already built, and the standing rule says a cell counts only if it names a file or a real gap with no reused phrasing. Without grounding, the 58 cells become templated prose.
  Done when: a cell-fill verb refuses a cell whose cited path or grep doesn't resolve, or whose wording matches a neighbour above a similarity threshold; a test covers both refusals.

- **Collapse the plan-gate checks into one `plan lint` verdict** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: the pack's idea list shows overlapping checks (distinct options, falsifier, first-reading diff, paraphrased readings) while the standing lean rule says growth must pay by deletion.
  Done when: one command returns a scored pass/fail with each failed check's one-line fix, and the old per-check messages delegate to it with tests unchanged.

- **Scale deliberation to risk and say so in one line** — FEATURE — value 5 — effort S — risk low — category: depth
  Why: gen-0 #2 says an S task must not pay an L task's cost, yet the user has no view of why depth was chosen; assumption: there's a tier and blast radius available at plan time.
  Done when: every plan prints "Depth: S (reason: 1 file, reversible)" or higher, and an S task's deliberation is capped by a test.

- **Record every decide-instead-of-ask with a one-line undo** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: standing rule says never block the user on process questions and land them in the final report as costly decisions; the user needs to review and reverse them cheaply.
  Done when: `fm decisions` lists each auto-decision with its undo line, and `fm undo N` runs it in a test.

- **Stop asking only on one-way AND ambiguous doors, with a visible tally** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the pack's door-gate work (fmdoors parks irreversible AND ambiguous steps) is built; the user sees no count of asks avoided versus asked.
  Done when: task close prints "doors passed: 7 two-way, 1 asked" from the door ledger.

- **Add a "meant it?" read-back before the first edit** — FEATURE — value 4 — effort S — risk low — category: intent
  Why: the user's recurring steers are letter-versus-intent corrections (T-2341 re-scope, the `--by harness` flag wording); assumption: a restatement in the user's own nouns catches these early.
  Done when: the plan has a Read-back section quoting the ask's verbs and nouns, and the gate fails if a quoted noun is absent from the plan's steps.

- **Answer "is this already built?" at capture time** — FEATURE — value 5 — effort M — risk low — category: dedupe
  Why: the lesson from Missions 3 and 4, plus the dropped list (several asks were already built), shows the user pays for work that exists.
  Done when: capturing a task whose terms match a verb or MASTER.md entry prints the path and offers to drop it, tested on a known-built example.

- **Weekly "what deliberation changed" digest** — FEATURE — value 4 — effort M — risk low — category: proof of value
  Why: the lean steer wants growth to show gain; nothing says whether readings, races or rivals ever changed an outcome. Assumption: the plan records the first-instinct approach.
  Done when: the digest lists tasks where the chosen approach differed from the first one, with the outcome, and is reachable from `fm doctor`.

- **Wild: Stubborn-reader child argues the user meant the opposite** — FEATURE — value 3 — effort M — risk low — category: ambiguity
  Why: wild; a cold child that is given only the user's sentence and must defend the least obvious reading makes a hidden ambiguity visible before the build.
  Done when: for an L plan, a one-line "strongest alternative reading" appears and the plan must answer it.

- **Wild: Replay the last 20 user corrections through today's plan gate** — FEATURE — value 4 — effort L — risk low — category: regression
  Why: wild; the "asked" and "steered" streams are real labelled misses, so a nightly replay shows whether the gate would now have caught them.
  Done when: `fm doctor` prints "gate would have caught 14/20 past corrections" with the missed ones listed.

- **Wild: Argue-for-the-runner-up button in the web UI** — FEATURE — value 3 — effort M — risk low — category: plan UX
  Why: wild; the user disagrees with plans by editing, and a one-click swap with the rival's falsifier makes redirection cheap.
  Done when: clicking it rewrites the plan's chosen approach to the runner-up and records the swap in the decision ledger.

- **Park the user-only row and continue on the rest** — FEATURE — value 4 — effort S — risk low — category: flow
  Why: the standing steers say don't stop work for questions only the user can answer; assumption: today a single blocked row can idle a lane.
  Done when: a goal with one user-only row finishes the other rows and lists the parked one in a single yes-card, tested.

Next question: Which of the 58 empty cells are already satisfied by an existing verb the grep can prove, so only the true gaps need new work?
Next question: When the user reads a plan, which single line decides whether they trust it, and does the card put that line first?
