# Brainstorm — lens: blind spots

- **Ask what the trigger layer's states are, and fail when a new one appears** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: T-2525 showed a rule written for open tasks that misfired on others. The class question is "which states did this rule assume?". The pack names task states like open, blocked, deferred and revisit date, but no check that every trigger rule lists each one.
  Done when: adding a task state to the enum without updating the trigger rules' state table fails a unit test, and the test names the rules that lack it.

- **Log every fallback as a named degradation event** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-2532 was a hook silently switching to a fallback. The class question is "what else falls back without telling anyone?". For triggers that means the committed-library fallback, a poller that can't reach its API, and a cheaper model tier. Assumption: the fallbacks share no common log today.
  Done when: forcing each fallback in a test writes one `degraded:<kind>` row, and `fm doctor` prints their counts for the last 7 days.

- **Meter the cost of each unattended fire, hook notes included** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: T-2533 found hook-note chars that the lean ratchet never counted. A self-started lane pays them with no user watching, so the unmetered cost is likely larger there.
  Done when: each fire row carries tokens, injected chars and seconds, and `fm night` prints the median per trigger family.

- **Add a "user typed it" arm for every trigger family in the exam** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: T-2534 added a missing comparison arm (guard-only). The same gap here is that nothing compares triggered work with the same task started by the user. Without it, "work starts without me" has no baseline.
  Done when: `fm exam` reports, per family, pass rate and time-to-start for triggered versus manual starts on the same scenarios.

- **Name the cause when a trigger's precision drops** — FEATURE — value 3 — effort M — risk low — category: attribution
  Why: T-2535 attributed ratchet growth to a commit. Triggers have no equivalent, so a falling precision (`fm triggers` already computes it) names no culprit. The cause may be a rule edit, a host CLI update or a new event shape.
  Done when: a seeded precision drop in a replay test is attributed to the correct change in `fm doctor`.

- **Ablate each trigger family on a schedule and file cleanup candidates** — CLEAN — value 3 — effort M — risk low — category: subtraction
  Why: T-2536 ablates hook features and files a cleanup candidate when the off arm loses nothing. Trigger families are the next obvious thing to measure this way. Assumption: families can be switched off individually.
  Done when: a family with 14 days of fires and no user action files exactly one cleanup task with its fire counts, and never removes it.

- **Turn unattended refusals into a yes-card, not a log line** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: T-2526 made `fm task finish` refuse on a failed full check. A night lane hitting that refusal currently has nowhere useful to send it. Assumption: the refusal reaches only the lane's own log.
  Done when: a lane stopped by a gate refusal adds one line to the morning note with the gate, the failing tests and the one command to retry.

- **Pin the installed unit to the library version it was written for** — SECURITY — value 3 — effort S — risk low — category: installs
  Why: the pack's installs (timers, units) wait for one yes, and a stale unit can outlive the code it was approved against.
  Done when: a unit whose pinned hash differs from the library runs notify-only and `fm doctor` says so.

- **Wild: Write a sealed prediction of the next three trigger asks** — FEATURE — value 3 — effort S — risk low — category: foresight
  Why: wild. T-2505 did this for steers. Do it for triggers: before proposing any, seal three guesses of what the user will want to start by itself, then score them when they ask.
  Done when: a sealed file exists before the proposals, and the next report shows hits and misses.

- **Wild: Have a stub user complain about each fire in one line** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: wild. A tool-less child that sees only the morning note and writes the user's likely irritation per fire. This is a cheap proxy for "was this unwanted?" before real precision data exists.
  Done when: a replayed week produces one complaint or "fine" per fire, and an unwanted trigger is flagged.

- **Wild: Hold a "no tick day" drill that records who noticed what** — FEATURE — value 2 — effort S — risk med — category: ablation
  Why: wild. Switch the tick off for a day with the user's consent and log which tasks, steers and notes were missed. It measures the real value of self-triggering, not the claimed value.
  Done when: a drill writes a report listing items that would have started and the ones the user started by hand.

- **Run cell probes against a deliberately broken fixture** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the 59 cells are to be filled from probes. A probe that cannot fail proves nothing, and the standing rule says a cell counts only when it is real.
  Done when: each filled trigger cell has a planted-fault fixture on which its probe goes red, checked in the sweep.

Next question: which asks did the user have to make this week that a trigger would have made unnecessary, and which of those did a trigger already fire for but fail to land?
Next question: where do two unattended paths (tick, watcher, lane) each assume the other checks something, so that neither does?
