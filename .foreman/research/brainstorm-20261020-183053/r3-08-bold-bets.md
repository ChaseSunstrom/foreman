# Brainstorm — lens: bold bets

- **Keep the TUI's data and screenshots on-box by default** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: assumption: exports (animated SVG, crash bundle, phone page, postcards) are all on the idea list and any of them can leak prompts, paths or keys. Nothing says what leaves the machine.
  Done when: with default settings a test run of every export and share command makes zero network connections (checked by a socket-blocking test) and each export writes a redaction report beside it.

- **Add a "paint budget" that the TUI proves in the bench** — PERFORMANCE — value 4 — effort M — risk low — category: ui
  Why: the pack shows Foreman is measured on CPU time (CI bounds, hook bench, context-tax ratchet), and the user wants cheaper and faster. Animations that cost the harness time contradict that.
  Done when: `fm code bench` records TUI CPU share and bytes written per minute with animation on and off, and a test fails if animation adds more than a set percent over the calm mode.

- **Make the screen a single composed "now" scene with one focal element** — FEATURE — value 5 — effort L — risk med — category: ui
  Why: the user said it "looked like crap with all the text" and asked for pictures, then asked again for more than static colors. Separate animated widgets can look busy. One layout rule fixes it: the focal element changes with the active station (diff while editing, Gantt while verifying, verdict while guarding) and everything else dims to a quiet rail.
  Done when: golden frames for each station show exactly one region at full contrast, and changing station cross-fades the focus in under 300 ms.

- **Derive theme palettes from the terminal's real colors** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: T-1217 records that Claude Code paints the docked pane at #262626, so fixed theme colors clash. Probing the background (OSC 11) and generating a contrast-checked ramp gives gradients that fit anywhere.
  Done when: on a probed light, dark and #262626 background, every theme's text and chip pairs pass a contrast ratio test, and a fallback is used when the probe gets no answer.

- **Run a tamper-proof "truth strip" that cross-checks the picture against the log** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: Foreman's identity is proof over claims. Animations that look done but aren't would break that. A strip compares what the screen shows (steps green, tests passed) with the event log, and flashes amber on disagreement.
  Done when: a test injects a log where a step failed but the render state says passed, and the strip shows a mismatch within one frame.

- **Provide a fully offline themes-and-motion pack format with signed local files** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: assumption: user theme files, extension widgets (any executable printing JSON lines) and hot-reload are planned. Executables loaded from a theme folder are a code-execution path.
  Done when: widgets run only if listed in a local allowlist with a content hash, and a changed file is refused with a message naming the hash mismatch.

- **Add a typographic hierarchy built from block, braille and box glyphs, not text** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: the redesign already moved toward pictures (station track, chips, bars). A shared glyph kit (thin and thick bars, eighth-blocks for smooth fills, rounded corners) gives sub-cell animation smoothness without graphics protocols.
  Done when: a progress bar advances in eighth-cell steps in a snapshot test and renders identically in a 16-color fallback using ASCII.

- **Wild: Turn the guard into a visible "bouncer" that blocks the screen edge** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The guard is Foreman's signature, but refusals are text today. A refused command slams a bar across the border, shows the command crossed out, and slides the suggested fix in below.
  Done when: a guard refusal event produces a distinct 4-frame sequence in golden frames, and the fix line appears after it.

- **Wild: Play the run back as a "match report" on a timeline with highlights** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: wild. Replay is on the list, but a finished run could instead auto-cut to its 5 key moments (first red, the fix, the proof, the refusal, the close) with a one-line caption each, shareable as a local HTML file.
  Done when: `fm code replay RUN --reel` outputs a self-contained HTML file under a size limit with at most 7 moments, each linked to an event id.

- **Wild: Let the TUI wear the repo's mood from its test history** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. Per-repo accent is already imagined. Going further, tint the header warm when the last N runs passed first time and cool when many needed retries, from data Foreman already keeps.
  Done when: two fixture repos with different pass histories produce different header tints, and `--calm` turns it off.

- **Wild: Make an `fm code tui --cast` mode that streams frames to a second terminal over a local socket** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: wild. A second monitor or tmux pane can run a viewer on a Unix socket, with no network, so the harness stays detached from rendering. It fits the detachable-viewer and local-first ideas.
  Done when: a viewer connected to the socket shows the same frame as the primary within 100 ms, and killing the viewer never changes the run's exit status.

- **Ship a motion "linter" that fails the build on idle animation** — CLEAN — value 3 — effort S — risk low — category: ui
  Why: the idea list says animate on state change, not idly, and respect reduced motion. Without a check this drifts. Run a headless clock with no events and assert zero cells change.
  Done when: a test runs the renderer for 10 simulated seconds with no events and asserts no writes beyond the clock cell, and it fails when a widget animates idly.

- **Add a first-run "this is what the colors mean" strip generated from the theme registry** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: more colors and motion add meaning the user must learn. Generating the legend from the same registry keeps it correct as themes change.
  Done when: adding a new status color to the registry makes it appear in the legend with no other edit, verified by a test.
