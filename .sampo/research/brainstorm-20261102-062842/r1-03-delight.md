# Brainstorm — lens: delight

- **Ride the session's edges when no timer exists** — FEATURE — value 5 — effort M — risk low — category: self-trigger
  Why: gen-2's gap is that live ticks wait on the user's timer install. Assumption: SessionStart, Stop and the first `fm` call of the day can run the same tick body (`fm night` tick) with a `source=session-edge` stamp.
  Done when: in a sandbox with no timer, starting a session runs the tick once, writes a row with `source=session-edge`, and a second start within the debounce window writes none.

- **Replay a recorded week through the dispatcher** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: "a week of live ticks graded" can't wait for an install. The repo's own git log, ledgers and CI history are a week of events already. Assumption: those timestamps are enough to reconstruct tick moments.
  Done when: `fm tick --replay 7d` prints each synthetic tick's decision (fired, skipped, why) and a graded line "N fired, M acted on, K missed" from a fixture history.

- **Log the shadow tick, grade it later** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the trigger is only measured at the end-of-run exam. Each session can record "a tick here would have done X" without doing it, then settle it against what the user actually did next (same style as bets and Brier).
  Done when: after a session, the shadow log has rows, and `fm outcomes` shows a hit rate per trigger kind once 10 are settled.

- **Pitch the timer with the user's own numbers** — FEATURE — value 4 — effort S — risk low — category: install card
  Why: the install has waited on the user so far. Instead of asking cold, show evidence: "this week it would have run 14 times, caught 3 red CIs, saved about 9 minutes." Assumption: shadow rows carry enough to estimate savings.
  Done when: the install card prints three figures drawn from the shadow log, and prints nothing when fewer than 5 shadow rows exist.

- **Open sessions with a "while you were away" card** — FEATURE — value 4 — effort M — risk low — category: welcome back
  Why: the piggyback tick finds new commits, red CI and expired deferrals since the last session, so the user gets a short warm card instead of silence. Must stay within the lean budget. Assumption: three lines or fewer is acceptable at SessionStart.
  Done when: with a fixture of 2 new commits and 1 red CI, the note is at most 3 lines and names each; with nothing new, it injects zero bytes.

- **Count asks avoided with a quiet counter** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: a self-trigger's worth is the command the user didn't have to type. Showing "saved you: ci-watch (3rd this week)" once per trigger kind makes it visible without nagging.
  Done when: the first piggyback fire of a kind prints one line, and later fires of that kind print nothing but still increment `fm status`'s counter.

- **Plant events in a fixture repo and score the tick on a scoreboard** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: self-triggering is "unmeasured until the end-of-run exam". A fixture with a scripted red CI, stale deferral and drifted branch gives a zero-token score now.
  Done when: `fm doctor` shows "tick caught 6/8 planted events" and names the two missed, and the number is deterministic across runs.

- **Celebrate the first self-started result the user kept, once** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the moment self-triggering earns trust is the first time its work gets used. Assumption: "kept" is detectable by a task from a trigger that landed without edits.
  Done when: a toast appears exactly once per project after the first kept trigger task, and never again after that.

- **Wild: Time-lapse the replayed week in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. The replay produces a timeline anyway; scrub it at 100x with a fire pulsing per decision, with reduced-motion fallback to a static strip. Something people would screenshot.
  Done when: the page renders a replay of a fixture week, play/pause works, and with `prefers-reduced-motion` no animation runs.

- **Wild: Show a terminal tab title that breathes with trigger state** — FEATURE — value 2 — effort S — risk low — category: terminal
  Why: wild. An OSC title like "fm · 2 would-fire" updates on each piggyback tick, so the shell tab shows ambient life without a daemon. Assumption: the harness lets hooks write OSC safely.
  Done when: after a shadow fire, the title sequence is emitted once, and nothing is emitted under `FOREMAN_QUIET=1`.

- **Wild: Sign the morning note as "the night watchman"** — FEATURE — value 2 — effort S — risk low — category: voice
  Why: wild. A consistent small persona with one line of personality ("nothing stirred") makes the empty case a pleasure, not a missing output. Assumption: the user would rather read this than a bare "0 events".
  Done when: an empty night prints a one-line, varied-but-deterministic sign-off, and a busy night prints the facts first and the sign-off last.

- **Say "checked, nothing found" so quiet reads as alive** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: self-triggering that never speaks looks dead. A one-line "checked CI, branches, deferrals at 08:14: all quiet" in `fm status` distinguishes alive from broken.
  Done when: after a quiet tick, `fm status` shows the line with its time, and a tick that crashed shows "did not run" instead.

- **Offer the trigger the user just did by hand** — FEATURE — value 3 — effort M — risk med — category: suggestion
  Why: when a session's third `fm ci-watch` is typed by hand in a week, say "want this to run itself? (shadow mode first)". Assumption: the event log records hand-typed verbs with timestamps.
  Done when: with three recorded manual runs in 7 days, the next session prints one offer, and a decline suppresses it for 30 days.

Next question: What is the user's actual reaction to a note they didn't ask for at SessionStart, and has any earlier ledger recorded a dismissal rate for such notes?
Next question: Which trigger kinds can be settled against ground truth from git alone, so shadow grading needs no user clicks?
