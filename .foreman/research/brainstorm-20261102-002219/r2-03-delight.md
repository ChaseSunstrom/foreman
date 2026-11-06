# Brainstorm — lens: delight

Answering two earlier questions from the delight lens: the output the user only misses once it has cost a task is the "stopped, not done" reason, which is silent today. The forecast surface the user acts on rather than reads is the one-word yes card, so cells should be judged by what happens after the card.

- **Stamp the passport on a real first fire** — FEATURE — value 4 — effort M — risk low — category: coverage, web UI
  Why: assumption: a cell filled by prose feels like paperwork, whereas one that fired for real feels earned. The pack's 58 empty cells and the steer that every capability be called by a real session path point the same way. A cell gets a dated stamp, with the task id and session path, the first time that path actually runs. The web UI grid shows stamped and unstamped cells like a stamp book.
  Done when: running a session that exercises a cited path flips exactly that cell from "written" to "stamped" with a date, and a unit test pins this.

- **Ring a topping-out when the last must-row closes** — FEATURE — value 4 — effort S — risk low — category: goal, ceremony
  Why: wild. Goals carry must, should and could tiers in earlier ideas, but nothing marks the moment the structure is complete. Foreman prints one "topped out" card with days, crashes and compactions survived. It then asks one question: continue with the stretch rows or hand over.
  Done when: closing the last must row in a fixture goal prints the card once, never twice after a resume, and records the choice.

- **Hand over a punch list at 90%** — FEATURE — value 4 — effort M — risk low — category: goal, finish
  Why: assumption: the last 10% of a goal is where "merely stopped" hides. At 90% Foreman collects every small leftover (a TODO it added, an unproven row, a doc number) into one list. Each item can be closed with a single keystroke or waived with a reason.
  Done when: a fixture goal at 90% shows a numbered list, and closing or waiving every item is what lets the finish verdict flip.

- **Seal a hope at goal start, read it back at finish** — FEATURE — value 3 — effort S — risk low — category: goal, memory
  Why: wild. The user types one optional sentence ("I want to stop thinking about X"). It is stored untouched. At finish it is read back beside the finish verdict, with a plain note on whether the built thing meets it. This catches intent the DONE-WHEN missed.
  Done when: finish output quotes the stored sentence verbatim, and goals without one print nothing.

- **Tag every day-end as a git ref** — FEATURE — value 3 — effort S — risk low — category: goal, git
  Why: assumption: multi-day goals leave no walkable trail. At each stop, write `refs/fm/goal/<name>/day-N` and list the refs in the goal page. The user can then check out "Tuesday night".
  Done when: after two simulated stop/resume cycles, `git rev-parse` resolves both refs and the goal page lists them.

- **Print a blueprint with lit rooms** — FEATURE — value 3 — effort M — risk low — category: terminal UI
  Why: wild. Terminal-first users have no picture of "the finished version". `fm goal blueprint` draws an ASCII floor plan where each plan row is a room: dark if unbuilt, lit if proven, dim if claimed. It fits narrow terminals and degrades to a plain list under NO_COLOR.
  Done when: golden-file tests at 60 and 120 columns show the right lit and dark rooms for a fixture goal.

- **Keep a foreman's logbook, one line per working day** — FEATURE — value 3 — effort S — risk low — category: narrative
  Why: wild. Postcards and morning notes are single-shot. A cumulative `logbook.md` appends one human-voiced line a day ("Day 3: laid the stop-reason rows, the crash drill held"). The result reads as a shareable story of the goal and is built from the ledger only, so nothing is invented.
  Done when: three simulated days yield three dated lines, and each line cites a ledger entry that exists.

- **Cut a "what got lighter" line on every finish** — FEATURE — value 3 — effort S — risk low — category: lean, receipts
  Why: the lean ratchet and the deletion-for-every-verb steer exist, but a finish only reports growth. A goal's finish line states net lines, verbs and cards removed alongside those added, so that deletion is something to be proud of.
  Done when: finishing a fixture goal that deleted a file prints a negative delta with the file named.

- **Show first-light toasts for cells in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI, motion
  Why: assumption: the Goal page is checked rarely, so progress goes unnoticed. When a stamp lands while the page is open, the cell does one brief fill animation. Reduced-motion users get a static border change, and there is a visible "since you last looked" count.
  Done when: a Playwright check sees the cell class change on a pushed event, and `prefers-reduced-motion` produces no animation.

- **Name every goal and put its codename on every surface** — FEATURE — value 2 — effort S — risk low — category: identity
  Why: assumption: "goal #4" is a number, while a codename ("lantern") reads in the status line, branch names, the logbook and the page title, so a user can say "how's lantern?". Names are derived from the request's own nouns, never invented text.
  Done when: creating a goal yields a stable slug visible in `fm status` and the web UI title, and a collision gets a numeric suffix.

- **Let the user veto a plan row with one reaction** — FEATURE — value 4 — effort M — risk med — category: planning UX
  Why: the user steered on "re-scope" and on dropping mistaken captures. A one-line "strike" on any row, with an optional "why", removes the row, records the reason in the scope ledger and refuses to re-add it silently later.
  Done when: striking a row removes it from the contents, and a later decomposition run does not re-add it without a printed reason.

- **Grant a "quiet finish" mode** — FEATURE — value 2 — effort S — risk low — category: restraint
  Why: wild. For small goals, a finish prints exactly one line plus a pointer to the full receipt. Ceremony scales with goal size and the user can tell which was which.
  Done when: an S-sized fixture goal finishes with at most two lines of output and the receipt file still exists.

Next question: Which of the delight surfaces (stamps, topping-out, punch list) does the user actually open, and can the lean ledger count that before more are added?
Next question: When the user stops a goal on purpose, what do they expect to see on resume, and does that match what the first three lines say today?
