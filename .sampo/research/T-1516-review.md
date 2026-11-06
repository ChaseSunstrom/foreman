**Verdict:** approve with nits. The two renderer fixes are sound in ASCII and plain CJK rows. The sweep is weaker than its changelog claims: it skips several views and checks structure more than width. I had no shell, so I could not run any tests.

## lens: adversary
- MEDIUM — plugin/lib/fmcodetui.py:401 — `_mark` makes U+FE0F zero-width, so `❤️`, `⚠️` and `✔️` now take 1 column. Terminals that honour VS16 (kitty, WezTerm, iTerm2, Windows Terminal) draw them in 2, so those rows run one column short and the border shifts. Before the fix, the stray VS16 cell happened to match them. — Count base+FE0F as 2 columns, or document the 1-column choice. — 50%
- MEDIUM — plugin/tests/test_code_tui.py:98 — The "independent" rule shares `east_asian_width in "WF"` and `Mn/Me` with the implementation, and its `Cf/Cc` branch is dead because `put` turns non-printables into spaces. So `👍🏽` (put draws 4 columns, a real terminal 2) and `❤️` pass by construction. The sweep checks structure only: orphan or doubled halves and row sums. — Add a small table of real terminal widths (`👍🏽`=2, `❤️`=2, `é`=1) asserted on `width()`, or compare with `wcwidth` when it is installed. — 80%
- MEDIUM — plugin/tests/test_code_tui.py:172 — The sweep could pass vacuously. Nothing asserts the hostile string reached the output. A wrong attribute name in `extra`, or an event the state ignores, leaves the view empty and green. — Assert that a distinctive character of `s` appears in `cv.text()` for each non-clipped screen. — 70%
- MEDIUM — plugin/tests/test_code_tui.py:126-136 — Not swept: the `settings`, `layout` and `runners` views, `prompt` mode (fmcodetui.py:1128, where `app.input` is user-pasted text, the likeliest hostile input) and extension panels. `VIEWS` has 10 entries and `extra` covers 7. — Add the three views and prompt, and assert `set(extra) | {…} == set(VIEWS)` so a new view can't be missed. Extension panels are probably low risk, since they share `_draw`/`put`. — 90%
- LOW — plugin/lib/fmcodetui.py:360 — The "half a wide character doesn't fit" branch still has the doubled-cell bug. Reproducer: `put(0,0,"日本")` then `put(0,1,"語",right=2)` leaves `日`, ` `, `本`, which is 5 columns in a row of 4. `line()` pre-fits its text, so this is reachable only through direct callers of `put` with `right=`. — Blank the neighbour halves here too. — 60%
- LOW — plugin/tests/test_code_tui.py:166 — The fixture name is a hash of the blob, which includes `str(ex)`. An error text with an address or id gives a new file per run, up to about 470 per run, and nothing prunes them. There is no path traversal: the name is 10 hex characters and `label` never reaches the path. — Hash `(label, size, mode, type(ex).__name__)` only, and stop after about 50 files. — 75%
- LOW — plugin/tests/test_code_tui.py:185 — Replay silently skips a fixture whose `label` no longer exists, so it passes while testing nothing. — Fail or skip with a message when no screen matched. — 80%
- LOW — plugin/tests/test_code_tui.py — No direct unit test of `Canvas.put` over a wide cell or of `_mark`/`width("❤️")`, so the fixes' necessity rests on the sweep. — Add a 3-line test each. — 70%

## Acceptance criteria (inferred from the changelog; the brief states none)
- Every panel and view swept at four sizes: partly met. `settings`, `layout`, `runners`, prompt and extension panels are not swept.
- Independent column rule: partly met (see the second finding).
- Crash saved and replayed: met. The writer stays in `fixtures/crashes`, with growth as noted above.
- Renderer fixes: met. In normal ASCII and CJK rows no cell is `""`, so the new branches never fire. Per-character cost is a few index operations.
- Claude Code parity: not met. For a test net it matters little, because the fixes ship in `plugin/lib` and work in the plugin too. A verb would add value only to run the sweep over a user's extension panels.

## Implicit decisions
- Width follows `unicodedata` East Asian Width (ambiguous = 1), not terminal-measured widths.
- Fixtures are written into the source tree.
- Both the oracle and the implementation reduce non-printable characters to a space.

## Not checked
- I ran no tests, so I can't confirm the sweep fails without the fixes.
- I did not review `fmcodeterm.frame` output.
- I did not read the CHANGELOG/MASTER entries beyond the diff.

Noticed: none
