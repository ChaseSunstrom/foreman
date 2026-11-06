# Brainstorm — lens: delight

- **Draw a pace band on the status line** — FEATURE — value 3 — effort S — risk low — category: progress
  Why: assumption: the pack has burn-up, finish-date bands and ghost-line ideas, but none puts a planned-versus-actual marker where the user already looks. A multi-day goal needs one glanceable "ahead or behind by N rows" cue that resets honestly at each replan.
  Done when: with a goal of 8 rows, closing a row that was planned for later moves the status-line marker ahead by one, and a replan redraws the planned line with a visible "replanned" flag.

- **Print a lost-work receipt after every crash or compaction** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: the brief says the plan must carry "over days, across crashes and compactions". Earlier ideas cover "where we were" stories, but none quantifies loss. The first resume line says exactly what was lost and recovered, e.g. "Cut at 14:02. Recovered 3 of 3 rows, 2 hunks. Lost: about 40s of uncommitted edits in `parser.py`."
  Done when: killing a session mid-edit and resuming prints one receipt line with the kill time, the recovered counts and the lost items, and a clean resume prints "nothing lost".

- **Show a resume countdown on the status line when a limit stops work** — FEATURE — value 4 — effort S — risk low — category: waiting
  Why: the steers say to wait out real usage limits and resume. Waiting is silent today. A countdown ("resumes 15:40, next: row 6") turns dead air into a promise.
  Done when: with a faked usage-limit pause, the status line shows the resume time and next row, and the line clears itself on resume.

- **Mark good places to stop** — FEATURE — value 3 — effort S — risk low — category: rhythm
  Why: assumption: an open-ended goal never says "you can close the laptop now". At the next green boundary (tests passing, tree clean, bookmark written), Foreman says "good place to stop; tomorrow starts with row 7".
  Done when: after a row closes with a clean tree, one stop suggestion appears at most once per row, and it never appears while the tree is dirty or a test is red.

- **Narrate every replan as a detour sign** — FEATURE — value 4 — effort M — risk low — category: transparency
  Why: plans change over days, and a silent replan is how scope drifts. A one-line sign names what moved, why, and where the route rejoins the old plan: "DETOUR: row 4 replaced (dep removed). Rejoin at row 6." The signs are kept in the goal file and shown at finish.
  Done when: replanning a row writes a sign with a reason and a rejoin row, and `fm goal` lists the signs in order.

- **Keep a wishing well for mid-goal "oh also…" asks** — FEATURE — value 4 — effort M — risk low — category: scope
  Why: the pack has scope-growth ledgers and parked shelves, but framed as warnings. The well is a friendly, countable list of everything the user wished for during the goal, each ending as granted, parked or declined with the reason. At finish it prints "7 wishes: 4 granted, 2 parked, 1 declined".
  Done when: a mid-goal ask lands in the well with an id, and finish lists every wish with an outcome and none left undecided.

- **Print a blooper reel at finish** — FEATURE — value 3 — effort M — risk low — category: finish
  Why: wild. A finished goal has a story of attempts that failed. The reel lists the 3–5 hardest moments from the ledger (most retries, a crash survived, a reverted approach) in one honest, light line each. It builds trust because it shows effort the receipt hides.
  Done when: a goal with at least one reopened row and one crash finishes with a reel naming them with their real counts, and a goal with none prints "no bloopers".

- **Write the product's diary** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Each working day gets one first-person entry from the thing being built, derived only from rows closed that day: "Today I learned to read dates. I still can't count past 999." It must cite closed rows, so it can't invent progress. The entries are bundled at finish and read as a changelog with a voice.
  Done when: each day with a closed row has an entry citing those row ids, and a day with none produces no entry.

- **Publish a weekly build newsletter for goals longer than a week** — FEATURE — value 3 — effort M — risk low — category: long-run
  Why: wild. Goals that "carry the plan over days" lose the user's attention. A two-minute issue (numbered, with "this week / next week / needs you") lands on day 7, 14 and so on, as a file and in the next session's first line. It is built from the ledger with no model call needed.
  Done when: a goal open 8 days has issue 1 on disk with closed rows, open rows and user-only items, and issue 2 appears only after day 14.

- **Show a fortune from the ledger at every stop** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A stop currently ends in a bookmark. Add one true, specific, mildly surprising fact computed from the day's data: "Row 3 passed first try; row 5 took four." Every number is derived from the ledger, never made up, which keeps it honest.
  Done when: two fortunes in a row never repeat a template, each embeds a number that matches the ledger, and an empty day prints none.

- **Fill the goal cockpit in the terminal with smooth motion** — FEATURE — value 3 — effort M — risk med — category: terminal UI
  Why: the web UI has goal-page ideas, but the user lives in the terminal. A full-screen `fm goal` view lets the user walk rows with j/k, press Enter to see the row's evidence, and watch a row fill in when it closes. It respects NO_COLOR and a narrow-terminal fallback.
  Done when: in a 40-column terminal the cockpit renders without wrapping, Enter on a closed row shows its evidence line, and with NO_COLOR set the output has no escape codes.

- **Reveal the finish in the order a newcomer meets it** — FEATURE — value 3 — effort M — risk low — category: finish
  Why: assumption: a finish list ordered by task id says nothing to someone opening the product for the first time. Order the receipt as the first-run path (install, first command, first success, first surprise), with each step carrying the proof that backs it.
  Done when: the finish card lists first-run steps in order, each linked to a closed row and its evidence, and a row with no user-visible step is listed under "plumbing".

Next question: Which delight moments in the finish flow would the user turn off after a week, and does Foreman learn that from their behaviour, or wait to be told?
Next question: If a goal lasts a month and the user is only present for twenty minutes a day, which single line of output in those twenty minutes carries the most trust, and is that line backed by something Foreman didn't write?
