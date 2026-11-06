# Brainstorm — lens: user value

- **Pre-flight the user's draft request** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: assumption: terse asks are the main source of wrong first readings, and the pack's ideas all start after the ask is sent. A local check on the typed request lists its likely readings and flags the one that costs most if wrong, before any lane spends.
  Done when: `fm preflight "<ask>"` prints at most 3 readings and one question for 5 fixture asks, uses zero model tokens in its first pass, and the test fails if the output is empty.

- **Triage a mid-run message as amend, replace or new** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: T-0790 (verbatim capture and folding bursts) is deferred, and the user's recent asks arrive as corrections to work already in flight. Deliberation should decide whether a new message amends the current plan, replaces it or is separate, and show the plan diff.
  Done when: a fixture session with a message sent mid-build is classified into the right one of the three, and the plan shows only the steps that changed.

- **Learn the user's tie-break profile** — FEATURE — value 4 — effort M — risk low — category: personalization
  Why: the dropped and steered lines show a consistent taste: measure before building, reuse before new, subtract by evidence. A picker that breaks ties the way decisions.md history does saves them from restating it. Assumption: enough decisions exist to derive it.
  Done when: `fm plan` shows "tie-break: prefers existing over new (7 of 9 past picks)" and the picker's choice flips in a test when the profile is removed.

- **Replan only what a veto touches** — FEATURE — value 4 — effort M — risk med — category: plan editing
  Why: assumption: a user who rejects one reading today triggers a full replan. A one-word veto of a reading or approach should re-deliberate only the dependent steps and keep the rest.
  Done when: vetoing one reading changes only the steps that cite it (checked by diff) and a replan token count is below half a fresh plan's on the fixture.

- **Fill the 58 cells from a task-kind by stage table** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: open work spans FEATURE, FIX, CLEAN, RESEARCH and PERFORMANCE, and each needs different thinking artifacts: a baseline number for performance, a characterization test for clean-up, a source for research. One table where each cell names a required artifact and its refusal code fills most cells with distinct, grounded text.
  Done when: every non-n/a cell names an artifact and a code path found by grep, the templating lint passes, and a test fails when a task kind has no artifact for the plan stage.

- **Mine the user's reverts and fixups into a personal edge-case deck** — FEATURE — value 4 — effort M — risk low — category: edge cases
  Why: the user's own past mistakes are the cheapest source of edge cases, and the git history already holds them (fixup, revert and "fix: forgot" commits). Assumption: enough such commits exist locally.
  Done when: `fm plan` for a task touching a file with 2 or more past fixups lists those cases, and the deck builds with no network.

- **Promise a plan-ready time and keep it** — FEATURE — value 3 — effort S — risk low — category: latency
  Why: deliberation cost is paid in the user's waiting. Show "plan in about 40s" by tier, and at the deadline hand over the best plan so far with the open questions marked.
  Done when: a test with a stalled child returns a labelled partial plan within the stated time plus 10%.

- **Put rejected alternatives in the PR body** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: reviewers ask "why not X" after the work, so the readings, the approaches rejected and the failure modes already recorded in the plan are the answer. A git note exists as an idea, but the PR body is where the reviewer looks.
  Done when: `fm ship` output for a task with a recorded race includes a "Considered" section listing at least 2 rejected options with reasons.

- **Decide the deferred queue as one batch** — CLEAN — value 4 — effort M — risk med — category: backlog
  Why: about 30 "Later from T-07xx/08xx" items sit deferred with only a loose "later" condition. One deliberation pass gives each a build, merge or drop verdict, with its revisit condition checked against current code, and the user answers once.
  Done when: each deferred item has a verdict line and a checked revisit condition, nothing is dropped without the user's yes, and the open count falls after the answer.

- **Counter-offer a smaller ask** — FEATURE — value 4 — effort M — risk low — category: scope — wild
  Why: assumption: "do less" is only an option in a list. For L tasks Foreman could instead propose the 20% that gives 80% of the value, with a cost estimate, and let the user pick the full or the cut version.
  Done when: for 3 fixture L asks the plan opens with a counter-offer naming what is cut and its estimated saving, and accepting it shrinks the step list.

- **Offer a thinking-partner mode that never edits** — FEATURE — value 4 — effort M — risk low — category: product — wild
  Why: the exhaustive-thinking machinery is useful before any code is wanted. A mode that only returns readings, options, failure modes and one next question, and writes no files except a decision note, is a product the user can use daily.
  Done when: `fm think "<idea>"` produces the sections with zero edits (a test asserts the working tree is unchanged) and offers to turn the note into a task.

- **Make depth follow attention** — FEATURE — value 3 — effort M — risk med — category: autonomy — wild
  Why: a user present in the session can answer a cheap question, while one away cannot, so ask-first and think-longer should trade off by whether anyone is watching. The standing steers assume no interactive user in full autonomy, and this makes the choice explicit and visible.
  Done when: the same ambiguous task asks one question when the session is live and records a decision with an undo line when it is not, and both appear in a test.

- **Interview a vague L ask by taps** — FEATURE — value 3 — effort M — risk low — category: web UI — wild
  Why: assumption: typing answers is the slow part of clarifying. The web UI shows 3 to 5 mock outcomes of the top readings and the user taps the one they mean.
  Done when: the page renders one card per reading from a fixture plan, a tap writes the choice into the plan, and the result matches the keyboard path.

Next question: Which of the 58 cells does a user actually feel being empty, and does any recorded correction map to one?
Next question: Does the user's real wait for a plan, in seconds per tier, appear anywhere in the ledger, or only the token cost?
