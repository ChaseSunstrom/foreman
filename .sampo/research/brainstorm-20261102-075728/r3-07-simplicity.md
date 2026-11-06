# Brainstorm — lens: simplicity

Lens: simplicity. Each idea removes a concept, a state or a step, and none repeats the "ideas so far" list.

- **Filter brainstorm output against the catalog instead of feeding the catalog in** — CLEAN — value 4 — effort S — risk low — category: brainstorm
  Why: this pack carries thousands of lines of "ideas so far" and children still repeat each other, so the input is bloated and the dedupe is unreliable.
  Done when: a brainstorm pack contains no ideas-so-far section, and a post-pass drops any returned idea whose title overlaps an existing catalog entry. A test with a planted duplicate shows it dropped.

- **Give steers content-hash ids** — FIX — value 3 — effort S — risk low — category: steers
  Why: the steer list reuses labels like "user steer 2026-10-31 #1/#2/#3" for different rules, so two rules share one id and a check can attach to the wrong one.
  Done when: no two stored steers share an id, and a test with two same-date, same-number steers keeps both distinct.

- **Keep goals of three rows or fewer in the session only** — FEATURE — value 3 — effort S — risk low — category: goal state
  Why: assumption: tiny goals pay the same persistence and resume cost as week-long ones. Only a goal stopping with work left needs a file.
  Done when: a 2-row goal that finishes in one session leaves no goal file, and the same goal killed mid-way leaves one that resumes.

- **Draft the plan with zero questions and a struck-through assumptions list** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: the user's habit, shown in the steers, is "never block on me, record it and keep going". Questions are the costliest interrupt.
  Done when: a vague goal yields a plan whose first lines list its assumptions. The user can strike one, and only the rows built on it re-plan.

- **Collapse task statuses to open, done and dropped, plus an optional wake condition** — CLEAN — value 4 — effort M — risk med — category: tasks
  Why: Open work mixes deferred and blocked with prose reasons ("later: needs…") that nothing reads.
  Done when: `fm tasks` shows exactly three statuses. Every old deferred or blocked item migrates to open with a wake text or to dropped, and the migration is tested on the real ledger.

- **Run the tick in two classes: must-run and when-someone's-looking** — FEATURE — value 4 — effort S — risk low — category: tick
  Why: this answers the earlier question about on-time versus eventual jobs. Only settling bets and the digest plausibly need a clock. The rest can run at session edges.
  Done when: the job table has a `class` field with 2 values. A fake-clock test shows must-run jobs fire on the first edge after they are due, and the other class never fires without a session.

- **Cap the user-facing nouns at eight** — CLEAN — value 3 — effort S — risk low — category: vocabulary
  Why: docs and steers use task, goal, steer, seed, mission, lesson, decision, bet, lane, door, tower and more. A newcomer cannot hold them all.
  Done when: `fm help` and the README introduce only eight nouns. A lint fails when a user-visible string uses a ninth without an alias to one of the eight.

- **Drop plan rows smaller than one commit** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: rows like "rename X" inflate the plan and the progress bar. Merging them into the neighbouring row shortens the plan without hiding work.
  Done when: a generated plan has no row whose estimate is under one commit, and the merged row's DONE-WHEN names both changes.

- **Wild: use stamp files and make semantics as row state** — FEATURE — value 3 — effort M — risk med — category: goal engine
  Why: wild. A row is a target and its proof output is a stamp file. Crash recovery, resume and "what's left" come from make's own dependency and mtime logic, with no state machine to corrupt.
  Done when: killing a goal at every row boundary and running `make done` resumes at the right row. The planner has no code that reads a status field.

- **Wild: plan the goal as a diff against a future README** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: wild. The finished version is written as the README it would ship, and plan rows are the sentences the current README lacks. "Done" is every sentence backed by a command that ran.
  Done when: a vague goal produces a future-README draft. Rows trace to its sentences, and an unbacked sentence blocks done.

- **Wild: accept a pasted plan from any chat and own only the carrying and finishing** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: wild. Foreman is the discipline layer, not a planner, and any model or human can write a checklist. Validating one (probes, order, grounding) is cheaper than generating one.
  Done when: pasting a markdown checklist creates a goal. Rows without a probe get one proposed, and it survives a kill and resume.

- **Wild: score the goal with one 0–100 number and a threshold** — FEATURE — value 2 — effort M — risk high — category: finish
  Why: wild. One command the user can read replaces five completeness signals, and "done" is the score crossing a line they set. The risk is metric gaming, so a cold read of each score definition is mandatory.
  Done when: a goal can declare a score command and a threshold. A planted gaming change (a deleted test that lifts the score) is caught by a cold-read fixture.

Next question: Which of Foreman's states, statuses and nouns has the user never typed or read in the last 30 days, and what happens if each is removed?
Next question: For a goal that survived several days, how many of its rows did the user actually check, and would the plan have been the same without the rest?
