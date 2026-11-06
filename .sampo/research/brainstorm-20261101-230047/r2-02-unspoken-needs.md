# Brainstorm — lens: unspoken needs

- **Show what woke up while I was away, in one file** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: the user's words keep asking for receipts ("what the guard stopped", "morning ledger", "fm triggers groups captures by trigger"), yet self-started work has no single place that says what started, why, and what it cost. Unattended work the user can't read is work they won't trust. Assumption: nothing like a per-trigger origin stamp exists on tasks today.
  Done when: after a simulated overnight tick that fires two triggers, `fm triggers --since last-seen` prints each fire with its origin, task id, spend and outcome, and a task created by a trigger carries that origin field.

- **Dry-run every trigger on last week before it can install** — FEATURE — value 5 — effort M — risk low — category: safety
  Why: install requests are "queued for one yes", but the user can't judge a yes without knowing how noisy the trigger would have been; the pack's own lesson is that ideas often have no failure behind them. Precision is already tracked by `fm triggers`, so the replay data exists.
  Done when: `fm trigger preview <spec>` replays the last 30 days of recorded events, prints would-have-fired count and how many matched an action the user actually took, and the install card embeds that line.

- **Put the unit text and uninstall line on the install card** — FEATURE — value 4 — effort S — risk low — category: consent
  Why: the user said installs get "one yes"; a yes on a name alone is a blind yes, and the standing steers fence anything outward-facing. Assumption: cards currently name the install, not its exact bytes.
  Done when: a queued timer/unit card shows the exact unit file, the enable command and the exact removal command, and a test asserts the card text equals what would be written.

- **Defer fires while the user is mid-flow, coalesce missed ones** — FEATURE — value 4 — effort M — risk med — category: courtesy
  Why: the standing rule "pause the shift when the user comes back" and the sleep/reboot gap ideas imply the user dislikes being competed with; a trigger firing in their tree during editing is the worst surprise. Assumption: the tick today fires regardless of recent user activity.
  Done when: with a recent edit in the repo, a due trigger is held and logged as "held: user active"; after a simulated 3-day suspend, N missed runs of one schedule run once.

- **Make self-started work land on its own branch/worktree only** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: the user granted push to main only via `fm ship` per task; a watcher-started lane must never be able to touch their working tree or main. Issue and CI text are attacker-controlled input to the model.
  Done when: a trigger-started lane runs in a fresh worktree on `night/<date>`, a test shows its attempt to write to the primary tree is refused, and issue text reaches it fenced as data.

- **Explain why a trigger did not fire** — FEATURE — value 4 — effort S — risk low — category: debuggability
  Why: the pack notes "the night tick logs only when something happens", so silence is ambiguous: dead timer or nothing to do. The user will ask "why didn't it run?" and have no answer.
  Done when: `fm triggers why <name>` reports last tick time, the condition evaluated, and the reason (not due / held / budget / disabled / tick dead), with a heartbeat showing the tick itself is alive.

- **Cap each trigger's spend and break storms** — SECURITY — value 4 — effort S — risk low — category: cost
  Why: a CI watcher on a flaky job or an issue burst could spawn repeated lanes against the user's usage limit; steers say waiting out limits is fine but burning them silently is not. Assumption: no per-trigger budget exists.
  Done when: a trigger firing 10 times in a minute starts one lane, logs the debounced rest, and refuses a fire past its configured cost line with a named reason.

- **Quarantine a trigger the user never acts on** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the lean steers and "sunset clock" ideas say growth must earn its keep; `fm triggers` already measures precision, so closing the loop costs little.
  Done when: a trigger with 0 acted-on fires over N fires moves to "proposed retire" on the next digest and stops firing only after one yes.

- **Wild: compile "whenever X, do Y" typed in chat into a trigger draft** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: assumption: users express schedules as sentences mid-task and then forget; the unspoken need is not writing a cron string. wild
  Done when: the prompt "whenever CI goes red on main, look at it" yields a queued trigger draft with a preview line, installing nothing until the yes.

- **Wild: mine the user's shell and git history for the triggers they'd have written** — FEATURE — value 4 — effort M — risk med — category: discovery
  Why: repeated manual sequences (rebase-then-test every Monday) are demand never voiced; matches the local-first, nothing-sent posture. wild
  Done when: `fm triggers suggest` lists at least one candidate from a fixture history with its measured repetition count, all computed locally.

- **Wild: fire a harmless fake CI failure weekly to prove the chain** — FEATURE — value 3 — effort M — risk med — category: liveness
  Why: "a guard that never fires" question applies equally to watchers; silence can't tell alive from blind. wild
  Done when: the weekly canary event travels watcher → trigger → lane (stubbed, no model spend) and `fm doctor` shows its last round-trip time, going red if overdue.

- **Write one morning note a person would write** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user steers toward plain words ("what the guard stopped in plain words"); a note ranking yeses by minutes unlocked and saying what was left alone is the shift's face.
  Done when: the first session of the day shows a note under 12 lines listing ran/held/waiting-on-you, each with one-word answers for pending installs.

- **Check the "work starts without you" claim against the trigger log** — FIX — value 3 — effort S — risk low — category: honesty
  Why: the standing "proof before presentation" steer; the site claims self-triggering and the user installed the timers, but no check ties the claim to real fires.
  Done when: the sweep goes red if the public claim exists and the log shows zero acted-on self-started tasks in 30 days.

Next question: Which of the 59 empty cells does a real overnight tick ever touch, and what would the user need to see to believe one of them is real?
Next question: If the user is away for a week, what should a self-triggering Foreman refuse to do on its own no matter how good the trigger looks?
