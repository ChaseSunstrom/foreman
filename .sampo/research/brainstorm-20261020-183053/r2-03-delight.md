# Brainstorm — lens: delight

- **Name the run's "mood" in the header** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the user dislikes static, text-heavy screens; a single word-sized state chip (cruising, stuck, retrying, verifying, waiting on you) derived from existing harness events gives the glance-level read that the earlier station-track ideas don't name.
  Done when: a replayed event log of a failed-then-retried step shows the header chip change from "cruising" to "retrying" to "verifying" in the golden frames.

- **Give each station a small ASCII "tool" glyph that acts out its job** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: assumption: the "pictures not text" steer (station track, chips, bars) wants a visual vocabulary; a tiny 3-frame glyph per station (magnifier sweeping for plan, hammer for edit, magnifier-check for verify) is cheaper and more legible than gradients.
  Done when: each of the stations renders a distinct glyph that advances frames only while that station is active, and holds a still frame when idle or in calm mode.

- **Show "time saved by the guard" as a running tally** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the user's steering is about Foreman beating Claude Code on cost and time; the guard's refusals and the proof gate are the unseen wins. A quiet counter ("3 refusals, 1 false green caught") makes that visible during the run, not only on the Benchmarks page.
  Done when: after a run with one guard refusal, the TUI footer shows a count of 1 that matches `fm guard` log entries for that session.

- **Typewriter-settle for the model's words, with the plan pinned above** — FEATURE — value 3 — effort S — risk low — category: readability
  Why: the user said the TUI "looked like crap with all the text"; words are now tucked behind a view. Streaming text that settles into one dimmed line once a tool call starts keeps prose present without a wall.
  Done when: when a tool call begins, the streamed paragraph collapses to a single dimmed line within 300 ms, and expanding it restores the full text.

- **Idle-aware "nudge" when the run is waiting on a human** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: runs are unattended and long (marathon showcase, overnight). Prior ideas cover a "needs you" alert; this is the gentler second-order piece: the border slowly warms and the title bar line changes to "waiting on you, 4 min", rather than a one-shot bell.
  Done when: a fake run paused for a permission prompt shows an increasing wait counter in the title and terminal title, and it resets when input arrives.

- **Per-task "personality" accent from the task ID** — FEATURE — value 2 — effort S — risk low — category: look
  Why: assumption: with many queued tasks (T-12xx) users lose track; a stable hue derived from the ID's hash, used on chips and the Gantt bar, makes tasks recognisable across views without added text.
  Done when: the same task ID gets an identical accent in two separate runs and in two different views, and two different IDs differ.

- **Ship a `fm code tui --tour` that runs a scripted fake run** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: the pack shows deferred tour/newcomer briefs (T-0862) and a fake-model loop already exists; a tour that plays a canned run through every station needs no API cost, doubles as the demo recorder's source, and lets people judge the look before spending a token.
  Done when: `fm code tui --tour` exits 0 with no network access and visits each station and view once.

- **Add a "highlight reel" end card listing the three most notable moments** — FEATURE — value 3 — effort M — risk low — category: close-out
  Why: it builds on the receipt-card idea but picks moments: the longest step, the guard's biggest save, the largest diff. This ties to the deferred "close-out legibility" brief (T-0795).
  Done when: a finished run's end card names exactly three moments, each with a step ID that resolves in `fm task show`.

- **Wild: Let the TUI "weather" report the run's health** — FEATURE — value 2 — effort M — risk low — category: wild
  Why: wild. A small corner glyph shifts from sun to cloud to storm from the rolling ratio of red verifies and refusals, so a glance across the room says whether to intervene.
  Done when: a synthetic stream of 5 consecutive red verifies changes the glyph to the storm state and a green streak returns it to clear.

- **Wild: Hand the keyboard a "tilt" gesture to peek at another lane** — FEATURE — value 2 — effort M — risk med — category: wild
  Why: wild. Fleet and lanes work is deferred (T-0792); holding one key slides the view sideways to peek at a sibling worker's station track, and releasing it snaps back. It's a glanceable multi-agent view with no layout change.
  Done when: with two fake lanes, holding the peek key shows the second lane's track and releasing returns to the first within one frame tick.

- **Wild: Play the run back as a one-line ticker for the shell prompt** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: wild. A tiny `fm code ticker` prints the live station and elapsed time as a single line suitable for tmux status bars or a shell prompt, so the run stays alive on the screen when the TUI isn't open.
  Done when: `fm code ticker` prints one line under 80 columns that updates when the run changes station, and exits cleanly when the run ends.

- **Keep a "last good frame" so a crash shows the final picture, not a blank** — FIX — value 3 — effort S — risk low — category: reliability
  Why: the idea list covers terminal restore but not leaving evidence. Dumping the last rendered frame (plain text) next to the exception makes TUI bugs reportable and reproducible.
  Done when: forcing an exception in a widget writes the last frame and the traceback to a file in the run directory, and the terminal is restored.

- **Make the keybinding hints context-sensitive in the footer** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: the request includes customizable keybindings; with a command palette still absent, a footer that shows only keys valid for the current view and station keeps the screen clean while teaching the controls.
  Done when: switching from the Gantt view to the diff view changes the footer hints to that view's actions, verified in a golden frame for each.
