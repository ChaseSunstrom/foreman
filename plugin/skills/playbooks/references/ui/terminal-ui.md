<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Terminal and mod UI

Use when building or reworking UI inside a terminal app or a Claude Code mod (panes, bands, status lines, tool rows), or a command-line tool's own output. Each rule below can be marked pass or fail by a reviewer. Foreman's own worked examples: `fmcodeterm.py` (the terminal: keys, paste, resize, colour depth, the session) and `fmcodetui.py` (the app drawn on it: `width`, `fit`, `render`).

## Hierarchy and colour

1. **Decide what the eye needs first.** One primary fact per row (task, step, verdict); everything else dims. Read the screen from 2 m away: what's left is the hierarchy.
2. **Colour carries meaning, not decoration.** Pick a palette of ≤ 7 roles (accent, ok, warn, error, dim, track, one per category). Use the same role everywhere; check both dark and light terminals; never rely on colour alone (add a glyph: ✓ ✗ ⚠ ▸ ○).
3. **Detect the colour depth, don't assume it.** `NO_COLOR` set → no colour at all; `COLORTERM=truecolor|24bit` → 24-bit; `TERM` with `256color` → 256; else 8. Map each role down per depth (fmcodeterm's `colour_depth`), and keep every state readable in the 8-colour and no-colour forms.
4. **True-colour bars and sparklines** beat ASCII art: a filled gradient for done, a flat dim track for the rest, a comet for indeterminate work. Give every rich element a text twin for surfaces that can't draw it (a pipe, `--plain`, a screen reader).

## Display width and wide glyphs

5. **Measure columns, never characters.** East Asian Wide and Fullwidth characters take two columns, combining marks and zero-width joiners none, and most emoji two. Every pad, truncation and alignment uses a width function (`unicodedata.east_asian_width` in `WF` → 2, `combining` → 0), never `len()`. A test row of CJK text keeps its right border in place (fmcodetui's Width tests).
6. **Cut by columns, mark the cut.** Truncate a string at a column count with `…` taking its own column; never split a wide glyph in half (a half glyph prints as a box or shifts the rest of the line). Titles cut at the end, paths at the start.
7. **Ambiguous-width and emoji sequences are wider than they look.** Treat ambiguous-width characters as one column unless the terminal says otherwise, and avoid emoji ZWJ sequences and variation selectors in chrome: terminals disagree on their width, and one disagreement shifts the whole row. Prefer box-drawing and geometric glyphs that every monospace font draws at one column.
8. **Strip control characters from anything shown.** Text from a file, a model or a subprocess can carry escape sequences that move the cursor, retitle the window or hide text. Replace them (keep `\n` and `\t` where the layout handles them) before they reach the screen.

## Resize

9. **A resize is an event, not a poll.** Catch `SIGWINCH`, write a byte to a wake pipe the key wait also selects on, and re-read the size on the next frame (fmcodeterm's `session`). A handler that draws is unsafe: it can interrupt a frame halfway.
10. **Lay out from state every frame.** Never cache a width or a wrapped line across frames; the next frame after a resize redraws everything from the state at the new size, and the first frame after it is a full one (no diff against cells the old size drew).
11. **Have a layout for small.** Name a narrow form (one column, the essentials) below a width and a too-small message below a floor (say the size needed); never draw past the edge or let the last column scroll the screen (turn autowrap off: `ESC[?7l`).

## Keys and bracketed paste

12. **Turn bracketed paste on and parse it.** Send `ESC[?2004h` on entry; text between `ESC[200~` and `ESC[201~` is a paste: one event, never keys. A paste never triggers a binding, a hotkey or Enter; in a prompt it inserts at the cursor with newlines kept.
13. **Cap and clean a paste.** Limit its size (say what was cut), strip control characters and tabs to spaces, and refuse a paste where text has no place (a list view) rather than replaying it as keystrokes.
14. **Parse escape sequences with a deadline.** A lone `ESC` is Escape only after a short wait (≈ 25–50 ms) with nothing following; a known prefix waits for its end. Unknown sequences are dropped whole, never typed into a field.

## Motion budget

15. **Motion has a job.** Animate only live work (a running call, a turn in progress); stop the clock when nothing runs. One shared frame counter, never a timer per element.
16. **Budget frames and bytes.** ≤ 10 fps for ambient motion, a frame only when something changed, and only the changed cells written after the first frame (fmcodeterm's `Term.frame`). Measure: an idle screen writes zero bytes a second.
17. **Respect reduced motion.** A setting (and `NO_COLOR`/`TERM=dumb`) turns every ambient animation off; state changes still show, instantly. Motion is a function of state and time so any instant can be drawn in a test.

## The terminal's lifecycle

18. **Leave the terminal as you found it, on every exit.** Alternate screen, hidden cursor, raw keys, paste mode and autowrap are set on entry and undone on a normal exit, an exception, Ctrl-C, `SIGTERM` and a closed terminal (`SIGHUP`). Write the restore sequence in a `finally` and in the signal handlers.
19. **Ctrl-Z gives the terminal back.** On `SIGTSTP` restore the terminal, then stop; on `SIGCONT` take it again and redraw in full.
20. **The window title is borrowed.** Push it (`ESC[22;0t`) before setting your own and pop it (`ESC[23;0t`) on exit; a title holds printable text only.

## Hierarchy over time: quiet by default

21. **Width and height.** Never wrap a status line. Cap lists (≤ 6 rows) and say "+N more".
22. **Fold routine, keep failures.** Successful rows fold to one line; failures stay full. Never hide what a command really ran.
23. **Consent lives next to what it approves.** A button that grants something sits beside the full plan it grants, needs a deliberate press, and has no one-key hotkey from a place that only shows a title. A key that ends live work asks for a second press.

## CLI product design

24. **Verbs a person would say.** `tool verb object`, not flag soup; `--help` opens with one example per common job before the flag list.
25. **Two audiences, one output contract.** A terminal gets readable lines; a pipe or `--json` gets one stable, documented record per line. Detect a TTY on both stdin and stdout before drawing anything rich or reading a key, and never read stdin unless it is a pipe or a file (and then with a deadline: an agent's stdin may never close).
26. **Errors say what to do next.** Every failure ends with one runnable command (`Next: …`), the exit code is non-zero, and the message names the thing that was wrong in the user's words, not the stack's.
27. **Progress goes to stderr, results to stdout.** A long command shows it's alive within a second (a heartbeat or a count), and its result is the only thing on stdout so a pipe gets clean data.
28. **Safe to run twice.** A command that is interrupted or repeated leaves the same state as one clean run; anything destructive needs an explicit flag and says what it would do first.

## Test the description, not the paint

29. Mount each component on every surface you support, find by text, press by key, and advance a mocked clock to prove animation starts and stops.
30. Render at several sizes (20×12, 40×16, 80×24, a wide one) and with hostile text (wide glyphs, control characters, very long words) and assert nothing draws past the border; keep a golden snapshot of the main screen and regenerate it on purpose, never by habit.
31. Drive the real binary in a pseudo-terminal once per release: entry, a resize, a paste, Ctrl-Z, quit, and check the terminal state afterwards.

Example: `references/ui/examples/terminal-ui.html`: one panel drawn at 80 and at 40 columns: hierarchy, colour roles, wide glyphs and truncation that keep the meaning. The site's Gallery shows it.

## UI contract

- motion: the motion budget has an off setting that honours the app's reduced setting: a still screen that says the same.
- contrast: colour roles pass on dark and light terminals, and every status has a glyph or word too, so NO_COLOR keeps the meaning.
- keyboard: every action has a key, listed in the help; nothing needs a mouse.
- small screens: it works at 40 columns and through a resize, with no line wider than the terminal.
- states: empty, working, error and done each have a designed line or panel, never a raw traceback.
