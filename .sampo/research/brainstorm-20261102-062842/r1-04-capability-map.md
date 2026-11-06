# Brainstorm — lens: capability map

Capability map for self-triggering that is measurable and useful without the user's install. Reference tools: GitHub Actions and Dependabot, Renovate, cron/systemd timers, Temporal and Airflow schedules, Zapier/n8n, pre-commit and Husky, Devin and Copilot coding agent issue assignment, Claude Code hooks and routines.

- **Replay a recorded week through the tick** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the gap is "a week of live ticks graded" waiting on the install. A recorded week of events (commits, CI results, task changes, git log timestamps) can be fed to the tick dispatcher in daylight at synthetic clock speed, with the same grading.
  Done when: `fm tick replay --days 7` runs the real dispatcher on a recorded event file with a fake clock and prints per-trigger fired/should-have-fired/missed counts, with no timer installed.

- **Grade triggers by shadow mode** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the exam only grades trigger and watch at the end. Shadow mode runs every trigger's decision on each real session event, logging "would have fired" without acting, and settling the outcome later (acted on, dropped, ignored).
  Done when: after one ordinary session, a ledger holds a would-fire row per trigger with a later-settled verdict, and `fm outcomes` splits precision by trigger.

- **Piggyback ticks on session hooks** — FEATURE — value 5 — effort S — risk low — category: reliability
  Why: assumption: the real tick is a systemd timer, so users without the install get nothing. SessionStart, UserPromptSubmit and Stop hooks already run; a debounced catch-up pass there ("tick if last beat is older than the interval") gives the same behaviour with no unit.
  Done when: with no timer installed, starting a session after a 6h gap runs exactly one catch-up tick, and a second start inside the interval runs none.

- **Write a beat file and a missed-tick ledger** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: T-2542 only reads systemd; without systemd there is no liveness signal. A beat row per tick (also from the hook path) gives gaps, which are the measurement of "did it self-trigger as often as it should".
  Done when: `fm doctor` prints "ticks: N in 7d, longest gap Xh, via timer|hook" from the beat file alone.

- **Plant a synthetic event and time the whole chain** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: wild-adjacent but practical; without live events nothing proves the chain. A fixture repo gets a failing CI result or new inbox item and the test times event, trigger, task filed, surfaced in `fm next`.
  Done when: a test in plugin/tests injects an event into a temp state dir and asserts the filed task appears within one tick, with the latency printed.

- **Trigger table as one declarative file with `fm why`** — FEATURE — value 4 — effort M — risk low — category: usefulness
  Why: self-started tasks need an origin stamp so the user can contest them; "why did this appear?" is the first question after any surprise.
  Done when: `fm why T-NNNN` names the trigger row, the event, and the time for any self-started task, and says "user-typed" otherwise.

- **Catch up missed schedules once with a cap** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: assumption: laptops sleep, so N missed ticks become one coalesced run. This also makes the hook-piggyback safe from storms.
  Done when: a replay with a 3-day gap fires each schedule at most once on wake and logs "coalesced 12".

- **Score each trigger against a do-nothing baseline** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the standing steer says a free arm beating the session arm is a top gap; same here, a trigger that fires no better than a fixed clock should be shown.
  Done when: the replay report lists per-trigger precision beside a "fire every N hours" baseline and marks losers.

- **Dry-run any trigger on the last 30 days before it arms** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: assumption: new triggers are the main source of noise; replay on the user's own git and task history says how often it would have fired.
  Done when: `fm trigger add` prints "would have fired 9 times in 30d; 6 had a later commit within a day" before saving.

- **Mark self-started work with its trigger and settle a bet on it** — FEATURE — value 3 — effort S — risk low — category: outcomes
  Why: bets exist but have no trigger dimension (the harness field was just added).
  Done when: `fm outcomes --by trigger` returns rows for self-started tasks.

- **Wild: Touch one file to freeze every trigger** — FEATURE — value 3 — effort S — risk low — category: control
  Why: wild; a single tripwire file the tick checks first gives the user a no-install, no-command kill switch.
  Done when: creating the file makes the next tick log "frozen" and file nothing, and removing it resumes.

- **Wild: A weekly canary event through the real chain** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: wild; a harmless fake failure is injected weekly and the morning note reports whether it was caught, proving liveness without waiting for a real event.
  Done when: the canary appears in the digest as "caught in Xm" or "missed" every 7 days.

- **Wild: Compile a sentence into a trigger row** — FEATURE — value 3 — effort M — risk med — category: usability
  Why: wild; "when CI goes red on main, draft a fix" becomes one table row, shown for a yes before it arms.
  Done when: `fm when "<sentence>"` prints the parsed row and arms nothing until confirmed.

Next question: what does the user do the first morning after a self-started task appears, and which of those steps (undo, why, mute) have no single verb?
Next question: which self-triggering premise holds only when a systemd user session is lingering, and does every non-systemd host get the hook path instead?
