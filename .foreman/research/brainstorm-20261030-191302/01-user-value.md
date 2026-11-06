# Brainstorm — lens: user value

- **Answer "what's left?" in one line the user can act on** — FEATURE — value 5 — effort S — risk low — category: goal status
  Why: assumption: after days away the user's first question is distance and next action, not the ledger. The pack has many card and verdict ideas but none that collapses them to one sentence ending in a command (e.g. "3 of 11 rows open; next: fm goal step").
  Done when: `fm goal left` prints exactly one line (open count, next action, a blocker if any) and matches `fm goal step` on 10 fixture goals.

- **Let the user veto a plan row with one word** — FEATURE — value 5 — effort S — risk low — category: plan control
  Why: the pack asks "which parts of a plan can the user veto in one line"; steers are the user's strongest signal (T-2206 and the "steered:" entries show them correcting by hand).
  Done when: `fm goal drop <row> "why"` removes the row from the done gate, logs it on the cut list, and the closing audit doesn't count it as missing.

- **Show the plan as a diff against what the user typed** — FEATURE — value 4 — effort M — risk low — category: plan review
  Why: the user's requests are long, precise and quoted; they will want to see which of their phrases became which rows and which rows are Foreman's additions, before work starts.
  Done when: `fm goal plan` renders user-sourced rows and added rows in two groups, and a phrase in the request with no row is listed under "unmapped".

- **Ask for approval only at the fork, never at the plan** — FEATURE — value 4 — effort M — risk med — category: interruptions
  Why: assumption: the user's standing grants (the "standing grant" for Genesis publishing) show they dislike per-step approvals. Plan only pauses where two rows conflict or an action is outward-facing.
  Done when: a fixture goal with 12 rows runs unattended to the first outward-facing row, then stops with exactly one question.

- **Report cost in the user's currency before work starts** — FEATURE — value 4 — effort M — risk low — category: budget
  Why: the environment shows a hard USD budget ($35). A goal plan with an estimate (dollars, hours, usage-limit windows) lets the user shrink scope up front.
  Done when: `fm goal plan` prints an estimated cost range per row from past tasks, and a finished goal prints actual versus estimate.

- **Make the finish receipt something to forward** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: T-0795 (plain receipts) sits deferred; the user publishes pages, changelogs and release notes themselves, so a one-page "what shipped, what was cut, how it was proven" is their natural output.
  Done when: closing a goal writes `receipt.md` with shipped rows, cut rows, and the command output for each done-when, with no ledger jargon.

- **Name the user's recurring rejection patterns as plan defaults** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: repeated steers and drops (e.g. reviewer-found bugs, "test-first", wrapped-line misreads) repeat across tasks. Mine `fm decide` and steers into default rows ("test-first", "show the stray quote") offered at plan time with a one-key reject.
  Done when: a plan on a new goal lists rows tagged "from your steers" citing the originating decision, and rejecting one stops it from reappearing.

- **Flag the rows only the user can finish** — FEATURE — value 4 — effort S — risk low — category: blockers
  Why: blocked items like T-0325 (needs a sudo install) and T-0352 sit for long; a goal should surface them on day one, not at the end.
  Done when: the plan has a "needs you" section listing rows with a human-only prerequisite, each with the exact command or grant to give.

- **Explain a stopped goal in plain words** — FEATURE — value 3 — effort S — risk low — category: stop cause
  Why: the pack covers verdict classifiers heavily but not the human message: "stopped because the usage limit hit at 14:02; resumes at 19:00; nothing lost".
  Done when: every non-done end writes a one-sentence reason and a resume time or command, shown at the next session start.

- **Wild: Let the user text a goal and get a photo-sized status** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; assumption: goals run for days while the user is away from the terminal, and an ntfy-style one-line status plus a reply-to-steer path suits that.
  Done when: a reply "drop 4" to the pushed status message executes the veto in the ledger.

- **Wild: Offer a "good enough" ending with a price tag** — FEATURE — value 3 — effort M — risk med — category: scope
  Why: wild; the goal is "best-in-class", which never ends. Show the user "stop now: 82% of rows, 40% of the remaining cost avoided" and let them close with the cut list recorded.
  Done when: `fm goal close --early` records the cut rows and the receipt shows the percent shipped.

- **Wild: Generate a "what you would have asked next" shortlist at close** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: wild; the "what earlier brainstorms missed" list shows the user filing follow-ups (T-2202…T-2231) right after a task. Offer 3 predicted follow-ups at close, so the user accepts, rejects or ignores them.
  Done when: closing prints up to 3 candidate follow-ups, and accepted ones become tasks with their origin recorded.

Next question: Which of the user's recurring follow-ups come straight after a close, and how many could the plan have included at the start?
Next question: How much of a goal's delay is waiting on the user (grants, installs, decisions), and can the plan collect those up front?
