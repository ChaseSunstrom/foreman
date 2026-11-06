# Brainstorm — lens: reliability

- **Enumerate crash points in every state write** — FEATURE — value 5 — effort M — risk low — category: durability (wild)
  Why: the pack lists atomic writes, torn-write checks and chaos soaks, but no deterministic version. A wrapper around the one write helper raises or kills at the Nth write or rename of a verb. After each kill, all readers must load the state and the verb must resume or roll back, the way SQLite crash-tests itself. Wild: nothing here has ever tested every interruption point.
  Done when: a test runs `fm task finish` and `fm lane merge` with a kill injected at each write index, and every post-kill state loads without error and passes `fm doctor`.

- **Count subprocesses per hook, not milliseconds** — PERFORMANCE — value 4 — effort S — risk low — category: hot path
  Why: the review lists "hot-path cost" as a recurring defect, and the dropped regex-compile task shows timing numbers mislead (22 ms against a profiled 80 ms). Spawn counts (git, python) and file opens are deterministic and don't flake on a loaded host.
  Done when: a test fails if any hook on the fixture repo spawns more than its recorded budget of child processes or opens more than N files, and the budget lives in a checked-in table.

- **Run the whole suite from a subdirectory and a symlinked path** — FIX — value 4 — effort S — risk low — category: test matrix
  Why: "cwd vs root" is a named recurring defect, and builders in lanes hit it. This is a gate variant rather than a path-normalising helper.
  Done when: `fm check --matrix cwd` runs the suite from `repo/sub/dir` and via a symlink to the repo, with a path containing spaces and unicode, and all three pass.

- **Replay archived real state from every release** — SECURITY — value 4 — effort M — risk low — category: upgrade safety
  Why: the pack lists a state-version floor and "last known good", but no corpus. Keep scrubbed `.foreman/` snapshots, one per released version, and run the current code over each read-only. T-0418 shows installs lag releases (foreman-ui 0.6.1 against 0.18.0), so old state will keep meeting new code.
  Done when: a test loads each snapshot with the current `fm`, and `fm state`, `fm next` and `fm lane list` exit 0 without rewriting the files in the read-only pass.

- **Preserve unknown fields on read-modify-write** — FIX — value 4 — effort M — risk med — category: version skew
  Why: an older installed copy and a lane's newer copy write the same ledger and brief files (builders already hit copy skew). An older writer that drops fields it doesn't know silently deletes newer state.
  Done when: a test adds an unknown key to a task, brief and lane file, runs every mutating verb, and the key is still there afterwards.

- **Detect lock re-entry and ordering in tests** — FIX — value 4 — effort M — risk low — category: concurrency
  Why: the review names "lock re-entry" among the defects every builder branch shipped, and the contract fix needed a "held lock in Stop" repair. Instrument the one lock helper under test to record the owner and acquisition order, and fail on self re-acquire or an inverted order.
  Done when: the suite fails on a seeded re-entrant acquire and on a two-lock inversion, and passes on main.

- **Identify live processes by pid, start time and boot id** — FIX — value 3 — effort S — risk low — category: liveness
  Why: lane heartbeats, leases, children reaping and the stalled-lane flag all depend on "is that owner alive". A bare pid is reused, so a dead builder looks alive, or a stale lock never clears. Assumption: the current code checks pids only, so verify first.
  Done when: a test that reuses a dead owner's pid for a new process sees the old lock as stale and reclaims it.

- **Test hook stdout purity under hostile conditions** — FIX — value 4 — effort S — risk low — category: hooks
  Why: a stray warning or traceback on stdout can corrupt Claude Code's hook protocol. Run each hook with `PYTHONWARNINGS=error`, a closed stdin, a broken stdout pipe (EPIPE) and a read-only HOME. Each must exit with valid JSON or nothing, and fail open or closed as documented.
  Done when: a matrix test passes for every registered hook and fails when a seeded `print` is added to one.

- **Fix a git topology matrix for commits and lane merges** — FIX — value 4 — effort M — risk low — category: git edge cases
  Why: recent work depends on git behaviour: task commits that leave out dirty files (T-1169), lane merges and PR posting. Cover detached HEAD, shallow clone, submodule, no `user.email`, a worktree of a worktree, a failing pre-commit hook and a gc'd ref.
  Done when: `fm task finish` and `fm lane merge` each give a clear result or a named refusal on all six topologies, never a traceback.

- **Make the web UI survive restarts and version skew** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: web UI is the surface found, and the pack shows a pane lagging its release (T-0418). Add a version handshake so a stale tab shows "server updated, reload", a visible disconnected state, and a free-port fallback with the URL printed. Assumption: it has a long-lived server or polling.
  Done when: a browser test kills and restarts the server on a new version and the open page shows the disconnected banner, then reloads itself within 10 seconds.

- **Stop on graceful signals at safe points only** — FIX — value 4 — effort M — risk med — category: unattended runs
  Why: `fm contract` bounds a run by time and spend, and the user is AFK. A bound that fires in the middle of a lane merge or a close leaves half-applied state. Define safe points, finish or roll back the current atomic step on SIGTERM or a contract stop, and print the receipt.
  Done when: a test sends SIGTERM during a lane merge and the next `fm state` shows the merge either complete or cleanly reverted, with the contract receipt printed.

- **Prove offline behaviour for every network verb** — FIX — value 3 — effort S — risk low — category: degraded mode
  Why: `fm pr --post`, `fm deps --capture` and the release push call out to gh and git remotes. Under a blackholed network, each should time out, say what was skipped, and leave no half-recorded state.
  Done when: with a fake gh that hangs, each verb returns within its deadline with a named skip and no partial ledger entry.

- **Run the suite under a time-warped clock** — FIX — value 3 — effort S — risk low — category: time (wild)
  Why: contract bounds, the 30-day defect window, "N minutes silent" lane flags and the away summary are all clock logic. Run the suite with the clock set to a leap day, a DST boundary and past 2038. Wild: no one has asked, but time bugs only show up on those dates.
  Done when: the gate runs the time-sensitive tests under three frozen dates and they pass, and a seeded `now()` that ignores the injected clock is caught.

- **Cross-check the guard against a real shell parser** — SECURITY — value 4 — effort L — risk med — category: guard (wild)
  Why: T-0275 (active) extends the guard to read script files, and the mined refusals show its splitting is hand-rolled. Use `bash -n` or a proper parser as an independent oracle on the mined corpus and flag commands where the two disagree about what runs. Wild: it's a second opinion that costs no model tokens.
  Done when: a nightly job replays the mined refusals and allows through the parser, and every disagreement is listed with the command, or the job reports zero.
