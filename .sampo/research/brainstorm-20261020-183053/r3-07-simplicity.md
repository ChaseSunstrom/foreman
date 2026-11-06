# Brainstorm — lens: simplicity

- **Print the final frame to scrollback on exit** — FEATURE — value 4 — effort S — risk low — category: ui
  Why: the user said the TUI "looked like crap with all the text" and was redesigned as pictures. Those pictures disappear from the terminal when the alt-screen closes, and the run's receipt goes with them. Assumption: the TUI uses the alt-screen.
  Done when: after `fm code tui` exits, the last frame (station track, chips, cost) is still in the terminal's scrollback and can be selected and copied.

- **Add a private mode key that masks words and paths** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: assumption: screenshots and screen-shares of a TUI full of model prose and repo paths leak. The pack's redaction ideas cover logs and exports, not the live screen. One key swaps prose for `▒▒▒`, paths for `…/file.py`, and dollar figures for bars.
  Done when: with the key on, a captured frame contains none of the run's file paths, model text or dollar amounts, and a test asserts it.

- **Leave the mouse alone by default** — CLEAN — value 3 — effort S — risk low — category: ui
  Why: the ideas so far lean on mouse capture (clickable ids, hover previews). Capture breaks native select, copy and tmux scrolling. Clickable ids can instead be OSC 8 hyperlinks, which need no capture. Assumption: the TUI currently captures or will capture the mouse.
  Done when: the default session emits no mouse-enable sequences, ids still open via OSC 8 links, and text selects and copies natively.

- **Lint that no state is told by color alone** — CLEAN — value 4 — effort S — risk low — category: ui
  Why: the user asked for more than "static colors". Every state must also differ in glyph or position, so the TUI reads in 1-bit, over `NO_COLOR` and for color-blind users. A test renders each view with colors stripped and asserts the distinct states still produce distinct text.
  Done when: the stripped-color render test passes for all views, and a deliberately color-only state makes it fail.

- **Budget the colors per frame** — CLEAN — value 3 — effort S — risk low — category: ui
  Why: "better looks" tends to drift into a rainbow. Cap a frame at N semantic roles (ok, warn, bad, accent, dim, text), each resolved by one theme table. A golden-frame test counts the distinct color codes.
  Done when: no golden frame exceeds the cap, and adding a seventh ad-hoc color fails the test.

- **Cap bytes per second for slow links** — PERFORMANCE — value 3 — effort S — risk low — category: ui
  Why: assumption: Foreman is often run over ssh or mosh, where a full-motion TUI floods the link. One setting (auto-detected from `SSH_CONNECTION`) throttles to a few diff-frames a second with no tweening.
  Done when: over `SSH_CONNECTION`, a 60-second replay writes under a set byte budget, and a local run is unaffected.

- **Prove the TUI makes no network calls** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: privacy is thin in the pack. A pty test runs a replayed session with sockets blocked (an `unshare -n` namespace, or a monkeypatched `socket`) and asserts it renders fully. This turns "it's local" into a ratchet like the hook bench.
  Done when: the replay passes with the network namespace empty, and adding any `socket.connect` to the TUI path fails CI.

- **Run widget executables with the network off** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: the pack proposes widgets as any executable printing JSON lines. Such a widget could send repo data anywhere. Default to no network and a read-only repo view, and let a widget declare what it needs in its manifest.
  Done when: a sample widget that tries to connect gets no route and the pane shows "widget: offline", while a declared one works.

- **Add `fm code tui --forget` and a run-log retention setting** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: the replay, ghost-run and digest ideas all keep event logs forever. Add one expiry setting (default 30 days) and one command to wipe a run's logs and frames.
  Done when: `--forget RUN` removes its event log and cached frames, and logs older than the setting are pruned on next start.

- **Wild: Dim into quiet hours** — FEATURE — value 2 — effort S — risk low — category: ui
  Why: wild. After local bedtime the TUI drops to a near-black palette and the station track stops moving except on events, so an unattended overnight run isn't a lit billboard. It reuses the reduced-motion switch.
  Done when: with the clock set inside quiet hours, a frame uses the dim palette and idle frames are byte-identical.

- **Wild: Pull a theme from any pasted ANSI screenshot** — FEATURE — value 2 — effort M — risk low — category: ui
  Why: wild. `fm code theme from-file frame.ansi` reads the colors another tool printed and maps the six semantic roles to its nearest hues. Themes become "make it look like my editor" without a theme format to learn.
  Done when: feeding a captured Solarized frame yields a six-role theme that passes the contrast and color-only lints.

- **Wild: Make a one-line mode the whole product when the pane is small** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: wild. Below a set height the TUI becomes one line: `▮▮▮▯▯ step 3/5 · tests ✓ · $0.41/2`. It is the same renderer with the region reduced, which the foreman-ui docked pane can also use, so the two surfaces share it.
  Done when: at 1×80 the frame is exactly one line carrying station, step count, last verdict and spend, and it never wraps.
