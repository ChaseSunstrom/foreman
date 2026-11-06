# Brainstorm — lens: beautiful UI and motion

- **Fly the evidence to its claim** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: assumption: the TUI shows check chips and a station track, but nothing visually ties a passing verify run to the step it proves. Foreman's pitch is "prove its work with commands it ran".
  Done when: in a golden-frame sequence, a green chip's glyph travels from the verify row to its step on the rail over at least 6 frames, and the step is marked proved only on the last frame.

- **Write motion as a declarative score** — CLEAN — value 4 — effort L — risk med — category: motion engine
  Why: assumption: animations are coded imperatively, and the exporter (animated SVG, replay) would have to reimplement each one. Earlier ideas have a tween clock and an SVG export, but nothing says one definition drives both.
  Done when: one JSON/TOML motion file renders identically in the live TUI and the SVG exporter, checked by a test comparing frame N of each.

- **Dither gradients on 256 and 16 colors** — FEATURE — value 3 — effort M — risk low — category: color
  Why: the request says "not just static colors". Earlier ideas have truecolor gradients and capability fallback, but a fallback that collapses a gradient into banded steps looks static again. Ordered dithering with shade glyphs (░▒▓) keeps the smoothness. Assumption: the user's terminal or pane (the docked pane paints #262626) sometimes lacks truecolor.
  Done when: with COLORTERM unset, the gradient bar renders at least 8 visually distinct levels using shade glyphs, and a golden frame confirms it.

- **Animate the context gauge through compaction** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the pack shows compaction-storm soaks, forced compactions and a context-tax ratchet, so compaction is a central event. Assumption: the TUI shows it as a number jump at most.
  Done when: a compaction event makes the gauge squeeze down over about 400 ms and leaves a "compacted" tick mark on the gauge's history.

- **Zoom the Gantt semantically** — FEATURE — value 3 — effort M — risk low — category: charts
  Why: runs are long, with marathon unattended sessions. A fixed time scale hides either the whole run or the individual calls. Assumption: the Gantt has one scale.
  Done when: `+`/`-` changes the Gantt scale between whole-run, minute and second views. Labels gain or lose detail by level, and a golden frame exists for each level.

- **Share one palette source with the site and web UI** — CLEAN — value 3 — effort S — risk low — category: design language
  Why: the recent commit "landing theme" and the web UI surface show Foreman has several skins. Assumption: the TUI themes and the site colors are defined separately and can drift.
  Done when: a single palette file generates both the TUI default theme and the site's CSS variables, and a test fails if either copy is edited by hand.

- **Show the headline number in big block numerals** — FEATURE — value 3 — effort S — risk low — category: typography
  Why: the user complained that the TUI "looked like crap with all the text". One large 3×5 block-font figure (tests passing, cost against cap, tasks left) is readable from across a room and is a picture, not text. Assumption: the header uses small text for these numbers.
  Done when: the header shows at least one figure at least 3 rows tall, which collapses to plain digits below a height threshold.

- **Stagger list entrances** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: assumption: new steps, chips and history rows appear all at once, so the eye can't tell what is new. A 30–40 ms cascade reads as ordered arrival, and reduced-motion mode keeps it instant.
  Done when: four rows added in one tick get entrance offsets that increase by a fixed delay, and the delay is 0 under reduced motion.

- **Animate reflow on resize and collapse** — FEATURE — value 3 — effort M — risk med — category: layout
  Why: earlier ideas cover resize safety and layout stability, but not continuity. Panels that snap to new positions break the "motion explains state" principle. Assumption: layout changes currently jump.
  Done when: toggling a panel moves neighbouring panels to their new rects over a short tween instead of jumping. A test confirms an intermediate frame lies between the two end rects.

- **Correct drawn circles and rings for the cell aspect ratio** — FIX — value 2 — effort S — risk low — category: charts
  Why: assumption: rings, dials and spinners drawn in braille or half-blocks look oval on a 1:2 cell grid. Ideas such as a progress ring around the screen and a pixel canvas would inherit the distortion.
  Done when: a ring-drawing test shows width and height within 5% of each other after an aspect correction setting is applied.

- **Add inertial scrolling to the transcript** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: assumption: scroll is line-stepped. The follow-camera exists, but a flick on a trackpad or wheel that glides and settles feels far more polished than jumping.
  Done when: a burst of wheel events produces a decelerating scroll that ends within 300 ms, and no overshoot beyond the content end.

- **Wild: Render overlays as frosted glass** — FEATURE — value 3 — effort M — risk low — category: depth. Wild.
  Why: assumption: the command palette and cards are opaque boxes. Alpha-blending the RGB of the cells beneath, with a slight desaturation, makes layers feel physical in truecolor terminals.
  Done when: opening the palette over a colored panel shows the underlying cell colors blended at the set alpha, verified by a golden frame, and it falls back to a solid box without truecolor.

- **Wild: Let a tide line show the queue draining** — FEATURE — value 3 — effort M — risk low — category: ambient. Wild.
  Why: the pack has a long task queue and an "unattended" use case. A faint waterline across the bottom of the pane that rises as the open-task count falls is readable at a glance without a number.
  Done when: the waterline height is a pure function of done/total tasks, with a slow wave on its crest that stops under reduced motion.

- **Wild: Match reveal speed to the user's reading pace** — FEATURE — value 2 — effort M — risk med — category: motion. Wild.
  Why: assumption: typewriter-settle uses a fixed rate. Measuring how quickly this user scrolls or dismisses text and adapting the rate gives text that is never too slow or too fast. Everything stays local.
  Done when: after 20 dismissals at a faster pace, the reveal rate rises within set bounds, and the learned value is one local setting that can be reset.
