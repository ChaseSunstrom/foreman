# Brainstorm — lens: beautiful UI and motion

- **Ghost-preview each edit before it lands** — FEATURE — value 4 — effort M — risk med — category: motion explains state
  Why: wild. The pane shows a diff only after the write, so a wrong target costs a full revert. assumption: a faint outline on the target lines, shown for about 300 ms before the write, makes the location visible first.
  Done when: a recorded fake edit shows a ghost frame whose line range matches the first diff hunk, and that frame appears before the write timestamp.

- **Use one motion scale: three durations and one easing curve** — CLEAN — value 3 — effort S — risk low — category: motion system
  Why: assumption: the web UI, pane, desk card and site charts each set their own timing. One shared scale keeps them consistent.
  Done when: a test fails if any animation duration or easing in the web UI, pane or site falls outside the scale.

- **Skip any transition with one key and never delay input** — FEATURE — value 4 — effort S — risk low — category: interruptible motion
  Why: assumption: a reveal or stalled-card countdown can hold a key press. The user should always act at once.
  Done when: a key sent 50 ms into a transition is handled within 50 ms, and the transition ends at its target state.

- **Highlight only the changed words inside each diff line** — FEATURE — value 4 — effort S — risk low — category: diff legibility
  Why: assumption: a one-word change in a long line reads as a full rewrite when the whole line is marked.
  Done when: a diff from `x = 1` to `x = 2` marks only the `1` and `2` spans in the rendered output.

- **Pick side-by-side or inline diff from the pane's width** — FEATURE — value 3 — effort S — risk low — category: responsive diff
  Why: assumption: the pane is docked beside the chat, so its width changes. A fixed layout wraps or clips code.
  Done when: at 120 columns the diff renders side by side, at 70 columns it renders inline, and neither wraps a code line.

- **Repaint only the cells that changed in the Foreman pane** — PERFORMANCE — value 3 — effort M — risk med — category: pane rendering
  Why: T-1217 shows the pane's background being painted wrongly, and a full redraw each tick adds flicker and cost. assumption: most ticks change no visible state.
  Done when: a captured terminal session with no state change writes zero bytes to the pane region.

- **Screenshot the web UI at desktop and phone widths on every commit** — FEATURE — value 4 — effort M — risk low — category: visual regression
  Why: test_showpieces checks markup, not pixels. assumption: a CSS change can break a layout while the markup stays the same.
  Done when: CI renders the index page at 1280 px and 390 px and fails when any pixel differs from the committed baseline by more than 0.5%.

- **Take the pane's accent colour from the project's own brand** — FEATURE — value 2 — effort S — risk low — category: personal theme
  Why: wild. The pane could read a repo's CSS variables or theme colour and tint its accents, so each project's pane looks like that project's product.
  Done when: a repo with `--brand: #ff5500` gives the pane that accent, and a repo without one keeps the default.

- **Drag a reveal slider between the before and after of a UI change** — FEATURE — value 3 — effort M — risk low — category: visual review
  Why: wild. A compare slider over two headless screenshots lets the user see a UI change in one glance.
  Done when: a closed UI task's receipt holds both screenshots, and the slider at 50% shows the before image's pixels on the left half.

- **Scroll the site through one real run, with the state changing as you scroll** — FEATURE — value 3 — effort M — risk low — category: storytelling
  Why: wild. The site already draws its charts once on view. A scroll-driven walkthrough of a recorded run would show the loop step by step instead of describing it.
  Done when: scrolling from top to bottom moves the run's state from "planned" to "closed" in recorded order, with no frame out of sequence.

- **Middle-truncate long task titles so the id and verb stay visible** — FIX — value 2 — effort S — risk low — category: text fit
  Why: assumption: the pane's narrow width cuts titles at the end, which hides the task id and the verb.
  Done when: a 200-character title at 60 columns still shows its `T-` id, its first word and an ellipsis in the middle.

- **Honour NO_COLOR and reduced motion with one switch** — FIX — value 3 — effort S — risk low — category: accessibility
  Why: assumption: the pack shows no such switch, and the pane and desk animate by default.
  Done when: with the switch on, the output has no colour escape codes and no animation frames after the first.
