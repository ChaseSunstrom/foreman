# Brainstorm — lens: delight

- **Ship a Look Book of one-file living specimens** — FEATURE — value 5 — effort M — risk low — category: design skills
  Why: the pack shows one 13-line ui playbook and cards that "teach no taste"; earlier ideas list a lookbook and style recipes but no format. Each specimen is a single self-contained HTML file (about 150 lines) that renders one named look (type pairing, palette, motion, one signature interaction) and carries its own tokens block in a comment header. Claude is told to open one, say which it is borrowing from and what it changes.
  Done when: `fm lib show lookbook` lists at least 12 specimens, each opens offline with no third-party host, and each has a tokens header that `fm check` parses.

- **Add a "kill the default" pass that rewrites generic UI one decision at a time** — FEATURE — value 4 — effort M — risk low — category: design skills
  Why: the user wants "non generic". Instead of only detecting slop, the pass lists the ten defaults in a diff (system font, purple gradient, rounded card grid, centred hero, and so on) and proposes a replacement for each, taken from the chosen look. The user approves or skips each in turn.
  Done when: running it on a fixture page shows at least eight defaults found with a proposed swap each, and applying one swap changes only that decision's lines.

- **Give the TUI settings screen a "feel it live" strip** — FEATURE — value 5 — effort M — risk low — category: TUI config
  Why: the pack says there's no settings screen and everything is hand-edited TOML. A strip along the bottom keeps real running content (a mini run, a diff, a guard flash) re-rendering as you scrub a theme, motion speed or density value, so each change is judged on the actual product, not a swatch.
  Done when: moving a theme or motion setting in the settings view re-renders the strip within one frame, and Esc restores the saved value.

- **Make 3D scene recipes that run in the terminal and the browser from one description** — FEATURE — value 4 — effort L — risk med — category: 3D
  Why: the request names 3D, and the pack has three-js cards but no composition skill. One small scene file (shapes, camera path, light) feeds a stdlib half-block rasteriser for the TUI and a plain WebGL page for `fm page`. The recipe set covers a turntable, a rail of stations and a particle burst.
  Done when: one scene file renders a recognisable frame in `fm code app` and in a browser, with a golden-frame test for the terminal side.

- **Show a "design diff" film strip as the receipt for UI tasks** — FEATURE — value 4 — effort M — risk low — category: visual proof
  Why: the user's closes are proof-based; UI work has no visual proof. At close, a strip of before, mid-transition and after frames (three viewports) goes into the receipt, with the motion tokens used listed under it.
  Done when: closing a UI task on a fixture writes a strip file referenced from the receipt, and a task with no visual change says so instead of showing one.

- **Let a pasted sentence roll the theme** — FEATURE — value 3 — effort S — risk low — category: themes
  Why: assumption: the user enjoys steering by words ("make it feel like a late-night print shop"). A mapper from words to palette, type and motion tokens (pure table lookup, no model call) proposes three variants into the live strip for a keypress to keep one.
  Done when: five sample phrases each produce three distinct, contrast-valid themes, and keeping one writes tui.toml with a confirm-or-revert prompt.

- **Add a motion "score" player that edits timing by dragging** — FEATURE — value 4 — effort M — risk med — category: motion
  Why: earlier ideas cover a motion playbook and tokens; none make timing tangible. A timeline in the settings view shows each state-to-motion pair as a bar; arrow keys nudge duration and easing, and the strip plays it on loop.
  Done when: changing a bar's duration changes the token in tui.toml and the animation in the strip, and a reduced-motion toggle collapses every bar to a cut.

- **Wild: Ship a "style tournament" where the user picks between two looks and Foreman builds the winner** — FEATURE — value 4 — effort L — risk med — category: design skills
  Why: wild; assumption: choosing beats describing. Two specimens built from one brief appear side by side, the user presses a key, the loser is retired, and the next round mutates the winner. After three rounds the survivor becomes the project's DESIGN.md.
  Done when: three rounds on a fixture brief end with a DESIGN.md naming fonts, palette and motion, and the lost specimens are kept in a rejected folder.

- **Wild: Render the repo as a small 3D city in `fm page`** — FEATURE — value 3 — effort M — risk low — category: 3D
  Why: wild; the pack has fm map data (1610 files, layout counts). Directories become blocks, height is file size, and tinted windows light up where the current task touched files. A slow orbit camera makes it the thing people show others.
  Done when: `fm page city` writes one offline HTML file that shows the repo's top-level directories as blocks, and touched files glow.

- **Wild: Draw a hand-lettered title card when a task closes proved** — FEATURE — value 3 — effort M — risk low — category: celebration
  Why: wild; closes are the moment the user cares about. A block-letter card composed from the task title, with the proof line underneath, animates in over a second and then settles into the scrollback as the receipt.
  Done when: closing a task prints the card in the app, a `--calm` run prints the same text with no motion, and the card is exactly one screen tall at 80 columns.

- **Wild: Offer a "shader looks" shelf where every snippet ships with a live thumbnail** — FEATURE — value 4 — effort M — risk low — category: 3D
  Why: wild; the pack lists GLSL cards without any visual output. Each of about 15 original fragment shaders (grain, caustics, halftone, aurora, ink bleed) is stored with a rendered still and a one-line note on cost, so Claude picks by sight.
  Done when: `fm lib show shaders` lists each look with a thumbnail path, and every shader compiles in a headless check.

- **Ask three taste questions before any UI work, with visual answers** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the request says "non generic"; vague taste asks produce average results. The intake shows three pairs of tiny swatches (type, density, motion energy) and records the picks as the brief's first lines.
  Done when: a UI request with no design brief triggers the pairs once, and the picks appear in the task brief and carry to later tasks in the project.

- **Teach the playbooks with before/after pairs, not rules** — FEATURE — value 3 — effort M — risk low — category: playbooks
  Why: cards give pitfalls but no taste. Each new design playbook leads with a generic version and a crafted version of the same component, plus three sentences on what changed, so the lesson sticks in a model's context faster than guidance.
  Done when: every design playbook has at least two pairs, and both halves render from files in the repo.

- **Add a hush button that kills all delight in one key** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: with this much motion, trust depends on an obvious off switch. One key sets calm mode live, saves it only if confirmed, and the footer shows "calm" until toggled back.
  Done when: pressing the key stops all animation within one frame, and the screen still shows every state.
