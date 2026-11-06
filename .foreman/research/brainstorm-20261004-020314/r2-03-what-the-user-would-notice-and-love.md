# Brainstorm — lens: what the user would notice and love

- **Show a one-line "closed because" receipt per criterion** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: user keeps asking for evidence that is visible (proof pack, receipts); the pane has cards for everything but a closing moment. Assumption: the ledger already links each criterion to the run that proved it.
  Done when: closing a task prints one line per criterion ("AC2 ← pytest -k parse, red→green, 0.8s") and the pane shows the same list.

- **Add `fm since` for a returning user** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: user runs drives, night shift and background work; friction shows turns that end to wait. Assumption: events.jsonl and the ledger carry enough to summarize. Distinct from the "morning report" idea: it works from any gap (an hour or a week), is pull-based, and groups by task, not by time.
  Done when: after a recorded drive, `fm since 2h` lists finished tasks, refusals, spend and the one decision awaiting the user, in ≤ 15 lines.

- **Make the pane show a "calm/needs-you" light** — FEATURE — value 4 — effort S — risk low — category: pane
  Why: user wants the drive to run unattended and be pinged "only when needed". One glanceable state (working / waiting on background / needs you) beats reading cards. Assumption: the view model can derive these three states from drive and park data.
  Done when: fmwatch emits a `attention` field with three values, and a UI test renders each.

- **Offer "did you mean the thing you already have?" at the pane level** — FEATURE — value 3 — effort S — risk low — category: nudges
  Why: capture-time covered-by-existing note shipped for the CLI; the user is unlikely to read CLI output mid-drive. Done when: a request that matches an existing command shows the note as a dismissible pane card and dismissal is recorded so it does not recur.

- **Write the diff tour as a self-contained HTML page** — FEATURE — value 4 — effort M — risk low — category: handoff
  Why: `fm tour` and `fm proof` exist as text. A single local file with the files in dependency order, red→green runs and lens findings inline is what a person shows someone. Assumption: the tour data is structured enough to render without new collection.
  Done when: `fm tour ID --html` writes one file under a size cap with no external fetches (grep for `http` in src/href is empty) and it opens correctly.

- **Add "ask before the big spend" with a one-keystroke default** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: caps exist but only refuse; the user said savings should prevent over-use, not capability. A prompt "this review fan-out ≈ $1.80, go?" with a remembered default per command keeps capability and avoids surprise. Done when: an estimate above a threshold asks once, and "always" is stored and honored next time.

- **Wild: Give each finished task a replayable 60-second "show me" cast** — FEATURE — value 4 — effort L — risk med — category: handoff
  Why: wild. Combines proof pack, tour and the pane card stream into a timed replay of the task from brief to close, generated from the ledger, not a screen recording.
  Done when: `fm show ID` replays events with timing compressed to ≤ 60 s in the terminal, and `--html` exports it.

- **Wild: Let Foreman keep a "taste file" the user can read and edit** — FEATURE — value 5 — effort M — risk med — category: personalization
  Why: wild. Vetoes, standing answers, accepted/rejected ideas, tier habits are scattered across the ledger; one plain-text file of "what I've learned about you", where each line cites its origin and deleting a line unlearns it, is both trust-building and the shared input for the bench judge and the shortlist.
  Done when: `fm taste` lists entries with source ids, removing a line stops the associated PreToolUse note, and the bench judge reads the same file.

- **Wild: Add a "pane weather" for the project's health** — FEATURE — value 3 — effort M — risk low — category: pane
  Why: wild. A small ambient glyph in the pane (gate pass streak, flake rate, open assumptions, research debt) that changes gradually, so a user senses drift without opening a report.
  Done when: the pane renders a glyph from a pure function of the last N gate/audit results, and a test pins three inputs to three outputs.

- **Make `fm` answer natural-language asks with the nearest command and its output** — FEATURE — value 4 — effort M — risk low — category: usability
  Why: the user says "ask Foreman anything" in many forms; typo suggestions exist as an idea, but a `fm ?` that maps "what did I decide about X" to `fm recall`/`decide` and runs the read-only one removes the need to learn verbs. Assumption: a keyword route table (like routing.json) suffices, no model call.
  Done when: `fm ? "what did we decide about the guard"` prints the matching decisions and names the command it ran; unknown questions list the three nearest verbs.

- **Wild: Let the user "pin" a moment in a turn and get it turned into a bench case** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: wild. The user's correction already becomes a veto; a one-word `fm pin good|bad` on the last turn captures a positive example too, feeding the regression court and bench with the user's own taste, not only their complaints.
  Done when: `fm pin bad "reason"` writes a bench case with the turn's inputs, and `fm bench` lists and runs it.
