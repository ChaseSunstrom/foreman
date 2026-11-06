# Brainstorm — lens: approaches

- **Fill the 58 cells from a rule table, not 58 sentences** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the request is to fill 58 empty cells for #2; the steer says a cell counts only if it names a concrete capability grounded in a file or a real gap, and templated phrasing is rejected. A table keyed by (surface, stage) that maps to a probe plus a grep'd path yields distinct, grounded cells mechanically. Approach: one lane per surface, each cell cites a `file:line` or verb.
  Done when: `fm genesis sweep` coverage pass reports 0 empty, 0 templated, 0 duplicated cells for capability #2.

- **Triage the 58 cells into existing, gap and n/a before writing prose** — FEATURE — value 5 — effort S — risk low — category: coverage
  Why: the Mission 3 and 4 lesson says most of #11 and #12 were already built. Classify first with grep over MASTER.md and plugin/lib, then write only the gap cells as tasks. Cheapest approach, and it avoids filing duplicates.
  Done when: a triage file lists 58 rows, each tagged existing (with path), gap (with task id) or n/a (with a reason and a counterexample search).

- **Mark n/a only after a recorded counterexample search comes back empty** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the standing rule says no idea is killed for ambition and every cell is a grounded idea, a feature path or a recorded n/a. A cheap n/a invites cheating, so each one needs a recorded search (grep terms and result), and an expiry so it gets rechecked.
  Done when: every n/a cell has a search line and a revisit date, and the sweep fails on a cell without them.

- **Collapse the plan-gate checks into one `plan lint` verdict** — CLEAN — value 4 — effort M — risk med — category: planning
  Why: the idea catalog is full of separate plan checks (distinct options, falsifier, first-reading diff, tier floor). Doing less means one scored verb instead of many. Trade-off: a refactor of working gates, so it needs the guard corpus replayed first.
  Done when: one command returns a per-check verdict for a plan, and the existing plan-gate tests pass unchanged.

- **Run a blind rival planner and diff its readings** — FEATURE — value 4 — effort M — risk med — category: deliberation
  Why: the pack's catalog repeats that the writer and judge are the same house. A tool-less child that sees only the user's words, with a different model family, gives a signal Foreman didn't author. Disagreement across readings becomes the ambiguity signal. Skip it for S tasks.
  Done when: for a seeded ambiguous request, `fm plan` shows a three-column table (user's words, plan, rival readings) and logs the skip on an S task.

- **Gate irreversible steps on a door ledger the model can't write** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: steers say ask only on one-way AND ambiguous. Deriving the door class from the guard's own deny rules reuses an existing tool rather than adding a new classifier. Each auto-decision gets a one-line undo receipt.
  Done when: a test shows an irreversible step with two readings parks, a reversible one logs a receipt with an undo line, and the model's write to the ledger is refused.

- **Race at plan time only when the top two options are close and verify is cheap** — PERFORMANCE — value 3 — effort M — risk low — category: racing
  Why: gen-0 #2 asks for parallel lanes, evidence over first instinct, and scaled depth. A trigger avoids paying L cost on S tasks. Assumption: the plan's percent split is available as the closeness signal (T-2507 work records it).
  Done when: a task with 55/45 options and a cheap verify spawns a race, and one with 90/10 does not, both logged with the reason.

- **Pre-register every confidence and score it at close** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: the bet ledger (ship bets, harness split, Brier) exists. Extending it to plan confidences is reuse, not new machinery. Cap stated confidence by evidence kind.
  Done when: closing a task scores its plan confidence, and `fm outcomes --judgment` shows a per-evidence-class reliability row.

- **Replay the last 20 user corrections through today's plan gate** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: "The user's own words" are mostly corrections of plans (the flag name, the premise, the reassigned beyond rows). Each becomes a fixture, so the gate is tested on signals Foreman didn't author.
  Done when: a suite of 20 fixtures runs in `fm check` and at least one is shown to fail on a pre-fix gate.

- **Do less: skip deliberation for S tasks and log the skip** — PERFORMANCE — value 3 — effort S — risk low — category: depth
  Why: gen-0 says scale depth to risk. A one-line "nothing to think about" receipt makes the skip auditable and cheap.
  Done when: an S task closes with a receipt naming the skipped steps, and a test caps its deliberation tokens.

- **Wild: Hold a pre-mortem with a child told the change already failed** — FEATURE — value 3 — effort M — risk low — category: deliberation
  Why: wild. A tool-less child that gets the plan plus "this failed in production, say why" finds failure modes the planner's own optimism hides.
  Done when: an L plan carries a pre-mortem section whose items are each tied to a test or an explicit accept.

- **Wild: Replay history to test the thinking itself** — FEATURE — value 3 — effort L — risk med — category: evaluation
  Why: wild. Take closed tasks, ask the planner what it would have chosen, and compare with what actually survived. This measures whether first-instinct plans lost to the runner-up.
  Done when: a report gives the share of closed tasks where the runner-up would have won, over at least 30 tasks.

- **Wild: Make a race just N lanes plus a judge file** — CLEAN — value 3 — effort M — risk med — category: racing
  Why: wild. Instead of a dedicated race verb, reuse the lane machinery and a user-owned judge file. It cuts a verb and removes the writer-also-judges problem.
  Done when: `fm race` is replaced by lanes plus a judge file, with the same race tests passing.

- **Show readings, options and the race on a web UI deliberation page** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the only surface is the web UI, so the cells for it need something concrete. A page with fork map, depth gauge and a "do less" chip gives the user a view of what was weighed.
  Done when: a screenshot test shows one task's readings, options and chosen approach, and an empty state for a task with no deliberation.

Next question: Which of the 58 cells are not reachable from a real session path, so that filling them would produce a documented capability nothing calls?
Next question: What does a cell's probe show on a harness without hooks (Codex, Gemini, opencode), where the plan gate cannot run at all?
