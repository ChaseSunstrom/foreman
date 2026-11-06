# Brainstorm — lens: delight

- **Greet with a one-line "welcome back" that names where you left off** — FEATURE — value 4 — effort S — risk low — category: first-launch
  Why: the user compares to `claude`, which opens ready; bare `fm code` currently errors. assumption: a "last session" record exists or is cheap to write per project.
  Done when: running `fm code` in a project with a prior run prints/shows "Last: T-#### <title>, <state>, <time ago>" as its first line in under 300 ms, and shows a blank-slate prompt hint when there is no prior run.

- **Show the first-call wait as a named, ticking sequence** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: nixie run "just isn't doing anything" for minutes with 66k–133k input tokens per call. A silent spinner reads as dead. Name the phases ("starting claude", "loading plugins", "reading repo", "planning") using the child's stream-json events or process state, each with elapsed seconds.
  Done when: a fake runner that sleeps 20 s before replying produces a visible phase label and elapsed counter that changes at least every 2 s, asserted by a pty test.

- **Say "done" in a sentence a person would say** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: user wants plain outcomes and hates text walls (the TUI "looked like crap with all the text"). One generated sentence from counts, not from the model: "Fixed the parser: 2 files, test failed before and passes now, 41 s."
  Done when: every closed run's final line matches the template built from stored counts, with a golden test for fix, feature, question and failed-run variants.

- **Offer the next request as a ghost placeholder in the prompt box** — FEATURE — value 3 — effort M — risk low — category: prompt
  Why: the user keeps asking for more and says they shouldn't need to ask. Fill the empty input with a dimmed suggestion drawn from the top open task or last run's "what I'd do next"; Tab accepts it.
  Done when: with an open task T-X queued, the empty prompt shows a dim "run T-X: <title>" and Tab then Enter starts that task, covered by a pty test.

- **Let a refusal teach once, then go quiet** — FEATURE — value 3 — effort S — risk low — category: microcopy
  Why: guard hints are long and repeat. Show the full explanation and rewrite the first time per verdict kind, then a one-word chip with `?` to expand. Safety unchanged, only the text shrinks.
  Done when: the second identical refusal in a user's history renders at most one line, the verdict stays identical, and `?` shows the full text.

- **Remember the last words when the terminal closes** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: the user quit while the planner ran orphaned and lost the picture of what was happening. On exit, always write a last-frame summary to a file and print it to scrollback.
  Done when: killing the TUI with SIGHUP leaves `last-run.txt` containing the final state and `fm code` next start shows it.

- **Give every runner a one-line hello when picked** — FEATURE — value 3 — effort M — risk low — category: runners
  Why: with many CLIs and models, picking one is faceless. On selection, run a cheap probe and show "claude 2.1 · ready · ~9 s startup · last passed 6/7 kinds" or why not.
  Done when: selecting a runner prints a status line from a real probe within 5 s, and a missing binary shows "not installed" with the install hint.

- **Name the run like a journal entry** — FEATURE — value 2 — effort S — risk low — category: history
  Why: history lists ids; the user speaks in sentences. Title each run from the request: "Wed evening, nixie: fix the parser crash". Pure string work, no model.
  Done when: the history list shows date-part, project and a trimmed request for each run, verified on a fixture of five runs.

- **Wild: Dock a tiny "desk plant" per project on the home screen** — FEATURE — value 2 — effort M — risk low — category: home screen
  Why: wild. A 3-line glyph that grows with proved tasks and wilts on long idle or red checks; a glance tells which project needs water. Derived only from task state.
  Done when: a fixture project with three proved tasks renders a larger plant than one with none, and a project idle for 30 days renders the wilted glyph, in golden frames.

- **Wild: Print a postcard to the shell when you quit** — FEATURE — value 3 — effort S — risk low — category: close-out
  Why: wild. After the alt-screen closes, leave a 5-line keepsake in scrollback: project, what closed, time, proof count, and the exact command to resume. The run stays visible after the app is gone, like a good CLI's exit line.
  Done when: quitting the TUI after a closed run leaves the postcard in terminal scrollback, ASCII-safe under `NO_COLOR`, tested through a pty capture.

- **Wild: Hum a different bell per outcome, off by default** — FEATURE — value 2 — effort S — risk low — category: sound
  Why: wild. One BEL for needs-you, two for closed green, none for quiet success; the user can look away during a long nixie-style wait and still know. Gated by a setting.
  Done when: with the setting on, the three outcomes emit 1, 2 and 0 BEL bytes respectively, and with it off none are emitted.

- **Make the wait feel like a workshop with a "what it's doing" line from the process itself** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: during the quiet planner stretch, read the child's `/proc` state (CPU ticks, open network sockets, files touched) and say "claude is busy: 38% CPU, reading 3 plugin files" or "waiting on the API, 41 s". Distinguishes wedged from working honestly.
  Done when: a child busy-looping and one blocked in sleep produce different lines in a test, and a child with no activity for 60 s produces a "looks stuck" line with a one-key kill.

- **Wild: Ask "are you still there?" back from the harness** — FEATURE — value 3 — effort M — risk med — category: unattended
  Why: wild. When an unattended run has been silent past a threshold, the harness pokes the runner with a trivial probe and reports "alive, thinking" or "unresponsive, restarted step" in the receipt, so silence never lasts unexplained.
  Done when: a fake runner that hangs triggers a probe at the threshold, the receipt records the outcome, and the step restarts per policy, asserted in a test.

- **Celebrate a first-ever success in a project, once** — FEATURE — value 2 — effort S — risk low — category: first-launch
  Why: the first closed run in a new project is the moment a new user decides whether it works. A one-time, brief, skippable flourish plus "next: try a question" nudges the second run.
  Done when: the first proved close in a project shows the flourish and writes a marker; the second close in that project shows none, with reduced-motion rendering a static line.
