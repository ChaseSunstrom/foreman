# Brainstorm — lens: simplicity

- **Make the plan gate one `plan lint` verdict** — CLEAN — value 4 — effort M — risk med — category: deliberation
  Why: the pack lists a dozen separate plan checks (distinct options, falsifier, first-reading diff, paraphrase detection, tier floor, unsupported-certainty lint). Each is a rule the user must learn; one scored verdict with a single runnable fix line is simpler to explain and test.
  Done when: `fm plan lint` returns one verdict plus at most one fix command, and the existing separate refusal messages are served from it, with the old gate tests still passing.

- **Derive depth as one number from blast radius and reversibility** — FEATURE — value 4 — effort M — risk med — category: deliberation
  Why: depth now comes from tier labels, floors and triggers; the pack's "so an S task doesn't pay an L task's cost" (gen-0 #2) wants one dial. Assumption: the blast-radius and door-class data already exist as inputs.
  Done when: a task's depth number is printed with its two inputs, and an S task with a small blast radius provably skips race and rival while an L task with an irreversible step runs both.

- **Fill the 58 cells from a rule table, not 58 sentences** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the request is to fill 58 empty cells, and the standing steer rejects templated prose, while earlier ideas repeatedly proposed deriving cells from probes. A table keyed by column rule, each row naming a file or grep, gives real cells with no reused wording.
  Done when: `fm genesis check` reports 0 empty cells, and the templating lint finds no two cells sharing wording beyond their file path.

- **Mark most cells "existing" or n/a with the grep that proves it** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the lesson from Missions 3 and 4 is that most of #11 and #12 were already built. Assumption: many of #2's cells map to the plan gate, `fm graph blast`, races and `fm decide`.
  Done when: each existing or n/a cell carries a command whose output a cold read can re-run, and the cold read passes the cells.

- **Delete a deliberation step for every one added** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the lean ratchet exists, deliberation ideas pile up, and the user's lean steers want growth paid for by deletion. Assumption: ship can measure verb count per capability.
  Done when: `fm ship` refuses a task that adds a deliberation verb or flag without a named removal in the same commit.

- **Collapse repeated stops into a standing answer** — FEATURE — value 3 — effort M — risk med — category: asking
  Why: the user's steers say never block on rules or process questions, and many ideas log stops. One user-owned answers file removes a question class from future asks.
  Done when: a question matching a stored answer is resolved from it, logged as a decision with a one-line undo, and the answer is listed by `fm decide`.

- **Show deliberation as three lines at close** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the user asks for plain receipts (T-0795) and many ideas add records. Three lines (readings kept, approach chosen with its runner-up, what would flip it) replace the plan prose in the finish receipt.
  Done when: `fm task finish` output ends with exactly those three lines for an M or L task and a "no deliberation needed" line for S.

- **Make a race just N lanes plus a judge file** — CLEAN — value 3 — effort M — risk med — category: deliberation
  Why: the race verb, rubric, Pareto card, halving and fragility ideas all extend one mechanism. Assumption: the existing lane code can host the judge as a file.
  Done when: a race runs through the generic lane path with a judge file, the dedicated race code is removed, and the race tests still pass.

- **Cap an S task's deliberation by test** — PERFORMANCE — value 3 — effort S — risk low — category: scaling
  Why: gen-0 says scale depth to risk, and nothing in the pack shows a test enforcing a ceiling for S tasks.
  Done when: a test fails if an S task's plan gate, research trigger or rival adds model calls or more than a set number of injected characters.

- **Share the idea catalog by canonical cluster** — CLEAN — value 3 — effort M — risk low — category: brainstorm
  Why: the "ideas so far" list repeats the same idea dozens of times in different words (heartbeat, replay, canary, tripwire). Clustering by capability shrinks the pack and prevents re-proposals.
  Done when: the pack builder emits at most one line per cluster for ideas outside the mission's capability, and the pack shrinks by at least half.

- **Wild: Make the plan one sentence plus a falsifier** — FEATURE — value 3 — effort S — risk med — category: deliberation
  Why: wild. Everything else is added ceremony; the simplest form of exhaustive thinking is a claim and the test that would break it.
  Done when: a plan with one sentence and one runnable falsifier passes the gate for an S task, and the same plan fails for an L task.

- **Wild: Let the cheapest model think once, then replay the plan** — PERFORMANCE — value 3 — effort L — risk high — category: cost
  Why: wild. Deliberation cost is paid per task; caching a plan by request shape lets repeats reuse it.
  Done when: a second task of the same shape reuses a stored plan, and a drift check rejects it when its files changed.

- **Wild: One question each night, from the dropped-as-built list** — FEATURE — value 2 — effort S — risk low — category: simplicity
  Why: wild. The "dropped" lines show many ideas were already built; surfacing one a day teaches the user what exists with no new surface.
  Done when: session start prints at most one such line per day and never repeats a line within 30 days.

Next question: Which of the 58 empty cells are already answered by a path in `plan/gate` code, and can a grep produce that list before any cell is written?
Next question: Which deliberation checks have never refused a real plan, so removing them costs nothing?
