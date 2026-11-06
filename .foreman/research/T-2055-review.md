**Verdict:** approve with nits

## lens: intent
- MEDIUM — CHANGELOG.md:4 — The entry says turning plugins off with `--settings` is why the ecc warning "no longer shows". The new `quiet()` docstring (demo/record_live.py:57) says a disabled plugin's hooks.json warning still prints at startup. So the warning is now hidden by blanking text after capture, not by `--settings`. Reword the entry to say the notice rows are blanked from the recording, and to name the login, plan and tmux notices it also hides. Confidence: high.
- LOW — demo/record_live.py:51 — `NOTICE` also blanks the login-expiry, plan-promo and tmux-focus rows. The user only asked about the ecc warning. This is sensible noise removal, but it is wider than asked, so say so in the changelog. Confidence: medium.
- AC1 checks that `only_foreman()` builds the right JSON. It does not check what the user sees. The visible result relies on `quiet()`, which the test does cover.

## lens: adversary
- Nothing found. `quiet()` blanks text and never executes it. It runs before the home-folder and name scrub, so it cannot reintroduce an identity string.

## lens: edge
- LOW — demo/record_live.py:52 — `hooks\.\w+\[\d+\]` is not limited to the startup banner. With `--repo .` on this repo, a tool row that shows code or docs mentioning `hooks.PreToolUse[0]` has its text blanked up to the next `│`. In `--from-cast` mode that change is written permanently into live.cast. Fix: limit matching to the first N rows (the startup area), or require the `hooks.json:` prefix and drop the bare `hooks.X[n]` alternative, accepting that wrapped second lines then need the row-position check. Confidence: medium.
- LOW — demo/record_live.py:68 — A character that is wider than one column becomes one space, so a `│` further along the row would shift left. The `ponytail:` comment acknowledges this. The current notices contain no wide characters. No action needed.
- A wrapped ecc warning line with no `hooks.X[n]` text (for example "and 43 more ignored" alone on a row) would survive. Whether the new live.mp4 shows this depends on the wrap width. Not verifiable from the code.

## lens: operator
- Nothing found. This is a dev-only recorder with no hook, install or startup cost. The one extra regex pass per captured frame is negligible. A recording costs one model turn, as before.

## lens: maintainer
- LOW — demo/record_live.py:53 — `ANSI` partly duplicates `shot._SGR`, which matches only `m` sequences. The wider pattern is needed here for the `\x1b[H\x1b[2J` prefix of cast events, so this is justified. Add a one-line comment saying why it isn't `shot._SGR`. Confidence: low.
- The test (plugin/tests/test_shot.py:82-93) asserts behaviour, not mocks. It covers both separators, that row lengths hold, and which rows survive. It has no case for a row that matches `NOTICE` but has no `│` after it. The first branch (`end < 0`) is only exercised through the `clau.de` row, so it is covered, though weakly.

## Acceptance criteria
- AC1 (only_foreman turns off non-foreman plugins via `--settings`): met. only_foreman() is at demo/record_live.py:38-48 and the settings are passed at line 155. The test at test_shot.py:~88-90 covers it. I did not run the test.
- AC2 (the new recording shows no other plugin's banner or status line): not verifiable from the code. It needs a look at ffmpeg frames of live.mp4. I did not do that, because I had no shell. The diff does show live.cast shrinking from 377 lines to 85, so it was re-recorded.

## Implicit decisions
- Notices are blanked by regex, and the row is cleared from column 0 up to the next `│`.
- The login, plan-promo and tmux-focus rows are hidden along with the ecc warning.
- Blanking runs in `scrub()` for new recordings and again over live.cast under `--from-cast`. It is idempotent.
- "Foreman's plugins" means any plugin whose marketplace suffix is `foreman`. Project-level or settings.local plugins are not touched.

## Not checked
- The contents of live.mp4, live.svg and live.cast, because the diff leaves them out and I had no ffmpeg.
- That the tmux capture really emits only SGR escape codes.
- Whether the marketplace is named `foreman` in the user's settings.

**Noticed:** none
