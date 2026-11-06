**Verdict:** approve with nits. The screen cannot write a value the schema rejects, and it cannot skip the guard or lock path, except in one narrow case (the first finding). I could only read code, not run it, so findings are code-path verified, not executed.

## lens: adversary
- MEDIUM — plugin/lib/fmsettings.py:337 (reachable from fmcodetui.py:375) — A rejected value can be written when tui.toml already has the same error. `_set_app` drops errors found in the old file, and the layout error texts name no value. With `[layout] widths = [50]` already bad, `:set layout.widths [10,20,30]` is not caught: `own` is empty, `write_atomic` runs, and the note shows green "ok" while the app skips the value. The logic was there before, but the screen now exposes it and the CLI printed a warning. — Fix: compare errors by (key, value) or re-check the target key's own error against the new text, not "new minus old". — high (CONFIRMED by reading).
- LOW — plugin/lib/fmcodetui.py:1505 — A paste into the search or `:set` line is fed raw to `_settings_key`, so an ESC, DEL or backspace in it acts as a key. A paste of `x\x1bq` cancels the line, then `q` closes the screen. Enter cannot be reached, because `split()` turns newlines into spaces, so the damage is limited to screen state. The prompt's paste path drops non-printable characters (T-1316). — Fix: `"".join(c for c in " ".join(k[1].split()) if c.isprintable())`. — high.
- LOW — plugin/lib/fmcodetui.py:1767 — `tomllib.loads` is guarded only for `TOMLDecodeError`. A typed value of about 490 or more `[` characters (the line cap is 500) probably raises `RecursionError`, which no handler in the loop catches, so the screen would crash. The same unguarded call is in fmsettings.py:150. — Fix: catch `(tomllib.TOMLDecodeError, RecursionError)` or cap the length. — low, PLAUSIBLE.

The guard and lock path holds. Every write goes through `set_key`, then `set_app` or `set_plugin`. Both use `_guard_block` when `CLAUDECODE` is set and take `fmcore.lock`. Pasted text cannot submit a line.

## lens: edge
- LOW — plugin/lib/fmcodetui.py:1160–1169 — With the terminal 13 rows or fewer, `lh` is forced to 1 while the foot starts at `iy+ih-5`. The foot overwrites the only list row and the selection is invisible. At 5 rows or fewer the overlay is blank. The test only uses h=30. — Fix: when `ih < head + foot + 2`, drop the foot's about and note lines, or say "too small". — high.
- LOW — plugin/lib/fmcodetui.py:1627 — Leaving settings to home calls `show_home()`, which re-runs the project listing and resets the cursor to row 0. Returning to the project view restores it. — Fix: keep `home_items` and `home_index` as the project view does. — high.

Empty search results, wide characters in the search or value, and narrow widths behave correctly. I checked these by reading the code: `fit`, `pad`, `tail` and `_set_cols` count columns, an empty list draws "no setting matches", and `_settings_step` and Enter guard on empty.

## lens: maintainer
- MEDIUM — plugin/tests/test_code_tui.py:1960 — `test_any_width_draws_and_rows_keep_their_columns` cannot fail. The canvas clips every row to its width, so `width(line) <= w` is always true, and no column position is checked. — Fix: assert that the VALUE and DEFAULT headers sit over the row's value and default at each width.
- LOW — plugin/tests/test_code_tui.py — Missing tests:
  - empty search ("no setting matches");
  - `:set` refused by the guard path with `CLAUDECODE=1` (the setUp blanks it);
  - Esc from project mode back to project;
  - the pre-existing-error case in the first finding.
- LOW — plugin/lib/fmcodetui.py:1168–1204 — The unused `iw=None` parameter was added to four row functions only to fit the new signature. — Fix: have `_list_view` call `row(item, iw)` only for rows that take it, or leave the parameter off.

## lens: intent
Both criteria match what the code does.
- LOW — plugin/lib/fmcodetui.py:1769 — `:set motion off` with no `--surface` also writes Claude Code's settings.json. This is the same as `fm settings set`, and the note names both. Enter on a row pre-fills `--surface` when a key exists on both surfaces.

## lens: operator
- LOW — The lane commit has no CHANGELOG or MASTER.md or README line for the new `,` key and settings screen. The CHANGELOG hunk in the diff belongs to a different task.

## Acceptance criteria
- Overlay lists every setting by group, search and modified-only work, rows show value, default and badge: met, by reading `test_every_setting_is_listed…` and `test_search_narrows…`. I did not run them.
- `:set key value` writes through fm settings and the screen shows it: met. The `set_key` and `set_app` path writes in place, the config reloads, and the test checks both the file and the drawn row.

## Implicit decisions
- `,` is the key that opens the screen, hard-coded `/`, `m` and `:` inside it, and Esc or `q` closes it.
- A `:set` on a key that exists on both surfaces writes both.
- The settings screen has no task grants (`p=None`), so inside Claude Code the guard decides as it would with none.
- A skipped setting is shown as only the first problem line.

## Not checked
- I ran no tests, so I did not check the golden-frame and fuzz tests, or whether a test pins the key list that now includes `,`.
- I did not review the guard and CHANGELOG hunks for the other task.

**Noticed:** none
