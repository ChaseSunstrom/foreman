# Brainstorm — lens: delight

- **Run the tick when a session opens, and say so** — FEATURE — value 5 — effort M — risk low — category: self-trigger
  Why: assumption: the user's timer install is pending; sessions already exist. A lazy tick at SessionStart/Stop records lateness and source (session, replay), so self-triggering is measured without an install.
  Done when: opening a session with an overdue job runs it once and appends a ledger row with `source=session` and its lateness in minutes.

- **Open with a "while you were away" card** — FEATURE — value 4 — effort S — risk low — category: return brief
  Why: assumption: the night tick's output goes unread. One three-line card (fired, found, "checked, nothing found") makes quiet read as alive.
  Done when: a session after an overnight tick prints at most 3 lines naming each fire and its result, or "checked, nothing found".

- **Say "checked, nothing found" instead of silence** — FEATURE — value 4 — effort S — risk low — category: liveness
  Why: a silent tick looks the same as a dead one. A one-line nightly receipt tells them apart.
  Done when: every tick writes a beat row, and `fm doctor` shows the last beat's age.

- **Replay a recorded week in a ten-second timelapse** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: tick tapes on a virtual clock grade the layer without live ticks; the web UI can draw the same tape as a strip of fires, skips and catch-ups.
  Done when: the page loads a fixture tape and plays it at 100x, showing each fire as a dot with its outcome colour.

- **Pitch the timer with the user's own numbers** — FEATURE — value 4 — effort S — risk low — category: install card
  Why: the install is the blocker. A card saying "N jobs overdue a median of H hours across your last 14 sessions; the timer would have run them" is more persuasive than a generic warning.
  Done when: `fm doctor` prints that line from the lateness ledger, and omits it with under 5 sessions of data.

- **Offer the trigger the user just did by hand** — FEATURE — value 4 — effort M — risk low — category: proposals
  Why: assumption: repeated manual sequences predict wanted triggers. A one-word yes card appears the second time the same verb sequence is typed.
  Done when: running a verb pair twice produces a single-line offer naming the trigger it would create, and declining mutes it for 30 days.

- **Give the first self-started result a moment** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: the first kept result of an unattended run is the point at which the feature is believed. One-time note: "Foreman did this while you were away: …, one command to undo".
  Done when: the first kept self-started result prints the note once, and a second never does.

- **Breathe a "next tick due" dot on the status line** — FEATURE — value 2 — effort S — risk low — category: status line
  Why: shows the clock exists, and turns amber when a job is overdue.
  Done when: the status line shows a dot whose state matches the lateness ledger in a fixture.

- **Add `fm demo tick`, a sandbox first fire** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: users distrust unattended work they have never watched. A fake repo with a planted red CI event fires through the real dispatcher in 20 seconds.
  Done when: the command runs in a temp dir, shows event, fire, result and cleanup, and leaves the user's tree untouched.

- **Show a tick tape drawn as a night skyline** — FEATURE — value 2 — effort M — risk low — category: web UI
  Why: a column per hour, tall for work done, flat for "nothing found", hollow for missed. Motion explains state: new fires rise on load; `prefers-reduced-motion` skips it.
  Done when: the skyline renders from the ledger, and hollow bars mark hours with an overdue job.

- **Wild: Sign the morning note as "the night watchman"** — FEATURE — value 2 — effort S — risk low — category: voice
  Why: wild — a person-like voice ("Quiet night. Looked at CI, issues, deferrals; nothing needed you.") makes the note read as care, not a log.
  Done when: the note is written from a template with no more than 3 sentences and passes a read-aloud lint.

- **Wild: Hatch a tick-egg on the status line** — FEATURE — value 2 — effort S — risk low — category: playful
  Why: wild — an egg that gains a crack for each on-time unattended tick, hatching at 7, becomes the visible proof of a week of live ticks.
  Done when: seven on-time ticks in a fixture change the glyph once, and a missed tick does not reset it silently.

- **Wild: Replay last Friday evening as a ghost shift** — FEATURE — value 3 — effort M — risk low — category: demo
  Why: wild — the user's own recorded history replays through the dispatcher showing what Foreman would have done unattended, with nothing written.
  Done when: `fm demo ghost` prints a per-fire list from the last 7 days of local events and changes no files.

Next question: What does the user do in the first minute after reading a morning note, and which of those steps still need typing a verb?
Next question: Would the user rather see a pending-timer pitch at session start or only in `fm doctor`?
