# Brainstorm — lens: unspoken needs

- **Diagnose a silent run before the user asks** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: "a run in ~/projects/nixie just isn't doing anything" was found by the user, not by Foreman; the planner ran minutes at 66k–133k input tokens with nothing shown. Assumption: the harness knows the child PID, last output time and token counts.
  Done when: a fake CLI runner that sleeps silently for N seconds makes fm code show "planner alive, no output for Ns, input ~100k tokens, here is what it is probably doing" and offer one-key kill/retry; a test asserts the line appears.

- **Cap and price every runner call up front** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: 66k–133k input tokens per nested Claude call came from loading every plugin and Foreman's own hooks; the user only learned it from slowness. Assumption: a lean-launch flag set (no plugins/hooks) is available for claude.
  Done when: each runner call records its input tokens, and a call over a configured ceiling (default e.g. 40k) is flagged in Activity and refused for planning with a message naming the lean-launch fix; test with a stub CLI reporting usage.

- **Self-trigger the friction-to-round loop** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: the user said twice "I shouldn't even need to ask you… foreman should figure it out", and a task about noticing "it just isn't doing anything" / "why can't I…" phrasing already exists. Assumption: the intake hook sees raw user prompts.
  Done when: replaying a corpus of the user's real complaint phrases through the intake hook queues exactly one "improve area X" round per area (deduped), and neutral prompts queue none.

- **Preflight a project before the first run** — FEATURE — value 4 — effort S — risk low — category: setup
  Why: `fm` wasn't on PATH, the user had no model set, and nixie's context was unknown; each cost a failed attempt. Assumption: a cheap check list (PATH, runner found, git clean, gates exist, hooks wired) is feasible.
  Done when: `fm code` in a fresh dir prints a ≤6-line readiness card with a one-line fix for each red item, and the home screen shows the same per project; a test covers a missing runner and a missing PATH entry.

- **Detect Foreman-inside-Foreman at the process level** — FIX — value 4 — effort S — risk med — category: reliability
  Why: the user wants "no duplicate Foreman when it runs Claude Code as a worker"; T-1327 strips context, but plugin-installed hooks can still load from the user's config. Assumption: an env marker is passed to children.
  Done when: a nested claude worker started by fm code reports exactly one Foreman hook set (via a probe command listing active hooks), with the guard still active; test fails if a second session-context injection occurs.

- **Survive the closed lid: resumable runs** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: stopping or closing the terminal now kills children (T-1326), which means long runs die with a laptop sleep or SSH drop. Assumption: harness state is already event-logged.
  Done when: killing the TUI mid-step and running `fm code --resume` continues from the last closed step without redoing proved ones; test uses a fake runner and a kill at step 2 of 3.

- **Choose the runner by evidence, per request kind** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: `fm code bench` already grades models and CLIs, and the user wants "ANY CLI or model" managed but must press `m` and guess. Assumption: bench results are stored per runner.
  Done when: with two runners benched, `fm code "fix X"` picks the one with the best held-rate and cost for that request kind, states why in one line, and `--runner` overrides; test with canned bench results.

- **Fleet view: one project's stuck, another's done** — FEATURE — value 4 — effort M — risk low — category: devices
  Why: the user manages multiple projects (nixie, foreman) and the planned home screen lists them, but nothing says which needs them. Assumption: terminal title/bell and a `fm code status --all` one-liner are cheap.
  Done when: `fm code status --all` prints one line per project with state (running, needs you, blocked, idle) sorted by urgency, and the terminal title mirrors the worst state; test with three fake project dirs.

- **Wild: Foreman as a menu-bar/tmux "shift supervisor"** — FEATURE — value 3 — effort M — risk low — category: devices — wild
  Why: assumption: the user runs several long CLI sessions and wants glanceable state without opening the app.
  Done when: `fm code status --tmux` emits a status-line string (e.g. `fm 2▶ 1⚠ 0✗`) updating within 2s of an event, verified by a golden string test.

- **Wild: Complaint-to-check compiler** — FEATURE — value 4 — effort L — risk med — category: agents — wild
  Why: the user's complaints ("looks like crap with all the text", "isn't doing anything") are turned into tasks by hand each time. Assumption: a phrase can map to a measurable proxy (text-cell ratio, silent seconds).
  Done when: a complaint like "too much text" creates a task whose first criterion is an automated metric check (e.g. text cells per frame under a limit) that fails before the fix and passes after.

- **Wild: Ask any project from anywhere** — FEATURE — value 3 — effort M — risk low — category: user value — wild
  Why: questions already get answers from files with no task; the multi-project home makes cross-project questions natural ("where did I leave nixie?"). Assumption: answers use the local runner only.
  Done when: `fm code "what's left in nixie?"` run from any directory answers from nixie's queue, last run and git state without modifying anything; test asserts no writes occurred.

- **Make config one file with a doctor that explains itself** — FEATURE — value 4 — effort S — risk low — category: setup
  Why: the request asks for "better config/setup", and `models.json` is resolved in two places with config split between files. Assumption: one `config` line selecting the default runner is the goal in T-1328.
  Done when: `fm code doctor` lists every detected runner, the active default and why, config file path, and any invalid line with its line number; a bad config line produces an exact error in a test.

- **Ratchet "first five minutes" in CI** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: each of the user's hits (no `fm` on PATH, no model, silent planner) was in the first minutes of use; releases 1.2.41–1.2.46 fixed CI reds, not onboarding. Assumption: a clean-HOME container run is feasible in CI.
  Done when: CI runs `fm code "add a docstring"` in an empty HOME with only a stub claude CLI and fails if time-to-first-visible-activity exceeds 3s or the run doesn't close.
