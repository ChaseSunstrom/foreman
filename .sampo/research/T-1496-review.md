**Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I read the code and tests and ran nothing. Findings 1 and 2 are worth fixing before merge.

The adversary checks held up:
- **Keys:** a key must be a schema key or `keys.X` where `parse_key` accepts X (an alias word, `ctrl+x`, f1–f12 or one printable character). It is written through `_toml_key`, so quotes, `#`, `[` and `.` end up inside a quoted key. No key is ever used as a path.
- **Values:** `_check` turns a typed word into a value, and the text written comes from `T._toml(value)`, never from the raw argument. A value like `1\n[evil]` therefore cannot add a line or table. A DEL character fails the `placed` check and is refused.

## lens: adversary
- LOW — `~/.claude/foreman/.claude/worktrees/agent-a7430adfe5a0a3d43/plugin/lib/fmsettings.py:262` — `set_app` never asks the guard, although `fmguard.py:53` lists `tui.toml` as `_CORE_CONFIG`, a file the user must approve. A session can run `fm settings set keys.q none` or `colors.ok 244` with no approval. The schema limits the damage to appearance and key bindings, and `_set_default_runner` (`fmcode.py:2099`) already writes `code.toml` the same way. — Call `_guard_block(path, p)` in `set_app` as `set_plugin` does, or record the decision in the docstring — medium
- LOW — `fmsettings.py:350` — `_guard_block` builds a `Ctx` with no `confine`, `scratch` or `unbriefed`. A builder lane with trust on can write `~/.claude/settings.json`, which the real hook would block as `confine`. — Pass `confine` from the lane meta — medium
- LOW — `fmsettings.py:312` — `claude_dir()` follows `CLAUDE_CONFIG_DIR`, but the guard protects only `~/.claude/settings.json` (`fmguard.py:535`). `CLAUDE_CONFIG_DIR=/x fm settings set mascot off` creates or edits `/x/settings.json` as ordinary. The test at `test_settings.py:108` depends on this. — Accept it, or refuse a config dir that is not under `~` — low

## lens: edge
- MEDIUM — `fmcodetui.py:1923` and `:1936` (also reached from `fmsettings.py:292` and `:395`) — `user["theme"] in PRESETS` and `val in BORDERS` raise `TypeError: unhashable` for a valid-TOML list or table. Input: `theme = ["x"]` or `border = {}`. Then `fm settings set theme night` and `fm settings list` both crash, so the tool cannot repair a file the app also crashes on at start. The lines predate this diff, but the new commands now depend on them. — Guard with `isinstance(.., str)` in `load_config`, and wrap the `old` `_load` in `set_app` — high
- MEDIUM — `fmsettings.py:274` to `:305` and `:372` to `:385` — both writers read, edit and replace the file with no lock, so two concurrent sets lose one update. Claude Code also rewrites `settings.json` itself. — Wrap each in `fmcore.lock(dir)`, which exists at `fmcore.py:823` — medium
- LOW — `fmsettings.py:210` — if any `\r\n` appears, every bare `\n` line is rewritten to CRLF. A mixed-ending file therefore breaks the byte-identical promise. — Keep each line's own ending — high
- LOW — `fmsettings.py:254` — `fm settings set colors.ok $'\xff'` produces a lone surrogate. `f.write` in `_load` then raises an uncaught `UnicodeEncodeError` instead of `SettingError`. The file stays unchanged. — Catch it in `set_app` — medium
- LOW — `fmsettings.py:385` — `settings.json` is rewritten whole with `indent=2`, so a differently formatted file gets a noisy diff. — Note it in the docs — high

## lens: operator
- LOW — `fmsettings.py:443` — `get` and `list` read only the schema. `fm settings set keys.y quit` succeeds, but `fm settings get keys.y` says "no such setting". — Use `find()` in `get` and list user-added keys — high
- LOW — `fmsettings.py:395` and `:399` — a `tui.toml` with errors or an unreadable `settings.json` is shown as plain defaults, with no warning. — Print the errors under the list — high

## lens: maintainer, intent
No findings. The `calm` to `reduced` migration is consistent across `plugin.json`, `register.tsx:551` and `load_config`.

## Acceptance criteria
- **1 (schema entry per DEFAULTS key; set keeps other bytes):** met by the tests I read (`test_code_tui.Settings`, line 792 onward). I traced `edit_toml` by hand against `test_a_missing_key_goes_into_its_table_and_a_missing_table_is_added` and `test_odd_but_valid_files_are_edited_in_place` and found no mismatch. Not run.
- **2 (bad value or failed render leaves the file unchanged):** met. `set_app` raises before `write_atomic`, and the test covers six bad inputs plus a patched render error.
- **3 (one schema covers both surfaces; `fm settings list` shows value, default and where):** met by the code and by `test_settings` (`Schema` and `Command` classes). Not run.

## Implicit decisions
- `tui.toml` writes skip the guard.
- A shared set writes the app first, then the plugin, and exits non-zero if the plugin half is refused. The app change stays written.
- A setting made bad indirectly (for example `widths` after a `columns` change) is written and reported, not refused.
- `settings.json` is reformatted with `indent=2` and `ensure_ascii=False`.
- The repo's `plugin.json` is read before the installed one.
- Unmatched keys are inserted before the first table, even between a table's doc comment and its header.

## Not checked
I ran no tests. I did not measure the quadratic cost of `_value_end` on a 1 MB file full of 1000-line arrays, and I did not read the `mods` TypeScript beyond the motion lines.

**Noticed:**
- `fm settings` has no test for concurrent writes, wrong-type values such as `theme = []`, or mixed line endings.
- `plugin.json` options and the checkout manifest can drift from an older installed foreman-ui. A stored `reduced` is then dropped by Claude Code and the pane silently falls back to `full`.
