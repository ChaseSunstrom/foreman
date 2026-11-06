# Brainstorm — lens: reliability

Most reliability ground is already covered in the pack (leases, breakers, journals, chaos tests, soaks), so these ideas target the gaps between those mechanisms, plus the reliability risks that come from importing the six upstream repos. Items marked "assumption" rest on something the pack doesn't show.

- **Share one retry-token pool down the deadline tree** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: assumption: slot repair, runner retry, fallback chains and spend-aware retries are separate mechanisms in the pack, so their attempts multiply under a flaky endpoint.
  Done when: a fake runner that fails every call produces at most N total attempts across all layers, and the exhaustion record shows how many each layer used.

- **Recover stale git locks by owner proof** — FIX — value 4 — effort S — risk low — category: crash recovery
  Why: the user asked that stop, quit and kill take down the workers, and a killed worker mid-`git add` leaves `.git/index.lock` that blocks the next run. Assumption: nothing clears it today.
  Done when: after `kill -9` of a worker mid-git, the next run removes the lock only if no live process has the repo as its cwd, and leaves the lock alone when one does.

- **Make path identity agree across case-folding and Unicode forms** — FIX — value 4 — effort M — risk med — category: portability
  Why: the macOS CI fixes (T-1249) and the guard, leases and changed-file judge each canonicalise paths. Assumption: they don't share one fold, so NFD `é` or `A.txt` vs `a.txt` could pass one check and fail another.
  Done when: a fixture with NFC/NFD and case-colliding names gives identical verdicts from the guard, the lease table and the diff judge on Linux and macOS.

- **Shed an overflowing prompt in a fixed priority order** — FEATURE — value 4 — effort M — risk low — category: models
  Why: local models' real context and silent-truncation detection are listed, but the pack shows no deterministic fallback for when a prompt is over budget.
  Done when: a 3x-oversized slot prompt drops sections in the documented order, never drops the request or DONE-WHEN, and writes a receipt naming what was cut.

- **Arm `faulthandler` in every long-running verb** — FEATURE — value 4 — effort S — risk low — category: diagnosability
  Why: the pack's "it just isn't doing anything" complaints and stall classifier name a cause only from outside the process. `faulthandler.dump_traceback_later` in stdlib would add a stack from inside it.
  Done when: a verb deliberately hung past its deadline writes a thread-stack dump into the crash bundle, and `fm code why` quotes the top frame.

- **Snapshot the run journal so resume cost stays flat** — PERFORMANCE — value 3 — effort M — risk low — category: resume
  Why: durable runs and journals are planned, and an append-only journal makes resume slower as runs get longer. Assumption: resume replays the whole journal.
  Done when: resuming a 5,000-event run takes about as long as resuming a 50-event run, and both give an identical state hash.

- **Tag imported scripts with an idempotence class** — SECURITY — value 4 — effort M — risk med — category: upstream safety
  Why: Agent Skills ship `scripts/`, and resume re-runs steps. Assumption: nothing marks a script as pure, idempotent or effectful, so a replay could double-apply an effect.
  Done when: replaying a journaled step that ran an effectful imported script is refused unless its effect receipt shows it completed, and a pure script replays freely.

- **Lint that every exit path writes a typed terminal record** — CLEAN — value 3 — effort M — risk low — category: invariants
  Why: assumption: with ~30 stall, signal, timeout, fallback and crash paths, some can end a run with no terminal state, which is the "silent" failure the user keeps reporting.
  Done when: an AST test fails if any `fm code` exit path (exception, SIGTERM, deadline, runner death) can return without a terminal-state record.

- **Assert resource flatness in the soak** — FEATURE — value 3 — effort S — risk low — category: soak
  Why: the TUI, supervisor and widget processes are long-lived, and the pack's soaks check behaviour but not slow leaks.
  Done when: a 1-hour replay soak ends with fds, threads, child processes and RSS within a set band of the start, and the test fails on drift.

- **Land multi-project sweeps as a saga with compensations** — FEATURE — value 3 — effort M — risk med — category: cross-project
  Why: "sweep one request across many projects" and "land everything proved in one pass" are listed, but all-or-nothing behaviour is not.
  Done when: forcing project 3 of 5 to fail at land time rolls projects 1 and 2 back to their recorded base refs, and the report says which stages were compensated.

- **Run a nightly resume drill on the user's own finished runs** (wild) — FEATURE — value 4 — effort M — risk low — category: resume
  Why: wild; assumption: resume is only tested on fixtures. The drill cuts a real finished run at step k in a scratch copy and resumes it.
  Done when: for the last 3 finished runs, resuming from a random step reproduces the original verdict, or files a task naming the first divergent step.

- **Leave a last-will sidecar that outlives `fm`** (wild) — FEATURE — value 4 — effort M — risk med — category: crash recovery
  Why: wild; the pack has a sidecar reaper, but this one is a 40-line stdlib script that survives a broken or uninstalled `fm`. On a lapsed heartbeat it reaps the worker group, releases leases, writes the terminal record and sends a notification with the exact resume command.
  Done when: `rm -rf` of the plugin dir mid-run still ends with no orphans, the lease released and a resume command printed.

- **Adapt checkpoint density to the repo's observed failure rate** (wild) — FEATURE — value 3 — effort M — risk med — category: adaptive reliability
  Why: wild; assumption: crash frequency varies by repo and host (NFS, huge monorepo, flaky laptop) while the pack's checkpoint cadence is fixed.
  Done when: after three simulated crashes in one project, new runs checkpoint more often and use smaller steps, and a stable streak relaxes both. `fm code why` shows the setting and the reason.

- **Add hysteresis to runner breakers and fallback** — FEATURE — value 3 — effort S — risk low — category: routing stability
  Why: breakers and classified fallback are listed, and a runner hovering near its threshold would flap between runners on every call.
  Done when: a fake runner alternating success and failure causes at most one runner switch per cool-down window, and the switch is recorded with its reason.
