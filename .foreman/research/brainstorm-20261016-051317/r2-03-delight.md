# Brainstorm — lens: delight

- **Land each close with a one-line "what you'd say to a friend" summary** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: assumption: closes today read as receipts (grade, evidence, commits); the user keeps asking for things they can glance at and show. Existing ideas cover stamps and plain receipts, not a single shareable sentence.
  Done when: closing a task prints one sentence under 100 chars, free of task ids and jargon, and `fm log --last` returns the same sentence.

- **Make the pane's idle screen a "while you were away" reel of three finished moments** — FEATURE — value 4 — effort M — risk low — category: pane
  Why: user went AFK repeatedly ("I will be AFK, do everything"); the "what did I miss" receipt idea is text. A reel of three concrete before/after moments is what they'd actually return to.
  Done when: after 30+ minutes idle with closed tasks, the pane shows up to three entries, each with title, one diff stat and a pass/fail dot, dismissable with one key.

- **Give each lane a callsign and a tiny signature glyph that follows it through pane, ledger and commits** — FEATURE — value 3 — effort S — risk low — category: identity
  Why: parallel builder lanes (4 at once, load 30–60) are hard to tell apart; "callsign" exists as an idea but not a glyph carried into commit trailers and the Agents graph.
  Done when: two concurrent lanes show distinct callsign+glyph in the pane and in `git log` trailers of their merges.

- **Add a guard "near miss" tally to the day's end line** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: the guard's saves are invisible by design; "caught it" moment covers the instant, not the cumulative count. Evidence: guard false positives cost the most debugging time, so showing true saves rebalances trust.
  Done when: the session-end line reads e.g. "guard: 3 blocked, 1 you overrode, 0 mistakes since" derived from the ledger, and the numbers match `fm ledger` counts in a test.

- **Let `fm ui` print a one-frame still of the pane on exit (a "last frame" keepsake)** — FEATURE — value 2 — effort S — risk low — category: pane
  Why: the user cares about screenshots and demo recordings (demo/live.svg, "screenshot every screen"); a still persisted per task close gives free README/PR material.
  Done when: closing a task writes `.foreman/stills/<task>.svg` and `fm still <task>` prints its path.

- **Fade quiet cards by recency with a slow brightness decay instead of hard collapse** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: user complained about clutter and a missing separator in the tree UI; collapse/ticker ideas exist but binary. A decay makes "what's fresh" legible without layout jumps.
  Done when: a card untouched for 10 minutes renders at a dimmer palette step than a card touched in the last minute, verified by a snapshot test; reduced-motion disables the gradual shift (steps instantly).

- **Phrase every error in the user's own recent vocabulary** — FEATURE — value 3 — effort M — risk med — category: voice
  Why: assumption: the user's steers ("tree UI", "band", "pane", "session/each sub agent thing") show consistent names. A glossary idea exists for learning vocabulary, but not applying it to messages.
  Done when: with a glossary entry mapping "subagent"→"agent thing", a refusal message uses the mapped term, and turning it off restores defaults.

- **Wild: Hum a "build weather" in the statusline: a single glyph for load, red/green streak and queue depth** — FEATURE — value 3 — effort S — risk low — category: statusline
  Why: wild; with load 30–60 from four builders, the user needs a glanceable "is the machine coping" signal; weather metaphor is shareable. Assumption: statusline has room for one glyph.
  Done when: the glyph changes between at least three states as load, failing gates and queue depth cross thresholds, covered by a unit test.

- **Wild: Generate a "director's cut" 30-second pane replay automatically when a release is cut** — FEATURE — value 4 — effort L — risk med — category: release
  Why: wild; releases 1.2.31/1.2.32 were shipped repeatedly and the README leads with a recorded demo that goes stale ("regenerate README pictures in CI" exists but not auto-cutting from real work).
  Done when: `fm release` attaches an SVG/MP4 replay built from that release's ledger events and fails softly if the recorder is unavailable.

- **Wild: Offer a "thank-you note" from the builder lane when a hard task finally goes green after retries** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: wild; hard closes (reviewers found defects in almost every branch) go unmarked. A short, honest note listing what was fought and what finally worked makes persistence visible.
  Done when: a task closing green after 2+ red runs appends a 2-line note naming the failure it overcame, and tasks that passed first time get none.

- **Wild: Render the Agents graph as a living tree whose branches thicken with tokens spent** — FEATURE — value 3 — effort M — risk low — category: pane
  Why: wild; the user asked for sub-agent areas holding inline chat and a visible separation; branch weight shows cost and activity at a glance, supporting the unexplained-spend alarm.
  Done when: node edge widths in the Agents graph map to token spend buckets, with a legend, and a snapshot test shows different glyph weights for low and high spend.

- **Show a tasteful "first time ever" toast for each new capability the user has never triggered** — FEATURE — value 3 — effort M — risk low — category: discovery
  Why: the backlog has many shipped verbs; "report unused features" exists as analytics, not as in-moment discovery. Assumption: users never learn most verbs.
  Done when: first use of a verb in a project prints a one-line "new to you" toast once, recorded so it never repeats, and it is silent in non-interactive mode.

- **Add a keypress "pin this moment" that bookmarks a pane state into the day's reel** — FEATURE — value 2 — effort M — risk low — category: pane
  Why: complements the replay scrubber ideas with a user-authored highlight, so the weekly recap and release reel are curated by the user rather than inferred.
  Done when: pressing the pin key stores a timestamped marker with the task, and `fm reel` lists pinned moments first.
