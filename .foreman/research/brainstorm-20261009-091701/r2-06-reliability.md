# Brainstorm — lens: reliability

- **Fail closed on hook crashes with a degraded-mode contract** — FEATURE — value 5 — effort M — risk med — category: hooks
  Why: the guard is the safety layer in bypass mode, but the pack shows only latency benches and a "watchdog" idea; assumption: an uncaught exception or timeout in a PreToolUse hook currently lets the command through or silently skips it. Define per-hook fail-open or fail-closed policy (guard closed for destructive categories, drive open), and record each degraded decision in the ledger.
  Done when: a test injects an exception and a hang into the guard, and `rm -rf` is refused while a read-only `ls` still runs; both events appear in the ledger as `hook_degraded`.

- **Version and migrate all on-disk state** — FEATURE — value 5 — effort M — risk med — category: state
  Why: Foreman releases every few days (1.2.8 → 1.2.16) across many consumer projects (JARVIS, others) with briefs, STATE, ledger and decisions on disk; no schema version is mentioned. Stamp each file with a schema version, and make `fm doctor` run ordered migrations with a backup.
  Done when: a fixture project written by 1.2.8 opens under the current version, is migrated with a backup, and `fm doctor` is clean; a downgrade attempt is refused with a clear message.

- **Make state writes transactional across files** — FIX — value 4 — effort M — risk med — category: durability
  Why: a task close touches the brief, STATE, ledger and queue; a crash or a concurrent lane merge can leave them disagreeing. T-0403 shows lanes and the main thread already write concurrently. Use a write-ahead intent file plus atomic renames, and replay or roll back on the next start.
  Done when: a test kills the process at each step of `fm task done`, and the next `fm` call either completes or rolls back so that `fm doctor` reports no divergence.

- **Lock and fence concurrent writers** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: builder lanes, `fm run`, `fm night`, `fm serve` and the desktop app all mutate the same central store; the pack shows a merge refused over a dirty checkout, which suggests ad hoc coordination. Add per-project advisory locks with owner and expiry, and a fencing counter so a stale writer is rejected.
  Done when: 20 parallel `fm log` and `fm task` calls from separate processes leave a ledger with no lost or interleaved entries, and a writer holding an expired lock is rejected.

- **Detect and recover a wedged or dead session** — FEATURE — value 4 — effort M — risk low — category: supervision
  Why: the drive keeps work going and the user asked that "long-lived jobs and an empty queue never leave a session idle", but a hung tool or dead headless `claude -p` is a different failure from idleness. A heartbeat per active task lets `fm run` and `fm serve` kill, checkpoint and restart from the resume point, with bounded retries.
  Done when: a headless run whose child is `SIGSTOP`ped is detected within the timeout, restarted from the checkpoint, and its task finishes; after N failed retries it is blocked with a reason.

- **Run a continuous invariant checker over live state** — FEATURE — value 4 — effort M — risk low — category: integrity
  Why: the user's steer "cleanup requests never got done — trace why" and the blocked-but-active tasks show state can drift from reality. Define invariants (exactly one active task, every step evidence resolves, no lane without a task, every queued dependency exists) and check them on SessionStart and in `fm night`, with auto-repair for the safe ones.
  Done when: seeded violations of five invariants are each reported by name on the next session start, and the safe ones are repaired with a ledger entry.

- **Contract-test Foreman against Claude Code's hook and settings surface** — FEATURE — value 5 — effort M — risk low — category: compatibility
  Why: T-0316 (re-run a lane after a Claude Code update) is blocked, the UI mod patches Claude Code internals, and the guard depends on hook payload shapes. Keep recorded payload fixtures per Claude Code version, plus a nightly probe against the installed one, and have `fm doctor` flag a version outside the tested range.
  Done when: replaying fixtures from three Claude Code versions passes, and a mutated payload field fails the contract test with the field named.

- **Quarantine the mod and UI from the core on failure** — FIX — value 3 — effort S — risk low — category: isolation
  Why: foreman-ui is installed into Claude Code, and T-0418 shows a stale installed version. A crash in the band or pane must never affect hooks or the guard. Run the view model with a timeout and a last-good cache, and disable the mod automatically after repeated render errors, with a one-line notice.
  Done when: a thrown error in the pane leaves the session usable, `fm ui --json` still answers, and the mod is auto-disabled after 3 failures and re-enabled by `fm doctor --fix`.

- **Ship a self-test that runs on the user's machine after every install or upgrade** — FEATURE — value 4 — effort S — risk low — category: install
  Why: the installer touches `~/.claude`, Python, Homebrew or `uv`, and plugins across Linux, macOS and WSL, and the gates named in the pack run only in the dev repo. Run a smoke roundtrip in a temp project (capture, plan, guard refusal, resume after a simulated compact) and roll back the wiring if it fails.
  Done when: the installer ends with a pass or fail summary, and a deliberately broken hook path makes the install roll back to the previous manifest.

- **Wild: Run a chaos monkey inside the real session** — FEATURE — value 3 — effort M — risk med — category: chaos
  Why: wild; there is a chaos-test-resume idea, but this one injects faults into a live disposable project (killed hooks, a full disk, a clock jump, a corrupt brief, a lost network) while a simulated task runs. Pass means Foreman reports the fault, degrades safely and completes.
  Done when: `fm chaos` runs 10 fault types against a scratch project and prints a table where every row is "recovered" or "failed safe", with none left silent.

- **Wild: Keep a black-box flight recorder for the last 200 hook events** — FEATURE — value 3 — effort S — risk low — category: diagnostics
  Why: wild; the friction digest relies on a ledger written by the code that may itself be failing. A small ring buffer written independently of the ledger holds the raw hook inputs, decisions and timings, so that when a user says "it refused wrongly" or "it hung", `fm crash-report` bundles a redacted capsule for a bug brief.
  Done when: after a forced hook failure, `fm crash-report` produces a redacted file with the last events including the failing one, and it contains no secrets according to `fm secrets`.

- **Wild: Hold a keep-alive twin that takes over when the main drive dies** — FEATURE — value 3 — effort L — risk high — category: failover
  Why: wild; `fm serve` runs as a systemd user unit and the user wants no idle sessions. A standby process watches the primary's lease; on loss it resumes the active task from the last checkpoint on the same lane, so an overnight run survives a reboot, an OOM kill or a dropped Remote Control.
  Done when: killing the primary mid-task with `SIGKILL` leads the standby to claim the lease within 60 seconds and finish the task from the recorded step, with a single ledger lineage and no duplicate commit.

- **Prove the done-gate itself against a corpus of known-bad closures** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: an assumption: earlier ideas verify the verifiers (mutation, vacuous proof), but nothing keeps a regression suite of false "done" claims. Keep a corpus of closures that must be refused (a no-op diff, evidence from another task, a stale gate run, edited criteria) and run it in the release gate.
  Done when: each corpus case is refused by `fm task done` with its named reason, and removing any gate check makes at least one case fail.
