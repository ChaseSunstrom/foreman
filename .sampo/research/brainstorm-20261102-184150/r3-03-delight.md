# Brainstorm — lens: delight

- **Print the "Left out" slip as a torn-edge receipt** — FEATURE — value 4 — effort S — risk low — category: request receipt
  Why: Mission 1's whole point is "says what it left out"; today that is prose in a Mission file. A small, bounded slip (≤5 lines, perforated top edge, ranked by cost of being wrong) at the end of every request is the thing a user shows someone. Assumption: the terminal and web finish card can render a boxed block.
  Done when: finishing a task whose Mission has an empty grid cell prints a slip of ≤5 lines naming that cell, and a request with nothing omitted prints "Left out: 0 of N cells checked" rather than a blank.

- **Open every Mission page on its interpretation banner and sting cell** — FEATURE — value 4 — effort S — risk low — category: Mission page
  Why: Earlier question: "which cell do they open first?" Users open the one that stings. One line ("I took your request as X, at width Y") plus the highest-sting empty cell above the fold lets them correct the reading in seconds. Assumption: sting can be ranked from the existing demand/failure signals.
  Done when: the rendered Mission page's first 6 lines contain an interpretation sentence and exactly one cell marked as the top left-out item.

- **Fill a cell with a short settle animation when its brief closes** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: The grid is static state; a cell changing from empty to filled is the one event worth feeling. Motion tied to a real ledger edge (never decorative), reduced-motion and NO_COLOR honoured.
  Done when: closing a brief changes its grid cell's state in the web UI with a ≤400 ms transition, and with `prefers-reduced-motion` it changes instantly (test checks both).

- **Draw a dissent as a two-sided scale that tips on the outcome** — FEATURE — value 4 — effort M — risk low — category: dissent scoring
  Why: Carried gap "dissents scored against outcomes" is invisible as a number. A small balance glyph (dissenter vs. builder) that tips toward whoever the 14-day close survival backed makes the score readable at a glance and gives the dissenter a face. Assumption: the existing close-survival signal is the only input.
  Done when: a settled dissent renders with a tipped scale and a one-line "survived 14 days / reopened on day N" caption, and an unsettled one renders level with "outcome not yet observed".

- **Show Exam readings as a "meter and clock" pair** — FEATURE — value 4 — effort S — risk low — category: Exam display
  Why: Every brief's Exam must now name an outcome measure and a live-state reading. Showing the value beside its age (and a plain cause when it couldn't be taken) turns two contract lines into one glanceable pair, and stops "stale" reading as "passing".
  Done when: an Exam card shows `value · read Nm ago`, and a reading that failed shows "couldn't read: <reason>" in the same slot, not blank.

- **Write designed empty, stale and "can't read" states for the Mission grid** — FEATURE — value 3 — effort S — risk low — category: states
  Why: The first thing a new Mission produces is an empty or partly-unmeasured grid. A kind sentence plus the one command that fills each state beats a bare dash.
  Done when: each of the three states has a distinct message naming a command, and a golden render test covers all three.

- **Add a "since you looked" ribbon at the top of Mission pages** — FEATURE — value 3 — effort M — risk low — category: continuity
  Why: Unattended Missions finish while the user is away; the ribbon ("2 cells filled, 1 dissent settled, 1 reading went stale") answers the first question on return. Assumption: last-viewed time can be kept locally.
  Done when: reopening a Mission page after a ledger change shows a ribbon listing exactly the changes since the stored view time, and none when nothing changed.

- **Name each canary hit with the user's own sentence beside it** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: Carried gap "canaries near the idea". Showing the three nearest existing things next to a "not built" claim, with the user's quoted words, makes the grounding feel like being listened to rather than audited.
  Done when: a "not built" line prints ≥1 nearest existing item and the quoted user phrase that prompted the idea, or "no near match" explicitly.

- **Let a settled bet show a one-line result in the feed** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: Dissents and forecasts settling are small wins/losses that currently vanish. A dated line ("dissent on M1-B: right, close reopened day 9") gives the system a pulse and teaches which lens earns trust.
  Done when: settling a prediction or dissent appends one line to the feed within the same sweep, shown in `fm next` or the pane.

- **Wild: Tear the left-out slip off and keep it** — FEATURE — value 3 — effort M — risk low — category: keepsake
  Why: wild. A one-key action that saves the slip as a dated small file (or printable one-pager) in a "kept" shelf; kept slips become a personal list of the gaps the user cared about, and feed which cells to fill next. Assumption: the user will keep things that mattered.
  Done when: pressing the keep action writes the slip to a kept folder, and the next Mission's pack lists kept slips as aged seeds.

- **Wild: Render the grid as a night-sky map where empty cells are dark** — FEATURE — value 3 — effort M — risk low — category: visualisation
  Why: wild. Filled cells are stars, n/a cells faint, empty cells dark patches; at a glance you see where the thinking didn't reach, and the sky brightens as Missions close. Must keep a data-table twin for accessibility.
  Done when: the web page shows the sky view with a toggle to a table, each star has an accessible label, and a Mission with all cells filled renders no dark patch.

- **Wild: Give the hard hat a lamp that dims as unexamined cells shrink** — FEATURE — value 2 — effort S — risk low — category: ambient
  Why: wild. The logo is already a character; a small lamp on the hat showing "how much of this request I haven't looked at" turns coverage into ambient feeling in the pane header and tray. Honest: it shows unknown when no grid exists.
  Done when: the pane header lamp brightness is a function of the empty-cell fraction of the open Mission, and shows a distinct "no grid" glyph otherwise.

- **Wild: Blind-spot pop quiz at Mission close** — FEATURE — value 3 — effort M — risk low — category: playful check
  Why: wild. At close, Foreman asks the user to guess one hole in its own thinking before revealing the left-out slip; guesses that match an empty cell score a point, guesses that don't are filed as candidate cells. It makes the user's intuition a data source.
  Done when: closing a Mission offers one optional guess prompt, and a miss lands as a candidate cell in the next pack.

- **Chime once when a long unattended Mission lands with a first** — FEATURE — value 2 — effort S — risk low — category: polish
  Why: Quiet success is easy to miss; a single soft bell plus a "first of its kind" badge (first dissent scored, first live reading) marks milestones without nagging. Off by default under `fm quiet`.
  Done when: a Mission whose close records a first-of-kind event emits one bell and badge, and none on routine closes.

Next question: Which of these moments does the user actually see (terminal finish, pane, web page, site), and is there evidence they look at any surface between Missions?
Next question: Do delight touches that fire on ledger edges survive a read-only or headless run, or do they silently vanish where the unattended work happens?
