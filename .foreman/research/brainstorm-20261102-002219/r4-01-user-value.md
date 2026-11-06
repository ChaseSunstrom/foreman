# Brainstorm — lens: user value

- **Preview a vague goal without creating state** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: assumption: a goal made while debugging pollutes state. The pack shows "captured by mistake" items already corrupting the user model (T-2547, T-2554).
  Done when: `fm goal plan --preview "text"` prints the decomposition and exit code 0, and `fm goal list` is unchanged afterwards.

- **Expire an unconfirmed draft goal** — FIX — value 3 — effort S — risk low — category: reliability
  Why: the dropped ledger holds "first brief" and "second brief" test lines that were captured as real asks. A goal should stay a draft until a second, deliberate action.
  Done when: a draft goal not confirmed within 24h is dropped with reason "never confirmed", and the user model never reads it.

- **Adopt a roadmap file as the plan's contents** — FEATURE — value 4 — effort M — risk med — category: capability
  Why: assumption: users already hold intent in ROADMAP.md, TODO.md or GitHub milestones. Each imported row still needs a grounding line (T-2547 rule).
  Done when: `fm goal import ROADMAP.md` yields rows whose titles and order match the file, each with a grounding line or a "no grounding" mark.

- **Choose interrupt classes at goal start** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the pack's steers say never block on process questions, but only the user knows which interruptions they would want. Offer three defaults: blocker, finish, cost over X.
  Done when: the goal file stores an interrupt policy, and a planted non-listed question is decided and logged rather than raised.

- **Pick today's goal across repos in one line** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: assumption: the user runs several projects and reopens the one they remember. `fm next` is per-project.
  Done when: `fm next --all` prints one ranked line per live goal with the reason, and the top one matches a planted stalled-versus-ready fixture.

- **Redact secrets and paths in a goal handoff page** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the handoff page and the Genesis site publish goal state (steer 2026-10-30: the site follows Genesis). The user's words and local paths can leak.
  Done when: a goal containing a planted token and `~` renders a handoff page with both masked.

- **Write the cells as promises the user can hold Foreman to** — DOCS-style FEATURE — value 4 — effort M — risk low — category: docs
  Why: "coverage must be real" (steer) and the 58 empty cells. Phrase each cell as "if you stop for 3 days, then X happens", not as an internal capability. A cell that can't be phrased this way is a candidate n/a.
  Done when: every filled cell is one line that starts with a user situation, and the lint rejects any that start with a module name.

- **Show why a goal isn't finished, in three lines** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: assumption: "where were we" is the commonest follow-up. Name the blocking row, who owns it (user or machine), and the next action.
  Done when: `fm goal why` on a planted stalled goal names the exact row and owner in at most three lines.

- **Count a user's goal-time in their own minutes** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: assumption: the real cost to the user is attention, not tokens. Log minutes of user presence per goal and per row, and show it beside dollars.
  Done when: a finished goal's receipt shows "you spent N min across K sessions" computed from session timestamps.

- **Wild: Ask the goal a question, answered offline with citations** — FEATURE — value 3 — effort L — risk med — category: privacy
  Why: wild. A local model answers "why is row 5 there?" from the goal file, ledger and git only, citing each source. Nothing leaves the machine.
  Done when: five planted questions each return an answer citing a real ledger or commit line, and none makes a network call.

- **Wild: Generate a 30-second "trailer" of the finished result from proof receipts** — FEATURE — value 3 — effort L — risk med — category: delight
  Why: wild. The `demo/live.svg` style already exists. Replay the proof receipts as a short recording so the user sees what finished means before reading anything.
  Done when: finishing a fixture goal writes an SVG or text recording listing each proven row in order.

- **Wild: Open every session with a one-sentence "while you were gone" spoken aloud locally** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: wild, assumption: the user may be away from the screen (car, phone). It reuses the morning note, spoken with a local TTS and off by default.
  Done when: with the setting on, resume writes one sentence and passes it to a local TTS command; with it off, nothing runs.

- **Wild: Let the user rate each filled cell "would I have noticed?" in one pass** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: wild. The 58 cells were written by Foreman and by children, and the user is the only signal Foreman doesn't author (steer on separate signals). Three keys on one screen, five random cells per run.
  Done when: ratings are stored per cell, and a cell rated "no" twice is flagged as a deletion candidate.

- **Check that a goal verb survives a typo** — FIX — value 2 — effort S — risk low — category: developer experience
  Why: the steered `--by harness` versus `--by-harness` correction shows the user's phrasing differs from the flag spelling. Goal verbs should accept the near-miss and print the canonical form.
  Done when: `fm goal status --by-harnes` runs and prints a "did you mean" line instead of failing.

Next question: Which of the 58 cells does the user ever actually meet in a normal week, and which exist only because the grid has the row?
Next question: What does a user do after a goal ends: start a sequel, forget it, or reopen it, and does anything in the pack record which?
