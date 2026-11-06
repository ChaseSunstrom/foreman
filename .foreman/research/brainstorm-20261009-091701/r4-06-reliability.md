# Brainstorm — lens: reliability

- **Journal every spawned resource and reap the orphans** — FEATURE — value 4 — effort M — risk low — category: lifecycle
  Why: assumption: lanes, `fm serve` units, `fm run` children, background jobs, and temp dirs are all created by different code paths, and a crashed run leaves them behind. Lane rm already needed a fix for tool caches (T-0408), which suggests leftovers are a recurring problem.
  Done when: killing a run mid-lane with `kill -9` leaves an entry that `fm doctor` reports with its owner task, and `fm tidy --apply` removes the worktree, process, and unit in one pass with nothing left over.

- **Give every event stream a cursor and replay** — FEATURE — value 4 — effort M — risk med — category: consistency
  Why: `fm projects --follow`, `fm watch`, `fm mcp`, the UI mod, and the desktop app all read state. The "band stuck on step 1/5" bug (T-0406) is the kind of drift a consumer gets when it misses or misorders an event. Assumption: streams currently have no sequence numbers.
  Done when: a consumer killed for 30 s and restarted with its last cursor receives every missed event exactly once, in order, and a test proves it.

- **Mutation-test Foreman's own guard and done-gate source** — FEATURE — value 5 — effort M — risk low — category: self-verification
  Why: the guard has real-bash differential tests and a 5000-command replay, but the pack shows repeated misses, such as `bash -lc` and `zsh -ic` slipping through. Assumption: nothing measures whether the tests would catch a subtly broken guard.
  Done when: `fm bench --mutants` seeds at least 50 small edits into `fmguard.py` and the done-gate code, reports a kill rate, and fails the release gate below a set threshold.

- **Count every swallowed exception in the hooks** — CLEAN — value 4 — effort S — risk low — category: observability
  Why: assumption: hooks have to fail open so they never wedge a session, so they contain many broad `except` blocks that hide real faults. Those faults only show up as odd behaviour much later.
  Done when: a lint fails on any bare or broad except in `plugin/lib` that doesn't increment a health counter, and `fm doctor` prints counts per site for the last 7 days.

- **Run a hostile-environment matrix in CI** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: the installer supports Linux, macOS, and WSL and relies on a Python version check. Assumption: nothing tests spaces or unicode in paths, symlinked repos (the node_modules symlink case in the pack), `HOME` unset, a non-UTF-8 locale, odd umasks, no TTY, or a case-insensitive filesystem.
  Done when: the roundtrip e2e passes under a documented matrix of at least 8 such environments, and a failure names the environment that broke.

- **Install blue/green with automatic rollback** — FEATURE — value 4 — effort M — risk med — category: upgrade
  Why: there are releases roughly every day (1.2.8 to 1.2.16), each installed onto live user machines. Assumption: a bad release currently needs a manual fix.
  Done when: `install.sh` keeps the previous version in a second slot, runs `fm doctor` plus the hook bench on the new one, and flips back on failure, verified by installing a deliberately broken build.

- **Declare each command's network needs and degrade offline** — FEATURE — value 3 — effort M — risk low — category: degradation
  Why: `landscape`, `ideas`, `second`, `deps`, `night`, and `run` need the network or a model, while the guard, resume, and done-gate must never need it. Assumption: this boundary is implicit.
  Done when: running with the network blocked, every core command works, and each network command exits with a clear message and a cached result where one exists.

- **Scale-test against a synthetic five-year history** — PERFORMANCE — value 3 — effort M — risk low — category: scale
  Why: there are 430+ tasks after a short life, and `recall`, `map`, `digest`, and `projects` all scan the central store. Assumption: nobody has tested 50k tasks or 1M ledger lines.
  Done when: a generated history of that size keeps every hook under the existing bench budget and `fm recall` and `fm projects` under 1 s.

- **Randomize and isolate Foreman's own test suite** — CLEAN — value 3 — effort S — risk low — category: test-health
  Why: there are 88 test files, and the suite itself is one of the release gates. Assumption: they share state and depend on order, the clock, and the real `~/.claude`.
  Done when: the suite passes under random order, parallel workers, a frozen clock, a temporary `HOME`, and denied network, run five times in a row.

- **Order events with logical clocks for multi-machine work** — FIX — value 3 — effort M — risk med — category: ordering
  Why: assumption: earlier ideas add multiple machines, lanes, and sessions that write one ledger, and wall-clock timestamps from skewed machines will reorder events. This breaks "resume at the exact step".
  Done when: two simulated machines whose clocks differ by 10 minutes produce a ledger whose replay gives the same STATE as a single-machine run.

- **Simulate torn writes and reordered renames** — FEATURE — value 4 — effort L — risk low — category: crash-consistency — wild
  Why: assumption: crash-safe state is a listed idea, but nothing checks it at the filesystem level. A recorder wraps `write`, `rename`, and `fsync`, then replays every legal post-crash disk state, in the style of CrashMonkey, and runs `fm doctor` on each one.
  Done when: every crash point across the task lifecycle leaves a state that `fm doctor` either accepts or repairs, with zero lost checkpoints.

- **Run a time-warped soak with a synthetic user** — FEATURE — value 4 — effort L — risk med — category: long-horizon — wild
  Why: assumption: bugs like lesson rot, queue bloat, and stale deferrals only appear after months. A fake clock and a scripted user agent compress 6 months of tasks into an hour.
  Done when: the soak runs, produces a report of state growth, hook latency drift, and stale-item counts, and fails the release if any exceeds its threshold.

- **Spend an error budget on Foreman's own misbehaviour** — FEATURE — value 4 — effort M — risk med — category: governance — wild
  Why: the user keeps relaying defects from downstream projects (JARVIS), many of them recurring guard misfires. Assumption: when guard false positives, resume failures, or doctor warnings exceed a threshold in a window, the drive stops offering FEATURE work and offers only FIX and CLEAN on Foreman itself until the rate recovers.
  Done when: a seeded burst of incidents flips the drive into reliability-only mode, it names the budget it burned, and it exits that mode once the rate drops.

- **Keep a last-known-good fallback for each hook** — FEATURE — value 3 — effort M — risk med — category: fail-safe — wild
  Why: assumption: a hook that crashes on a new Python or Claude Code version leaves the session unguarded. Each hook ships a tiny frozen fallback (guard blocklist only) that runs when the main path throws, and it records the degraded state in the statusline.
  Done when: injecting a syntax error into `fmguard.py` still blocks `rm -rf ~` via the fallback and the band shows "degraded".
