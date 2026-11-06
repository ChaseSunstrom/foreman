**Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the test suite wasn't run.

## lens: adversary
- No finding on escape injection. Every canvas cell goes through `Canvas.put` (`fmcodetui.py:280`), which replaces any non-printable character with a space. That covers C0, C1 (0x9b), and bidi/Cf characters. SGR parameters come only from validated `#rrggbb` or 0-255 values.
- LOW — `fmcodetui.py:1733-1736` — ffmpeg inherits the terminal's stdin and reads interactive commands. A `--record` path that starts with `-` is parsed as an option. — Add `-nostdin`, and pass `"--"` or `./path` for the output. — medium

## lens: edge
- MEDIUM — `fmcodeterm.py:97-100` — Under NO_COLOR with the default night theme, `resolve(..., cv.bg)` (`fmcodetui.py:392`) gives every cell inside a panel a tint `bg`. The reverse test is then true for any style outside the six excluded names. Dim, strong, ok and bad text and the gradient bars all show inverted. `_focus_line` (`fmcodetui.py:517`) reverses the whole newest Activity line, which looks the same as a selected line. — Reverse only on the style's own `bg` (`style_has_bg`, not the merged one), and test the depth-0 output for `;7`. — high
- MEDIUM — `fmcodeterm.py:93-103`, `fmcodetui.py:276-281` — The canvas has one cell per character, with no width handling. A CJK or emoji character in Activity text (model output) takes two columns, so the rest of the row shifts right and the right border wraps. If it lands on the bottom row (the prompt or status bar), the screen scrolls. Diff frames only rewrite changed cells, so the damage stays. Zero-width combining characters shift the row left. — Use `unicodedata.east_asian_width` to space-fill the extra cell, or replace wide and combining characters with `?`. Add `\x1b[?7l` to `ENTER`. — high
- LOW — `fmcodeterm.py:173-178` — On SIGHUP, writing `LEAVE` to the dead tty raises `OSError`, then `tcsetattr` raises `termios.error`. That replaces `SystemExit(129)` with a traceback. There is no SIGTERM handler, so `kill` leaves the alternate screen, cbreak mode and a hidden cursor behind. Ctrl-Z suspends inside the alternate screen, and on SIGCONT nothing repaints because `prev` is stale. — Catch `OSError` and `termios.error` in the restore, handle SIGTERM like SIGHUP, and on SIGCONT redo `ENTER` and set `prev = None`. — medium
- LOW — `fmcodeterm.py:42-47,152` — A sequence split across reads (`"\x1b["` then `"A"`) is swallowed, and the `A` arrives as a literal key. In prompt mode it is typed into the request. — Buffer an incomplete trailing escape for the next read. — medium
- LOW — `fmcodeterm.py:152` — PEP 475 retries `select` after SIGWINCH, so an idle screen (fps 1) stays at the old size for up to 1 s. — Wake `select` with `signal.set_wakeup_fd` or a self-pipe. — medium
- LOW — `fmcodeterm.py:135`, `fmcodetui.py:1791` — Only `stdout.isatty()` is checked. `echo req | fm code tui` has no tty on stdin, so `tcgetattr` raises a raw `termios.error` traceback. — Add `sys.stdin.isatty()` to the `--plain` fallback. — high
- LOW — `fmcodetui.py:541,590,747,862`, `faded` at `:492` — On the mono theme, the flash and fade styles drop `reverse`, because `rgb()` has no such field. The "now" chip, check chips, the status chip and GUARD show as plain bold for the length of the flash, then snap back reversed. — Carry `reverse` through `resolve` into the computed style, or skip the flash when colours are None. — high

## lens: maintainer
- MEDIUM, unmeasured — `fmcodeterm.py:87-105,71-77` — `Term.cells` recomputes `resolve`, the SGR string and `to_256` for every cell on every frame, with no memo and an `import` inside the loop. At 30 fps that is 1,920 cells per frame at 80x24 and about 12,000 at 200x60. At depth 256 or 8, each `to_256` call runs several `min()` loops. This could miss the 30 fps cap. — Cache `_code` and `to_256` with `lru_cache`, and memoize per style within a frame. Measure before and after. — plausible
- Nit — `fmcodeterm.py:36` sorts `SEQS` for every input character; sort it once at module level.
- Nit — the depth-0 test (`test_code_tui.py:234-241`) only checks that `38;` is absent, so it misses the NO_COLOR bug above.

## Acceptance criteria
- ANSI renderer with 24/256/8/0 colour and diff frames: met by reading `colour_depth` and `Term.frame`, except that NO_COLOR renders wrongly (see above).
- Motion as a function of state and time: met in code (`FX`, `Motion`); I didn't run the tests.
- Gradients that still read in 256 colours, mono and SVG: met except the mono flashes above.
- `motion = full|reduced|off`, idle at most 4 redraws a second, animating at most 30: met in `App.fps` (1/4/12/30). Whether the loop holds 30 fps is unmeasured.
- `--record` with ffmpeg: met. A missing tool returns exit 2 with a message, not a skip.

## Implicit decisions
- `rsvg-convert` is a second required tool; the video is built from SVG frames.
- Colour depth comes from the `COLORTERM`/`TERM` environment variables only.
- The curses key names are kept, so existing `tui.toml` files still work.
- NO_COLOR is decided by which styles get reversed, not by the theme.

## Not checked
The test suite, `demo/code-tui.mp4`, the README, MASTER and site prose, `_faint` contrast edge cases, and the full `fmcli.py` hunk.

**Noticed:** pasting multi-line text in prompt mode submits at the first newline, and the remaining lines then arrive as hotkeys (`q`, `s` and so on). Bracketed paste is not handled.
