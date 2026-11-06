# Brainstorm — lens: user value

- **Show an egress ledger for every run** — FEATURE — value 5 — effort M — risk low — category: privacy
  Why: assumption: the user wants proof of what leaves the machine, since they care about cost and trust (benchmarks, "published whichever way it falls"). No listed idea shows network traffic.
  Done when: after a run, `fm code tui` has a strip listing each host contacted, call count and bytes sent, and a test with a fake model on loopback shows exactly one host.

- **Add `--local-only` that refuses non-loopback endpoints** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: assumption: `fm code` takes any model or CLI via `models.json`, so a typo or shared config could send code to a cloud endpoint.
  Done when: with the flag, a model entry pointing at a non-loopback host fails before any request, and the TUI header shows a "local" badge.

- **Preview what the model is about to see** — FEATURE — value 4 — effort M — risk med — category: privacy
  Why: assumption: the harness builds context from files, diffs and tool output, and nothing shows the user that payload. A "files the model saw" list with byte counts would cover it.
  Done when: a key in the TUI opens the next request's file list and sizes, and a `--hold` option pauses until the user approves it.

- **Block secret-looking paths from model context by default** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the guard already stops dangerous commands. The same idea applies to reads of `.env`, `~/.ssh` and `*.pem` that would be sent upstream.
  Done when: a fake run that reads `.env` shows a masked "withheld" chip in the TUI, and the model's request contains no file contents.

- **Make exports portable and private by default** — FEATURE — value 4 — effort M — risk low — category: privacy
  Why: earlier ideas share runs as SVG or HTML and as a postcard, but a shared clip carries the home path, username and hostname. This is a different problem from redacting secrets.
  Done when: an exported clip has paths made relative and the user and host stripped, and a "what's inside" summary prints before the file is written.

- **Prove the TUI is offline with a socket-denied test** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the repo already ratchets hook CPU time and context bytes in tests. A matching zero-sockets test for the renderer and its themes would keep the animation and widget work from adding a phone-home path.
  Done when: CI runs the TUI replay with socket creation patched to raise, and it passes.

- **Seal run logs with expiry** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: assumption: event logs now drive replay and reattach, so they hold code and prompts. They need a retention window and optional encryption at rest.
  Done when: `fm code --retain 7d` deletes older logs, and an encrypted log replays only after a passphrase.

- **Give the TUI a visual design language of depth** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: the user said the TUI "looked like crap with all the text" and wants more than static colors. Rounded panels, half-block shadows and a three-level surface palette (base, raised, focus) would give structure that doesn't depend on motion.
  Done when: every view draws from the same three surface tokens, and the golden frames show raised cards over a darker base.

- **Remember each task's view, scroll and focus** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: assumption: with several tasks and unattended runs, the user drops in and out. Returning to a task should land where they left off.
  Done when: quitting and relaunching restores the last view and selected station per task, checked by a pty test.

- **Add a hover card on the Gantt and token charts** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the Gantt and token columns exist as pictures. A bar says nothing without a tooltip naming the step, duration, cost and verdict.
  Done when: hovering or selecting a bar shows a card with those four fields.

- **Morph the failing test into the passing one** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: "prove the test fails without the change" is Foreman's signature moment, and it is currently text. A before/after pair of chips that turns red to green on the run would show it.
  Done when: the proof step shows both runs side by side, and the second chip animates to its result only after the real exit code arrives.

- **Narrate the run offline with a tiny local model (wild)** — FEATURE — value 3 — effort L — risk med — category: ui
  Why: wild. A local model, run via Ollama or similar, summarizes the event log into one plain line such as "fixing the parser, tests red". It stays on the machine and is off unless enabled.
  Done when: with the setting on and a local model available, the header line updates at each station change, and with it off no process starts.

- **Add a shoulder-surf shutter key (wild)** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: wild. One key swaps the screen for a bland view, such as a plain progress bar with no code or paths, and the same key brings the real view back. It is useful on a train or in a shared office.
  Done when: pressing the key replaces every code, path and prose cell with the neutral view, and a golden-frame test finds none of the hidden strings on screen.

- **Take the theme from the terminal's own palette (wild)** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: wild. Querying the terminal for its background and 16 colors (OSC 4/11) makes the TUI match any setup with no config. The Claude Code pane's #262626 mismatch (T-1217) shows what a hard-coded background costs.
  Done when: on a terminal that answers the query, the TUI derives its surfaces from the reported colors, and on one that doesn't it falls back to the default theme.

- **Print a poster of the run as unicode half-block art (wild)** — FEATURE — value 2 — effort M — risk low — category: ui
  Why: wild. A one-screen ANSI picture of the run (stations, Gantt, proof chips, cost), paste-safe and carrying no code, would work as a shareable receipt and be private by construction.
  Done when: `fm code poster RUN` writes a file under 80 columns wide that contains none of the run's file contents.
