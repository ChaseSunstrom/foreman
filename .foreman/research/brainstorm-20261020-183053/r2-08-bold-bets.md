# Brainstorm — lens: bold bets

- **Detach and reattach the TUI from a headless run** — FEATURE — value 5 — effort L — risk med — category: devices
  Why: assumption: the "Marathon" unattended runs (T-1240) outlive a terminal, and the idea list has no way to leave and return. The run writes its event log to a local socket, and any number of TUI, web or phone clients attach read-only or in control. A killed terminal never kills the run.
  Done when: starting `fm code`, closing the terminal, then running `fm code attach` shows the same live station, with no turns lost.

- **Make "needs you" an actionable decision inbox** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: the pack's guard refusals and "needs you" alerts are only notifications. Each pending decision (a guard block, a destructive command, an ambiguous step) becomes a card with keys: allow once, allow for this task, deny with a steer note. Decisions queue while the user is away.
  Done when: a scripted run that hits a guard block waits on the card, a keypress resolves it, and the run continues on the choice made.

- **Review hunks mid-run and feed rejections back** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: assumption: diffs are shown but the user can only watch. Pressing `x` on a hunk rejects it, reverts it under the run's lease, and sends the model a one-line reason. This turns the diff view from display into steering.
  Done when: rejecting a hunk restores the file text and the model's next turn contains the rejection note.

- **Checkpoint every step and rewind the harness** — FEATURE — value 4 — effort L — risk high — category: reliability
  Why: `fm code` workers edit under leases (T-1294), and a bad step currently means manual cleanup. Snapshot the tree and the plan state at each station boundary, and let `r` rewind to any station and re-run from there. Assumption: git worktrees or a shadow ref are acceptable storage.
  Done when: rewinding to step 2 restores files byte-identical to the step-2 snapshot and the plan shows step 3 as pending.

- **Add a stuck-loop detector with a visible diagnosis** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the long-session benchmarks and compaction storms show agents repeating themselves (the piped-tail test runs in the T-1252 round). Detect the same command or edit repeated N times, or no evidence for K turns, and turn the heartbeat amber with a sentence saying what repeated.
  Done when: a fake model that repeats one command 4 times trips the banner, and a normal run never does.

- **Redact secrets in the render, the logs and every export** — SECURITY — value 4 — effort M — risk low — category: security
  Why: the idea list only covers stripping escape sequences. Tool output and env dumps can carry API keys, and the planned recorder, replay and SVG export would copy them out. Run one shared redactor (key patterns, `models.json` values, `.env` values) in front of the screen and every writer.
  Done when: a fixture command that prints a fake `sk-…` key shows `▒▒▒` on screen and in an exported recording.

- **Explain any element with `?`** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: assumption: a new user can't tell why a chip is red or why the guard refused. Focusing a chip, verdict or station and pressing `?` shows the rule that fired, the evidence it wanted, and the command that fixes it. This reuses the guard hints from T-1289 and T-1288.
  Done when: pressing `?` on a refused verdict shows the rule name and the hint text the guard emitted.

- **Forecast cost and finish time against the cap** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: Foreman's pitch is cheaper and faster (T-1231), and runs have dollar caps. Use the Gantt so far plus bench history for that task size to project the final cost and time, and warn before the cap is hit, not after.
  Done when: with a $0.10 cap and a fake model priced to overrun, a warning appears at least one turn before the cap trips.

- **Drive the TUI from a scripted pty test driver** — CLEAN — value 3 — effort M — risk low — category: developer experience
  Why: golden frames check output only. A stdlib pty driver that sends keys, waits for text and asserts on the screen gives end-to-end tests for keybindings, resize and exit-path terminal restore. It also feeds the CPU-time bounds in CI.
  Done when: a test opens the TUI, presses `?`, resizes, quits, and asserts the terminal modes are restored.

- **Wild: Run a live duel split-screen, Foreman against plain Claude** — FEATURE — value 4 — effort L — risk med — category: showcase
  Why: wild; T-1231 and the Marathon showcase need proof people can see. Two panes run the same task in throwaway repos, with cost and test counters racing side by side, and the result feeds the Benchmarks page.
  Done when: `fm code duel TASK` shows two live panes and writes both results to a bench file.

- **Wild: Follow the model's edits with a ghost cursor in a live file view** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: wild; the idea list reveals diffs but never shows the file as a whole. A pane tails the file being edited, with a second cursor sliding to each changed line, so the user sees where in the code the work lands.
  Done when: an edit to line 40 of a fixture file scrolls the view to line 40 and highlights the line.

- **Wild: Write the PR description as the run goes** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: wild; every closed step already carries evidence and a diff. A sidebar assembles a running changelog, "what changed, how it was proved", ready to copy at the end, so the receipt card becomes a shippable artifact.
  Done when: finishing a fixture task produces a markdown file listing each step, its proving command and its pass line.

- **Push phone alerts through a self-hosted channel, off by default** — FEATURE — value 3 — effort S — risk med — category: devices
  Why: assumption: unattended runs need a way to reach the user away from the desk. An ntfy-style webhook, configured only by an explicit setting, sends "needs you" and "done" with approve and deny links back to the decision inbox. Nothing leaves the machine without the setting.
  Done when: with no setting, a run makes zero outbound requests, and with a local test URL set, a blocked run posts one message.
