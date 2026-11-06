# Brainstorm — lens: delight

- **Open each goal with an interruption contract** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: assumption: users abandon multi-day goals when they can't tell when Foreman will stop and ask. The steers say "ask nothing mid-run", but nothing shows that promise to the user.
  Done when: `fm goal start` prints at most 4 lines ("I will interrupt you only for: …; never for: …") and each line matches a real config value, checked by a test.

- **Add `fm goal whatif "<situation>"`** — FEATURE — value 4 — effort M — risk med — category: discovery
  Why: assumption: the 58 cells are written for the tower, but a user's real question is "what happens if I close the laptop at row 4?". Matching the phrase to a cell and printing that cell's last probe output turns the grid into an answer.
  Done when: `whatif "session killed mid-row"` names the matching cell id and prints its latest recorded probe output; an unmatched phrase says "no cell covers this" and does not guess.

- **Close Mission 7 with a "try these three" card** — FEATURE — value 4 — effort S — risk low — category: final report
  Why: the final report is where user-only items already land, and 58 filled cells are too many to feel. Three cells with paste-ready probe commands let the user feel the capability in a minute.
  Done when: the report ends with 3 commands. Running each exits 0 and prints something the cell's text promised.

- **Show a cell of the day at session start** — FEATURE — value 3 — effort S — risk low — category: discovery
  Why: assumption: most filled cells describe behaviour the user never finds. One rotating line with a try-it command, under the existing silence ratio and muted after two dismissals, teaches it without a new surface.
  Done when: the line appears at most once per day, never repeats a cell inside 30 days, and respects the one-line cap.

- **Add a break-it-yourself drill** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: kill-and-resume drills exist only as tests. A guided `fm goal drill --play` on a scratch goal lets the user kill the session and watch the resume. That earns trust more than any cell text.
  Done when: the command creates a throwaway goal, tells the user to kill the session, and on restart prints the resume with "your goal was never touched". It leaves nothing in real state.

- **Print a terminal mini-grid strip in `fm status`** — FEATURE — value 3 — effort S — risk low — category: status
  Why: heatmaps are planned for the web UI only. A one-line strip (`▓▓░▓▒…`, with letters for colour-blind use) gives terminal-only users the same glance.
  Done when: `fm status` renders one row per capability from `coverage.md`, with legible glyphs under `NO_COLOR` and a non-TTY pipe.

- **Report what the cheap lanes saved** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: pillar 1 builds on the cheapest capable model, but the user never sees the payoff. Assumption: lane cost per model is already recorded.
  Done when: the finish receipt has one line, "this goal cost $X; an all-strongest-model run would be about $Y". The estimate comes from recorded token counts, not a guess.

- **Give the 58 cells a voice pass** — CLEAN — value 2 — effort S — risk low — category: docs
  Why: 58 cells written by many cheap lanes read as many authors, and the "templated phrase" linter only catches duplicates. A shared 6-line voice guide checked by a read-aloud lint fixes the tone.
  Done when: every cell passes the lint (second person, one verb, no jargon list), and a tool-less child asked to guess the number of authors says "one".

- **Wild: Announce BINGO on a completed column or row of the grid** — FEATURE — value 2 — effort S — risk low — category: playful
  Why: wild. The grid is already rows by columns, so completing a whole stage across surfaces ("every Resume cell filled on every surface") is a natural milestone and costs almost nothing to detect.
  Done when: closing the last cell of a row or column prints one celebration line in `fm status` and on `site/genesis`, once per completion, and not at all under `FOREMAN_QUIET`.

- **Wild: Run a blind resume taste test** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: wild. After a real kill, the user sees two anonymised resume briefings (Foreman's and a plain one) and picks one. That gives a human delight signal Foreman didn't author, which the standing rules prize.
  Done when: `fm goal taste` shows both options with the order randomised, records the pick without the labels, and a report tallies picks.

- **Wild: Dictate a vague goal in the web UI** — FEATURE — value 3 — effort L — risk med — category: input
  Why: wild. People state vague goals aloud better than they type them. Local transcription (nothing sent anywhere) feeds the existing "deck of parts the user can strike out".
  Done when: a mic button in the web UI turns 20 seconds of speech into a text goal using a local engine, with the network disabled, and the goal opens as an editable deck.

- **Wild: Print collectible cell cards on the Genesis site** — FEATURE — value 2 — effort M — risk low — category: playful
  Why: wild. Each filled cell becomes a small SVG card with a name, its stage-by-surface coordinates and a rarity by how often a real session path reached it. The site already carries SVG art, and the cards make the grid shareable.
  Done when: `site/genesis` renders one card per filled cell generated from `coverage.md` and the trace data, with no card for a cell no session has reached.

- **Wild: Add an SVG goal card to hand to a teammate** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild. A local-only card shows the codename, days spent, crashes and compactions survived, and rows with evidence. It matches the demo asset style and uploads nothing.
  Done when: `fm goal card` writes one SVG whose numbers match `fm status`, and it contains no file paths or secrets.

Next question: Which of the 58 cells does a real session path never reach, so a delight output built on it would be seen by nobody?
Next question: What would make the user tell someone else about the goal engine unprompted, and does any current surface produce that moment?
