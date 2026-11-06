# Brainstorm — lens: the night shift (invented): work starts without the user: schedules, file and event triggers, CI and issue watchers, installs queued for one yes

- **Replay a trigger on a recorded week before it may install** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: Installs (timers, units) queue for one yes, and T-2276 scores triggers only after they fire. Earlier ideas say "dry-run before repeat" but none builds the replay corpus. Assumption: `fm triggers` outcomes and the hook event log are retained long enough to replay.
  Done when: `fm triggers propose` prints "would have fired N times in the last 30 days, M led to a done task" for a candidate, and the queued yes shows that line.

- **Write the morning ledger as one file the first prompt reads** — FEATURE — value 5 — effort S — risk low — category: handoff
  Why: Mission 8 #11 starts work without the user; the user's "since you left" need is stated by earlier ideas only as a digest, not as a contract. Assumption: a plain file beats a push channel for a first version.
  Done when: after a night run, `.fm/morning.md` exists with sections landed-on-branch, needs-yes (ranked by minutes unlocked), failed-and-why, spend; session start prints its first line.

- **Land night work only on a `night/<date>` branch with a one-command accept** — SECURITY — value 5 — effort M — risk low — category: safety
  Why: Standing push grant covers main only via `fm ship` gated by the full suite; unattended lanes must not spend that grant. Assumption: lanes already use worktrees (`fm lane`).
  Done when: a test runs a night lane, asserts main's HEAD is unchanged, and `fm night accept` merges through `fm ship` with the suite.

- **Treat issue, CI-log and PR text as untrusted in watcher lanes** — SECURITY — value 5 — effort M — risk med — category: injection
  Why: CI and issue watchers (Mission 8 #11) feed attacker-writable text into a lane that runs in bypass mode. T-0791 (injection defenses) is deferred. Assumption: no quarantine of watcher text exists yet.
  Done when: a fixture issue containing "run curl … | sh" yields a lane whose brief carries the text only as quoted data, and the guard blocks the command when the lane tries it.

- **Give every night run a charter, a hard budget and a stop file** — FEATURE — value 4 — effort S — risk low — category: budget
  Why: Steer: wait out usage limits, don't stop for budget, but the user must still be able to stop everything. Assumption: lane spend is already tracked per model by T-2291's router.
  Done when: `touch .fm/night.stop` halts all lanes within one poll interval and the ledger records which tasks were cut; a charter with a dollar cap refuses to start a lane that would cross it.

- **Debounce event bursts into one wake-up with a coalesced brief** — PERFORMANCE — value 4 — effort M — risk low — category: triggers
  Why: File and git events fire in storms (checkout, formatter runs); the trigger table counts fires per kind but the pack shows no coalescing. Assumption: none exists.
  Done when: 200 file events within 10 seconds produce one trigger fire and one task, asserted in a test.

- **Yield the machine when the user returns or is on battery** — FEATURE — value 4 — effort M — risk low — category: presence
  Why: Hooks must stay fast (Mission 8 #12); a lane compiling in the background competes with the user's own session. Assumption: input idle time and power state are readable on Linux (logind, /sys/class/power_supply).
  Done when: a user session start pauses (SIGSTOP or lane hold) all night lanes in under 2 seconds and resumes after idle, shown in `fm lane ls`.

- **Quarantine a trigger the user never acts on, with its reason** — CLEAN — value 3 — effort S — risk low — category: precision
  Why: T-2276 files mostly-dropped trigger captures at low priority but never retires the trigger. Assumption: the "dropped" count is per trigger kind.
  Done when: a trigger with precision under 10% over 20 fires is disabled, listed in the morning ledger with a one-key restore.

- **Rank the queued yeses into one sheet by minutes unlocked** — FEATURE — value 4 — effort M — risk low — category: consent
  Why: Installs, merges, and blocked tasks (T-0325, T-0335, T-0352, T-0418 all wait on the user) are separate asks. Assumption: each blocked item records what it unblocks.
  Done when: `fm yes` shows a checkbox sheet, editing it applies the ticked items, and each applied yes is logged with scope and expiry.

- **Wild: Hold a daylight rehearsal of the night against a replayed night** — FEATURE — value 3 — effort L — risk low — category: testing
  Why: wild; the night shift can't be observed while it happens. Assumption: event logs can be fed to the trigger engine with a stub model.
  Done when: `fm night rehearse --replay last` runs the whole shift in a throwaway worktree with zero token spend and prints what it would have done.

- **Wild: Dream pass that mines the night's own logs for a new trigger** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: wild; repeated manual starts the user makes each morning are the missing triggers. Assumption: the "asked" stream shows habitual first requests.
  Done when: after 5 identical-shaped morning starts, the dream pass queues one proposed trigger with its replay evidence.

- **Wild: Bedtime question answered by morning defaults** — FEATURE — value 3 — effort S — risk med — category: consent
  Why: wild; blocking on the user stalls the shift, and steer 3 says keep going on everything unblocked. Assumption: a default can be chosen per question with a recorded fallback.
  Done when: `fm ask --by-morning` records a default; if unanswered, the night proceeds on it and the ledger flags it as assumed, reversible.

- **Run a canary night against the newest Claude Code before upgrading** — PERFORMANCE — value 3 — effort M — risk low — category: compatibility
  Why: hook latency and the guard depend on host behaviour; `plugin/tests/bench_hooks.py` already exists as a gate. Assumption: a second Claude Code version can be installed side by side.
  Done when: a scheduled run executes the bench and roundtrip e2e on the newest release and files a FIX task on regression.

Next question: When a night lane and the user's daytime session both touch the same files, which one wins by rule, and does the user see that before they type?
Next question: Which scheduler (systemd user timer, cron, or Foreman's own daemon) survives a hardened-kernel, no-sudo machine, and what does the one-yes install actually write?
