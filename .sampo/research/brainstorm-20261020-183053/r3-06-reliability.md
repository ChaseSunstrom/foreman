# Brainstorm — lens: reliability

- **Run the TUI on an injectable clock** — FIX — value 4 — effort M — risk low — category: testing
  Why: CI went red twice on timing (CPU-time bounds, a 5 s hook budget), and the existing ideas stack easing, shimmer, odometers and heat-cooling on top of wall-clock time. Assumption: the renderer currently reads real time directly.
  Done when: a test drives a 10 s animation with a virtual clock in under 100 ms of real time, and two runs produce byte-identical frames.

- **Fuzz layout and event sequences** — FIX — value 4 — effort M — risk low — category: testing
  Why: the existing ideas cover golden frames for known states. Nothing covers unknown ones, such as random widths from 1 to 400, wide or combining glyphs, truncated or reordered events, and huge diffs. Assumption: golden tests only pin hand-picked inputs.
  Done when: a seeded fuzz test of 2,000 cases never raises, never emits a line wider than the terminal, and fails with a replayable seed.

- **Restore the terminal after a hard kill** — FIX — value 4 — effort S — risk med — category: terminal
  Why: "restore on every exit path" cannot cover SIGKILL or an OOM kill, which leave raw mode, the alt screen, mouse reporting and hidden cursor behind. Assumption: no out-of-process reset exists.
  Done when: `kill -9` on the TUI process leaves the tty cooked, with the cursor shown and the alt screen left, within 1 s, checked in a pty test.

- **Route every terminal query through one timed broker** — FIX — value 3 — effort M — risk med — category: terminal
  Why: the ideas so far add background probing, capability detection and DEC 2026, and each needs a reply read from stdin. Replies that arrive late or never (tmux, ssh, dumb terminals) can leak into the input stream as keystrokes. Assumption: the probes are added independently.
  Done when: with a pty that never answers, startup is delayed by under 150 ms, falls back to a safe profile, and no stray bytes reach the keymap.

- **Treat paste and key floods as data** — FIX — value 3 — effort S — risk low — category: input
  Why: with keybindings, a command palette and note-box steering planned, pasted text containing letters or escape bytes could fire commands mid-run. Assumption: bracketed paste isn't enabled today.
  Done when: pasting "qdx\x1b[A" into the note box inserts it verbatim, triggers no bindings, and holding a key for 1,000 repeats cannot queue more than one redraw.

- **Prove the TUI makes no network calls** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: privacy is thin, and the ideas so far add phone views, LAN status pages, notifications and exports. Assumption: no test currently asserts the viewer is offline-only.
  Done when: the TUI test suite runs with sockets patched to raise, so any connect fails the test, and an explicit allowlist names the one model endpoint the harness uses.

- **Scrub paths and identity from every export, with a preview** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: the SVG postcards, session clips, crash bundles and receipts proposed so far all leave the machine. Redaction is planned for secrets but not for home paths, usernames, emails or hostnames. Assumption: exports embed raw absolute paths.
  Done when: an export of a fixture run contains none of the fixture's home path, user or email, and a `--preview` lists each substitution before anything is written.

- **Expire run logs and add a purge** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: replay, reattach and black-box recording all depend on keeping event logs, and logs hold prompts, diffs and command output. Assumption: there is no retention limit today.
  Done when: logs older than a configured TTL (default 30 days) are removed on startup, and `fm code purge --run X` deletes one run's log and every derived artifact, listing what it removed.

- **Make several viewers on one run safe** — FIX — value 3 — effort M — risk med — category: concurrency
  Why: the ideas so far include reattach, a phone view, a tmux companion and a foreman-ui pane, so two viewers on one event log is a likely case. Assumption: viewer state (scroll, view, theme) is written to shared files.
  Done when: two TUIs attached to one run keep independent view state, and killing either leaves the other and the harness unaffected.

- **Show a post-mortem card when a run dies** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: the existing ideas replay finished runs and keep a last good frame, but a killed or crashed run needs a diagnosis, not just a freeze. Assumption: the event log survives the crash.
  Done when: reattaching to a run whose harness was killed shows a card with the last station, the last three events, the last guard verdict and the exit cause within 1 s.

- **Wild: Replay mutated copies of real logs** — FIX — value 3 — effort M — risk low — category: testing (wild)
  Why: assumption: the user's own event logs are the best fuzz corpus. A nightly job takes real logs, then drops lines, shuffles timestamps, doubles events and truncates mid-line, and renders each.
  Done when: 500 mutated logs render without exceptions, and any failure is saved as a minimal fixture under the tests.

- **Wild: Add an airgap seal to the header** — FEATURE — value 3 — effort M — risk med — category: privacy (wild)
  Why: assumption: trust is the unspoken need behind local-first. A small lock glyph lights only while a socket-level check confirms the only open connection is the configured model endpoint, and it turns amber with the destination if anything else appears.
  Done when: a test that opens a connection to a second host flips the glyph amber and names that host within one frame.

- **Wild: Add a panic-room fallback that ignores all configuration** — FEATURE — value 3 — effort S — risk low — category: recovery (wild)
  Why: assumption: custom themes, widgets and keymaps are the likeliest cause of a broken launch. Holding a key or passing `--safe` at start boots a 100-line plain renderer with built-in defaults, and shows which user files it skipped.
  Done when: with deliberately corrupted theme, keymap and widget files, `fm code tui --safe` starts and completes a fake run, and lists the three skipped files.
