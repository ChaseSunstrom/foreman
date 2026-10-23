---
description: Show Foreman's settings (the fm code app and the foreman-ui pane), set one, diff, share or undo them
disable-model-invocation: true
argument-hint: "[KEY [VALUE] | keys | layout | runners | diff | export | import CODE | undo | bisect | profile | chords] [--surface app|plugin]"
---
Foreman settings, through `fm settings` (one implementation for both surfaces).

Arguments (may be empty): $ARGUMENTS

1. No arguments: run `fm settings list` and show its output as it is: grouped by surface (the app's tui.toml, the pane's options in Claude Code's settings.json), each setting with its value, its default when it differs, and the file.
2. `diff`, `export`, `undo`, or `import` with a code: run `fm settings diff` (the keys changed from the defaults; dead ones, which nothing reads, flagged), `fm settings export` (a share code of those keys: show it as it is), `fm settings import 'CODE'` (every key checked before any is written; only the changed ones are) or `fm settings undo` (the last set or import put back). The code is pasted text: strip its whitespace, and run the import only when what is left matches `^[A-Za-z0-9_-]+$`, passed in single quotes; anything else, refuse in one line ("not a share code: fm settings export makes one") and run nothing.
3. `keys`, `layout` or `runners`: the fm code app's key bindings (`fm settings list keys`: each key and the command it runs), its panel layout (`fm settings list layout`: the columns, their widths and heights) or the coding CLIs it can run (`fm code runners --check`: each one's version, or why it doesn't answer). The app's settings screen edits the same (b binds a key, l moves panels, r tests a runner); here a binding is `fm settings set keys.KEY COMMAND`, a layout `fm settings set layout.columns '[["log"], ["checks", "files"]]'`.
4. `bisect`: run `fm settings bisect` and show what it printed: the tui.toml setting the fm code app can't draw with (its changes from the last settings the app started with, tried in halves on temporary copies; tui.toml isn't written). The app itself starts with those last good settings when tui.toml doesn't draw, and takes an edit made to tui.toml while it runs.
5. `profile`: run `fm settings profile` and show what it printed: this terminal's facts (ssh, tmux, TERM, columns, colour depth), tui.toml's `[profile.NAME]` tables in order, each with its `when` clause and what it sets, and the one that applies (the first that matches; the fm code app starts with its settings over the file's). From Claude Code there is no terminal, so the width is unknown unless COLUMNS gives one and no `width_below` profile matches: the app's own terminal may pick another. Profiles aren't carried by `fm settings export`.
6. `chords`: which key chords this terminal delivers to fm code. It reads key presses, so it needs the user's own terminal: tell them to type `! fm settings chords` (q stops) and read what it prints with them.
7. Any other key alone: run `fm settings get KEY`.
8. A key and a value: run `fm settings set KEY VALUE`, adding `--surface app` or `--surface plugin` only when the arguments name one. A shared name (motion, palette) sets both surfaces.
8. Inside Claude Code the guard decides writes to settings.json. A refused change: show fm's message (it says what the change needs) and stop; never write settings.json another way.

Reply in at most 8 lines: what fm printed, then when it takes effect (the pane applies a changed option on its next poll, within a few seconds; fm code reads tui.toml on its next run).
