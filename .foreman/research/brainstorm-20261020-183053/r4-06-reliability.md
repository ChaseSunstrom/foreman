# Brainstorm — lens: reliability

- **Diff-test the renderer against a tiny VT emulator** — FEATURE — value 5 — effort M — risk low — category: testing
  Why: the idea list has golden frames, but those compare the cell grid the renderer intends, not what a terminal does with the escape bytes (cursor moves, scroll regions, wrap-at-edge, DEC 2026). Assumption: the TUI diff-draws and emits raw escapes.
  Done when: a test feeds every view's byte stream into a stdlib VT interpreter and asserts the resulting screen equals a naive full-repaint of the same state, across 3 sizes and all themes.

- **Survive suspend, SIGHUP and SIGWINCH storms** — FIX — value 5 — effort M — risk med — category: signals
  Why: assumption: Ctrl-Z/`fg`, an ssh drop and tmux resizes are the common ways a long-lived TUI corrupts a terminal. Restoring on exit and hard-kill is listed, but the suspend/resume path is not.
  Done when: a pty test sends SIGTSTP then SIGCONT and gets raw mode, alt-screen and a full repaint back. SIGHUP leaves the harness running and the log intact, and 50 resizes in 1 s produce one coalesced repaint.

- **Count work instead of timing it in CI** — PERFORMANCE — value 4 — effort M — risk low — category: test-stability
  Why: the CI-red entries (a 5 s hook limit on Linux 3.12, "CPU-time bounds that hold on GitHub's runners") show wall-time bounds flaking. A TUI frame-budget test would flake the same way.
  Done when: the frame-cost ratchet asserts cells written, bytes emitted and widget render calls per frame from a fixed replay. It passes unchanged under a `taskset`/10% CPU throttle.

- **Make time monotonic and sleep-proof** — FIX — value 4 — effort S — risk low — category: clock
  Why: assumption: laptops sleep during unattended runs. Wall-clock deltas would draw a 6-hour Gantt bar, burst-play animations, and trip stuck-loop and "waiting on you" detectors falsely.
  Done when: with an injected clock jumped forward 3 h, the Gantt bar is capped and marked "asleep", no animation catches up, and no stuck alert fires.

- **Hold on a full disk or an unwritable log** — FIX — value 4 — effort S — risk low — category: durability
  Why: the pack makes the TUI a pure function of the event log, so a failed append silently breaks replay and reattach.
  Done when: with ENOSPC or EACCES injected into the log writer, the harness keeps running and the header shows "log not recording" within one frame. Once space returns, a gap marker is written and replay still loads.

- **Detect version skew mid-run** — FEATURE — value 4 — effort M — risk low — category: upgrades
  Why: the user releases every few days (1.2.41 to 1.2.44) and "feel free to release at any time". A plugin update under a live run can pair a new TUI with an old event schema, or the reverse.
  Done when: the log header carries the harness version, and a TUI built for a different schema shows a banner and renders the readable subset. A test pairs N-1 and N+1 logs with the current reader.

- **Boot into safe mode after a crash loop** — FEATURE — value 4 — effort S — risk low — category: recovery
  Why: the list has "panic-room fallback" and "last good copy", but nothing decides automatically. T-0798 already names crash-loop quarantine for the harness.
  Done when: two launches that die within 3 s each cause the third to start with the built-in theme, no widgets and no motion. It says why in one line, and `--reset` clears the flag.

- **Soak the TUI through a marathon replay** — PERFORMANCE — value 4 — effort M — risk low — category: soak
  Why: the marathon showcase (forced compactions, hours unattended) is the user's current focus, and nothing checks the TUI itself over hours.
  Done when: a nightly job replays an 8-hour synthetic log at 500x. RSS growth stays under a set bound, the fd count is flat and p95 frame cost doesn't drift more than 10% between hour 1 and hour 8.

- **Give destructive keys an undo window** — FEATURE — value 3 — effort S — risk low — category: input-safety
  Why: assumption: once the TUI is interactive (reject hunks, abort run, edit queue), a stray key mid-run is the likeliest user-caused loss.
  Done when: abort, discard-hunk and drop-task show "undo (u) 5 s" and defer the effect, and a test shows `u` restores the state exactly.

- **Wild: Shrink any glitch to a minimal repro** — FEATURE — value 4 — effort L — risk med — category: debugging
  Why: assumption: wild. A "report glitch" key freezes the last 200 events and terminal facts. `fm code tui --shrink` then delta-debugs the event sequence down to the smallest one that still reproduces the failure, and emits it as a new fixture.
  Done when: a deliberately injected renderer bug is reduced from 200 events to at most 5 and saved as a passing regression test after the fix.

- **Wild: Build a terminal compat table from local probes** — FEATURE — value 3 — effort M — risk low — category: compatibility
  Why: assumption: wild. `fm code tui --probe` records what the terminal answers (DA1, XTVERSION, truecolor, sync output, width of 10 test glyphs) into a local file. Contributors attach files, and CI generates the supported-terminal table and fallback rules from them.
  Done when: two sample probe files produce a table and a different capability profile each, and nothing leaves the machine unless the user copies the file.

- **Wild: Run a sentinel that watches the watchers** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: assumption: wild. In a marathon, the harness and the TUI could both die and no screen is there to say so. A 20-line shell sentinel checks a heartbeat file the harness touches and, if it goes stale, uses the terminal bell, `notify-send` or a user-set command.
  Done when: killing the harness with SIGKILL triggers the configured alert within the stale threshold, and a healthy run triggers none over 10 min.

- **Count swallowed errors and ratchet them** — CLEAN — value 3 — effort S — risk low — category: observability
  Why: firewalled widgets, tolerant readers and fallbacks all hide failures, so quiet failure can look like health.
  Done when: each swallow increments a named counter shown in `fm doctor`, and the replay-corpus test fails if any counter is above its recorded baseline.
