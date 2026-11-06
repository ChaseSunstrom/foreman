# Brainstorm — lens: simplicity

- **Put a line-count ratchet on the TUI** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: assumption: the TUI is already large (T-0166 is about moving the band and pane out of `register.tsx`), and each round of "more animation" adds code. The hook code already has CPU and byte ratchets.
  Done when: a test fails if the TUI modules exceed a stated line budget, and the failure names the biggest file.

- **Confine all escape codes to one palette module** — CLEAN — value 4 — effort S — risk low — category: color
  Why: "not just static colors" is easiest to deliver when no view hardcodes a color. Assumption: some views still do.
  Done when: a grep test finds no raw `\x1b[` or `38;2` outside the palette module, and every view takes color from semantic roles.

- **Split each view into a plain layer and a style mask** — CLEAN — value 4 — effort M — risk med — category: testing
  Why: golden frames with embedded colors break on every tint tweak, which discourages polish. The idea is one function returning text, a second returning a per-cell role map.
  Done when: changing a theme's colors alters no plain-text golden, and a separate role-map test covers styling.

- **Limit state to seven glyphs with one legend** — FEATURE — value 4 — effort S — risk low — category: visual language
  Why: the user said the old TUI "looked like crap with all the text". A closed set (pending, running, passed, failed, refused, waiting-on-you, skipped) replaces status words. The same set doubles as the `--calm` fallback.
  Done when: every status in every view is one of the seven glyphs, and a test fails on any status word printed beside its glyph.

- **Animate with a 2 Hz two-beat tick** — PERFORMANCE — value 3 — effort S — risk low — category: motion
  Why: assumption: the earlier ideas lean on 30 fps diff-drawn frames, which is costly over ssh and in the docked pane. A blink or glyph-cycle at 2 Hz on only the live element reads as alive and needs no frame scheduler.
  Done when: an idle run issues at most 2 redraws per second, and exactly one cell group changes per beat in a replayed log.

- **Fold finished stations into a dot row** — FEATURE — value 4 — effort M — risk low — category: layout
  Why: assumption: the screen mostly shows work that is already done. A closed station collapses to one colored dot in the track and its detail moves behind a key.
  Done when: after a station passes, the frame drops its lines and gains one dot, and the key reopens the detail.

- **Regenerate the README demo from a scripted fake run at release** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the README shows `demo/live.svg` of the Claude Code pane, while the new `fm code` TUI has no picture. It has a fake model client from T-1211/T-1212, and release steps are routine (1.2.43 and 1.2.44).
  Done when: the release step rebuilds the TUI demo from a deterministic fake run, and a test fails if the committed file differs.

- **Attach a before/after frame diff to a TUI task's proof** — FEATURE — value 3 — effort M — risk low — category: proof
  Why: the project's discipline is "prove it", but a look change has no observable proof today. Assumption: golden frames are the only evidence available.
  Done when: closing a TUI-labelled task stores the changed golden frames in its proof and `fm task show` lists them.

- **Wild: Give each weekday its own default palette** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; zero config. The look changes day to day without a theme gallery, and a user's explicit theme overrides it. Assumption: users find a fixed look dull.
  Done when: with no theme set, two dates a day apart render different accents, and setting a theme pins the look.

- **Wild: End each run with a haiku built from the run's counts** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; template-only, with no model call and no cost. The close-out gets a small thing people screenshot, instead of a receipt card.
  Done when: finishing a run prints three lines of 5, 7 and 5 syllables from templates filled with real counts (steps, refusals, seconds), and a test checks the numbers.

- **Wild: Derive the accent from a hash of the user's git email, locally** — FEATURE — value 2 — effort S — risk low — category: personalization
  Why: wild; nothing is configured or sent anywhere. The hash is computed on the user's machine, never stored or exported, and kept out of exports.
  Done when: the same email gives the same accent across runs, no export contains the email or its hash, and a theme file overrides it.

- **Wild: Show only a focal line when the run goes quiet** — FEATURE — value 3 — effort M — risk med — category: layout
  Why: wild; during long thinking the screen dims to one line, "waiting on the model, 42 s, $0.03", and the rest returns on the next event. This pairs with the existing "why is this so quiet" idea but removes chrome rather than adding it.
  Done when: after N seconds without events the frame shows one line, and the first event restores the full frame in one redraw.
