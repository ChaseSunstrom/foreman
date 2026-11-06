# Brainstorm — lens: approaches

- **Make the harness emit one event stream and the TUI just a reader** — FEATURE — value 5 — effort M — risk low — category: architecture
  Why: assumption: the TUI is drawn from harness state directly. Many ideas on the list (replay, SVG export, web mirror, golden frames, usage stats) each need the same event log. Building the log once gives each of them a cheap reader.
  Done when: `fm code --events out.jsonl` records a run, and replaying that file into the TUI yields frames identical to the live run's.

- **Ratchet the text per screen** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: the user said the TUI "looked like crap with all the text", and the context-tax ratchet (T-1274/T-1275) already shows Foreman enforcing a budget in tests. Apply the same idea to words: a test counts letters per frame, so prose can't creep back in.
  Done when: a test fails if any view's golden frame at 100×30 has more than N alphabetic characters outside the model-text area.

- **Add a context fuel gauge with a compaction forecast** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the marathon showcase and the compaction-storm soak (T-1259) make compaction central, yet no listed idea shows how full the context is or when the next compaction is likely.
  Done when: a replayed run with forced compaction shows a gauge that drops at each compaction and a forecast within 20% of the actual turn count.

- **Probe the terminal's real background and match the docked pane** — FIX — value 3 — effort S — risk low — category: theming
  Why: T-1217 notes Claude Code paints the docked pane's background #262626, so fixed theme colors clash with it. Querying the background (OSC 11) lets themes derive from the real surface and pick light or dark automatically.
  Done when: in a terminal that answers the query, the TUI's base color equals the reported background, and with no answer it falls back to the theme default without delay.

- **Let widgets be any executable that prints JSON lines** — FEATURE — value 4 — effort M — risk med — category: extensibility
  Why: assumption: a Python-level plugin API is heavier than needed. Executables in the style of tmux or waybar status commands work in any language, are timeout-bounded and can be restricted by the guard.
  Done when: a 5-line shell script in `~/.foreman/widgets/` shows a live value in the TUI, and a hung widget is killed after its timeout without dropping a frame.

- **Share one widget kit between the foreman-ui pane and the fm code TUI** — CLEAN — value 4 — effort L — risk med — category: reuse
  Why: T-0166 says the band and pane are stuck in register.tsx, and the two surfaces draw the same stations, bars and Gantt separately. One kit with two hosts halves the polish work.
  Done when: the station track is defined once and both the pane and `fm code tui` render it from that definition, with the same golden frame for it in each.

- **Add a linear mode for screen readers, pipes and CI** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: assumption: reduced-motion only stops animation, but cursor-addressed redraws still break screen readers, `tee` and CI logs. A mode that prints one plain line per event covers all three.
  Done when: `fm code tui --linear` outputs no cursor-movement escapes and one stable line per station change.

- **Generate keymap, theme and widget docs from the registry** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the TUI request was for a customizable, extendable UI. Without generated docs, the help overlay and the docs page drift from the code.
  Done when: the `?` overlay and the docs page are built from the same registry, and a test fails if a bound key is missing from either.

- **Count view dwell time locally to prune unused panels** — FEATURE — value 2 — effort S — risk low — category: observability
  Why: "delete panels nobody looks at" is listed but nothing measures it. Counters stay in `~/.foreman`, are never sent anywhere, and `fm code tui --usage` prints them.
  Done when: after a session, `--usage` lists seconds per view, and no network call is made.

- **Show Foreman and plain Claude Code side by side live in a duel view (wild)** — FEATURE — value 4 — effort L — risk med — category: showcase
  Why: the user wants Foreman better, cheaper and faster than Claude Code, and the marathon showcase and bench (T-1231) already run both. A split view of cost, tasks passed and elapsed time makes that visible while it happens.
  Done when: `fm code bench --watch` shows two columns updating live, and the final frame matches the published scorecard numbers.

- **Run a designer agent that restyles the TUI unattended (wild)** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: golden frames can judge a design change. An agent renders each view across themes and sizes, proposes tweaks, and a second agent rejects any that raise the text count or break the frames.
  Done when: one unattended run produces a patch that changes at least one theme, passes the text ratchet, and ships with before/after frames.

- **Give a phone a read-only live view over the local network (wild)** — FEATURE — value 3 — effort M — risk high — category: devices
  Why: assumption: unattended runs are watched from elsewhere. It would be opt-in only, scan a QR code to join, bind to the LAN with a one-time token, and show the station track and the "needs you" state.
  Done when: with the setting off, no port opens, and with it on, a phone loads the station track within 2 s and the token stops working when the run ends.

- **Score each frame with a cheap model's glance test (wild)** — FEATURE — value 3 — effort M — risk low — category: design QA
  Why: assumption: "looks good" has no test. Haiku gets the text dump of a frame and must say what is running, what failed and what needs the user. A view it can't read fails.
  Done when: a bench of 10 scripted states passes at ≥90% answer accuracy, and a deliberately cluttered frame fails.
