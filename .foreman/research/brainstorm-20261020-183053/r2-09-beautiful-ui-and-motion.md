# Brainstorm — lens: beautiful UI and motion

- **Fisheye the active station** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: the user said the TUI "looked like crap with all the text". A fisheye gives the active station full detail and shrinks the rest to a one-glyph chip, so the screen shows one thing at a time. A glide animation moves the expansion between stations.
  Done when: a golden-frame test shows the active station expanded and the others collapsed, and a station change produces at least 3 distinct intermediate widths.

- **Fold model prose into expandable headline chips** — FEATURE — value 5 — effort M — risk low — category: progressive disclosure
  Why: the steer says the model's words went "behind" the pictures. Folding each message to a ~40-column headline, with a glyph for its kind (thinking, plan, claim), completes that. A key or click opens an accordion that eases open over 3 frames.
  Done when: a 500-word model message renders as one line, and pressing Enter expands it and Esc folds it back.

- **Contrast-correct every theme against the real background** — FIX — value 4 — effort S — risk low — category: accessibility
  Why: T-1217 notes that Claude Code paints the docked pane #262626, so fixed theme colors can be unreadable on it. The theme loader computes WCAG contrast against the detected or configured background and nudges failing foregrounds. `fm code theme check` lists what it changed.
  Done when: a test loads every bundled theme on #262626 and on white, and no text slot falls below 4.5:1.

- **Hold layout still while numbers tick** — FIX — value 4 — effort S — risk low — category: polish
  Why: assumption: live cost, tokens and timers in a text UI make neighbouring columns jitter. Counters get fixed-width, right-aligned slots with reserved padding, and the renderer never moves a neighbour.
  Done when: a replayed 200-frame run shows no cell outside a counter's slot changing when only the counter's value changes.

- **Roll digits like an odometer** — DELIGHT/FEATURE — value 3 — effort S — risk low — category: motion
  Why: the cost and dollar-cap gauge is already planned as a sparkline. Digit-level rolling, where each column steps through its intermediate glyphs in 2–3 frames, makes spend feel physical without extra screen space. It is off under reduced motion.
  Done when: a cost change from 0.19 to 0.21 renders a middle frame with a rolling digit, and under `--calm` it jumps straight to the new value.

- **Cool recently changed cells like heat** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: this goes past the pulse and flash ideas by giving everything on screen one timer. A cell that changed in the last 2 s is bright, then eases to the muted baseline over ~8 s. The eye finds what moved without anything animating while idle.
  Done when: a frame test shows a changed chip at full intensity at t=0 and at baseline after the decay window, with no repaint in between when nothing else changed.

- **Follow-camera with a "N new" chip** — FEATURE — value 4 — effort M — risk low — category: scrolling
  Why: assumption: a long unattended run scrolls constantly. Auto-follow glides to the active station. Scrolling manually pauses it and shows a "↓ 12 new" chip, and the End key re-engages follow with an eased catch-up.
  Done when: a scripted scroll-up during output stops following and shows the chip, and End returns to the live edge.

- **Show a contextual key-hint bar that flashes on press** — FEATURE — value 3 — effort S — risk low — category: discoverability
  Why: the TUI is meant to be customizable, with keybindings. The bottom bar lists only the keys valid in the current view or state, taken from the live keymap, and the pressed key inverts for one frame.
  Done when: remapping a key in the user config changes the bar in the next frame, and a view with no actions shows an empty bar.

- **Name the motion tokens and lint them** — CLEAN — value 3 — effort S — risk low — category: design system
  Why: the pack lists many animations, but none shares a vocabulary. Named durations and easings (`snap` 80 ms, `settle` 240 ms, `breathe` 3 s) live in one table, and a test fails if a view hard-codes a timing outside it or exceeds the frame budget.
  Done when: a grep-style test finds no raw duration literals in view code, and a new animation using an unknown token fails the test.

- **Fall back to ASCII glyph sets on dumb terminals** — FIX — value 3 — effort S — risk low — category: glyph design
  Why: the pictures (station track, chips, bars) depend on box and braille glyphs. On the Linux console, over ssh with a bad locale, or in a font without them, these render as tofu. A glyph-set token (`rounded`, `sharp`, `ascii`) is picked from locale and `TERM`, and the theme can override it.
  Done when: running with `LANG=C TERM=linux` renders every view using only ASCII, with no frame losing structure.

- **Wild: Draw the run as weather in the title bar** — FEATURE — value 2 — effort S — risk low — category: ambient status
  Why: wild. Run health becomes a single weather glyph and word in the terminal title and header: sun when green, drizzle for retries, storm when the guard refuses repeatedly, fog while the model thinks. A glance across the room is enough to know whether to step in.
  Done when: replaying a run with 3 guard refusals in a minute sets the title to the storm state, and returning to green clears it.

- **Wild: Dim the screen into a task constellation when idle** — FEATURE — value 2 — effort M — risk low — category: ambient
  Why: wild. After 60 s idle or while waiting on a long verify, the panels fade to a dark starfield of tasks, each star sized by effort, with dependency lines between them. The finished work glows steady and the active task twinkles. Any key snaps back with a fast fade.
  Done when: 60 s of idle triggers the constellation with the task count matching `fm` state, and any key restores the previous view within 200 ms.

- **Wild: Cast a per-project accent from the repo's identity** — FEATURE — value 3 — effort S — risk low — category: identity
  Why: wild. A stable hash of the repo path, or its dominant language color, picks the accent hue for borders and the station track. Several panes across projects then look different at a glance, and a user can still pin one in the theme file.
  Done when: two different repo paths yield different accent hues, one path always yields the same hue, and a pinned accent in the theme file overrides both.
