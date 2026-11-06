# Brainstorm — lens: reliability

- **Run the TUI as a detachable viewer that can never stall the harness** — FIX — value 5 — effort M — risk med — category: isolation
  Why: assumption: the TUI shares a process or pipe with the `fm code` loop, and Foreman's whole pitch is unattended runs. A full pipe, a SIGSTOP'd terminal, or a renderer crash must not cost a run.
  Done when: a test `kill -9`s the TUI, then `SIGSTOP`s it for 30s, mid-run, and the run still finishes with the same verdict and timing.

- **Reattach to a live run from its event log** — FEATURE — value 5 — effort M — risk med — category: recovery
  Why: assumption: runs are logged as events (replay and the scrubber depend on that). That same log lets a closed or crashed TUI rebuild its state, which replay of finished runs does not cover.
  Done when: `fm code tui --attach RUN` against a running job shows the same station, steps and chips as the original session did, after the original TUI was killed.

- **Put a firewall around each widget's render** — FIX — value 4 — effort S — risk low — category: fault isolation
  Why: assumption: one widget exception (a bad theme value, a odd diff) currently takes down the frame. The earlier "auto-fallback when frames repeatedly fail" is whole-frame; this is per-widget.
  Done when: a test that injects an exception into the Gantt widget still renders every other widget, shows an error placeholder in the Gantt's place, and writes the traceback to a file.

- **Make the event reader tolerant and versioned** — FIX — value 4 — effort S — risk low — category: robustness
  Why: assumption: the log schema will keep growing, as it did across 1.2.x, and a truncated last line is normal after a crash or a kill.
  Done when: a fuzz test feeds truncated, duplicated, reordered and unknown-kind lines, and the TUI never raises and shows a "skipped N events" count.

- **Coalesce event floods with a bounded transcript** — PERFORMANCE — value 4 — effort M — risk med — category: backpressure
  Why: assumption: a chatty tool (a test run printing 100k lines) can outrun a render loop. Memory and latency need a ceiling, and `fm code bench` already gives a place to measure it.
  Done when: a 200k-line burst keeps the TUI under a set RSS and per-frame time, the older transcript spills to disk, and scrolling back still reaches line 1.

- **Show liveness truthfully: spinners stop when the harness is gone** — FIX — value 5 — effort S — risk low — category: honesty
  Why: assumption: animations run on the renderer's clock, not on the harness's. A dead or wedged harness behind a happily pulsing track is the worst lie a monitor can tell. This is the check behind the earlier heartbeat idea, not another strip.
  Done when: after `kill -9` of the harness, every animation freezes and a "harness gone, last event 2s ago" banner appears within 3s.

- **Check the display against the log (truth invariants)** — FIX — value 4 — effort M — risk low — category: correctness
  Why: assumption: chips, verdict stamps and the receipt card are derived state. A bug that shows green for a red verify is a trust failure for a tool whose product is proof.
  Done when: a property test replays recorded runs and asserts each rendered verdict, step state and total equals what the log's ground truth says, including after resize and theme change.

- **Route worker stderr and child output into the pane, never the tty** — FIX — value 4 — effort S — risk low — category: screen integrity
  Why: assumption: `fm code --worker` spawns other CLIs (codex, gemini, opencode) that write straight to the terminal and tear the screen. The earlier escape-stripping covers model text, not child processes' raw writes.
  Done when: a fake worker that writes cursor-move escapes to stderr leaves the golden frame unchanged and the text appears, neutralised, in a log lane.

- **Test in a real pty matrix: tmux, screen, linux console, ssh, TERM=dumb** — FIX — value 4 — effort M — risk low — category: CI
  Why: the pack shows CI went red on Linux 3.12 and macOS more than once; terminals vary more than Python versions. The earlier golden frames test output, not terminal behaviour.
  Done when: a CI job drives the TUI under each pty setup and asserts clean enter, resize and exit with the terminal state restored.

- **Wild: Add a chaos mode that attacks the TUI** — FEATURE — value 3 — effort M — risk low — category: resilience
  Why: wild. `fm code tui --chaos` fires resize storms, SIGSTOP/SIGCONT, slow stdout, garbled events and a dropped clock, with a fixed seed so any failure can be reproduced. The suite in `fm code bench` is the natural home.
  Done when: a 5-minute seeded chaos run ends with no exception, a clean terminal, and the same final verdict as the unattacked run.

- **Wild: Keep a black-box recorder and a one-command crash bundle** — FEATURE — value 4 — effort M — risk low — category: diagnosis
  Why: wild. The last 200 frames, the last events, terminal capabilities and the theme go into a ring buffer on disk. `fm code tui --report` produces a redacted bundle fit for an issue, so "the TUI looked wrong" becomes reproducible.
  Done when: after an injected crash, the bundle replays the final frames offline and holds no home-directory paths or secrets.

- **Wild: Self-heal by restarting the renderer in a fallback mode** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: wild. If the rich renderer dies twice in a minute, a supervisor relaunches it as plain text with the same state, and offers `--rich` to retry later. The run never notices.
  Done when: a test that forces two renderer crashes ends with a working plain-mode screen showing the correct current station.

- **Write settings, themes and keybindings atomically with a last-good copy** — FIX — value 3 — effort S — risk low — category: config
  Why: assumption: hot-reloaded themes get edited live, and half-written files will be read. The earlier validation idea reports errors but doesn't say what to fall back to.
  Done when: a theme file replaced mid-read or left invalid keeps the previous good theme on screen and names the bad line, and a partial write never corrupts the saved copy.

- **Handle wide characters and graphemes in layout** — FIX — value 3 — effort S — risk low — category: layout
  Why: assumption: model output and file names carry CJK, emoji and combining marks, and a miscounted width shifts every column to its right, including the Gantt and chips.
  Done when: a golden test with mixed-width text keeps box edges aligned in every view and truncates without splitting a grapheme.
