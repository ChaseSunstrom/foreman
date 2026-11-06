# Brainstorm — lens: user value

Answering two of the open questions through the user-value lens first:

- **After a self-started mistake:** the user finds what it did (`fm why`), stops it, undoes it, and mutes the trigger. The last step, telling Foreman why it was wrong, has no one-word verb. Idea 5 covers it.
- **Unchecked outputs:** the user acts on the morning card without checking it against anything outside Foreman. Idea 4 gives each card item a cheap external check, in minutes of review.

I assumed throughout that the user has no timer installed, so every idea works from session edges, transcripts or git.

- **Add `fm since`, the pull form of the tick** — FEATURE — value 4 — effort S — risk low — category: self-trigger
  Why: assumption: the user will run a verb sooner than install a unit. The pack shows the install still hasn't happened. `fm since` evaluates every trigger against the git, CI and ledger state right now and prints what would have fired while they were away. The number of times the user runs it is the first install-free demand signal.
  Done when: `fm since` in a fixture repo lists the 3 planted events in order and writes one `pull` row to the tick ledger.

- **Rescue sessions stalled on a permission prompt** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: the steers say never block on the user, but nothing in the pack covers a live session waiting on a prompt after they leave. Mine existing transcripts for gaps between a permission request and the next user event to get a free baseline. A session-edge tick can then check whether a durable grant covers the prompt. If none does, it parks the lane and leaves one yes-card.
  Done when: a replayed transcript with a 40-minute prompt stall produces a parked-lane note, and the baseline stall hours appear in `fm doctor`.

- **Fire the lazy tick from the editor and the directory** — FEATURE — value 4 — effort M — risk low — category: edge clocks
  Why: assumption: the user already has an editor or shell. A committed VS Code `runOn: folderOpen` task, a `.envrc` for direnv and a Neovim autocmd are cheaper to accept than a systemd unit. Each stamps `source=editor|direnv` on the fire so the scoreboard shows which clock actually runs.
  Done when: opening the fixture folder in a headless editor harness runs the tick once and the ledger row names its source.

- **Price every self-started result in review minutes** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the first-hour question above shows unchecked acting. Estimate the minutes to review from diff size, touched files and proof present, calibrated on the user's past review gaps. Show it next to the proof line, so "2 min, proof ran" is checkable at a glance.
  Done when: each card item prints a minutes estimate, and the median error against actual open-to-decision time is reported once 20 items are settled.

- **Add a one-word decline reason: timing, content, scope or noise** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: assumption: today a drop is a single bit. Splitting it lets the layer fix lateness differently from wrong content. It also gives the missing step from the first-hour question a verb: `fm drop T-123 timing`.
  Done when: dropping with a reason is stored, and `fm outcomes` splits drops by reason per trigger.

- **Show only what changed in the tick card** — FEATURE — value 3 — effort S — risk low — category: noise
  Why: assumption: repeating an unchanged CI-red line daily teaches the user to skip the card. Hash each item and show only new, resolved and aged-past-threshold items, plus "N unchanged".
  Done when: two consecutive ticks on a static fixture print the full card once, then a one-line card.

- **Schedule the user's questions, not the work** — FEATURE — value 3 — effort M — risk low — category: attention
  Why: assumption: yes-cards sit unanswered because they land at the wrong hour. Learn reply latency by hour from past asks, and release non-urgent cards at the next fast-reply window.
  Done when: a replay over 30 recorded asks shows the median simulated reply latency falling against the as-sent baseline.

- **Route a fire to the code's owner as a staged draft** — FEATURE — value 3 — effort M — risk med — category: team
  Why: assumption: some users work in shared repos. When CI red traces to another author's lines (CODEOWNERS or blame), draft the note to them and stage it behind one yes. Nothing is sent without that yes.
  Done when: a fixture failure blamed to a second author yields a staged draft addressed to them, and no outbound call happens before the yes.

- **Make the empty tick informative with a "checked, found nothing" ledger** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: a quiet tick looks identical to a dead one. Record per job what it looked at and the age of the newest input, so "nothing" shows evidence.
  Done when: a no-event tick prints per-job input ages, and a job with a stale input is flagged rather than silent.

- **Wild: Print a regret-of-speech score** — FEATURE — value 3 — effort M — risk low — category: precision
  Why: wild. The pack tracks the cost of silence, but nothing tallies the times Foreman spoke and the user was right to be annoyed. Settle fires by drop, ignore and quick dismissal, then print "bothered you N times, wrongly K".
  Done when: after a replayed week the score appears, and the fire with the most regret names its trigger.

- **Wild: Use a single daily whistle graded by reaction time** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Only the day's top item gets a notification (a terminal bell or `notify-send`). The time from whistle to the user's first touch is a measure that needs no questions asked, and the user can pick the sound.
  Done when: the whistle fires once per day at most, and its reaction time is logged and shown in `fm outcomes`.

- **Wild: Adapt card density to the user's chronotype** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Terse one-liners during the user's historically fast-typing hours and fuller context in slow ones, learned from message timestamps and lengths. Everything stays local.
  Done when: replaying two timestamps from different hours yields cards of different density, with the same facts present in both.

Next question: what share of the user's last 30 days contained hours with open Foreman work and no live session, and could any of those hours have been served by the three edge clocks above instead of a timer?
Next question: which self-started outputs would the user have wanted at a different time rather than not at all, and does any ledger distinguish those from true misses?
