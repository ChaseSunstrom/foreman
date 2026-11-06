# Brainstorm — lens: simplicity

- **Cap every Mission at one outcome line and one live reading** — CLEAN — value 5 — effort S — risk low — category: simplicity
  Why: The request asks for "an outcome measure and a live-state reading" per Exam. The ideas list already holds roughly a dozen elaborations of those two (cards, provenance blocks, sandboxes, stale verdicts, cold/warm pairs). Assumption: those would be weighed together. Take the two lines as the whole contract; a third field must retire one.
  Done when: a test fails any brief whose Exam has more than two reading fields, and the Exam template has exactly two.

- **Collapse "left out" into one capped list per Mission** — CLEAN — value 5 — effort S — risk low — category: simplicity
  Why: The request says Foreman "says what it left out", and the list holds about thirty variants (receipts, aged seeds, ledgers, slips, git notes, grids). One list of at most five lines, ranked by cost of being wrong, with the flag that shows the rest, meets it.
  Done when: a Mission page renders at most five left-out lines plus an "N more" pointer, and a test fails on a sixth inline line.

- **Score a dissent with one existing bit** — FEATURE — value 4 — effort S — risk low — category: outcomes
  Why: The carried gap is "dissents scored against outcomes". `fm outcomes` already records whether a close survives 14 days (see M-12's kill test), so the score needs no new instrument. Mark each dissent right if the task it opposed was reverted or reopened in that window and wrong otherwise.
  Done when: `fm outcomes --dissents` prints each dissent as right, wrong or unobserved, reading only existing ledgers, with no new record class.

- **Replace the grid with six fixed questions** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: The grid-based coverage idea keeps growing (heat, age, shading, orphan checks, covering arrays). Six questions (who, where, when it fails, what's unsafe, what's slow, what's undocumented) can be answered in a line each and read on a phone. Assumption: the user opens the sting cell first and doesn't scan the full matrix.
  Done when: a Mission page answers all six questions or marks each "n/a: reason", and a cold child can restate the request's coverage from them alone.

- **Make the canary one command with one output line** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: "Canaries near the idea" is a carried gap, and about twenty canary variants are listed. The core is `fm canary "<claim>"`: grep, `fm --help`, and the tombstones. It prints "N hits, nearest: X" and is called by the brief filer.
  Done when: filing a brief containing "not built" runs the canary, and the brief carries its single output line.

- **Retire a field when a field is added** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: Every Mission adds fields to the brief (outcome, live, blind author, parent-differs, provenance). The footprint rises with each. A test counts the template's fields against a ceiling, so a new one forces an old one out.
  Done when: the test fails when the brief template exceeds N fields, and the ceiling is recorded in one place.

- **Delete the Ideas-so-far list from the pack and keep a 100-line digest** — PERFORMANCE — value 4 — effort M — risk med — category: simplicity
  Why: The pack lists well over a thousand idea titles, many near-duplicates, and the lens child has no tools, so every round pays for them in tokens and still repeats. Assumption: a clustered digest loses few distinct ideas.
  Done when: the pack's idea section is at most 100 lines, and a repeat-rate check on the next round's output shows no rise.

- **Default the outcome measure to "the user did not re-ask"** — FEATURE — value 3 — effort S — risk low — category: outcomes
  Why: "What earlier brainstorms missed" holds eight cases where the user had to re-ask. That is a measure Foreman didn't author (steer on outside signals) and needs no per-brief instrument.
  Done when: a brief with no explicit outcome line gets this default, and `fm outcomes` reports re-asks per closed brief.

- **Wild: Argue for doing nothing** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: wild. Each Mission includes a lens child whose only job is to say which requested clause needs no work and why, with a canary line backing it.
  Done when: a Mission page has a "does nothing" paragraph, and at least one clause per Mission is either confirmed or refuted by a command.

- **Wild: Let a cold child delete one section from every Mission page** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: wild. The Mission page is the thing the user reads, and it only grows. A deleter child names the section least needed, and that section moves to an appendix when the user doesn't object.
  Done when: each Mission page is shorter than its predecessor, or states why not.

- **Wild: Hold a "one-page Foreman" Mission** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: wild. A generation where the only brief is deleting something: the verb with no session path, or the largest addition of the previous Mission. This matches the lean steer and the "no session path" standing rule.
  Done when: the net count of verbs, fields and files falls over the Mission, shown by `fm doctor`.

- **Sweep carried gaps into one register with a two-generation expiry** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: The request names three carried gaps; the earlier-questions list shows others that lingered. A gap not closed in two generations is closed with a recorded reason or promoted to a task.
  Done when: `fm genesis check` fails on a carried gap older than two generations without a decision.

**Next question:** Which of the pack's thousand-odd ideas has a session path that calls it today, and what does the ratio say about building more?
**Next question:** If the Exam were reduced to two lines, which past brief would have passed it without doing the work?
