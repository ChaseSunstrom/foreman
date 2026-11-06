## Verdict
Approve with nits.

## lens: intent
ok. `fm scene cells FILE` draws through `fmraster` as 24-bit upper half blocks. It is deterministic, culls back faces and refuses a bad `--cols`. T-1846 (shader subset) and T-1847 (three.js import) are split off, so their absence is not a gap. That leaves the "scene.json to terminal cells" half of T-1635.

## lens: edge
ok.
- **`--cols` bounds:** `fmscene.py:643` checks 2 to 400, and `cmd_scene` catches the `ValueError` and exits 2 (`fmscene.py:1020`).
- **Heights:** `fmscene.py:645` always gives an even height of at least 2. `cols=2` and `cols=3` both give h=2.
- **Background null:** `_background` returns `(0,0,0)` (`fmscene.py:629`).
- **Turntable refactor:** I compared the old and new `turntable` code in the diff. Focal length, background and per-frame render are the same expressions moved into `_frame`, so the output is unchanged.
- **Non-finite `--turn`:** `nan` and `inf` raise `ValueError` inside `triangles`, so they exit 2 with a message.
- **Largest frame:** `--cols 400` is 400x250 pixels, 100k pixels and about 0.1 s.

## lens: maintainer
- LOW — `plugin/tests/test_scene.py:141-154` — Only the `cols=1` and `cols=500` refusals are tested. `cols=2` and `cols=400` are not, and the `max(2, …)` clamp at `fmscene.py:645` is never exercised — add `fmscene.cells(plate(…), cols=2)` and assert `len == 1` — high.
- LOW — `MASTER.md:136` — The T-1635 note sits after the closing parenthesis with no separator. The neighbouring lines use `; T-16xx:` inside the parens — move it inside as `; T-1635: …` — high.

## lens: operator
- LOW — `plugin/lib/fmscene.py:1006` and `:652` — Truecolor escapes print unconditionally. Piped to a file or run with `NO_COLOR` or a non-truecolor terminal, the output is raw `ESC[38;2…` garbage. The docstring, `scene-3d.md` and the `ponytail:` comment all say "truecolor only", but the `--help` text says nothing about it. Add "truecolor terminal" to the `cells:` action help at `fmcli.py:6713`. A `NO_COLOR` or isatty guard is optional. — medium.
- `--json` is fine. `fmcli.out` escapes the raw ESC bytes (`\u001b`), and `lines` is a list of strings.

## Acceptance criteria
The one criterion is met, from code reading only. I did not run `python3 plugin/tests/run.py Offline`.
- **Rows of 24-bit half-block cells:** met. `fmscene.py:648-653` builds them, and `test_cells_draw_the_scene_as_half_blocks` asserts the count of `▀` per row and the `38;2;` escapes.
- **Deterministic:** met. The test compares two calls in the same process.
- **Back faces culled:** met. The `turn=180` test (`test_scene.py:151-152`) expects only black.
- **Bad `--cols` refused:** met. `test_fm_scene_cells` expects a nonzero exit for `--cols 500`.

## Implicit decisions
- The default is 64 columns.
- Pixel height is 5/8 of the width, rounded down to even.
- Every cell carries both a foreground and a background colour, about 40 bytes per cell.
- `--json` returns `{cols, rows, lines}`.
- The `--cols` check runs after the scene loads.
- `--turn` is in degrees about +Y.

## Not checked
- I did not run the tests or the CLI.
- I did not check how the output looks in a real terminal.
- I did not check the mid-sentence `CHANGELOG.md` wording.

Noticed: none
