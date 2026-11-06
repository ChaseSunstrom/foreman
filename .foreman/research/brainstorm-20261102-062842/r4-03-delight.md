# Brainstorm — lens: delight

- **Run the tick when a session opens, and say so in one warm line** — FEATURE — value 5 — effort S — risk low — category: self-trigger
  Why: the gap is "a week of live ticks waits on the user's install." Sessions already exist, so a lazy tick at SessionStart (or the first prompt of the local day) gives live ticks with no install. A line like "Ran last night's checks on arrival: 2 things found, 0 needed you" turns an invisible mechanism into a pleasant hello. Each fire records `source=session` and its lateness, so it is gradable.
  Done when: a fresh session with a stale tick prints one line naming what ran and why, and the tick ledger has a row with source `session` and a lateness in seconds.

- **Say "checked, nothing found" so quiet reads as alive** — FEATURE — value 4 — effort S — risk low — category: self-trigger
  Why: assumption: a silent tick is indistinguishable from a dead one, and users stop trusting what they can't see. One overwritten `tick.md` with a human sentence per run ("Looked at CI, issues, 3 deferrals: all calm") gives the user something to glance at.
  Done when: a tick with zero findings still writes `tick.md` with a timestamp and a one-line summary, and `fm doctor` shows its age.

- **Give the first self-started result a moment** — FEATURE — value 4 — effort S — risk low — category: delight
  Why: assumption: the first time Foreman does something useful unasked is the moment the user decides to install the timer. Mark it once ("First one: I found X while you were away. Want this every night? `fm yes timer`"). It shows once per user and pitches the install with the user's own result instead of a generic warning.
  Done when: the first kept self-started result shows the card once, and a second one doesn't repeat it.

- **Replay last Friday evening as a ghost shift** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the pack says self-triggering is "unmeasured until the end-of-run exam" and the week of live ticks waits on the install. Feed the user's own recorded week of git, CI and ledger events through the dispatcher on a virtual clock, then show "here is what the night shift would have done". It grades the tick and shows the user the value before they commit to anything.
  Done when: `fm tick replay --week` runs on the repo's history and prints fires, hits and misses, and the same tape gives identical output twice.

- **Draw the tick tape as a night skyline** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: assumption: the web UI has room for a panel. Each fire is a lit window in a skyline across 24 hours; dark windows are missed ticks, and a hover gives the fire's one-line receipt. Reduced-motion users get a static strip. It makes "is this thing alive?" answerable at a glance.
  Done when: the web UI shows a 24-hour strip from the tick ledger, lit and dark windows match the ledger rows, and it has a text alternative.

- **Offer the trigger the user just did by hand** — FEATURE — value 4 — effort M — risk med — category: self-trigger
  Why: assumption: the user repeats manual sequences (rerun CI, check issues, rebase). When the same verb sequence happens three times, propose "make this a trigger?" as a draft that is never installed. It is the moment a trigger feels earned.
  Done when: a fixture history with a repeated sequence produces exactly one proposal naming the sequence, and declining it silences it for 30 days.

- **Write the morning note in a person's voice** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: terse machine summaries get skimmed. "Quiet night. CI went red once at 02:10 and fixed itself. I left your branch alone." Three lines, from facts in the ledger only, so nothing can be invented.
  Done when: the note is generated from ledger fields with no model call, and every sentence maps to a ledger row.

- **Show a "next tick due" dot on the status line** — FEATURE — value 3 — effort S — risk low — category: polish
  Why: assumption: with session-borne ticks, the user wonders when the next one runs. A small dot ("● due in 4h", amber when overdue) turns hidden scheduling into something legible.
  Done when: the status line shows the dot, it turns amber past three intervals, and it adds under 5 ms.

- **Add `fm demo tick`, a sandbox first fire** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the install is user-only, so there's no way to feel the feature first. A throwaway repo with a planted red CI and a stale deferral lets the user watch one fire end to end in 30 seconds, then see exactly what a real install would add.
  Done when: `fm demo tick` makes a temp repo, fires, prints the receipt, and leaves nothing outside the temp dir.

- **Wild: Play the tick tournament** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. Several tick drivers (session, replay, timer-simulated) run the same tape and race to the earliest correct notice. The leaderboard shows what the user loses without a timer in plain minutes.
  Done when: `fm tick race` prints per-driver notice latency on one tape, with a no-tick baseline row.

- **Wild: Hatch a tick-egg on the status line** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A small glyph grows (egg, crack, chick, hard hat) with each day the tick catches something real, and rests when it catches nothing. It is playful, local, and makes the streak visible without a metric.
  Done when: the glyph stage is a pure function of ledger days with a kept result, and the user can switch it off.

- **Wild: Seal the tick's predicted morning card and settle it at wake** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. Before sleeping, the tick writes what it expects to find; in the morning it shows hits and misses beside what actually happened. Brier scores accumulate in the bets ledger, giving a free grade that needs no install.
  Done when: a sealed prediction is stored with a hash, settled at the next session, and appears in `fm outcomes --judgment`.

- **Show an install counterfactual card** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the pack's gap is that the timer waits on the user. Compute from session gaps how late each notice came ("CI red sat 9h before your next session") and show "a timer would have saved ~9h on 3 events". The pitch is the user's own numbers and the install stays their choice.
  Done when: `fm doctor` prints the counterfactual from the ledger, or says "insufficient data" when under 5 events.

Next question: what does the user do in the first minute after a self-started result they didn't expect, and is there a one-word way to say "keep" or "undo"?
Next question: which tick output would the user miss within a week if it vanished, and does any ledger record that they read it?
