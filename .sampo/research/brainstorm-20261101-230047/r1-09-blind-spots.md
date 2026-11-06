# Brainstorm — lens: blind spots

- **Show each trigger's last-fired time against its expected cadence** — FEATURE — value 5 — effort S — risk low — category: observability
  Why: T-2532 (a hook event silently off) was a user ask no brainstorm predicted. The night tick "logs only when something happens", so a dead timer and a quiet day look the same. Blind-spot question: what fails silently here?
  Done when: with the night timer disabled in a scratch HOME, `fm doctor` marks it "overdue by N h" and still shows green for a quiet but live timer.

- **Make the watcher tell you when it goes blind** — FIX — value 5 — effort M — risk low — category: reliability
  Why: assumption: `fm ci-watch` and issue watchers depend on a `gh` token, network and an API quota. When any of them lapses, the watch ends with no signal, the same class as T-2532.
  Done when: with an expired or absent token, the next tick writes a "watcher blind: reason" line that `fm next` shows once, and a planted CI failure is not reported as "all green".

- **Check a trigger's premise against every task state before it fires** — FIX — value 4 — effort M — risk med — category: correctness
  Why: T-2525 found that T-2334's start-point fix was only valid for open tasks. A trigger that picks up "tasks" will hit blocked, deferred and closed ones too.
  Done when: a test table runs each trigger kind against open, blocked, deferred, closed and dropped tasks and asserts the intended action for each.

- **Search for an existing feature before filing a trigger task** — CLEAN — value 4 — effort S — risk low — category: planning
  Why: T-2534 was already built (the plain arm is Claude plus the guard), and Mission 3 found 3 of 5 briefs built or with no failure behind them. Several triggers here (`fm night`, `fm ci-watch --last-ship`, `fm triggers`) already exist.
  Done when: filing a trigger task prints the matching verb and its file:line, or "none found", and a task for an existing verb is refused with that pointer.

- **Tag every task and lane with the trigger that started it** — FEATURE — value 4 — effort S — risk low — category: attribution
  Why: assumption: `fm triggers` groups captures by trigger, but nothing shows whether outcome survival differs for self-started work versus user-asked work. Self-started work can't be judged without that split.
  Done when: `fm outcomes --by origin` splits held and reopened tasks into user, schedule, file, ci and issue.

- **Stop a trigger from re-firing on its own output** — FIX — value 4 — effort M — risk med — category: safety
  Why: assumption: a file trigger over a path the lane writes, or a CI watcher that fixes CI and so produces new CI runs, can loop. The mission's "Break trigger storms" idea covers budgets, not self-causation.
  Done when: a test where a lane's own commit matches its trigger produces zero further fires, and a log line names the suppressed one.

- **Replay missed fires after sleep or reboot, with a cap** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: assumption: the machine is a laptop. A timer that missed three nights should run once on wake and say so, not skip silently or run three times.
  Done when: with the clock jumped over two scheduled times, exactly one catch-up runs and the morning note says "missed 2, ran 1".

- **Check scheduled times across DST and time-zone changes** — FIX — value 3 — effort S — risk low — category: correctness
  Why: assumption: timer units use local time, and zero or double fires on DST days are the classic bug. No existing idea covers it.
  Done when: tests under faked clocks for a spring-forward day, a fall-back day and a zone change show a daily 02:30 job fires exactly once each day.

- **Check the site's "work starts without you" claim against the trigger log** — SECURITY — value 3 — effort S — risk low — category: proof
  Why: T-2504 (proof before presentation) was an unpredicted ask. Any public statement about self-triggering should carry its own count.
  Done when: the sweep goes red if the page says triggers fired and the log has none in the last 30 days, and green with the count printed otherwise.

- **Wild: Fire a harmless fake CI failure weekly to prove the whole chain** — FEATURE — value 4 — effort M — risk med — category: liveness
  Why: wild. A planted event travels through watcher, trigger, lane and morning note, and proves the chain without waiting for a real failure.
  Done when: the weekly canary shows up in the morning note tagged "canary", and a skipped one turns `fm doctor` red.

- **Wild: Propose schedules from the user's own repeated habits** — FEATURE — value 3 — effort M — risk low — category: unspoken needs
  Why: wild. The user's "asked" stream shows habits such as running `fm next` at the same time of day. Foreman could offer "you do this at 9am, install a timer?" as one queued yes.
  Done when: after 5 same-time repeats, one install proposal appears with its evidence, and declining it is remembered.

- **Wild: Run a dry-run week against the user's real history before any timer installs** — FEATURE — value 4 — effort L — risk med — category: preflight
  Why: wild. The pack's trigger-replay idea covers one trigger. This version replays the whole proposed trigger set and prints "would have started 14 lanes, 11 useful, 3 noise" before the user says yes.
  Done when: the install card shows the replayed fire count and precision for the last 30 days, computed from recorded events.

- **Diff installed units against what the user said yes to** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: assumption: queued installs are the one place self-triggering touches the system. A later edit to a unit file, or an extra unit, would run unattended work the user never approved.
  Done when: editing an approved unit's `ExecStart` makes `fm doctor` name the file and the difference, and the tick refuses to run it.

Next question: What does each trigger do when the thing it depends on (token, network, disk, clock, installed library) is missing, and who is told?
Next question: Which unattended outcomes has the user never seen with their own eyes, and what would show them without a session?
