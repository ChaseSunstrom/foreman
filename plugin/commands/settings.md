---
description: Show Foreman's settings (the fm code app and the foreman-ui pane) or set one
disable-model-invocation: true
argument-hint: "[KEY [VALUE]] [--surface app|plugin]"
---
Foreman settings, through `fm settings` (one implementation for both surfaces).

Arguments (may be empty): $ARGUMENTS

1. No arguments: run `fm settings list` and show its output as it is: grouped by surface (the app's tui.toml, the pane's options in Claude Code's settings.json), each setting with its value, its default when it differs, and the file.
2. A key alone: run `fm settings get KEY`.
3. A key and a value: run `fm settings set KEY VALUE`, adding `--surface app` or `--surface plugin` only when the arguments name one. A shared name (motion, palette) sets both surfaces.
4. Inside Claude Code the guard decides writes to settings.json. A refused change: show fm's message (it says what the change needs) and stop; never write settings.json another way.

Reply in at most 8 lines: what fm printed, then when it takes effect (the pane applies a changed option on its next poll, within a few seconds; fm code reads tui.toml on its next run).
