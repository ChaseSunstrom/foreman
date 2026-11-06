# Brainstorm — lens: done-vs-stopped auditor (invented): an adversary that tries to prove the work merely stopped — usage limit, drive cap, no-progress stop, crash, the model saying done

- **Write a stop-cause classifier** — FEATURE — value 5 — effort M — risk low — category: verdict
  Why: gap map lists "done-vs-stopped verdict" as missing; the stop causes are already enumerable (usage limit, crash, DRIVE_MAX, no-progress stop, contract bound, model says done) but nothing records which one ended a session.
  Done when: a fixture session ending in each of the six causes yields `fm goal status` output naming exactly that cause, and only an all-criteria-fresh run yields `finished`.

- **Make "done" a proof the auditor attacks** — FEATURE — value 5 — effort M — risk med — category: audit
  Why: `fm task finish` already demands fresh evidence per criterion, but nothing adversarially asks "what would still be missing if this were only stopped?" Both session arms in earlier Missions closed no scenario on a self-declared done.
  Done when: `fm goal audit` lists, per goal, each MUST item (tests, exam scenarios, docs, site page, pane, surfaces) as proven/unproven with the command and its output, and exits non-zero if any is unproven.

- **Bind the Stop hook to the goal ledger** — FEATURE — value 5 — effort M — risk med — category: stop hook
  Why: gap map "Clauses wired to the Stop hook". Today the drive stops on caps and no-progress even when MUST clauses are unmet, which is exactly a "merely stopped" outcome.
  Done when: with an unmet MUST clause, a Stop at the drive cap writes a `stopped:<cause>` verdict and a Resume-here entry rather than letting the goal read as closed; a test covers each cap.

- **Check the completion checklist as data** — FEATURE — value 4 — effort M — risk low — category: checklist
  Why: the gen-0 MUST list (tests, exam, MASTER, README, CHANGELOG, site, pane, every surface) lives only in prose. Assumption: it can be a per-capability grid like coverage.md.
  Done when: `fm goal check` validates every goal-bound capability against the surface×artifact grid and fails on any empty cell lacking a "not applicable" reason.

- **Detect a premature done by diffing claim against ledger** — FEATURE — value 4 — effort S — risk low — category: claim check
  Why: the model saying "done" is one of the stop causes; the hash-chained ledger can contradict it cheaply.
  Done when: a final message claiming completion while the ledger shows an open criterion or a failing gate is flagged in the next SessionStart context with the specific contradiction.

- **Separate usage-limit stops from give-ups** — FEATURE — value 4 — effort M — risk med — category: resumability
  Why: a usage-limit or crash stop is not a failure of the goal; it must resume without re-deriving the plan. Assumption: the limit event is detectable from the hook or transcript tail.
  Done when: a killed run resumes, `fm goal status` shows `stopped:limit` then `resumed`, and no completed step is repeated.

- **Require the stop verdict before any session summary** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the system's own rule is to report outcomes faithfully; a goal carried over days needs a per-session one-liner saying finished, stopped, or blocked, and why.
  Done when: every Stop writes exactly one verdict line to the goal ledger, and a test fails if a Stop path exits without one.

- **Run a cold "is this really done" reader on goal close** — FEATURE — value 4 — effort M — risk med — category: second opinion
  Why: one reviewer pass per task catches what its own tests missed (Mission lesson). The same applies at the goal level.
  Done when: closing a goal spawns a tool-less reader given only the goal text and the evidence list, and a `not done` from it keeps the goal open with its reason.

- **Wild: Plant a fake finish and see if the auditor catches it** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: wild; the exam already plants defects, so plant a goal that is 90% done with one missing doc or surface and require the auditor to name exactly that gap.
  Done when: a held-out exam kind "G-almost" passes only when the verdict is `stopped` and names the planted gap.

- **Wild: Keep a dead-man's receipt for each goal day** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: wild; written at session start, completed at stop. A receipt that never closed means crash, distinct from a clean stop.
  Done when: killing the process mid-session leaves an open receipt and the next SessionStart reports "crashed, not stopped".

- **Wild: Show a goal's remaining distance as a single number** — FEATURE — value 3 — effort M — risk low — category: pane
  Why: wild; the pane has no goal surface. Count of unproven grid cells over total, with the oldest stale cell shown.
  Done when: the pane and `fm status` show the same fraction, and it reaches 0 only when `fm goal audit` exits zero.

- **Stop the forever loop from calling dry rounds "done"** — FIX — value 4 — effort S — risk low — category: loop
  Why: `fm loop on` stops after 2 dry rounds, which is a stop, not a finish. Assumption: it currently reads as complete.
  Done when: a dry-round stop with unproven goal cells records `stopped:dry` and the next session re-injects the goal.

- **Expire a done verdict when its evidence goes stale** — FEATURE — value 3 — effort M — risk low — category: staleness
  Why: finishing on fresh evidence is today's rule, but a goal closed on Monday can be broken by Wednesday's edit.
  Done when: a commit touching a goal-bound file reopens that cell and flips the goal from `finished` to `needs re-proof`.

Next question: What is the smallest event the harness can observe that distinguishes a usage-limit stop from a crash from a user interrupt, and does it survive in the hook payload?

Next question: Who audits the auditor: which held-out scenarios would show the verdict is wrong in the "finished" direction, not just the "stopped" one?
