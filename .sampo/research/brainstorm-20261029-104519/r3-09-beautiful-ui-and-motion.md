# Brainstorm — lens: beautiful UI and motion

- **Add a change-flash to every live value** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: assumption: the pane and web UI redraw counters, stage and lane values in place, so a change is easy to miss. The existing stage-rail animation covers transitions between stages, not individual values.
  Done when: a test that changes one value in the web UI and one in the pane shows that cell, and only that cell, carrying a flash class or style for about 600 ms, and none under reduced-motion.

- **Route all animation through one motion governor** — CLEAN — value 4 — effort M — risk low — category: motion
  Why: the pack lists breathing borders, living trees, constellations and flourishes as separate ideas. Each added alone would bring its own timer. Assumption: the pane runs inside Claude Code's render loop, so idle CPU matters.
  Done when: every animation registers with one scheduler that pauses when the pane is hidden or the session idle, honors a reduced-motion setting, and a bench shows under 1% CPU with the pane idle for 60 s.

- **Show a "needs you" beacon on every surface** — FEATURE — value 5 — effort M — risk low — category: attention
  Why: the user says "make sure it doesn't sit idle", and Foreman often stops on human-only blockers (T-0325, T-0335, T-0418). Nothing tells them from across the room that it is waiting. Assumption: the terminal title and the web favicon and tab title are not set today.
  Done when: a blocked-on-human state sets the terminal title (OSC 0) and the web favicon and document title to a distinct "needs you · T-nnnn" form, and clears them when the user acts.

- **Define one status glyph vocabulary with ASCII fallback** — CLEAN — value 3 — effort S — risk low — category: design language
  Why: assumption: ✓, ✗ and spinner glyphs are chosen per surface. T-0796 lists spinner and progress polish, and T-1217 shows the pane already fights terminal quirks.
  Done when: one table maps each state to a glyph and an ASCII fallback, the pane, web UI and site import it, and a test renders both sets with no state sharing a glyph.

- **Degrade the palette by color depth and never rely on color alone** — FIX — value 4 — effort M — risk low — category: accessibility
  Why: T-1217 (the pane background painted 48;2;38;38;38 by Claude Code) shows color handling is already brittle. The web UI accessibility audit idea doesn't cover terminal color depth.
  Done when: the pane renders legibly at truecolor, 256 and 16 colors (snapshot test per depth), and every state is distinguishable in grayscale by glyph or weight.

- **Animate queue reorders with FLIP, not jumps** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: assumption: tasks leave the queue and reach done by re-render. A row that slides toward its new place explains what changed, which a vanishing row does not.
  Done when: closing a task in the web UI moves its row to the done list over 250–350 ms, and with prefers-reduced-motion it moves instantly.

- **Show a peek card when hovering or focusing a task id** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: T-0796 plans clickable ids, and the user's own requests cite ids constantly ("Ship T-1987 to main"). A popover with title, status, proof marks and files saves a click.
  Done when: hovering or keyboard-focusing any T-id in the web UI shows a card with those four fields within 150 ms, and Esc dismisses it.

- **Fuzz the pane and web layout at every size** — CLEAN — value 3 — effort M — risk low — category: layout
  Why: assumption: width bugs surface only when the user resizes. The share-one-truncation-helper idea fixes the code, and this idea adds the test that catches regressions.
  Done when: a test renders the pane at widths 20–200 and heights 5–60 and asserts no line exceeds the width and no panel disappears, and the web UI is checked at 320, 768 and 1440 px.

- **Wild: Draw an ECG heartbeat across the top of the pane** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild; assumption: edits, test runs, hook denies and gate results are already emitted as events. Each event becomes a pulse, the line goes flat when idle, and it turns amber when waiting on you.
  Done when: replaying a recorded event log into the pane draws a distinct pulse per event type, and an empty log draws a flat line.

- **Wild: Add a pixel-art foreman sprite with three moods** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; three terminal rows of sprite for working, waiting-on-you and blocked, reusing the glyph and motion governor. Assumption: the pane has a few spare rows, and the sprite hides when it does not.
  Done when: each of the three states renders a different sprite frame set, and it is hidden when the pane is under 30 columns.

- **Wild: Let site visitors try the guard in the browser** — FEATURE — value 4 — effort M — risk med — category: site
  Why: wild; the site hero is a recorded demo. A text box where a visitor types `rm -rf ~` and sees the guard's actual verdict and message (rules compiled to client-side JS) shows the product without a sandbox server. Risk: the JS rules can drift from the Python ones.
  Done when: a parity test runs 50 sample commands through the Python guard and the JS port and gets identical allow/deny results, and the site page makes no network request while the visitor types.

- **Wild: Make themes shareable files with a gallery** — FEATURE — value 2 — effort M — risk low — category: theming
  Why: wild; a theme is a small token file (builds on the design-token idea) that applies to the pane, web UI and site together, with auto light/dark by time of day. Assumption: the shared token file exists first.
  Done when: dropping a theme file into the config directory restyles the web UI and pane on next load, and an invalid file falls back to the default with one named warning.

- **Make every empty and blocked screen end in one clickable next step** — FEATURE — value 4 — effort S — risk low — category: web UI
  Why: the pack records repeated fixes for refusals with no way forward (docs-impact suggestions, "no test matches"). The same rule applies in the web UI: any empty or error state shows a button or copy-able command, not just a message.
  Done when: a test walks every empty and error state in the web UI and asserts each contains at least one action element with a runnable `fm` command.
