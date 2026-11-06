# Brainstorm — lens: unspoken needs

- **Make the first install a 7-day trial that removes itself** — FEATURE — value 4 — effort M — risk low — category: install
  Why: assumption: the install is still pending because it's a standing commitment. A timer unit with `RuntimeMaxSec`/an expiry date and a final self-disable step turns it into a trial. The user keeps it only by renewing, and the week of live ticks gets graded either way.
  Done when: after the expiry date in a faketime test, `systemctl --user list-timers` shows no foreman unit, and `fm doctor` prints "trial ended: N fires, M kept" with no manual cleanup.

- **Write the wake-up condition when you defer** — FEATURE — value 4 — effort M — risk low — category: tasks
  Why: about 35 open items say "later: needs evidence/cases/an event" (T-0827, T-0862 to T-0869, T-0829, T-0832). Those conditions sit in prose, so only the user's memory un-defers them. A machine-checkable predicate (a file exists, a count passes a threshold, an exam line appears) lets any tick wake the item.
  Done when: `fm task defer --until 'exam:lines>=20'` stores a predicate, and a tick run on a fixture where it becomes true moves the task to open with a "woken because …" line.

- **Stop self-started output when too much is still unread** — FEATURE — value 4 — effort S — risk low — category: backpressure
  Why: the user already steered `--round-first` to hold Foreman-filed items. That shows they dislike a queue Foreman fills for itself. Nothing yet caps how many tick results can pile up unseen.
  Done when: with 3 unseen tick-filed items, the next tick files nothing, logs "held: 3 unseen", and the count resets after `fm next` shows them.

- **Add `fm oops`: undo everything self-started in the last N hours** — FEATURE — value 5 — effort M — risk med — category: recovery
  Why: the open question "what does the user do in the first hour after something Foreman did goes wrong" has no single verb. The tick is the first path that acts while no one is watching, so it raises the stakes.
  Done when: `fm oops --since 12h` lists each unattended branch, task and file, prints a revert command for each, and a fixture run restores the tree to its pre-tick state.

- **Prove each tick left the user's tree untouched** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: assumption: "worktree only" is a claim, not a measurement. Recording tree, index, stash and branch-ref hashes before and after every tick gives a gauge the user can believe without trusting Foreman's own ledgers.
  Done when: a tick that edits a tracked file in the main checkout (planted bug) fails its own receipt with "user tree changed", and a normal tick records "unchanged".

- **Learn quiet hours from the user's own timestamps** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: assumption: the user won't fill in a quiet-hours setting, but commit and transcript times already show when they work. Ticks should avoid those hours by default and run before the habitual start.
  Done when: `fm tick --explain-hours` prints the inferred band and its sample count, and a fixture with commits clustered 9:00–18:00 never fires a tick inside that band.

- **Run ticks during waits Foreman already owns** — FEATURE — value 3 — effort S — risk low — category: no-install
  Why: `fm ship`, `fm ci-watch`, exam runs and bench runs sit idle for minutes with a live process. Running a due tick there is free, needs no install, and goes into the lateness ledger tagged by source.
  Done when: a 3-minute `fm ship` wait on a fixture runs a due tick, and the ledger row says `source=ship-wait`.

- **Publish the self-triggering scoreboard on the Genesis site with denominators** — DOCS — value 3 — effort S — risk low — category: proof
  Why: the standing rule says the site follows Genesis, and another says claims need proof. A page listing ticks due, ticks run, source (timer, session edge or replay), and fires the user kept, each with its denominator, makes "measurable" visible.
  Done when: `fm genesis live` publishes `site/genesis` data containing those counts, and a claim with no count fails the proof-before-presentation sweep.

- **Order the return brief by what the user types first after an absence** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: the user's own words show they check state ("where were we" style). What tick output goes first is guesswork until measured from their first message after gaps over 8 hours.
  Done when: the brief's top item matches the user's actual first request in at least X% of replayed past absences, with the baseline "newest first" printed beside it.

- **Honour a per-repo consent file for ticks** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: assumption: a tick that wakes across all repos will reach work repos the user never meant to hand to an agent. A `.fm/tick` file (or the absence of one for repos whose remote isn't the user's) keeps them out.
  Done when: a tick run on a fixture repo with no consent file does nothing and logs "skipped: no consent", and one with the file proceeds.

- **Hibernate when the user has gone quiet (wild)** — FEATURE — value 3 — effort S — risk low — category: waste
  Why: if no session opens for 14 days, ticks should shrink to one weekly "still waiting" beat rather than burn usage on a user who left. The unit is the user's usage limit, not wall time.
  Done when: a fixture 15 days idle runs only the heartbeat, and the first session after it resumes full cadence with a "was hibernating" line.

- **Land all unattended output in an airlock that only a present user promotes (wild)** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: assumption: a tick that can only write to `pending/` is harmless by construction. That lets it run at full cadence and get graded without risking a bad unattended write.
  Done when: a tick-started lane's diff sits under `pending/` untouched by `main`, and `fm next` offers one-word promote or discard.

- **Carry the tick on a timer the user already trusts (wild)** — FEATURE — value 3 — effort M — risk med — category: install
  Why: assumption: a one-line systemd drop-in or `ExecStartPost` on a timer the user already installed (backup, updates) is a smaller consent than a new unit. Foreman scans the user's existing timers and proposes the line as a diff.
  Done when: `fm tick --piggyback` lists candidate existing timers read-only and prints the exact drop-in text for one, changing nothing on disk.

Next question: which of the user's repos do they open most, and should tick attention follow that distribution instead of treating every repo equally?
Next question: when a tick result goes unread for a week, is that because it was useless or because it was in the wrong place, and what in the pack could tell those apart?
