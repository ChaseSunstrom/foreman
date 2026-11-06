# Brainstorm — lens: simplicity

- **Make bare `fm code` print one answer before anything else** — FEATURE — value 5 — effort S — risk low — category: first-run
  Why: the user's complaint was "it just isn't doing anything" and `fm code` alone errors. Assumption: the ~40 existing ideas add screens, none fix the first second.
  Done when: `fm code` in a fresh dir prints within 1s a three-line status (project, runner chosen and why, what happens on Enter) before any model call, and a test asserts the lines.

- **Collapse the ~300 listed TUI ideas into a frozen "v1 screen" budget** — CLEAN — value 4 — effort M — risk low — category: scope
  Why: the idea list repeats motion/theme/replay dozens of times; the user said the TUI "looked like crap with all the text", so fewer things done well beat more.
  Done when: a checked-in file lists at most 5 TUI views and 3 motions, and a test fails if the renderer registers more without editing that file.

- **Make one process group the unit of a run** — FIX — value 5 — effort S — risk low — category: lifecycle
  Why: the orphaned planner after quit (T-1326). Simplest fix is `setsid` plus killing the group, not a registry.
  Done when: a test starts a run with a sleeping fake CLI, kills fm code with SIGKILL of the parent via the supervisor wrapper and SIGTERM/SIGHUP/quit, and no descendant survives.

- **Refuse to nest by one environment variable** — FIX — value 5 — effort S — risk low — category: duplicates
  Why: the request "no duplicate Foreman when it runs Claude Code as a worker". One `FM_DEPTH` variable, checked by every hook, replaces lineage detection, installs scanning and similar.
  Done when: with `FM_DEPTH=1` set, Foreman's hooks emit nothing and add no context in a nested claude run, while the guard still blocks `git reset --hard`, shown by a test.

- **Run workers bare by default** — PERFORMANCE — value 5 — effort S — risk med — category: startup tax
  Why: 66k–133k input tokens per call came from plugins and rules loading in nested Claude. Assumption: a flag set like `--bare`/`--setting-sources` exists in the installed claude version.
  Done when: a nested planner call's first-request input tokens are under 15k, measured and asserted in `fm code bench`.

- **Let the project be the current directory, nothing else** — FEATURE — value 4 — effort S — risk low — category: multi-project
  Why: T-1330 plans a registry and home over all projects. Simplest version scans `~/projects/*/.foreman` on demand. Assumption: Foreman state lives in a per-project folder.
  Done when: `fm code` home lists projects discovered from disk with no registration step, and deleting a project folder removes it from the list.

- **Use one config line, and derive everything else** — CLEAN — value 4 — effort S — risk low — category: config
  Why: the user asked for "better config/setup"; many ideas add layers, wizards and explainers. One `runner = claude` line plus detected defaults is enough.
  Done when: a fresh HOME with only claude on PATH runs a request with no config file, and adding `runner = codex` changes the choice, in a test.

- **Print `Next:` on every failure and delete the rest of the explainers** — CLEAN — value 4 — effort S — risk low — category: errors
  Why: "needs a request" and the silent planner were dead ends. Assumption: error paths are scattered across fmcode.py.
  Done when: a test triggers each known failure (no runner, no request, runner missing, planner timeout) and each output's last line starts with `Next:` and names a runnable command.

- **Show a single "last heard from the runner N s ago" line** — FEATURE — value 4 — effort S — risk low — category: liveness
  Why: minutes of silence; this replaces the watchdog, heartbeat, weather and pulse ideas with one honest number.
  Done when: with a fake CLI that stays silent, the line counts up in the TUI and in plain output, and turns red past a configured limit.

- **Wild: Make `fm code` a plain prompt that never leaves the shell** — FEATURE — value 3 — effort M — risk low — category: interface
  Why: assumption: many runs need only a line-based loop. Same harness, a readline-style prompt with the status line, TUI optional.
  Done when: `fm code --plain` completes a fix request end to end in a pty with no escape sequences beyond newline.

- **Wild: Treat the user's complaint as the spec by echoing it** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the user's words ("it just isn't doing anything") are the trigger; Foreman should open a task quoting them verbatim and nothing more, instead of a scorecard system. wild
  Done when: typing a friction phrase into a session creates one task whose title holds the exact phrase, with a test.

- **Wild: Ship Foreman as one file that deletes itself from the plugin copy** — CLEAN — value 3 — effort M — risk med — category: install
  Why: duplicates arise because the plugin and the CLI both exist. A single `fm.pyz` that the plugin merely calls leaves one code path. wild
  Done when: with the plugin installed and `fm.pyz` on PATH, `fm doctor` reports exactly one Foreman code path in use.

- **Wild: Make "nothing happening" impossible by running the worker visibly in a split** — FEATURE — value 3 — effort M — risk med — category: transparency
  Why: instead of rendering progress, show the worker's own raw output in a tmux pane or the lower half of the screen. wild
  Done when: running a CLI worker shows its raw stdout lines in the lower pane within 1s of emission, verified in a pty test.
