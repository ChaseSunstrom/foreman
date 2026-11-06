# Brainstorm — lens: beautiful UI and motion

- **Throttle run-state announcements to one live-region message per 5 s** — FIX — value 4 — effort S — risk low — category: accessibility
  Why: assumption: the web UI and pane update on every journal event, so a screen reader either floods or stays silent during a burst.
  Done when: a test replays 50 events in 2 s and asserts at most one `aria-live` announcement in that window, with the final state always announced.

- **Enforce a reduced-motion branch for every animation in the build** — CLEAN — value 3 — effort S — risk low — category: motion safety
  Why: the pack lists reduced motion as a single switch, but nothing checks that each new keyframe honours it.
  Done when: the build fails on a fixture CSS file containing an unguarded `@keyframes` or transition, and passes once the `prefers-reduced-motion` branch is added.

- **Tint each diff gutter by edit age so fresh lines glow and settle over the session** — FEATURE — value 3 — effort S — risk low — category: diff clarity
  Why: assumption: in a long session it is hard to tell which hunks came from this turn and which came earlier.
  Done when: a diff with lines from two turns renders two distinct gutter tints, and the older tint is at least 3:1 contrast against the background.

- **Show a reason tooltip on every disabled control** — FEATURE — value 3 — effort S — risk low — category: clarity
  Why: assumption: a greyed-out "close" or "run" button gives no reason, so users guess which gate is holding it.
  Done when: each disabled control in the web UI and pane names one blocking cause in its tooltip, and a test fails if a disabled control has an empty reason.

- **Add a hairline progress edge to the web header** — FEATURE — value 3 — effort S — risk low — category: status glance
  Why: assumption: the full work bar is hard to read from across the room, but a 1 px edge along the top shows motion at a glance.
  Done when: the edge's width matches the work bar's fraction within one percent in a fixture run, and it is hidden when no run is open.

- **Make History day headers sticky and compress them on scroll** — FEATURE — value 2 — effort S — risk low — category: navigation
  Why: assumption: a long History list loses its date context once the header scrolls away.
  Done when: a day header stays visible while its rows scroll and shrinks to one line, and no row is covered by it in a 200-row fixture.

- **Tween token and dollar counters upward only, with tabular figures** — FEATURE — value 2 — effort S — risk low — category: numeric motion
  Why: the pack asks for tabular figures and damped estimates, but counters still jump. Upward-only tweens keep the "never goes backwards" rule visible.
  Done when: a counter reaches its target within 400 ms, never decreases during a tween, and its width does not change between frames.

- **Show run state as a favicon dot that swaps between three shapes** — FEATURE — value 2 — effort S — risk low — category: ambient status
  Why: assumption: people keep the web UI in a background tab and cannot see its state without switching to it.
  Done when: the favicon changes to one of three distinct shapes (running, needs you, done) within 2 s of the matching journal event, and each shape is still readable at 16 px.

- **Set receipts in a fixed measure with hanging punctuation** — CLEAN — value 2 — effort S — risk low — category: typography
  Why: the close receipt is the main prose a user reads each time, and long lines make it tiring.
  Done when: receipt text wraps at no more than 68 characters, and a snapshot test shows punctuation hanging outside the text column.

- **Wild: drive a slow ambient field whose turbulence follows the queue's spend rate** — FEATURE — value 2 — effort M — risk med — category: ambient delight
  Why: wild: a background that moves with spend makes cost felt without a number. Capped at 1 fps and paused on battery or when the tab is hidden.
  Done when: the field's frame rate stays at or below 1 fps in a 5-minute fixture run, and CPU use with the tab hidden is below 1% in the bench.

- **Wild: page-turn between the web UI and the pane when one run is open in both** — FEATURE — value 2 — effort M — risk low — category: surface continuity
  Why: wild: a short turn animation tells the user the same run has moved surfaces, which a cut does not.
  Done when: switching surfaces with the same run open plays one transition under 300 ms, and it is skipped under reduced motion.

- **Wild: draw each run as a plotter path that finishes when its gate does** — FEATURE — value 2 — effort M — risk low — category: progress motion
  Why: wild: a single stroke that completes at the gate gives a finished-feeling close that a spinner never does.
  Done when: the stroke reaches 100% exactly when the gate verdict lands, and a fixture with a failing gate leaves it stopped short with a visible break.
