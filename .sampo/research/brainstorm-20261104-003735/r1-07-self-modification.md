# Brainstorm — lens: self-modification

- **Compile spoken triggers into specs** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: the request is "work starts without the user". The user states rules in sentences (e.g. "when CI goes red on main, fix it"). Assumption: a trigger file is something they would rather not hand-write.
  Done when: a sentence is turned by a local model into a trigger spec, `sampo trigger add "<sentence>"` echoes it back as a plain restated rule plus the last 30 days of events it would have matched, and nothing arms until the user confirms.

- **Replay the event history through a trigger set** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: unattended triggers can fire in loops, or never fire. The pack shows drive stops and phantom waits, so firing logic has already been wrong here.
  Done when: `sampo trigger replay --days 30` prints, per trigger, the times it would have fired and the work it would have filed, using only recorded ledgers and zero model tokens.

- **Fix recurring failed-tool-call signatures** — FIX — value 5 — effort M — risk med — category: self-repair
  Why: failed tool calls are up by half (Mission 6 gaps). Assumption: failures cluster by tool and error text.
  Done when: failures are grouped by (tool, normalised error) and a signature seen 3 times in 7 days files one lane task carrying the three transcripts, and a test with a planted recurring failure files exactly one task.

- **Cap the depth of self-triggered work** — SECURITY — value 4 — effort S — risk low — category: loop safety
  Why: assumption: a CI watcher that fixes CI, whose fix triggers CI, can run away overnight. The steers say the drive must not stall, but nothing bounds runaway.
  Done when: every task carries a `trigger_depth`, depth 2 is refused with a morning-card line, and a nightly self-trigger count cap is enforced and tested.

- **Diagnose each drive stop into a class and a fix task** — FIX — value 5 — effort M — risk low — category: drive reliability
  Why: drive stops appeared (0 to 0.1) and T-2873/2900/2901 each fixed a different false-wait by hand.
  Done when: every drive stop writes a stop class (usage limit, false wait, crash, grant needed), and a class seen twice files a fix task naming the transcript evidence.

- **Bundle queued installs under one hashed yes** — FEATURE — value 4 — effort M — risk med — category: installs
  Why: the request says "installs queued for one yes". The standing rule says never interrupt, but installs are user-only grants.
  Done when: pending installs show as one manifest (names, sources, hashes, disk use). The single yes applies exactly that hash; adding or changing an entry invalidates the yes, and a test proves a swapped entry is refused.

- **Detect host and model version changes and run a contract canary** — FEATURE — value 4 — effort M — risk low — category: self-maintenance
  Why: hooks, engine background lists and hook payloads drifted from the host more than once (T-0115, T-0575, T-2873). Assumption: the host version is cheap to read at SessionStart.
  Done when: a changed host version triggers one lane running the roundtrip e2e and the hook bench, filing a task only on diff, and a fake version bump in a test fires it exactly once.

- **Mute triggers the user ignores** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: the lean steers say growth that earns nothing is subtracted. Triggers are a new source of noise.
  Done when: each fired trigger is scored accepted or ignored from the existing close-survival and re-ask signals, and a trigger below the accept floor over 10 fires goes dormant with a one-line notice.

- **Watch the scheduler itself with a dead-man heartbeat** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: if a systemd timer or cron entry is silently lost, no overnight trigger runs and nothing says so.
  Done when: each tick writes a heartbeat, `sampo doctor` names a missing or stale scheduler, and the first session after a gap prints one line stating what was missed.

- **Draft self-edits overnight on the local model into a quarantine branch** — FEATURE — value 4 — effort L — risk med — category: local models
  Why: the user wants local models used without limit for background volume. Cold reads already exist for tower filing.
  Done when: a nightly lane lets qwen3.8-27b draft patches for open `self` tasks on a quarantine branch, and none merges without a green gate and a cold read, shown in the morning card with a count.

- **Wild: Dream replay of failed calls against candidate patches** — FEATURE — value 3 — effort L — risk med — category: self-repair — wild
  Why: assumption: idle local hardware is free. Failed tool calls are recorded with their inputs.
  Done when: an idle-time lane replays a recorded failed call in a scratch worktree with a candidate fix applied and reports "fixed / still fails / worse" per candidate.

- **Wild: Self-trigger on the user's silence** — FEATURE — value 3 — effort M — risk med — category: away mode
  Why: overnight progress is the goal, but "overnight" is a guess. Assumption: last-input time and ledger gaps give a better signal.
  Done when: input idle beyond a learned threshold switches the drive to away mode, and the first keystroke back drops it within one tick, tested with a fake clock.

- **Wild: Trigger that writes its own retirement** — FEATURE — value 2 — effort S — risk low — category: simplicity — wild
  Why: assumption: most triggers are born for one incident.
  Done when: every trigger spec carries a "stop when" predicate, and one that has not fired in 30 days is proposed for deletion in the morning card.

Next question: When a self-triggered lane and the user edit the same file at 2 a.m., which one wins, and where is that recorded?
Next question: What fraction of the last month's hand-started tasks matched a pattern a trigger could have started, and how would we measure it?
