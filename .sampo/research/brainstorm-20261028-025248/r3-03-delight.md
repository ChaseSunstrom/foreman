# Brainstorm — lens: delight

- **Show the shorter command after a slow repeat** — FEATURE — value 3 — effort S — risk low — category: surprise
  Why: assumption: the pack shows the user retyping long phrasings ("Push foreman/build to main", "Cut Foreman's usage burn" recreated after a drop). A quiet hint teaches the short form without a lecture.
  Done when: a long-form command run three times in one session prints its shorter equivalent once, and never again that session.

- **Pin a receipt as a bookmark ribbon** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: users return to specific closes (a verdict they liked, a fix they want to cite), and History only sorts by time.
  Done when: a pinned receipt sits at the top of History with a ribbon and is still pinned after `fm` restarts.

- **Dim the unchanged numbers on each receipt** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: receipts repeat the same counts run after run, so the one number that moved gets lost. Dimming the stable ones lets the change stand out at a glance.
  Done when: numbers equal to the last receipt render at reduced opacity, changed ones at full opacity with one pulse, and reduced-motion turns the pulse off.

- **Give undo a calm rewind glyph, never a red alarm** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: undo currently reads like an error, which makes a deliberate rollback feel like a failure. Tone matches the action's intent.
  Done when: the undo confirmation uses the rewind glyph and no error colour token, and a test asserts the token is absent.

- **Settle gauges with one spring overshoot on a pass** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: assumption: a gate needle that eases to a flat value reads as dead. One small overshoot on a pass makes the moment feel earned, and a failure stays flat.
  Done when: a passing gauge reaches its value within 400 ms with at most one overshoot, a failing one does not overshoot, and reduced-motion jumps straight to the value.

- **Give each task kind a fleuron on its receipt** — FEATURE — value 2 — effort S — risk low — category: polish
  Why: assumption: receipts show the kind (FIX, FEATURE, CLEAN, PERFORMANCE, SECURITY) only as a word, so the five kinds look the same at a glance. A small distinct ornament per kind is cheap and scannable.
  Done when: all five kinds render a distinct glyph in the pane and the web UI, and a test checks the five glyphs are unique.

- **Leave a sticky note with one tidy thing when idle** — FEATURE — value 2 — effort S — risk low — category: idle screen
  Why: assumption: an empty queue shows nothing, which wastes a quiet moment. One stale or small item shown as a note invites the next action without nagging.
  Done when: with no running or queued work and one stale backlog item, the pane shows exactly that item as one note; with no stale items, it shows nothing.

- **Draw the run's elapsed time as a sundial** — FEATURE — value 2 — effort M — risk low — category: wild motion
  Why: wild: a shadow sweeping across a small dial shows elapsed time without a number, so a long run feels calm rather than like a clock being watched.
  Done when: the shadow angle advances monotonically with elapsed time, and two readings at the same elapsed value draw the same angle.

- **Turn the work bar into cassette reels** — FEATURE — value 2 — effort M — risk low — category: wild motion
  Why: wild: reels that turn while the run works and slow as it nears done give the bar a physical, nostalgic feel with no extra information to read.
  Done when: reel rotation speed follows the work bar's rate of change, and the reels stop when the run stops.

- **Break a tie between equal backlog items with a dice roll** — FEATURE — value 2 — effort S — risk low — category: wild surprise
  Why: wild: when two items have the same value and effort, the order is arbitrary anyway. A visible roll with its seed logged makes the choice fun, fair and reproducible.
  Done when: two equal items yield one stable order for a given logged seed, the roll and seed show in the queue, and one key re-rolls before the run starts.

- **Write a day's closing acrostic from the closed task slugs** — FEATURE — value 1 — effort S — risk low — category: wild delight
  Why: wild: the first letters of the day's closed slugs, read in order, make a small word or line that people enjoy sharing.
  Done when: the acrostic's letters equal the first letters of the day's closed slugs in close order, and a day with no closes shows no acrostic.
