# Brainstorm — lens: user value

- **Track every request to its outcome, and flag asks closed unmet** — FEATURE — value 5 — effort M — risk low — category: request ledger
  Why: The user's words show the same asks coming back ("redo", "recreated with interpretation", "dropped … deferred by decision"). Nothing ties a request to whether it was actually met.
  Done when: `fm status` lists each user request with its state, and a task closed without satisfying its request's wording shows as "open" with the unmet phrase quoted.

- **Pick the reading the user chose last time, and say so** — FEATURE — value 5 — effort S — risk low — category: ambiguity without asking
  Why: The user said "don't ask me for anything either … just go". When a request has two readings, Foreman should follow the reading the user picked for the same kind of request before, and state which one it took.
  Done when: For a request with two readings and a prior choice on record, the run's first line names the chosen reading and the prior task it matched; no question is asked.

- **Quote the user's exact words beside each acceptance check at close** — CLEAN — value 4 — effort S — risk low — category: close receipt
  Why: Several user corrections were about what was meant versus what was built. Putting their wording next to the check that covers it makes a mismatch visible at close.
  Done when: The close receipt shows each user phrase from the request paired with the check that proves it, and a phrase with no check is marked "uncovered".

- **Show spend in dollars and days of budget left, not tokens** — FEATURE — value 4 — effort S — risk low — category: budget clarity
  Why: The session carries a USD budget ($17.5 remaining), and the user's main worry is usage. Token counts don't answer "can I afford this queue?".
  Done when: `fm status` prints "$X left, about N days at this week's pace" and a queue preview prints its expected dollar cost before it starts.

- **Write each close as what the user can now do** — CLEAN — value 3 — effort S — risk low — category: close wording
  Why: Close notes describe the diff ("added a parser branch"). The user acts on capability, so the receipt should state the new ability first.
  Done when: Every closed task's receipt opens with a sentence beginning "You can now …" or "Still can't: …", checked by a test on three sample closes.

- **Print a "what this will touch" card before the first write in a project** — FEATURE — value 4 — effort S — risk low — category: trust at first run
  Why: assumption: a user new to a project has no idea what Foreman will write, so a short card of paths and commands builds trust before the first edit.
  Done when: The first write in a project with no prior approval shows a card listing the paths and gate commands, and the card is written to the journal.

- **Show what each deferred item costs to wait** — FEATURE — value 3 — effort S — risk low — category: deferral trade-off
  Why: The user deferred items to the weekly reset, and deferral has a cost (work sits, reviews go stale). Showing the cost makes the deferral choice informed.
  Done when: `fm task defer` prints the wait in hours and the open dependents it holds up, and a test covers a deferral with two dependents.

- **Undo only the part the user objected to, not the whole task** — FEATURE — value 3 — effort M — risk med — category: targeted revert
  Why: The user often pushes back on one piece ("fm quiet … does nothing"). Reverting the whole task throws away the parts they liked.
  Done when: Given a task and one file or hunk, `fm task revert --hunk` restores that hunk only, and the gate still passes on the result.

- **Surprise me: run the best small backlog item under a spend cap** — FEATURE — value 4 — effort M — risk med — category: one-key progress
  Why: The user wants "any and ALL ideas implemented" and no permission prompts. A single command that takes the highest-value small item and runs it within a cap matches that.
  Done when: `fm surprise --cap 2` picks one S-effort item from the backlog, runs it through the gate, stops at the cap, and prints the receipt.

- **Wild: a hands-off window the guard enforces** — FEATURE — value 4 — effort M — risk med — category: time-boxed trust
  Why: assumption: the user wants to leave Foreman running and sleep. A declared window ("for two hours, touch only tests and docs") that the guard enforces would let them stop watching.
  Done when: With the window set, a write outside tests and docs is refused by the hook within the window, and the refusal appears in the morning receipt.

- **Wild: a sealed prediction of the user's next request, opened next week** — FEATURE — value 2 — effort S — risk low — category: anticipation
  Why: assumption: the user's requests follow a visible pattern (the "Round 3" and "recursive" asks recur). Foreman writes its guess at the next ask and scores it a week later, which shows how well it knows the user.
  Done when: Each week a dated guess is saved, and the next week's note shows the guess beside the real request and a match score.

- **Wild: a weekly "what you got for your budget" letter in dollars and outcomes** — FEATURE — value 4 — effort S — risk low — category: value report
  Why: assumption: the user will judge whether the spend was worth it by outcomes, not activity. A short letter listing dollars spent against requests met answers that directly.
  Done when: `fm week` prints dollars spent, requests closed, and requests still open from the ledger, and matches the totals in the journal for a test week.
