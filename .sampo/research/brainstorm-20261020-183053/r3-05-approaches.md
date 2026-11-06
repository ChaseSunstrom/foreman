# Brainstorm — lens: approaches

- **Build a cell-shader layer where a theme is a function** — FEATURE — value 5 — effort M — risk med — category: rendering
  Why: the request is "not just static colors"; earlier ideas add gradients and pulses one effect at a time. A per-cell `(x, y, t, state) -> color` function, in a sandboxed expression format, makes every effect and theme data on one primitive. Assumption: the renderer can call a function for each dirty cell within the frame budget.
  Done when: a 20-line shader file makes the station track shimmer, and `fm code tui --calm` evaluates the same file at a fixed `t` with identical output across runs.

- **Interpolate color in OKLCH, not RGB** — FIX — value 4 — effort S — risk low — category: color
  Why: the pack's gradient ideas never say how colors blend. RGB mixing goes muddy between hues (green to red passes through brown), and that is what "static, ugly colors" looks like once animated. Assumption: the current theme code lerps in sRGB.
  Done when: a unit test shows a green-to-red ramp with monotonic perceptual lightness, and a golden frame of the cost-burn gauge shows no brown midpoint.

- **Add a pixel-canvas primitive with half-block, quadrant, sextant and braille backends** — FEATURE — value 4 — effort M — risk low — category: charts
  Why: the Gantt, sparklines, token columns and bars each need their own sub-cell drawing. One `Canvas.plot(x, y, color)` abstraction picks the finest glyph set the terminal supports and gives all of them antialiased edges. The new Gantt and token river become small clients of it.
  Done when: one canvas call draws the same line in all four glyph backends, and a golden test covers each.

- **Use springs instead of fixed-duration easing** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: earlier ideas say "ease between states". Event-driven runs retarget constantly (a step finishes mid-transition), and fixed tweens snap or restart. A velocity-carrying spring retargets mid-flight with no jump.
  Done when: a test that retargets a bar at 50% progress shows continuous position and velocity across the retarget.

- **Mark state with underline style and color instead of only foreground color** — FEATURE — value 3 — effort S — risk low — category: typography
  Why: SGR curly/dotted/dashed underlines and the separate underline color (SGR 58) are cheap, widely supported, and give a second visual channel. Check chips and refusals would read without hue, which also serves the color-blind mode. Assumption: the target terminals render them (kitty, wezterm, iTerm2, foot, recent VTE) and the rest ignore them harmlessly.
  Done when: a refused guard verdict renders with a red curly underline, and the same frame with `NO_COLOR` still differs from a passed one.

- **Prove the TUI never touches the network** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the privacy side of this pack is thin, and local-first is a claim a test can enforce. Run the TUI test suite with socket creation patched to raise, so a themed, animated and extended TUI can't quietly phone home, fetch fonts or check for updates.
  Done when: a test replays a full fake run and every theme with `socket.socket` patched to raise, and passes.

- **Give extension widgets a capability manifest** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: the idea list proposes executable JSON-line widgets and a plugin API, but no limits on what they read. A widget declares `reads: [events, diff]` and `net: none`, runs with network blocked and a scrubbed environment, and sees only declared event kinds. Assumption: widgets run as subprocesses.
  Done when: a widget that opens a socket or reads an undeclared event kind fails with a named error in the pane, and the TUI keeps running.

- **Add a stream-safe toggle with stable pseudonyms** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: the earlier redaction idea covers secrets. This toggle (one key) is for screen sharing and recording: home path, email, hostnames and repo names are replaced by consistent aliases (`~/proj-a`) so a shared recording still reads coherently. The user email in this session's context shows the real data in play.
  Done when: with the toggle on, a golden frame contains none of a seeded list of identifiers, and the same alias appears for the same input across frames.

- **Fall back to a plain-text transcript when the pane can't animate** — FEATURE — value 3 — effort S — risk low — category: fallback
  Why: the pack covers pipes and `TERM=dumb`. This idea is narrower: when two frames in a row overrun the budget (slow ssh, a weak CI box), the TUI drops to static, line-per-event output, announces it once, and tries to return after 30 s. Assumption: a frame-time sensor exists or is cheap to add.
  Done when: injecting a 200 ms render delay switches modes within 2 frames and prints the notice once, and removing the delay restores animation.

- **Add a "wild": a pet whose health is the harness's discipline** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: assumption: users show off terminals. A small half-block creature on the status line perks up with proved tasks, droops when the guard refuses repeatedly, and sleeps when the queue is empty. It turns "proved vs claimed" into something people notice without reading numbers.
  Done when: replaying a run with 3 proved closes and 2 refusals produces distinct sprite states at each point, and `--no-pet` removes it.

- **Add a "wild": a theme that follows local sunrise and sunset** — FEATURE — value 2 — effort S — risk low — category: color — wild
  Why: assumption: long unattended runs span the evening. Compute solar position offline from the timezone and a user-set latitude (no location lookup), then drift the palette's warmth and brightness through the day. This respects the local-first rule and makes a static palette feel alive.
  Done when: a test with a fixed latitude and clock gives a cool palette at noon and a warm, dim one at 22:00, and no network or geolocation call is made.

- **Add a "wild": a two-minute generative opening that is also the cold-start check** — FEATURE — value 2 — effort M — risk med — category: delight — wild
  Why: assumption: first impression matters for the TUI the user called ugly. A half-second boot animation draws the station track by testing each capability (truecolor, synchronized output, underline styles, mouse) and ticks each off. The result picks the render profile and doubles as `--doctor` output.
  Done when: launching on a truecolor terminal and under `TERM=vt100` shows different capability lines, and the chosen profile is saved to the settings file.

- **Cap the TUI's own cost with a render-time budget in the bench** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: Foreman already ratchets hooks, CPU time and context bytes in CI, and the new animation makes the TUI a CPU consumer next to the worker. A bench replays a canned 500-event run headless and fails if mean ms per frame or total CPU exceeds a stored bound. Assumption: CI can use CPU time, as the T-1281 fix did.
  Done when: the bench passes on the current tree and fails when a 50 ms sleep is injected in the draw path.
