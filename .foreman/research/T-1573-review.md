**Verdict:** approve with nits. I found no way for a kept value to differ from the previewed one, or for the app to stay in the previewed look after a revert. I only read the code. I had no shell, so I did not run `test_code_tui.SettingsPreview`.

## lens: intent / adversary / edge / maintainer
- LOW — plugin/lib/fmsettings.py:303-312 — `preview_app` never runs the guard check that `set_app` runs at :293-297. In a Claude Code session (`CLAUDECODE` set, or no tty) the preview shows, and the refusal only comes after the keep. The guard test at test_code_tui.py:257 pins that behaviour, but the docstring's "refused now, not after the keep" overstates it. Fix: call `_guard_block` in `preview_app` when `in_claude_code()`, or say in the docstring that the guard is checked at keep. Confidence: high.
- LOW — plugin/lib/fmsettings.py:322-367 — `_set_app` returns `cfg` when `write=False` and `(value, errors)` when it writes, so one function has two return shapes. Fix: split out a `_plan_app` that returns `cfg`, and have `_set_app` call it. Confidence: high.
- LOW — plugin/tests/test_code_tui.py:216-218 — nothing asserts that the config the app shows after the keep equals the config it showed during the preview. The existing tests check only `preset`, `palette` and `motion`. Fix: in the keep test, save `app.cfg` before the key and `assertEqual` it afterwards. Add a `preview_app` test in `test_settings.py` that checks it refuses what `set_app` refuses (`theme nope`, a lone surrogate) and writes nothing. Confidence: high.
- LOW — plugin/lib/fmcodetui.py:1475 — `App.clock` is `time.monotonic`, which on Linux does not count suspend. After a suspend the preview stays on screen until 10 awake seconds have passed. Nothing is written in the meantime, so it fails safe. Don't change the clock, because `Motion` also uses it. At most, add a note. Confidence: medium.

## Your questions
- **Can preview accept what set_app refuses?** No. `preview_app` does the same lookup, `_check`, `_utf8` and `_set_app` body (parse, placement, own-error and render checks), and only the guard and the lock are skipped. On keep, `set_key` runs `set_app` again on the already-normalised value, and the vocabulary is shared (`fmsettings.py:17-23`), so a canonical value passes again.
- **Does the preview config match what a keep loads?** Yes. `_load(new, path)` and `_settings_reload()` both call `load_config` on the same text.
- **Can a revert be missed?**
  - Crash, Ctrl-C or SIGTERM: nothing was written, so the file is unchanged.
  - Leaving the screen: Esc and `q` are keys, so they keep the preview and stay on the screen (tested).
  - A second preview, or `:set` on another key: unreachable, because `key()` at 1519-1521 turns the first keypress into a keep and returns. The only way two keys act within one preview is two keys read in the same batch, and then the second one acts normally.
  - A key at or after the deadline: `_settings_expire` runs first and the key is processed normally (tested).
  - Timing: `poll()` runs every loop pass and `fps` is at least 1, so a revert is at most about 1 s late.
- **Is the keep path guarded and locked?** Yes. `_settings_write` calls `set_key`, then `set_app`, which does the guard check, the `fmcore.lock` and the atomic write. A refused keep leaves `cfg` at the old look with the note shown (tested).
- **Does the repaint test prove the screen behind repainted?** Yes, though it checks one colour. `"shade"` is used only by `_overlay` (`fmcodetui.py:1110`), which fades every cell behind the box to that colour. So `fill="#c9d1dd"` appearing only after the preview shows the background repainted. The revert test checks the night shade `#2a3650`. The palette test checks `cfg`, not the SVG, but `cb` changes `accent` and `warn`, and the overlay draws those (select bar and key chips).

## Acceptance criteria
- A theme change repaints behind the overlay before it is kept: met (above).
- An unkept change reverts after 10 s in the file and on screen: met. The file is never touched, and the tests check both the screen and the file.
- Any key keeps it: met, including a paste and Esc. The test run is not verified.

## Implicit decisions
- The preview writes nothing, so the pane half of a shared setting (`motion`, `palette`) also waits for the keep.
- The keypress that keeps a preview is consumed and does nothing else.
- Only `theme`, `palette` and `motion` preview, and only for the app surface or both surfaces.
- The preview is validated against an empty `State()` at two sizes, not the live state.
- Preview and keep both read the file, so an edit by another process during the 10 s is picked up at keep.
- Hunks: each serves the single acceptance criterion, since the steps name no files. No scope creep. The pre-audit's `test_settings.py` point is the LOW test gap above.

## Not checked
The security lens (terminal escapes, injection) beyond the guard path; docs and MASTER.md; the other lenses' history items. Running the tests.

**Noticed:** none
