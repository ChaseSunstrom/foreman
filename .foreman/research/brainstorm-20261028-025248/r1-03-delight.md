# Brainstorm — lens: delight

- **Name the elegant part of each diff** — FEATURE — value 3 — effort S — risk low — category: close receipt
  Why: assumption: closes list what changed and what passed, but never point at the one clever or simple move in the diff. One line naming it would make a good fix feel finished.
  Done when: a closed task's receipt includes one line that cites a real `file:line` from the diff and names a specific construct (a reused helper, a deleted branch), and the line is absent when the diff has no such construct.

- **Type the user's request as the working line** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: assumption: the pane shows a generic spinner while a run works, which says nothing about what it's doing. The user's own sentence, typed out once and then fading back into the stage rail, ties the work to the ask.
  Done when: the pane's working line shows the request's first 60 characters, types out in under 1 s, and renders as static text under reduced motion.

- **Explain each pane glyph on focus** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: assumption: the stage rail and Activity lanes use symbols with no visible legend, so a new user has to learn them by trial. A one-line gloss on focus teaches without a manual.
  Done when: focusing any status glyph in the pane shows a gloss of at most 60 characters, and every glyph in the set has a gloss (a test enumerates them).

- **Mark each hundredth green gate with a flourish** — FEATURE — value 2 — effort S — risk low — category: milestone
  Why: assumption: green gates accumulate silently in History, so a long run of passes never registers as an achievement. A single, once-a-day flourish at each hundredth pass gives a reason to look.
  Done when: the 100th, 200th and so on green gate of a project shows one flourish in the pane once, and a second flourish on the same day does not appear.

- **Ship one glyph set for pane and web** — FEATURE — value 2 — effort M — risk low — category: design system
  Why: assumption: the pane, web UI and desk card each draw status marks differently, so the same state can look like three states. One shared set, drawn once, keeps the look consistent.
  Done when: a single glyph table feeds the pane, web UI and desk card, and a test fails when any surface draws a status mark outside that table.

- **Sail a ship across the pane as the queue drains** — FEATURE — value 2 — effort M — risk low — category: wild
  Why: wild: a small ASCII ship crosses a harbour line in the pane, with its position set by closed tasks over total queued tasks. Queue progress becomes a picture the user can read at a glance.
  Done when: the ship's column equals the closed-over-total ratio rounded to the pane width, and the ship docks with a one-frame flag when the queue empties.

- **Read a run as a chess game** — FEATURE — value 2 — effort S — risk low — category: wild
  Why: wild: each edit is a move in short algebraic notation, a failing gate is a check, and a closed task is a result. Anyone who knows chess can follow a run without reading diffs.
  Done when: `fm task moves <id>` prints one move per edit in order, a failed gate appears with a "+" marker on the move before it, and the output is a deterministic function of the journal.

- **Greet an old file with its first commit message** — FEATURE — value 2 — effort S — risk low — category: wild
  Why: wild: when a run first edits a file in a session, the pane shows that file's earliest commit subject for one line. It makes long-lived code feel like it has a history worth respecting.
  Done when: the first edit to a tracked file in a session shows its first-commit subject exactly once, and a file with no history shows nothing.

- **Pin a postcard of each release's best fix in the docs** — FEATURE — value 2 — effort S — risk low — category: community
  Why: assumption: release notes list changes but not the single fix a user would show a friend. One curated postcard per release, with its proof, makes the project's craft visible.
  Done when: each release tag produces one postcard file in the docs folder containing the task title, the proof command, and the before/after result, and the release gate fails if the file is missing.

- **Offer one unanswered TODO as a daily riddle** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: the blank pane wastes its quiet moments, and a repo's TODO comments are unclaimed small wins. One riddle a day with a single key to start it turns idle time into an invitation.
  Done when: with an empty queue, the pane shows one `TODO` from the repo with its file:line and a single key that files it as a task, and the same TODO is not shown twice in a week.

- **Let the close sign off in the user's own tone** — FEATURE — value 2 — effort M — risk med — category: voice
  Why: assumption: closes use a fixed voice, but users write in very different registers. Matching their message length and warmth, without changing the facts, makes the receipt feel written for them.
  Done when: over ten sample requests, the receipt's length tracks the user's median message length within a set band, and every number and file reference in the receipt is unchanged from the non-matched version.

- **Show a faint pulse on the pane border when a proof lands** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: assumption: a passed proof changes a number but nothing the eye catches in peripheral vision. A one-time border pulse, skipped under reduced motion, marks the moment without a sound.
  Done when: a proof transitioning to pass draws one border pulse of under 400 ms, and no pulse occurs when reduced motion is set or when the proof was already passing.
