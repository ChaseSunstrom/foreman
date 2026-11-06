# Brainstorm — lens: reliability

- **Re-judge scheduled intents when they fire** — SECURITY — value 4 — effort M — risk low — category: native tools
  Why: assumption: wiring in CronCreate, ScheduleWakeup, RemoteTrigger and Monitor means a command or prompt is approved once and runs later. By then the task may be dropped, a veto added, or the step moved on. The guard only judges at creation today.
  Done when: a wake scheduled for task T-x, then T-x dropped, fires as a logged no-op. A scheduled command that a newer veto forbids is refused at fire time.

- **Pair every persisted format with its readers in a round-trip contract** — FIX — value 4 — effort M — risk low — category: state integrity
  Why: T-0749 and T-0750 were both a writer emitting `✗ exit N` while readers matched `exit N`. Bugs from format mismatch recur in the commit log.
  Done when: a registry lists each stored format with its writers and readers. A test feeds every writer's real output to every reader. Changing a writer's output without updating a reader fails CI.

- **Pin the hook interpreter with a PATH-proof launcher** — FIX — value 4 — effort S — risk low — category: hooks
  Why: the installer puts 3.12.7+ `python3` in `~/.local/bin`, and hooks resolve `python3` at run time. An activated venv, an older system python, or a planted `python3` earlier on PATH breaks or hijacks every hook (assumption: hook commands use a bare `python3`).
  Done when: with PATH starting with a fake `python3` that exits 1, a PreToolUse hook still runs under the recorded absolute interpreter. `fm doctor` reports the pinned path.

- **File every idle-while-queued incident with the liveness path that failed** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: the user asked "make sure it doesn't sit idle like it is" (T-0758). Existing ideas add more wake paths but none learn which one failed. Each path (Stop block, Monitor, ScheduleWakeup, send-keys, push) would log armed/fired/acked.
  Done when: forcing an idle gap with a queued task creates a FIX task naming the path that was armed but never fired, with the last 20 events attached.

- **Run every new native-integration gate in shadow mode before it can block** — FEATURE — value 4 — effort S — risk low — category: rollout
  Why: T-0759 (step drift) and the new Monitor/Artifact paths all add gates. A false block in bypass-mode autonomy costs more than a miss. Shadow mode logs would-block decisions and `fm doctor` shows the false-positive rate. Promotion happens once it passes a threshold on real sessions.
  Done when: the step-drift check ships as log-only. After the threshold it flips to blocking and the setting records the evidence that justified it.

- **Add a per-tool circuit breaker for native tools** — FEATURE — value 3 — effort S — risk low — category: native tools
  Why: assumption: Artifact, PushNotification and RemoteTrigger can fail (plan limits, no remote, offline). Retrying them every turn wastes tokens and clutters the transcript. A failed tool is skipped for a TTL and tried again with one cheap probe.
  Done when: after two Artifact failures the next ten turns make zero Artifact calls, `fm doctor` shows "open until HH:MM", and a successful probe closes the breaker.

- **Replay recorded hook payloads through the old and new release and diff the decisions** — CLEAN — value 4 — effort M — risk low — category: release gate
  Why: Foreman ships often (1.2.17 to 1.2.27) and the guard is the highest-stakes code. A scrubbed corpus of real payloads, run on both builds, makes any changed allow/deny/inject explicit.
  Done when: `release.py` prints a decision diff and fails on any unreviewed change from deny to allow.

- **Handshake the protocol version between the UI, desktop app and `fm serve`** — FIX — value 3 — effort S — risk low — category: UI
  Why: a long-lived browser tab or an older Desktop AppImage can talk to a newer server (assumption). The mod is also pinned at 0.6.1 against newer state (T-0418).
  Done when: a client with an older version shows "reloading for v1.2.28" and reconnects without blanking. An incompatible client gets a readable message instead of a broken view.

- **Detect API brownouts from Foreman's own hook telemetry and ride them out** — PERFORMANCE — value 3 — effort M — risk med — category: resilience
  Why: PostToolUseFailure and turn latency are already visible to hooks. A rising failure rate or latency tells Foreman to stop launching new expensive lanes and fall back to cheaper work until it clears (assumption: the signals are separable from task failures).
  Done when: a replayed brownout trace pauses new lanes within N events and resumes after recovery. The band shows "API degraded".

- **Wild: Rehearse the resume at every step boundary with a cold cheap agent** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: wild. Resume after `/compact` is a core promise. A haiku child that gets only the resume capsule and must state the next action catches capsule defects while the session is healthy, not after a crash.
  Done when: a deliberately corrupted capsule makes the rehearsal disagree with the plan pointer and raises a visible warning. A good capsule passes at under 2 seconds of added wall time, because the check runs in the background.

- **Wild: Buy redundancy for risky unattended work** — FEATURE — value 3 — effort L — risk med — category: night runs
  Why: wild. The history gives a failure probability per task type. For a queue task above a threshold before a night run, Foreman runs a second independent lane and keeps the one that passes the gate, deciding on prior failure rate and budget.
  Done when: a high-risk task in `fm night` shows two lanes and the cost, and the gate-passing diff wins.

- **Wild: Print a nightly reliability receipt that names every silent recovery** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: wild. Retries, wake rescues and breaker trips hide success from the user, who asked for "keep going until done". One line per night, e.g. "7h12m, 0 idle min, 3 rescues (wake ×2, resume ×1)", makes reliability visible and trendable.
  Done when: the morning SessionStart line lists the run's recoveries by type, and the count matches the ledger.
