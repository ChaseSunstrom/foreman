# Brainstorm — lens: simplicity

- **Route every runner launch through one `spawn_runner()`** — CLEAN — value 5 — effort M — risk med — category: architecture
  Why: the open work splits one launch path across five tasks (T-1326 stop kills children, T-1327 nested sessions run lean, T-1329 live progress, plus the depth marker and process group). Without one choke point these will drift apart.
  Done when: a test greps that no module outside `spawn_runner` calls `subprocess.Popen` for a runner, and one fake-CLI test shows scrubbed env, own process group, stream tap and kill-on-quit all applied.

- **Define runners as 8-line spec files** — CLEAN — value 4 — effort M — risk med — category: runners
  Why: assumption: `--worker claude|codex|gemini|aider` are separate code paths. T-0794 already says "retire adapters", and the user wants "ANY CLI". A spec (argv template, prompt via arg or stdin, stream format, plan-mode flag) makes a new CLI a data file.
  Done when: claude, codex and a made-up CLI run through the same code, with the made-up one added only by a spec file, and the 7-request-kind bench still passes on claude.

- **End every fm code failure with one "Next:" command** — FEATURE — value 4 — effort S — risk low — category: errors
  Why: the user hit "fm code needs a request", `fm` not found, and a silent planner. Each dead end had a known fix.
  Done when: a test runs 6 known failure paths (no request, no model, missing PATH link, no runner found, stalled planner, unwritable state) and each prints exactly one final line starting with `Next:` that is a runnable command.

- **Pipe stdin in as the request context** — FEATURE — value 3 — effort S — risk low — category: CLI grammar
  Why: assumption: `git diff | fm code "review this"` isn't supported. This is the cheapest way to make fm code feel like a unix tool.
  Done when: `printf 'x' | fm code "what is on stdin"` answers with the piped text in context and creates no task.

- **Give `fm code` one grammar: `fm code [REQUEST]`, everything else a flag** — CLEAN — value 4 — effort S — risk med — category: CLI grammar
  Why: the dropped item about a request literally "tui" needed a `--` escape because the token after `code` is rewritten. Bare `fm code` becoming the app makes the subcommand rewrite more fragile.
  Done when: `fm code tui` still opens the TUI and prints a one-line deprecation, `fm code --tui` is canonical, and the request "tui" works with no `--`.

- **Cap `fm code --help` at one screen and ratchet it** — CLEAN — value 3 — effort S — risk low — category: complexity budget
  Why: fm code has accumulated tui, bench, --task, --worker, template workers, themes and a motion setting. Help length is a cheap proxy for sprawl.
  Done when: a test fails if `fm code --help` exceeds 40 lines or 8 top-level flags, and advanced options sit behind `--help-all`.

- **Make prompts optional, with every decision logged for review** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: the user said "dont' stop until complete, full auto" and "stop asking me", so questions are friction. Each question Foreman would ask gets a default, and the answers land in a "decisions I made" list.
  Done when: an unattended run on a fixture finishes with zero reads from stdin, and `fm code decisions` lists each defaulted choice with its alternative.

- **Ship `fm.pyz`, a single-file zipapp, so fm works with no plugin or PATH setup** — FEATURE — value 4 — effort M — risk low — category: install
  Why: the user's first blocker was "`fm` wasn't a command" outside Claude Code. A stdlib zipapp can be copied into any PATH dir.
  Done when: `python3 fm.pyz code --help` runs on a clean HOME on Linux and macOS in CI, and `fm.pyz setup` copies itself to `~/.local/bin/fm`.

- **Lint a six-noun vocabulary in all UI strings** — CLEAN — value 3 — effort S — risk low — category: language
  Why: the pack mixes request, task, run, lane, step, station, check and criterion. Newcomer-facing text should use few terms.
  Done when: a test scans fm code user-facing strings and fails on any word outside the glossary file or on a synonym of a glossary term.

- **Wild: Treat a `TODO.fm` file in any project as the queue** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: wild. Lines in the file become tasks, and Foreman strikes them through as they close. Edit the queue in an editor, with no commands.
  Done when: adding a line to `TODO.fm` shows up on the home screen within 5 s, and closing the task writes the line back as `[x] … (T-id)`.

- **Wild: Pick a runner by intent: `--careful`, `--cheap`, `--free`** — FEATURE — value 3 — effort M — risk med — category: routing
  Why: wild. Users shouldn't need model names. Each word maps to the best proven runner (from `fm code bench` grades) for that axis, with the choice shown.
  Done when: `fm code --free "…"` picks a local endpoint if one is present, otherwise says "no free runner found. Next: …", and the header names the choice and the bench grade behind it.

- **Wild: Print the whole app state as a single sentence when you run `fm code` without a tty** — FEATURE — value 2 — effort S — risk low — category: status
  Why: wild. "3 tasks queued in nixie, 1 blocked, nothing running. Next: fm code --task T-1330." It works in a shell prompt, a cron mail or a tmux status line.
  Done when: `fm code | cat` prints exactly one line under 120 chars, built from the same data the home screen uses, and exits 0.

- **Wild: Make `fm code` refuse to start a second copy of itself, then adopt the first** — FEATURE — value 3 — effort M — risk med — category: single instance
  Why: wild. This extends the user's "no duplicate Foreman" complaint to the app itself. A second launch attaches to the live run as a viewer instead of racing it.
  Done when: starting `fm code` twice in one project opens the second as a viewer of the first run, and killing the second leaves the first running.
