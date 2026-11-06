# Brainstorm — lens: capability map

- **Add an egress ledger panel** — FEATURE — value 5 — effort M — risk low — category: privacy
  Why: assumption: `fm code` has a stdlib model client (T-1211) and a `models.json` of endpoints, but the pack shows no view of what leaves the machine. The thin lens is privacy.
  Done when: after a fake-model run, `fm code tui` lists every outbound request (host, bytes, file paths included), and its total matches the client's request log.

- **Fence secret paths out of model context** — SECURITY — value 5 — effort M — risk med — category: privacy
  Why: assumption: the guard already stops commands but nothing is shown to block `.env` or key files from being read into a prompt. Locked chips in the UI would make the fence visible.
  Done when: with `.env` on the deny list, a worker read of it is refused, the file never appears in the request body, and the TUI shows a "locked" chip.

- **Gate OSC 52, title and bell output behind settings** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the ideas list proposes tab-title status, bells and clipboard copy, but those escape sequences leak run text to the terminal, tmux and ssh peers. They should be off until switched on.
  Done when: a pty test with default settings sees no OSC 52 or OSC 0/2 bytes, and each turns on only through its own named setting.

- **Add a panic-mask key** — FEATURE — value 4 — effort S — risk low — category: privacy, ui
  Why: assumption: people run it on screen-shared or public displays. One key (for example `Ctrl-\`) replaces all prose, paths and diffs with block glyphs while keeping the motion and station track.
  Done when: in a golden-frame test, the masked frame contains none of the transcript or path text, and the same key restores the view.

- **Ship a share-safe export profile** — FEATURE — value 4 — effort M — risk low — category: privacy
  Why: the ideas list has SVG, HTML and postcard exports, but nothing on stripping home paths, usernames, hostnames and repo remotes. Those leak the moment a clip is shared.
  Done when: exporting a run recorded under `~` yields a file with no `chase`, hostname or remote URL, checked by a scan test.

- **Add an inline mode that keeps terminal scrollback** — FEATURE — value 4 — effort M — risk med — category: ui
  Why: assumption: a full-screen TUI hides history from the terminal's own scroll and search. Printing finished blocks above a live bottom region gives both the polish and native selection and copy.
  Done when: `--inline` runs leave every finished station's card in scrollback after exit, and the live region never exceeds N rows.

- **Add transcript search and filter (`/`)** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: assumption: the "model's words behind" the pictures grow long, and the user's complaint about "all the text" suggests they want to find things instead of reading. Filter by station, verdict or text.
  Done when: typing `/red` narrows the list to red verdicts and failed checks, and `Esc` restores the full list.

- **Add a notification center with toasts** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: assumption: the "needs you" strip, verdict flashes and release notes each invent their own surface. A single stack with auto-expiry and a history key gives them one home.
  Done when: three events in one second show as stacked toasts that expire, and `n` lists all of them with timestamps.

- **Add a side-by-side and unified diff toggle** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the ideas list covers diff syntax color and line reveal but not layout, and wide terminals waste space on unified diffs.
  Done when: at 160 columns, `d` toggles between two layouts, and below 100 columns it falls back to unified.

- **Add an in-TUI settings screen with undo** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the ideas list has theme files, keybindings and layout config, all of which are edit-a-file. A live screen that writes through the atomic last-good path would be easier to use.
  Done when: changing the theme and the motion level in the screen takes effect immediately, and `u` reverts the last change on disk.

- **Run a workspace tab bar for parallel lanes** — FEATURE — value 3 — effort L — risk med — category: ui
  Why: assumption: T-0792 (lanes and fleet) and the worker leases imply several concurrent runs. A tab bar would show each one's mini station track and a badge when it needs you.
  Done when: two fake runs appear as two tabs with live mini tracks, and `Alt-2` switches without a redraw glitch.

- **Fork a replay at any frame into a new run** — FEATURE — value 4 — effort L — risk high — category: replay
  Why: wild. The scrubber is already on the list, and the harness checkpoints and event log could turn "what if I'd steered here" into a real branch.
  Done when: scrubbing to step 3 of a finished fake run and pressing `f` starts a new run whose first three steps match the log and whose fourth takes new input.

- **Cage the worker in an egress-only network namespace** — SECURITY — value 4 — effort L — risk high — category: privacy
  Why: wild. The environment is hardened Linux, so a worker whose only reachable host is the model endpoint would make "nothing leaves" enforceable instead of just logged. The TUI would show a "caged" badge.
  Done when: a worker command that tries `curl example.com` fails inside the cage while the model call succeeds, and the badge is visible.

- **Add a harness pet that grows with proved tasks** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A tiny glyph creature in the footer is fed by green proofs and sulks after guard refusals. It keeps its state in a local file and stays off by default.
  Done when: closing a task proved changes the pet's state in the next frame, and `--no-pet` or reduced motion shows nothing.
