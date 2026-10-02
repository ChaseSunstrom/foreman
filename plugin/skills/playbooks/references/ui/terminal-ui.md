<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Terminal and mod UI

Use when building or reworking UI inside a terminal app or a Claude Code mod (panes, bands, status lines, tool rows).

1. **Decide what the eye needs first.** One primary fact per row (task, step, verdict); everything else dims. Read the screen from 2 m away: what's left is the hierarchy.
2. **Motion has a job.** Animate only live work (a running call, a turn in progress); stop the clock when nothing runs. Budget ≤ 10 fps; one shared frame counter, never a timer per element.
3. **Color carries meaning, not decoration.** Pick a palette of ≤ 7 roles (accent, ok, warn, error, dim, track, one per category). Use the same role everywhere; check both dark and light terminals; never rely on color alone (add a glyph: ✓ ✗ ⚠ ▸ ○).
4. **True-color bars and sparklines** beat ASCII art: a filled gradient for done, a flat dim track for the rest, a comet for indeterminate work. Give every rich element a text twin for surfaces that can't draw it.
5. **Width and height.** Truncate at the end (titles) or the start (paths); never wrap a status line. Cap lists (≤ 6 rows) and say "+N more".
6. **Quiet by default.** Fold routine, successful rows to one line; keep failures full. Never hide what a command really ran.
7. **Consent lives next to what it approves.** A button that grants something sits beside the full plan it grants, needs a deliberate press, and has no one-key hotkey from a place that only shows a title.
8. **Test the description, not the paint:** mount each component on every surface you support, find by text, press by key, advance a mocked clock to prove animation starts and stops.
