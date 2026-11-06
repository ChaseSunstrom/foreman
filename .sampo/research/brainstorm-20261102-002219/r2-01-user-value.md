# Brainstorm — lens: user value

Answers to earlier questions from the user-value side:
- **Cells dependent on Claude Code:** Any cell that cites a hook event (SessionStart, PreCompact) quietly depends on Claude Code. Assumption: this is the biggest source of hidden harness dependence among the 58.
- **Output nobody reads:** The goal's progress and finish outputs are the least read. The user only notices a missing one after it has cost them a task.

- **Seed the plan from the user's own finished goals** — FEATURE — value 4 — effort M — risk low — category: goal planning
  Why: assumption: users repeat goal shapes (a new verb, a new surface, a new capability), and each plan is decomposed from scratch. Retrieval over closed goals' rows gives a head start.
  Done when: `fm goal new` on a request resembling a closed goal prints the matching goal's rows as a draft, each marked reused or new, and a test covers it.

- **Predict every user-only item at plan time** — FEATURE — value 5 — effort M — risk low — category: handoff
  Why: the standing rule says user-only items go in the final report, but the user finds them at the end. Scanning the plan for pushes, grants, credentials and merges would show the list on day one.
  Done when: a goal's plan page lists "needs you" items with the row that triggers each, and one fixture goal's list matches the items it actually produced.

- **Let the user edit the goal as a plain markdown file** — FEATURE — value 4 — effort M — risk med — category: control
  Why: assumption: striking, reordering or adding a row by editing a file is faster than any verb, and it works on every harness.
  Done when: editing `goal.md` (strike, move, add a line) changes the plan on the next `fm goal status`, with a diff receipt and a refusal on malformed edits.

- **Print a human handoff page for a goal** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: assumption: goals sometimes need to go to a teammate, or to the user's later self, who has no Foreman session. `fm goal handoff` would write one page covering done, open, decisions and how to resume without Foreman.
  Done when: the page is generated from state files only, and a fixture test shows every open row, decision and user-only item appears in it.

- **Show a parity table against rival products at finish** — FEATURE — value 4 — effort M — risk med — category: completeness
  Why: pillar 2 asks for a capability map, but the "knows when it's actually done" claim only becomes believable to the user when they can see what the best products do and what this one has, half-has or lacks.
  Done when: finishing a goal with a capability-map step writes a table with every row marked has, half or lacks. Any "lacks" row is a filed task or an explicit user waiver.

- **Cap the questions at three, each with a default** — FIX — value 4 — effort S — risk low — category: vague goals
  Why: assumption: a vague goal can trigger a stream of clarifications, and the standing rule says never to block on process questions. A hard cap with recorded defaults keeps the autonomy rule.
  Done when: a vague-goal fixture produces ≤3 questions, each with a default, and the run proceeds on the defaults when unanswered.

- **Rank the 58 cells by what the user would notice missing** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the ask is to fill all 58, but order matters if a run is cut short. Ranking by user-visible moment (resume, finish, crash recovery) over internal moments puts the worthwhile fills first.
  Done when: the fill order file lists each cell with a one-word user-visible tag, and the first 15 filled cells all carry a user-visible tag.

- **Flag cells that depend on one harness** — FIX — value 3 — effort S — risk low — category: coverage
  Why: the earlier question about harness dependence is unanswered, and the standing rule says Foreman isn't specific to Claude Code.
  Done when: each cell carries a `harness:` tag, and the sweep names any cell that cites a Claude-only hook without a fallback path.

- **Write the "stopped vs done" line on every goal exit** — FEATURE — value 5 — effort S — risk low — category: finish
  Why: the capability says to know "when it's actually done rather than merely stopped". A one-line typed verdict on every exit (done, budget, blocked, crash, user stop) makes it visible.
  Done when: every goal exit path in the code writes the typed verdict, and a test kills a run at each exit path and finds the line.

- **Wild: Seal a "what delight looks like" sentence at goal start** — FEATURE — value 3 — effort S — risk low — category: acceptance
  Why: wild. Foreman asks the user for one sentence about what the finished product feels like, then reads it back at finish next to the evidence and asks "true?". It tests meaning rather than checklist completion.
  Done when: finishing a goal prints the sealed sentence next to the finish evidence and records the user's answer.

- **Wild: Let the user place a finish-date bet** — FEATURE — value 2 — effort S — risk low — category: planning
  Why: wild. The user guesses a date and Foreman guesses one. Both are scored at the end, which calibrates the forecast against a human baseline and makes progress more playful.
  Done when: a finished goal shows both dates and the actual date, and the Brier score is written to the calibration ledger.

- **Wild: Run a "stranger on day one" walkthrough at finish** — FEATURE — value 4 — effort L — risk med — category: acceptance
  Why: wild. A tool-less child is given only the README and the finished goal's try-this card, and must complete the first-use path. It reports where it got lost.
  Done when: finish records the child's walkthrough result, and a failed walkthrough blocks "done" until a row is filed.

- **Wild: Mark a row "surprise me" so Foreman picks its approach** — FEATURE — value 2 — effort M — risk med — category: control
  Why: wild. Some rows the user doesn't care about. Marking them lets Foreman choose the cheapest approach without asking, recording the choice as a costly decision for the final report.
  Done when: a surprise row finishes with a decision entry and no question asked.

Next question: Which of the goal's outputs does the user actually open after a multi-day run, and which do they only discover when something goes wrong?
Next question: Does anything in the goal engine break when the user edits its state files by hand, since users will do that?
