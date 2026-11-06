# Brainstorm — lens: the recurring miss (invented): each failure, friction or user correction that recurs becomes a fix with a test, without being asked

- **Fingerprint the miss before counting it** — FEATURE — value 5 — effort M — risk low — category: recurrence
  Why: T-2272 counts failure signatures across 3+ tasks, but the "asked" stream shows the same miss in different words (T-2285 and T-2288 are both "the gate missed a shape"). Counting by text undercounts. Assumption: signatures today are mostly literal or command-normalised.
  Done when: a fixture of 5 corrections phrased differently for one gap clusters into one signature, and `fm doctor` shows a count of 5 for it.

- **Make every FIX task carry a "would have caught" test** — FIX — value 5 — effort M — risk low — category: regression
  Why: T-2285, T-2289 and T-2326 were each a user ask the earlier tooling had no test for. Nothing requires the fix's test to be derived from the miss itself.
  Done when: `fm task finish` on a FIX refuses unless a test is recorded that fails on the task's start commit and passes now, with both runs shown.

- **Sweep the sibling class when a miss closes** — FEATURE — value 5 — effort M — risk med — category: generalise
  Why: T-2285 (plan gate misses a flag-first option) is one of a class: every parser in plan-gate/fm task prose that counts "text after a marker". Assumption: sibling parsers share a shape greppable by `fm graph`.
  Done when: closing a FIX lists the other call sites that share the pattern, and each gets either a probe case added or a recorded "checked, fine".

- **Score "stayed gone" at 7 and 30 days** — FEATURE — value 4 — effort S — risk low — category: outcomes
  Why: the fix loop closes on the test passing, but the steers say the user wants the miss to stay fixed. Dropped items like "same failure as T-2283" show a fix that didn't hold slipped through dedupe.
  Done when: each closed FIX gets two dated rows, and `fm doctor` prints held / returned counts with the returned ones linked to the original task.

- **Reopen by signature, not by new task** — FIX — value 4 — effort S — risk low — category: dedupe
  Why: "Baseline red" was dropped because dedupe by command text missed an interpreter-path variant. Same miss, new ticket, no history.
  Done when: a recurrence with a different surface form attaches to the old task as a reopen entry and the fix count on that task rises.

- **Treat a repeated steer as a failed check** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: steers are stored with `fm decide --check`, but 2026-10-31 #1 to #3 repeat the "don't stop for budget" theme from the 10-30 set. Assumption: repeats show a check that was missing or too weak.
  Done when: a new steer matching an existing one by cold-read similarity marks the old rule "weak", opens a task to strengthen its check, and `fm doctor` lists it.

- **Count friction as a signal source** — FEATURE — value 4 — effort M — risk med — category: friction
  Why: the loop learns from failures and tasks, but the user's costliest misses are corrections in the "asked" stream, such as the user having to say "also make sure the website is updated, it doesn't look like it has been". That was friction with no failing command.
  Done when: a correction that follows a "done" within the same session is logged as a miss with the done claim attached, and 3 similar ones open a FIX.

- **Rank misses by user cost, not count** — FEATURE — value 3 — effort S — risk low — category: prioritise
  Why: one miss that cost the user a reopened ship outweighs five harmless warnings, yet the threshold is a flat 3+.
  Done when: each signature has a cost (reopens, user messages, minutes) and the queue is ordered by it, with the ordering shown in `fm triggers`.

- **Quarantine a fix that needed a fix** — SECURITY — value 4 — effort M — risk low — category: self-repair
  Why: T-2283 was "fixed" and then reappeared as a Baseline red through the scratch run's path. Self-repair classes with fix-of-fix chains shouldn't keep running unattended.
  Done when: a second FIX naming the same signature within 14 days lowers that class's autonomy and `fm why` states it.

- **Wild: Add a "that again" key** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: wild. The user typing "again" or "same as before" should resolve to the last matching miss and open its reopen automatically, with no description required.
  Done when: `fm again` with no argument finds the most recent closed FIX whose signature fits the latest failure, and reopens it with the new evidence.

- **Wild: Mutation night for the repairer** — SECURITY — value 4 — effort L — risk med — category: trust
  Why: wild. Nightly, plant a known past miss into a copy (a reverted fix) and time how long the loop takes to notice and file it.
  Done when: a planted regression yields a FIX task within a set number of hours, and a miss is reported when it doesn't.

- **Wild: Replay last week's corrections against today's build** — FEATURE — value 4 — effort L — risk low — category: regression
  Why: wild. Corrections already live in the "asked" stream, so they could become a standing corpus that every ship replays.
  Done when: `fm ship` runs the corpus and fails if any correction that was once fixed reproduces.

- **Wild: A weekly "what Foreman got wrong" page** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: wild. The site already publishes Genesis data daily, so the miss ledger could be published beside it with each miss, its fix and whether it held.
  Done when: the site shows a page generated from the ledger, refreshed by the daily genesis publish.

Next question: Which corrections did the user make that left no trace in the task ledger, so no signature could ever have seen them?
Next question: When a fix holds on the bench but the same miss returns in a real session, which signal does Foreman trust, and who decides?
