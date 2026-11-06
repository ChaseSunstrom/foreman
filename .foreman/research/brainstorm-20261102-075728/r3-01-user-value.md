# Brainstorm — lens: user value

- **Quote the finish in your sittings** — FEATURE — value 4 — effort S — risk low — category: estimates
  Why: assumption: the user works in bursts with long gaps, so a date band in days misleads. Existing ideas cover date bands, not sitting counts.
  Done when: against a fixture session history, `fm goal status` prints "about N sittings (median M min each)", and N matches a hand computation.

- **Record my acceptance walk as the oracle** — FEATURE — value 5 — effort M — risk med — category: done-detection
  Why: assumption: the user's own first manual try of the finished thing is the truest acceptance test, and nothing converts it into a permanent probe. Pack ideas cover a stranger test and a try-this-first card, but they are generated, not the user's.
  Done when: `fm goal accept --record` captures the user's commands and exit codes, a later re-run replays them, and breaking the product turns the replay red.

- **Review the planner's doubts, not the whole plan** — FEATURE — value 4 — effort S — risk low — category: attention
  Why: the user's steers show repeated effort policing Foreman. Plan review should cost minutes. Assumption: rows carry a confidence from grounding and backtest class.
  Done when: the plan-accept card lists only rows below a confidence floor, with an "everything else was auto-accepted, N rows" line, and the floor is a setting.

- **Open a 14-day warranty after finish** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: "done versus merely stopped" ends at the verdict, but the user's real worry is breakage found afterwards. Existing soak and reopen-calibration ideas are internal, not a user-facing promise.
  Done when: `fm warranty "<what broke>"` maps to the closest finished rows, reopens them as first in the queue, and the finish receipt shows "warranty open until <date>".

- **Make the finished README the finish oracle** — FEATURE — value 4 — effort M — risk med — category: done-detection
  Why: the pack has "write the press release first" and "smoke-run the docs' commands" separately. Combined: the README's runnable claims become the final gate, so "done" means the documentation is true.
  Done when: a goal cannot close while any fenced command in its README section fails in a clean clone, and a planted false claim blocks the close.

- **Shape the spend to the usage window** — PERFORMANCE — value 3 — effort M — risk low — category: cost
  Why: there are steers to wait out limits and not drop work. Nothing orders rows so expensive ones run right after a window reset and cheap ones run during the user's live use.
  Done when: in a replayed week, expensive rows start within an hour of a reset at least 80% of the time, with no extra limit stalls versus FIFO.

- **Flag finished rows nobody used in 30 days** — FEATURE — value 3 — effort M — risk med — category: post-finish value
  Why: assumption: part of a "best-in-class" plan is never touched by the user. The pack has soak tests and a keep-or-leave check-in, but nothing tests whether the user's own usage reaches each row.
  Done when: a day-30 card lists rows with no hit in shell history, the CLI event log or coverage, each with a keep/delete choice, and deleting one removes its code and tests in a gated change.

- **Intake in the user's language** — FEATURE — value 2 — effort S — risk low — category: intake
  Why: assumption: goals and steers may be written in another language or in mixed language, and the pack never tests that. A paraphrase-stable tier check would catch it.
  Done when: the same goal in two languages yields plans whose row sets overlap at least 80%, and rows echo the user's own words.

- **Wild: let a vague goal marinate overnight** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. The vaguest goals get planned from the least information. Waiting 24 hours lets the user's edits, searches and commits sharpen the plan, and the tick already exists.
  Done when: a goal marked "marinate" files no plan until the next tick, then produces a plan citing at least one repo or ledger signal that arrived in between.

- **Wild: compost abandoned goals** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: wild. A parked or dropped goal wastes its good parts. Assumption: some of its tests, helpers and research notes would be reused if surfaced.
  Done when: `fm goal park` writes a compost list of reusable files with one-line reasons, and a later goal's plan cites an entry as prior art.

- **Wild: the goal's price tag in the user's attention** — FEATURE — value 4 — effort S — risk low — category: honest cost
  Why: wild. The user keeps adding meters, so the cost they feel is attention, not tokens. A single "you were asked N times, read M lines, waited K minutes" line would be the number they trust.
  Done when: every finish receipt prints the three attention counts, computed from ledgers and checked against a fixture session.

- **Wild: ask the goal "stop now?" and get a priced answer** — FEATURE — value 4 — effort S — risk low — category: stopping
  Why: wild. At any point the user can ask, and the answer is what works today, what is unproven, what the next day buys and what quitting loses. The pack has a stop-now receipt idea, but not as an on-demand price comparison.
  Done when: `fm goal stop?` prints those four items in under 10 lines and agrees with the finish verdict logic on a fixture.

Next question: Which of these value claims (sittings, attention minutes, warranty) can the user verify with a stopwatch or their own git log, without trusting Foreman's ledgers?
Next question: What does the user do in the first 60 seconds after a goal says "done", and does any idea here shorten that check?
