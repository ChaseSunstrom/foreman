# Brainstorm — lens: beautiful UI and motion

- **Make Foreman's own chrome unforgeable** — SECURITY — value 4 — effort M — risk low — category: trust UI
  Why: the pack covers escape-sequence stripping and provenance glyphs, but nothing stops tool or third-party skill output from drawing a fake Foreman panel. This matters more once six upstream repos' plugins can run inside the app. Assumption: panel borders are plain glyphs today.
  Done when: a test feeds output that imitates a panel, a verdict stamp and a "needs you" strip, and the frame shows it inside a visibly different quarantine gutter. Genuine chrome uses a per-session glyph seed, and the test asserts that only genuine chrome carries it.

- **Encode progress certainty in texture** — FEATURE — value 4 — effort S — risk low — category: honest motion
  Why: the pack has progress bars, ETA arcs and ghost-pace markers, but none says whether a number is measured, estimated or unknown. Assumption: bars currently share one style. The user keeps saying "it just isn't doing anything", so fake-looking progress costs trust.
  Done when: measured progress renders solid, estimated renders hatched and unknown renders as a travelling dotted segment. A lint fails any bar given a value with no source tag, and golden frames show all three.

- **Add minimum-dwell and hysteresis to status changes** — FIX — value 3 — effort S — risk low — category: motion stability
  Why: with stall detection, heartbeats and event floods driving states, a state that flips running→waiting→running in 200 ms shows up as flicker. Assumption: states render the instant an event arrives.
  Done when: a replay with a rapid state oscillation produces at most one visible transition per 400 ms. Terminal states (red, closed) bypass the dwell, and a test asserts this.

- **Remap worker ANSI colours onto theme roles** — FEATURE — value 4 — effort M — risk low — category: theming
  Why: runners such as claude, codex, aider and gemini emit their own SGR colours, which clash with the theme and can be unreadable on the docked #262626 background (T-1217). Assumption: worker output is currently passed through raw or stripped.
  Done when: a fixture of raw SGR red, green and dim output renders in the active theme's semantic error, success and muted roles. Every pair passes the contrast check on light and dark themes.

- **Fold stack traces by ownership** — FEATURE — value 4 — effort M — risk low — category: failure legibility
  Why: failure cards are planned ("first red line"), but a raw trace still buries the project frame under vendor frames. Assumption: traces print unfolded.
  Done when: a Python and a Node trace fixture show project frames bright and vendor frames dimmed into a single "7 library frames" row. Expanding that row works, and the first project frame is a clickable `file:line`.

- **Highlight diff syntax with a stdlib-only lexer table** — FEATURE — value 4 — effort M — risk med — category: diff rendering
  Why: "syntax-aware diff colour" is listed, but the stdlib-only constraint rules out Pygments. Python can use `tokenize`; other languages need small data-driven rule tables.
  Done when: diffs of .py, .js, .sh, .json and .md files colour keywords, strings and comments, and a degrade ladder drops to plain on 16-colour terminals. A 5,000-line diff highlights within a stated frame budget.

- **Define a three-level interruption ladder** — CLEAN — value 3 — effort S — risk low — category: attention design
  Why: the pack proposes many separate alert mechanisms (toasts, bell, tab title, OSC 9, pulsing strip, push) with no single rule for when each fires. Assumption: they were added independently.
  Done when: one table maps ambient, nudge and interrupt each to its visual, motion, sound and notification spec. A test fails if any emitter is not tagged with a level, and the same event never appears at two levels.

- **Build one data-grid component for every table** — CLEAN — value 3 — effort M — risk low — category: components
  Why: the queue, runs, runners, skills, grants and marketplace shelf each need sort, filter chips, column choice and truncation. Without a shared grid they will drift apart.
  Done when: all list views use one `grid()` function with sticky header, sort key, filter chips and ellipsis rules. Golden frames for each view are generated from it, and a lint rejects hand-rolled column layouts.

- **Give relative times a tick-stable grammar** — FIX — value 2 — effort S — risk low — category: microtypography
  Why: "last heard 12 s ago" counters on the stall line and heartbeat re-layout as they roll over from 9 s to 10 s or 59 s to 1 m. Assumption: widths aren't reserved.
  Done when: relative times render in fixed-width tabular form with one unit vocabulary. A fuzz test over 0 s to 99 h never changes a line's width.

- **Make recorded SVG casts re-skin with CSS variables** — FEATURE — value 3 — effort M — risk low — category: site and docs
  Why: demo/live.svg is a fixed-palette recording, and the site theme and reduced-motion state don't affect it. Assumption: the palette is baked in.
  Done when: the exported SVG references palette variables only, and the site's theme toggle recolours the cast. Under `prefers-reduced-motion` it shows its final frame, and a CI check rejects hard-coded colours.

- **Wild: shade model prose by token confidence** — FEATURE — wild — value 3 — effort M — risk med — category: epistemic UI
  Why: assumption: OpenAI-compatible endpoints and codex can return logprobs. Low-confidence spans would show as a faint haze and confident spans as solid text, so users see where a small model is guessing before its slot is checked.
  Done when: replaying a logprob fixture shades low-probability tokens, the shading is off by default, and runners without logprobs show nothing.

- **Wild: add a tape-counter footer** — FEATURE — wild — value 2 — effort S — risk low — category: delight
  Why: assumption: the footer shows static elapsed time and token counts. A cassette-style counter whose reel glyphs step faster with tokens per second, and stop dead when the harness is wedged, gives liveness and throughput in one glance.
  Done when: the glyph rate tracks a scripted token rate in a test, freezes when the heartbeat lapses, and `--calm` renders plain digits.

- **Wild: add pressure mode for deadline and spend boxes** — FEATURE — wild — value 3 — effort M — risk med — category: adaptive UI
  Why: the pack proposes time-and-money boxes and spend caps but only as gauges. Assumption: users near a cap want less on screen, not more. Past 85% of a box, the chrome could shed everything except the remaining box, the next action and "needs you".
  Done when: a replay that crosses 85% of the cap collapses to that three-element view with a one-beat transition. A key restores the full view, and crossing back below the threshold restores it automatically.
