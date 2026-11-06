# Brainstorm — lens: deepen: reliability

- **Beat ledger for every trigger path** — FEATURE — value 5 — effort M — risk low — category: heartbeat
  Why: the reliability list repeats "silence means alive" ~8 times, and the night tick "logs only when something happens", so a dead tick and a quiet one look identical. Combine the repeats into one file: each tick, timer, file watcher and ci-watch poll appends a timestamped beat, and `fm doctor` reads the gaps against each trigger's expected interval.
  Done when: stopping the timer's service makes `fm doctor` name that trigger as silent past 2× its interval, and a quiet but running tick shows as alive.

- **Catch up missed schedules once, capped** — FEATURE — value 4 — effort M — risk med — category: schedules
  Why: the pack lists "run missed schedules once on wake" and "coalesce after sleep" several times. A laptop that sleeps through five night ticks should run one catch-up, not five. A cap on how old a missed slot can be stops a week-old schedule from firing on boot.
  Done when: a test simulating 5 missed slots and a 3-day gap runs one catch-up in the first case, none past the cap in the second, and logs both decisions.

- **Check installed units at the install site** — FIX — value 4 — effort S — risk low — category: install health
  Why: it's an idea from the list ("units still point at a live interpreter and library"). Timers outlive Python upgrades (the pack mentions 3.14 and a setuptools split), and a unit pointing at a deleted path fails silently.
  Done when: renaming the interpreter a unit's ExecStart uses makes `fm doctor` report that unit as broken with the missing path, and `fm doctor --fix` queues the repair for one yes through `fm ask --later`.

- **Verify the first fire after every install and boot** — FEATURE — value 4 — effort S — risk low — category: install health
  Why: "installs get queued for one yes" means the user approves something unseen. After approval, trigger one dry fire and record that it ran, so the yes is confirmed by evidence.
  Done when: approving a timer install leaves a "first fire ok" row within the timer's interval, or a named failure with the unit's journal tail.

- **Give each trigger an overlap policy** — FEATURE — value 4 — effort M — risk med — category: concurrency
  Why: listed as "overlap policy per trigger". Builder lanes run in parallel and CI-watch and file triggers can fire during a running task, so a second fire needs a rule: skip, queue one, or replace.
  Done when: a trigger declared `overlap=skip` fires twice while its first run is live and records one run plus one logged skip.

- **Retry with a dead-letter list** — FEATURE — value 4 — effort M — risk low — category: failure handling
  Why: "retry failed fires and keep a dead-letter list" is in the pack. Combine it with the beat ledger: a fire that failed three times with backoff lands in a list `fm next` shows once, instead of vanishing from a log nobody reads.
  Done when: a trigger whose action always fails shows exactly 3 attempts with increasing delays and then one dead-letter entry visible in `fm next`.

- **Give each trigger a service level and a miss count** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: "per-trigger service levels and misses" is on the list. It extends `fm triggers`, which already records precision, with recall of the fire side: how many expected fires happened on time.
  Done when: `fm triggers` prints on-time rate and misses per trigger over 14 days, computed from the beat ledger.

- **Make the watcher say when it goes blind** — FEATURE — value 4 — effort S — risk low — category: watchers
  Why: `fm ci-watch` settles ship bets, and 11 held in a row. A blind poll (expired auth, rate limit, offline) would look like 11 more quiet successes. A watcher that can't read its source should write a "blind" beat, not a clean one.
  Done when: running `fm ci-watch` with the CI API credentials revoked records a blind state and `fm doctor` names it, not "no new runs".

- **Add a state registry that fails when a new state appears** — CLEAN — value 3 — effort S — risk low — category: test guard
  Why: the list asks "what the trigger layer's states are, and fail when a new one appears". One enum for alive/quiet/blind/silent/dead-lettered/skipped with a test that every code path emits only members, so the doctor can't miss a state.
  Done when: adding an unlisted state string to a trigger path fails a unit test that names it.

- **Wild: let a missing beat be the alarm, off-machine** — FEATURE — value 3 — effort M — risk med — category: heartbeat (wild)
  Why: wild; assumption: the user opts into a ping to a URL they own (a dead-man service or a self-hosted receiver), so a powered-off machine, which no local doctor can report on, still raises a message. It must stay opt-in because of the local-first rules.
  Done when: with the setting on, skipping beats for 2 intervals makes the receiver send an alert, and with it off no network call is made, checked by a test.

- **Wild: rehearse one chaos night before the first install** — FEATURE — value 4 — effort M — risk low — category: rehearsal (wild)
  Why: wild; the standing steers want real-path verification and planted faults. Before the yes, run a sandbox night with a fake clock: sleep, a killed tick, a full disk, a revoked token, a double fire, and print what Foreman did in each.
  Done when: `fm night --rehearse` prints a pass/fail row for each of those six faults and the install ask shows the result.

- **Wild: a weekly canary event across the whole chain** — FEATURE — value 3 — effort M — risk low — category: end-to-end (wild)
  Why: wild; each part can be alive while the chain is broken. A synthetic issue or file touch enters through the trigger and must come out as a task that auto-closes, which catches broken glue that unit beats can't.
  Done when: the canary runs weekly, a deliberately broken trigger-to-task link makes it fail, and the failure appears in `fm doctor`.

- **Wild: a trigger that proposes its own retirement** — FEATURE — value 2 — effort S — risk low — category: precision (wild)
  Why: wild; `fm triggers` already measures precision. A trigger that fires for 30 days with none of its tasks surviving gets a one-yes "retire this?" ask, in line with the lean-substance steer.
  Done when: a trigger with 30 days of zero-survival fires produces a single retire ask, and answering yes removes its unit.

Next question: Which trigger actions are safe to run unattended after a catch-up or retry, and which need a human yes because rerunning them has side effects (pushes, issue comments)?
Next question: How does the user learn a trigger died when they only open the web UI rarely, and which channel (notification, digest, session start line) do they actually read?
