# Brainstorm — lens: reliability

- **Sweep crash points on the drive** — FEATURE — value 5 — effort M — risk low — category: resilience
  Why: the drive runs unattended, waits out usage limits and resumes "where stopped" (steer 3). Nothing shows that a kill at each step boundary resumes cleanly. A random chaos run won't enumerate the boundaries.
  Done when: a test kills the drive at every named checkpoint (claim, edit, prove, finish, ship) and each resume ends in the same final ledger state as an uninterrupted run, with no duplicate records.

- **Probe the guard from the timer's environment** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the guard is the one thing that must hold in bypass mode. Systemd units and hooks run with a thinner PATH and env than an interactive shell. Foreman is also meant to run with no `claude` on PATH. Assumption: no probe covers the guard under those conditions.
  Done when: `fm doctor` runs a canned set of dangerous commands through the guard under `env -i` and the unit's env, and WARNs if any is allowed or the guard errors open.

- **Inject a fake clock into every windowed reader** — FIX — value 4 — effort M — risk low — category: time
  Why: T-2610 added 30-day settlement windows, the timers use "three intervals", and bets settle at 20+ scored. Month ends, DST, suspend/resume and a skewed clock make these readers wrong without raising an error. Assumption: they read the wall clock directly.
  Done when: readers take a clock argument, and tests at DST, month-end, a clock set backwards and a 3-day suspend all give the expected bet, liveness and window results.

- **Reap orphaned children on a drive kill** — FIX — value 4 — effort S — risk low — category: processes
  Why: `claude -p` children are capped (T-0831) and lanes run in parallel. A killed drive or `fm night` tick could leave children that still spend usage and write to ledgers. Assumption: children aren't in a killable process group today.
  Done when: killing the drive with SIGKILL leaves zero descendant processes after 5s, checked by a test that spawns a lane and counts them.

- **Add a stale-safe claim heartbeat to tasks** — FEATURE — value 4 — effort M — risk med — category: concurrency
  Why: parallel lanes, the drive, the night tick and an interactive session can all touch the same task. Assumption: claims are a status flag with no owner or expiry. A dead lane then leaves a task stuck "in progress", or two writers finish it twice.
  Done when: a task claim carries an owner and a heartbeat, a claim whose heartbeat is older than N minutes can be taken over (recorded as a takeover), and a test with two racing claimers shows exactly one winner.

- **Queue publishes and retry them idempotently offline** — FEATURE — value 4 — effort M — risk med — category: network
  Why: `fm ship` pushes to main under a publish grant spent on use, and `fm genesis live` publishes site data. A dropped connection mid-push could spend the grant without publishing, or leave the site stale.
  Done when: with the network cut mid-ship, the grant is not marked spent, a retry later pushes exactly once, and `fm doctor` shows the pending publish.

- **Check repo hazards before a finish or ship** — FIX — value 3 — effort S — risk low — category: git
  Why: finish gates and ships assume a clean git state. A stale `index.lock`, a rebase in progress, a detached HEAD or a submodule dirty state would produce a confusing failure or a wrong diff. The docs proof kind now diffs "to its own id-prefixed commit" (T-2616).
  Done when: each hazard in a test repo produces a named, actionable refusal rather than a stack trace or a wrong proof.

- **Degrade to notes when the disk is full or read-only** — FIX — value 3 — effort S — risk low — category: storage
  Why: the working path here is `/run/user/1000`, a tmpfs. Hooks and ledgers writing under ENOSPC or a read-only home could crash a hook, and a crashed hook could block a session or let a command through.
  Done when: a test with a full tmpfs shows hooks still decide (guard fails closed, notes dropped), and `fm doctor` names the full volume.

- **Calibrate the noise floor for the self-change gate** — FIX — value 3 — effort M — risk low — category: gates
  Why: T-2605 switched to median wall time to remove the LeanKind flake. A gate on a loaded bench still has run-to-run variance it doesn't state.
  Done when: the gate records its measured variance per run, refuses to rule "regressed" or "ok" when the delta is inside it (reporting "inconclusive"), and a loaded-machine test shows no false failure.

- **Replay old ledger fixtures through the current readers** — FEATURE — value 4 — effort M — risk low — category: migration
  Why: recent work keeps changing record shapes (bet harness field, the author tag idea, override states). Assumption: no corpus of old-format ledgers is replayed on each change. Version-skew checks cover installed parts, not old data.
  Done when: a checked-in fixture for each release's ledger shapes loads through the current readers in CI, and adding a required field without a default fails the test.

- **Shadow twin on the last good release (wild)** — FEATURE — value 4 — effort L — risk med — category: drift
  Why: assumption: Foreman judges itself with its own code. A twin pinned at the last released tag consumes the same events read-only and diffs its verdicts (guard, proof, done-gate) against the live install. A disagreement in either direction is flagged.
  Done when: replaying a day of hook events through both versions yields a divergence report, and a planted regression in the live guard shows up as a diff.

- **Bisect Foreman's own regressions automatically (wild)** — FEATURE — value 3 — effort L — risk low — category: self-repair
  Why: Foreman already has the free-arm exam, a Haiku smoke run and a lean ratchet that can say "this got worse". Today a human finds the commit. When a ratchet trips, a lane could bisect the commits since the last green run with the cheapest zero-token arm and file a task naming the culprit.
  Done when: a seeded regression commit is named by the bisect lane and a task is filed that cites it.

- **Replay real poison inputs through every hook (wild)** — SECURITY — value 4 — effort M — risk low — category: robustness
  Why: hooks parse transcripts, tool output and commands that the user didn't write. Pasted credentials (T-2624), truncated JSON, binary output, huge lines and non-UTF-8 all cause "wrong answer, not an error". Assumption: no corpus harvested from real sessions exists.
  Done when: a redacted corpus of malformed events harvested from past sessions runs through all hook events nightly, and any crash, hang past the p95 budget or fail-open on a guard event files a task.

- **Pull the plug on a whole session (wild)** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: T-0798 (transcript repair, crash-loop quarantine) is deferred. A scripted `kill -9` of the terminal mid-edit, then a fresh session start, could be the test that shows whether Foreman's SessionStart picks up the half-finished task without help.
  Done when: after the kill, the next session start names the interrupted task, its uncommitted diff and its next step, and the test passes with no manual cleanup.

Next question: which Foreman state do the drive, timers and hooks all write at once, and has anyone seen it corrupt or lose a record under real parallel lanes?
Next question: if the user's machine were suspended for a weekend mid-task, which of Foreman's clocks (usage windows, bet settlement, timer liveness, claim expiry) would give a wrong answer on wake?
