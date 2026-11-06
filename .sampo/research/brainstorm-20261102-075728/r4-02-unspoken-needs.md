# Brainstorm — lens: unspoken needs

Two earlier questions my lens can answer:
- **Which jobs need to run on time:** settled bets and the nightly digest. Doctor repairs and exam refreshes can wait, so catch-up should run in that order.
- **A gauge with no input the user could falsify by hand:** the Brier and held-rate numbers. Every outcome behind them is graded by Foreman. The cheapest outside check is the user's own `git revert` of a Foreman-landed commit, counted as a miss.

- **Cap the tower's self-improvement share** — FEATURE — value 4 — effort S — risk low — category: focus
  Why: the open queue and nearly every recent commit are Foreman internals (T-2598 to T-2611), and the standing rule says the tower advances itself. Assumption: the user wants their own goals to get a guaranteed share. A ratio steer (for example, at most 30% of drive hours on Foreman's own tasks) would be checked by `fm next`.
  Done when: with a 30% cap set and self-filed work already above it, `fm next` offers only goal work, and `fm doctor` prints the measured ratio.

- **Detect hunk ping-pong across plan rows** — FEATURE — value 4 — effort M — risk low — category: drift
  Why: assumption. A multi-day plan can have row 7 quietly undo row 3, and the oracle still passes. Existing thrash breakers work at plan level, not hunk level.
  Done when: a fixture where two rows rewrite the same hunk back and forth makes `fm goal` stop with "rows 3 and 7 conflict on file:line".

- **Refuse to plan from a stale map** — FIX — value 3 — effort S — risk low — category: planning
  Why: the pack itself says the map is "as of an older HEAD". Planning from it hides rows and invents others.
  Done when: planning with a map more than N commits behind HEAD triggers a map refresh first, or is refused with the distance named.

- **Keep an adjective dictionary for "best-in-class"** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the request is "best-in-class", "complete" and "knows when it's done". Each such word means something specific to this user. Confirm once what it means (for example "best-in-class" = the three rival tools' features, plus latency under a bound). Store that and reuse it on later goals.
  Done when: a second goal containing "best-in-class" reuses the stored definition and shows it as rows, with no question asked.

- **Say what a stop did not complete** — FEATURE — value 5 — effort S — risk low — category: honesty
  Why: the goal is "done rather than merely stopped". Every non-done exit should print a typed "unfinished" list of the rows, probes and steers still open, not just a reason code.
  Done when: killing a goal mid-way prints an unfinished list that matches the ledger row for row.

- **Reconcile the unspoken "who can raise this cap"** — FEATURE — value 3 — effort S — risk low — category: blockers
  Why: a steer says to wait out limits and ask once if only the user can raise a cap. The dollar budget (this child shows $0/$100) is such a cap. Assumption: caps stop work silently today.
  Done when: hitting a spend cap writes one `fm ask` naming the cap, its current value, who can change it, and the rows still runnable without it.

- **Weight rows by the user's attention** — FEATURE — value 3 — effort M — risk med — category: prioritisation
  Why: assumption. Which files the user edits by hand, and which reports they open, reveals what they care about. Use that locally and opt-in to order equal-value rows.
  Done when: with the opt-in on, two rows of equal value are ordered by the user's recent hand-edit paths, and `fm why` says so.

- **Give a goal's final report a read-time budget** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption. The user reads on return after a gap, and the final report already collects costly decisions. Cap it at about 90 seconds of reading, spilling detail into linked files ranked by reversal cost.
  Done when: a report from a 40-row goal stays under the word cap, and every dropped detail is reachable by one path.

- **Rehearse "done" on a fresh clone before saying it** — FIX — value 5 — effort M — risk low — category: done-detection
  Why: the recent T-2606 (criteria matching no test) and the vacuous-proof history show a green oracle can pass on the working copy only. A clean clone with no ignored files and no local state is the cheapest outside witness.
  Done when: a goal whose oracle passes only because of an untracked file is refused at finish with that file named.

- **Wild: Annotate a replay into steers** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: wild. The user watches an overnight run at 20x, pauses at a frame and types "no, not that", and the pause point plus text becomes a steer with its check attached. It turns reviewing into steering without the user having to articulate a rule.
  Done when: annotating one frame of a recorded run creates a stored steer that names the commit and row.

- **Wild: Write the user's regret letter first** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. Before the plan is accepted, a tool-less child that has seen only the goal and steers writes one paragraph from the user, a week later, about what they wish had been asked. Each regret becomes a candidate row or a question, checked against what's already built.
  Done when: a vague goal fixture gets at least one regret-derived row that a blind reader rates as non-obvious.

- **Wild: Leave an "if I vanish" file per goal** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: wild. The user may disappear for weeks, and the pack's questions about long gaps show nobody has designed that case. Write a plain-text file with the next three actions, what is safe to leave running, and what to cancel. A cold child with no history must be able to follow it.
  Done when: a cold child given only that file and the repo continues the goal at the right row.

- **Print which rows the user's steers have never constrained** — CLEAN — value 2 — effort S — risk low — category: steers
  Why: 40-plus steers exist, and some have never bound a single decision. Showing which rows or tasks each steer touched makes dead steers visible.
  Done when: `fm decide --check` lists each steer with its last-bound date, and the never-bound ones are flagged.

Next question: Which of the user's current steers would they now phrase differently, and how would Foreman notice?
Next question: When a goal's first row has no probe the user could run by hand, what does the user see to believe the goal is progressing at all?
