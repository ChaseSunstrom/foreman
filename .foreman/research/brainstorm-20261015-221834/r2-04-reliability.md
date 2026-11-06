# Brainstorm — lens: reliability

- **Run the whole suite in a hermetic sandbox that trips on any escape** — FIX — value 5 — effort M — risk low — category: test safety
  Why: T-0990's `~/.local/bin` fallback let test runs reach the paid `claude` binary after a test replaced PATH. A per-binary lockout fixture is already proposed. This goes wider: run the suite under `unshare`/`bwrap` with a temp HOME, no network, and a stub `claude`. Any touch of the real HOME, binaries or network fails the run.
  Done when: a test that execs the real `claude` or writes to the real `~/.claude` fails the suite, and a clean run passes.

- **Fuzz every state reader with corrupt input** — FIX — value 4 — effort M — risk low — category: robustness
  Why: a single malformed ledger time crashed `gather()` (fixed in T-1026) after the fact. Assumption: other readers (ledger, tasks, hints, by-pid records, snapshots) have the same class of bug.
  Done when: a generated suite feeds truncated, binary, wrong-type and huge lines to each reader, and none raise or hang.

- **Add a single-owner lease to tasks and worktrees** — FEATURE — value 5 — effort M — risk med — category: concurrency
  Why: the pack shows a harness session grabbing the queue from the working session (shot.py driven by the Stop hook). Resume and parallel builders add more sessions. Assumption: nothing stops two sessions claiming one task or worktree.
  Done when: a second session claiming a leased task is refused with the owner's pid and age, and a dead owner's lease is reclaimed after its heartbeat expires.

- **Run every hook twice and require identical state** — FIX — value 4 — effort S — risk low — category: idempotence
  Why: SessionStart appended the same exports on every start/compact (8x seen in the Bash prelude). The same bug can exist in any hook that writes state.
  Done when: a test replays each hook's recorded stdin twice, and state bytes after the second run equal those after the first, or the hook is on an explicit allowlist.

- **Reap orphaned `claude -p` children and their process groups** — FIX — value 4 — effort M — risk med — category: process hygiene
  Why: fan-out verbs, brainstorm children, a capped-child salvage task (T-0831) and killed sessions all point at leaked headless children that keep spending money. Assumption: children aren't tracked by pgid today.
  Done when: killing a parent session leaves no descendant of its fan-out alive after 10 seconds, and `fm doctor` lists any strays.

- **Preflight disk, inodes and worktree budget before dispatching builders** — FEATURE — value 3 — effort S — risk low — category: resources
  Why: many worktrees plus snapshots and backups are planned (warm pool, copy-on-write, incremental tidy). Assumption: a full disk mid-build today leaves a half-written worktree and ledger.
  Done when: dispatch refuses with the size needed and the free space when below a threshold, and the test uses a size-limited tmpfs.

- **Bundle a flight-recorder report with one verb** — FEATURE — value 4 — effort M — risk low — category: diagnostics
  Why: T-0317 ("new bug feedback") and the repeated "catch it earlier" drops show failures are diagnosed after the fact. Keep a ring buffer of the last N hook calls (event, duration, exit, stderr tail), and `fm report` writes a redacted bundle.
  Done when: after a forced hook crash, `fm report` outputs a file containing that call's stderr, with the home path and secrets scrubbed.

- **Resolve every external binary through one provenance-recording resolver** — CLEAN — value 4 — effort S — risk low — category: environment
  Why: "can't find claude" with only the native install, plus the test lockout bypass, both come from ad-hoc PATH lookups. Add one resolver that checks the known install locations, records where it found each binary, and shows this in doctor.
  Done when: `grep` finds no direct `shutil.which("claude")` outside the resolver, and `fm doctor` prints each tool's path and why it was chosen.

- **Roll out rule and hint changes on a canary basis with auto-rollback** — FEATURE — value 4 — effort L — risk med — category: change safety
  Why: git-carried hints (T-1032) and plugin updates reach every clone at once. Apply a new hint or rule to the originating project first, compare the pass and block rates over N tasks, and revert it if they worsen.
  Done when: a deliberately bad hint is auto-disabled after N worse outcomes and the pane says so.

- **Wild: Make each feature trip its own breaker after repeated crashes** — FEATURE — value 4 — effort M — risk med — category: self-healing
  Why: assumption: one crashing optional feature (the edit-time sentinel, the pane panel) can currently degrade every turn. Each feature counts its own exceptions, switches itself off past a threshold, shows a one-line note, and retries after a cooldown.
  Done when: injecting an exception three times disables only that feature, with the other hooks unaffected, and it re-enables after the cooldown.

- **Wild: Diff old and new hooks in shadow on real recorded stdin** — FEATURE — value 4 — effort L — risk low — category: regression
  Why: this goes beyond replaying sessions against rules. Before an update goes live, run the previous and the next version of every hook over the last week's recorded inputs and report any output that differs and was not intended.
  Done when: `fm release --shadow` lists exactly the hooks whose output changed on a seeded change, and none on a no-op.

- **Wild: Run an external watchdog timer that resumes stalled work overnight** — FEATURE — value 3 — effort M — risk high — category: unattended
  Why: assumption: a session killed at 3am leaves resumable worktrees (T-1028) but nobody notices. A systemd user timer checks heartbeats and resumes under a cost cap, or leaves a note if the lease or budget forbids it.
  Done when: a killed builder with a stale heartbeat is resumed once by the timer, and a second stall at the cap leaves a morning note instead.

- **Detect clock jumps and make ledger ordering monotonic** — FIX — value 2 — effort S — risk low — category: time
  Why: malformed ledger times already broke the pane. Sleep, NTP steps and timezone changes can reorder history and charts.
  Done when: a test that steps the clock back 1h leaves ledger order stable and charts non-negative.
