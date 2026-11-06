# Brainstorm — lens: simplicity

- **Make bare `fm code` do the one obvious thing** — FEATURE — value 5 — effort S — risk low — category: entry
  Why: the user's complaint was that `fm code` alone errors and `fm code tui` is a one-run viewer. Simplest fix: no args means open the app, and every other form (`fm code "req"`, `--task ID`) is the same app started with a pre-filled action. Delete the separate `tui` verb path by keeping it as an alias.
  Done when: in a fresh HOME with only the claude CLI installed, `fm code` in a pty opens a screen with a prompt box and exits 0 on quit, and `fm code tui` renders the identical first frame.

- **Collapse runner setup to zero questions plus one line** — FEATURE — value 5 — effort S — risk low — category: config
  Why: the pack says the user needed to press m and pick the claude worker before the first request worked. Probe PATH once, pick the first found CLI in a fixed order, and store a single `default = "claude"` line only when the user overrides it. No setup wizard.
  Done when: with no `models.json` and only `codex` on PATH, `fm code "fix typo"` picks codex, and `fm code runners` prints the choice and the one config line that changes it.

- **Add one `fm code why` command that answers "is it doing anything?"** — FEATURE — value 5 — effort S — risk low — category: observability
  Why: the nixie run "just isn't doing anything" while a planner ran for minutes with no signal. A single command reads the run's event log and the child process table and prints one sentence: waiting on claude planner for 4m12s, 118k tokens in, last output 3m ago, pid 4821.
  Done when: against a run whose planner child is sleeping, `fm code why` names the stage, the child pid, and the idle seconds, and against a dead run says the run is gone.

- **Detect Foreman-inside-Foreman once, at the process boundary** — FIX — value 5 — effort S — risk low — category: reliability
  Why: the user wants no duplicate Foreman when it runs Claude Code as a worker, and the planned T-1327 is about stripping context. Simplest root cause is one environment marker, set when fm code spawns a child. Every Foreman entry point (hooks, session context, drive, request capture) checks that marker first and exits quietly. One rule replaces many per-feature exclusions.
  Done when: a child started by fm code has the marker set, and its session-start and prompt hooks emit zero bytes while the guard still blocks a destructive command.

- **Run nested workers with a bare profile by default** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: 66k–133k input tokens per planner call came from loading every plugin and Foreman's own rules. Start worker CLIs in an isolated settings directory with only the guard hook. Assumption: the claude CLI honours a settings or config-dir override and a plugin-off flag in the installed version.
  Done when: a planner call through fm code reports input tokens under 15k on a trivial request, and the guard test corpus gives the same verdicts as before.

- **Make one process group the unit of a run** — FIX — value 4 — effort S — risk low — category: reliability
  Why: quitting left the planner orphaned. Start each child in its own session under the run, and have every exit path (quit, SIGHUP, SIGTERM, parent death) kill the group. One mechanism, not a list of cleanups.
  Done when: a test starts a run with a sleeping fake worker, sends SIGKILL to the fm parent's TUI, and the worker is gone within 5 seconds.

- **Show the project list from what's already on disk, no registry** — FEATURE — value 4 — effort M — risk low — category: projects
  Why: the home screen over every project needs a source of truth. Scan Foreman's existing state directories rather than adding a project-add command. Assumption: each project already leaves state under foreman_home keyed by path.
  Done when: after running fm in two repos, the home screen lists both with queue counts, and no new registration step or file exists.

- **Print a plain status line when not a tty** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: `fm code` piped, in CI or over a dumb terminal shouldn't attempt the renderer. Falling back to one line per event is also the test mode and the screen-reader mode, so one path serves three needs.
  Done when: `fm code "x" | cat` prints readable lines with no escape bytes and the same exit code as the tty run.

- **Delete the panels and settings nobody uses, measured locally** — CLEAN — value 3 — effort M — risk low — category: scope
  Why: the idea list above is very large, and the user earlier said the TUI looked like crap with all the text. Keep a local counter of view dwell and keypresses, and ship removal tasks for anything under a threshold after a month. Assumption: counters stay on the machine.
  Done when: `fm code usage` prints per-view counts from a local file, and a ratchet test fails if a view is added without a key that opens it.

- **Wild: Make the whole TUI one sentence that grows** — FEATURE — value 3 — effort M — risk med — category: ui
  Why: wild. The default view is a single line such as "Fixing parser bug: step 3 of 5, tests failing, 4m, $0.31", and pressing a key expands it into panels. Small terminals and tmux status bars get the product for free.
  Done when: at 80x3 the screen shows exactly the sentence, and pressing Enter reveals the full layout.

- **Wild: Let Foreman file its own friction tickets from your words** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: wild, and straight from the request that Foreman should figure this out unasked. When a prompt matches friction phrases ("isn't doing anything", "why can't I"), create a single task naming the feature area and attaching the last run's `fm code why` output. Assumption: the prompt hook can match phrases cheaply inside its 5 s budget.
  Done when: a prompt containing "it just isn't doing anything" in a project with a recent run creates one task with the run's state attached, and a repeat within an hour adds no second task.

- **Wild: Offer `fm code` as a shell prompt segment instead of an app** — FEATURE — value 2 — effort S — risk low — category: surface
  Why: wild. A tiny `fm code prompt` prints "fm 3q 1b" (queued, blocked) so the user sees work without opening anything, and the app is one keystroke away.
  Done when: running it in a project with 3 queued and 1 blocked tasks prints that text in under 100 ms.

- **Replace the many themes with one palette plus an accent flag** — CLEAN — value 2 — effort S — risk low — category: ui
  Why: four themes and a gallery add surface area for a taste the user hasn't asked to tune. One derived palette from the terminal's own colors and `--accent` covers the need.
  Done when: only one theme file exists, `fm code --accent teal` recolors the header, and golden frames pass.
