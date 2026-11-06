# Brainstorm — lens: performance

- **Import only the hook module each verdict needs** — PERFORMANCE — value 4 — effort S — risk low — category: hook startup
  Why: the pack says box plus startup is the whole hook cost, and PreToolUse:Bash:script p95 sits about 10 ms over its 300 ms budget. Assumption: hook entry points import the whole plugin on every call.
  Done when: `python -X importtime` on a Bash hook call lists only that hook's modules, and `bench_hooks --runs 20` keeps the PreToolUse:Bash:script p95 under 300 ms at load 0.6 per core.

- **Start hook interpreters with `-S -I` and a frozen bytecode bundle** — PERFORMANCE — value 4 — effort M — risk med — category: hook startup
  Why: the same startup cost dominates the hook budget. Assumption: site-packages scanning and `.pyc` checks run on every hook call.
  Done when: the median hook call drops by at least 25% in `bench_hooks`, and a test fails if the bundle's hash no longer matches its sources.

- **Memoize guard verdicts by command hash and rules hash** — PERFORMANCE — value 3 — effort S — risk low — category: guard cache
  Why: a guard verdict depends only on the command text, the rules, and the config. Agents repeat the same commands often.
  Done when: a second identical Bash call skips rule evaluation, which a journal counter shows, and changing one rule invalidates the cached verdicts.

- **Shard the test suite by measured duration, longest first** — PERFORMANCE — value 4 — effort M — risk low — category: test wall time
  Why: CI's 20-minute job cap hid where a test hung, and run.py already records per-class timing. Assumption: classes run in a fixed order, so one slow shard sets the wall time.
  Done when: the full suite's wall time falls on CI, and no shard exceeds the slowest single class by more than 10%.

- **Read the journal tail by seeking from the end** — PERFORMANCE — value 3 — effort S — risk low — category: journal reads
  Why: `fm status` and `fm why` read without the gate lock, and the journal only grows. Assumption: they parse the whole file to show the last few events.
  Done when: `fm status` on a 500 MB journal answers in under 100 ms, and its output matches a full parse.

- **Cache backlog parses by inode, size and mtime_ns** — PERFORMANCE — value 3 — effort S — risk low — category: backlog reads
  Why: the backlog is re-read on every surface refresh, and most calls find nothing changed.
  Done when: an unchanged backlog triggers zero backlog reads, which a counter shows, and an edit made within the same second still invalidates the cache.

- **Invalidate doctor probes with inotify, not by re-running them** — PERFORMANCE — value 3 — effort M — risk med — category: doctor speed
  Why: `fm doctor` runs every probe on each call, and most inputs have not changed since the last run.
  Done when: a second `fm doctor` on an unchanged tree spawns no probe subprocess, and touching one probed file re-runs only its probe.

- **Paint the terminal UI from the last snapshot before the journal loads** — PERFORMANCE — value 4 — effort M — risk low — category: TUI latency
  Why: the pane waits on the full journal before its first frame, so a large journal delays every open. Assumption: the snapshot is written at each clean exit.
  Done when: the first frame appears in under 50 ms on a 500 MB journal, and the snapshot is marked stale until the live state replaces it.

- **Push web UI state over server-sent events instead of polling** — PERFORMANCE — value 3 — effort M — risk low — category: web UI polling
  Why: the web UI and the site both refresh on a timer, which costs requests even when nothing has changed.
  Done when: an idle web UI makes no requests except a heartbeat once a minute, and a state change reaches the page within 500 ms.

- **Wild: let systemd socket-activate the hook daemon** — PERFORMANCE — value 3 — effort M — risk med — category: hook lifecycle
  Why: a warm worker costs memory all day, but a socket-activated one costs nothing until the first hook call. Assumption: the user's machine runs systemd user services, as the Linux runs here do.
  Done when: the first hook call after login starts the daemon in under 100 ms, the daemon exits after 10 idle minutes, and the next call reconnects.

- **Wild: load the hook bytecode from a tmpfs image at login** — PERFORMANCE — value 2 — effort M — risk med — category: cold start
  Why: cold hook starts read bytecode from disk, which hurts after a reboot or a cache flush.
  Done when: a cold start with the page cache dropped runs in the same time as a warm one, and the image rebuilds when any source file changes.

- **Wild: skip the rules scan when a command matches a learned safe shape** — PERFORMANCE — value 3 — effort M — risk high — category: guard fast path
  Why: most Bash calls are plain reads and builds that the guard never blocks. Assumption: a shape learned from past allowed commands can be generalised without loosening the guard.
  Done when: a shape hit stays within the guard's existing refusal tests, a fuzz run finds no new allowed refusal, and a shape miss falls back to the full rules.

- **Wild: run a hook's second check only when the first one passes** — PERFORMANCE — value 2 — effort S — risk med — category: hook pipeline
  Why: hooks currently run every check in sequence even after an early verdict is already decided.
  Done when: a refused command makes no further check calls, a journal entry records the skip, and no refusal changes in the guard test suite.
