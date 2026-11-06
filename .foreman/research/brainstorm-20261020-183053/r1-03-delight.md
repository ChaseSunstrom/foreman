# Brainstorm — lens: delight

- **Breathing station track** — FEATURE — value 4 — effort M — risk low — category: motion
  Why: the user said the TUI "looked like crap with all the text" and wants "not just static colors"; the station track (plan, steps, guard, verify) is the spine of the redesign. Assumption: it is currently painted per-frame without easing.
  Done when: the active station pulses on a ~1.2 s sine on its brightness, finished stations settle to a steady tint, and a snapshot test at two timestamps shows different color values for the active station only.

- **Truecolor gradient theme engine** — FEATURE — value 5 — effort M — risk low — category: themes
  Why: "not just static colors" plus the existing request for "customizable" themes. Assumption: themes today map roles to flat colors.
  Done when: a theme file can declare a two-stop gradient for a role, the work bar and Gantt render it across their width, and 256-color and no-color terminals fall back to the nearest flat color with a test for each.

- **Verdict stamps with a landing animation** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: guard verdicts (allow, refuse, hint) are the product's identity but a refusal reads like any other line. Assumption: verdicts currently print as a colored word.
  Done when: a refusal slides in over 3 frames with a brief inverted flash, then rests as a dim chip, and `--reduce-motion` skips straight to the final chip.

- **Diff reveal that writes itself** — FEATURE — value 4 — effort M — risk low — category: diffs
  Why: diffs and change bars are named stations in the ask. Assumption: diffs appear whole.
  Done when: added and removed lines stream in over at most 400 ms in total regardless of size, change bars grow from zero to length, and the final frame equals the static render byte for byte.

- **Test-run heartbeat chips** — FEATURE — value 4 — effort S — risk low — category: verify
  Why: check chips exist; a verify run in progress is the most anxious moment of a task. Assumption: chips are static while running.
  Done when: a running chip shows a braille spinner plus elapsed seconds, flips to a green check with a brief bloom or to a red cross with a small shake (2 frames offset), and the tests assert each frame sequence.

- **Smooth view transitions with cross-fade** — FEATURE — value 3 — effort M — risk med — category: motion
  Why: the pack says "views fade the screen"; extending that to every view switch and pane resize would keep it coherent. Assumption: only some transitions fade today.
  Done when: every view switch runs the same 150 ms fade through the same easing function, and a frame-budget test shows no frame takes more than 16 ms in the render path.

- **Token river sparkline** — FEATURE — value 3 — effort S — risk low — category: data viz
  Why: token columns exist; a flowing sparkline of the last 60 s of spend per turn would show cost, which is the user's "cheaper" obsession, as it happens. Assumption: cost shows as totals.
  Done when: the footer shows a sparkline of tokens per turn with the dollar cap as a ceiling line, and it turns amber at 80% and red at 95% of the cap.

- **Adaptive motion budget** — FEATURE — value 4 — effort M — risk low — category: performance
  Why: the repo cares about CPU-time bounds on CI, and animation over SSH or on a slow terminal can flicker. Assumption: there is a single fixed frame rate.
  Done when: the renderer measures frame cost, drops from 30 to 15 to 0 fps over a slow link, and restores when it recovers; a test with a fake slow writer asserts the downgrade.

- **Theme gallery with live preview** — FEATURE — value 3 — effort M — risk low — category: themes
  Why: "customizable, extendable" was in the T-code TUI ask. Assumption: themes are switched by editing config.
  Done when: `fm code tui --themes` shows a grid of themes rendered on a real sample session, arrow keys preview each live, and Enter writes the choice.

- **Celebration on a closed task (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; a task passing its proof is the product's payoff and currently ends as a text line. Assumption: nothing marks it.
  Done when: closing a proved task fires a 600 ms confetti-of-block-characters sweep across the station track, off by default under `--reduce-motion` and in non-TTY output.

- **Ghost replay scrubber (wild)** — FEATURE — value 4 — effort L — risk med — category: replay
  Why: wild; the demo is a recorded session, and each run already stores stations, timings and diffs. Assumption: the run log has enough timestamps to reconstruct frames.
  Done when: `fm code tui --replay RUN` plays a finished run with a timeline you scrub with ←/→ and speed with +/-, and frame N matches the live render of that moment.

- **Terminal-native sound and bell cues (wild)** — FEATURE — value 2 — effort S — risk low — category: audio
  Why: wild; long unattended runs (the marathon showcase) end while the user is away. Assumption: nothing signals completion beyond the screen.
  Done when: with `sound = on` a distinct bell pattern marks "needs you", "done" and "refused", and the default is off with a test that no BEL is emitted otherwise.

- **Foreman mascot status line** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: small, sharable touch; people screenshot TUIs with character. Assumption: no persistent identity element.
  Done when: a 3-row ASCII foreman changes pose among idle, working, waiting for you and celebrating, driven by the same state as the station track, and it hides below 24 rows.

- **Clickable ids and hover highlights** — FEATURE — value 3 — effort M — risk med — category: interaction
  Why: T-0796 already lists clickable ids, progress bar, spinner, motion and palette as deferred polish; this ask is the moment to build it. Assumption: terminal mouse reporting is available.
  Done when: hovering a T-id underlines it, clicking opens that task's detail view, and the keyboard path (Tab, Enter) does the same.
