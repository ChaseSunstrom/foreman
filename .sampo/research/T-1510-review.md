**Verdict: changes needed.** One terminal-escape hole (it is the key question you asked) and one injection path in the slash command. Nothing was run; this is a read-only trace of the code.

## lens: adversary

- MEDIUM — plugin/lib/fmcodetui.py:2200 (reached from plugin/lib/fmsettings.py:383-385 and :656-659) — A share code prints raw escape bytes to the terminal. The code `{"app":{"colors.ok":{"\u001b]0;x\u0007":true}}}` passes `_check`, because style values that aren't strings are returned unchanged. `_toml` writes the key escaped, so it survives parsing. `_style_error` then returns `f"{k}: not a style field"` with `k` unquoted. `_plan_app` re-raises that as an "own" error, `import_code` joins it into `bad`, and `PolicyError` prints it raw. The test at plugin/tests/test_settings.py:608 only covers a bad key and a bad surface, so this case is untested. Fix: use `{k!r}` in `_style_error`, and also escape control characters in `import_code`'s `bad` text before it is raised. Confidence high (traced, not run).
- MEDIUM — plugin/commands/settings.md:11 — `fm settings import CODE` is built from `$ARGUMENTS`, which is text the user pasted from someone else, with no quoting or shape check. A "code" like `e30; <cmd>` becomes part of a Bash line the model composes, and the whole string also goes into the model's prompt. Fix: tell the model to run import only when the code matches `^[A-Za-z0-9_-]+$` (after stripping whitespace), to pass it single-quoted, and otherwise to refuse. Confidence medium.
- LOW — plugin/lib/fmsettings.py:570 — `written()` calls `T.load_config` with no try. A hand-written tui.toml like `[layout]\ncolumns = 5\nwidths = [1]` makes `_layout_error` raise `TypeError` at fmcodetui.py:2219. Every `set`, `import`, `undo`, `diff` and `export` now fails first, including the `set layout.columns …` that used to repair the file. Fix: wrap the call, set `skips = []`, and add a problem entry.
- LOW — plugin/lib/fmsettings.py:533 — `old if ok else None` means undo deletes a value the app had skipped (an invalid word, or a colour that was too faint) along with its trailing comment, instead of restoring it. Fix: record the raw old text, or say so in the undo output.
- LOW — plugin/lib/fmsettings.py:701-703 — A failing `_keep` in `finally` raises after the setting was already written, so the caller sees a failure and the change is missing from history. `_history()` also treats an `OSError` as empty, so the next `_keep` overwrites the whole history. Fix: catch `OSError` in the `finally` and warn; fall back to empty only on `ValueError`.
- LOW — plugin/lib/fmsettings.py:221-223 — A code holding both `keys.enter` and `keys.ENTER` records two changes with the same `old` value. Undo then reports "changed since" for the first one and exits non-zero, even though the file is restored. Fix: take `old` from the live state, or merge changes by key.

Findings that came back clean:
- **TOML injection:** `_toml` and `_toml_key` use `json.dumps`, so quotes, newlines and table headers are escaped. A DEL byte makes the file unparseable, which the "can't place it" check refuses.
- **settings.json injection:** none; `json.dumps` writes it and values are schema-bound.
- **Size limits:** code length, key count, recursion and non-finite numbers are all capped.
- **Writes:** all go through `set_app`/`set_plugin`, so the guard and lock apply, undo included.
- **None-unset:** `None` reaches a write only from undo. The CLI and the app's `:set` reject an empty value, and import rejects JSON null.
- **History:** it goes through `fmcore.write_atomic` under the lock, is capped at 50 entries, tolerates a corrupt file, and undo never records itself, so it cannot loop.
- **Hand edits:** undo leaves them alone via `cur != new`.

## Acceptance criteria
- **diff against defaults:** met by reading; I did not run it.
- **export/import round trip:** met; the test at test_settings.py:575 covers it.
- **undo restores the previous value:** met; the test at test_settings.py:632 covers it.
- **Verify command:** not verifiable; I had no shell.

## Implicit decisions
- Share code format is base64url of JSON, with the `=` padding stripped.
- Limits are 32 KB, 300 keys and 50 history entries.
- Unreadable history becomes an empty history.
- Undo drops an entry whose value changed since.
- The history is global, not per project.

## Not checked
Test execution, fmcli.py beyond the argparse hunk, and the README text.

**Noticed:**
- `fm settings diff --json` drops the "plugin.json not found" problem (fmsettings.py:494-496). The plugin rows are not misreported as dead, but the warning is lost in JSON mode, and no test covers a missing plugin.json.
- `fm settings set colors.ok '{ "\u001b[2J" = true }'` shows the same escape output through the existing CLI.
