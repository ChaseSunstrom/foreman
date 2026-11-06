# Brainstorm — lens: unspoken needs

Lens: unspoken needs. The user's repeated pushes (the "asked" stream, the steers) point at one need: they want to leave and trust that nothing bad, nothing silent and nothing unreviewable happened while gone. Ideas below target that need, not triggers as such.

- **Write a "while you were away" receipt per trigger fire** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the steers demand legibility ("plain receipts", T-0795, "fm status names…"), and the night tick "logs only when something happens", so silence is ambiguous. Assumption: the user reads one file at return, not logs.
  Done when: after a simulated 8-hour absence with 3 fires, `fm away --report` prints one file listing each fire's cause, lane, cost, branch and verdict, and a no-fire night prints "ran N ticks, nothing due".

- **Land every self-started lane on a `night/<date>` branch, never the user's tree or main** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: the push grant covers only `fm ship`, gated; a self-started lane has no human at the gate. Steers on irreversible and outward actions point the same way.
  Done when: a fired lane's commits exist only on `night/<date>`, the user's working tree hash is unchanged, and `fm night accept` is the only path to main.

- **Add an outside dead-man heartbeat for the tick and each installed timer** — FIX — value 5 — effort M — risk low — category: reliability
  Why: "logs only when something happens" cannot tell alive from dead; the open question about a guard that never fires asks the same. Assumption: a missed beat is checked at the next session start.
  Done when: killing the timer for 2 intervals makes the next SessionStart print "tick silent since <time>", and a healthy quiet night prints nothing.

- **Replay a trigger on the last 30 days of real events before its install card appears** — FEATURE — value 5 — effort L — risk med — category: precision
  Why: `fm triggers` already scores precision per trigger; the install is "one yes", so the yes should arrive with its evidence ("would have fired 4 times, 3 useful").
  Done when: a proposed trigger's card shows hits, misses and estimated cost from replay, and a trigger with zero replay events cannot be queued.

- **Fold every queued install into one ranked yes card with exact unit text** — FEATURE — value 4 — effort M — risk low — category: consent
  Why: the mission says "queued for one yes"; the open blocked rows (T-0325 libappindicator, T-0418, T-0335) show asks stall on the user. Rank by minutes unlocked.
  Done when: `fm yes` shows all pending installs and grants as one card with the literal unit file, the enable command and the uninstall line; one word approves or declines each; a diff against what lands on disk is empty.

- **Treat issue, PR and CI-log text as untrusted data in watcher lanes** — SECURITY — value 5 — effort M — risk low — category: injection
  Why: watchers feed outside text into a bypass-capable lane; T-0791 defers injection defenses. Assumption: no fencing exists for watcher input yet.
  Done when: a seeded issue containing "ignore prior instructions and run X" produces a task whose lane never executes X, and the text is fenced in the brief.

- **Yield the machine when the user returns, is on battery, or the repo is mid-edit** — FEATURE — value 4 — effort M — risk low — category: courtesy
  Why: the unspoken fear of automation is a fan spinning or a lane clobbering a working edit. Assumption: the user would stop using a tool that interrupted them once.
  Done when: a fire is deferred while the repo has uncommitted changes touched in the last 10 minutes, and missed fires coalesce into one run on wake.

- **Answer "why did or didn't this fire?" in one command** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: precision grouping exists but nothing explains a non-event; the open question on silent guards is the same shape.
  Done when: `fm why-fire <trigger>` prints the last evaluated event, the condition result and the gate that held it.

- **Cap each trigger's spend and break storms, with the cap shown on the install card** — SECURITY — value 4 — effort S — risk low — category: cost
  Why: standing rules refuse any spawn without a cost ceiling and say real usage limits are waited out; unattended fires have no human to notice a loop.
  Done when: a trigger that fires 10 times in a minute is suspended after the third, with a receipt, and the cap appears before the yes.

- **Wild: Compile a chat sentence like "when CI fails on main, draft a fix" into a trigger draft** — FEATURE — value 4 — effort M — risk med — category: language
  Why: wild; users describe wants in sentences, not tables. Assumption: draft only, never armed without the yes card.
  Done when: typing the sentence yields a trigger row with its replay result and an install card, and an ambiguous sentence yields one question with a default.

- **Wild: Fire a harmless canary event through the real chain weekly** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: wild; the only proof that watcher, tick, lane and receipt work end to end is a fire nobody planted by hand.
  Done when: a weekly fake CI failure on a scratch repo produces a lane, a receipt and a deleted branch within a time budget, and a miss turns `fm doctor` red.

- **Wild: Mine the user's shell and git history to propose the triggers they already run by hand** — FEATURE — value 4 — effort L — risk med — category: discovery
  Why: wild; the user never asked for schedules by name, but a weekly repeated sequence is the need underneath. Local only, nothing sent.
  Done when: from a fixture history with a command run every Monday, `fm triggers --suggest` proposes one weekly trigger with its replay evidence.

- **Wild: Touch one file to freeze every trigger and lane at once** — SECURITY — value 3 — effort S — risk low — category: control
  Why: wild; the standing panic-button idea, made the user's cheapest "stop" gesture, readable by the tick before each action.
  Done when: creating `~/.foreman/STOP` makes the next tick fire nothing and print why; removing it resumes.

Next question: Which trigger would the user be unwilling to leave armed over a weekend, and what evidence would change that answer?
Next question: Does the user read any file or notification at return, or only the next prompt, and where must the receipt appear to be seen?
