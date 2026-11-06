**Verdict: changes needed.** The runner test is sound. Key capture can lock the user out of list navigation, and two other findings are real but narrower.

## lens: adversary
- MEDIUM — plugin/lib/fmcodetui.py:2061 — Capture refuses only `q`, Esc, `^C`, `?`, `z` and the `settings` key. Enter (`\n`/`KEY_ENTER`), `KEY_UP`/`KEY_DOWN`, `j`/`k`, `KEY_PPAGE`/`KEY_NPAGE` and Tab can all be overwritten. Outside typing, the settings list (1924-1926), home and project lists (1819-1830), the views (1644-1652) and the runners list (2145) all navigate by `cfg["keys"]`, not by hard-coded keys.
  - Trigger: `b` on `keys.d`, then Enter, which is the natural "confirm" key. Enter now runs `diff`. The list can no longer open an editor, home can't open a project, and runners can't test.
  - Trigger: binding Up, Down, `j` and `k` away leaves the list unscrollable. The only way out is `/` plus an arrow (hard-coded only while typing) or `fm settings undo` from a shell.
  - Fix: add those keys to the refusal, or refuse when the key is the last one bound to up, down or expand. Alternatively make `_settings_key` honour `KEY_UP`, `KEY_DOWN`, `KEY_PPAGE`, `KEY_NPAGE` and Enter unconditionally, as its typing branch already does. — high
- LOW — plugin/lib/fmcodetui.py:1303 — `RESERVED` is a static literal. Only `settings` is checked against the live config. If the user moved hush or help to another key, `b` can overwrite that key. Fix: check `cfg["keys"].get(k)` against the commands `hush`, `help`, `quit`. — medium
- Cleared: Ctrl-[ arrives as `\x1b` and cancels. Case is distinct (`Q` is not `q`). F1-F12 map to `f1`-`f12`, and `KEY_DC` and `F13+` are refused. Pastes are refused. Names like `.` are written quoted and placed.
- Cleared: `test_runner` (fmcode.py:38-58) refuses any name not in `all_runners()` with a `work` command, so shell metacharacters or a path never run.
- Cleared: it runs only `shlex.join([argv[0], "--version"])`, so args and flags in the template are dropped. `all_runners` still raises on dangerous flags unless acked. Nothing is auto-approved. Canvas also blanks non-printable characters in names and CLI output.

## lens: edge
- MEDIUM — plugin/lib/fmcodetui.py:2313 (`_runner_test`) with fmcode.py:939 — Quitting mid-test leaves the CLI running. The test runs in a daemon thread, and `run_bounded` starts the child with `start_new_session=True`. It is killed only in that thread's `finally`.
  - Trigger: `r`, Enter, Esc, Esc, `q` within 10 s, with a runner whose first word ignores `--version` and keeps running. `run_screen`'s `app.stop()` knows nothing of this thread. SIGHUP and SIGTERM do the same.
  - Fix: keep the pid, or the thread, on the app and kill its process group in `App.stop()`. Alternatively run the test with `reap=True` and join it on exit. — high
- MEDIUM — plugin/lib/fmsettings.py:535-537 and plugin/lib/fmcodetui.py:2110-2113 — `set_keys` is atomic only for history. There are two separate `set_app` writes.
  - A refusal of the first pair is swallowed by `_set_key` (552-554) and the loop goes on, so `layout.heights` can be written without `layout.columns`.
  - An exception on the second write, such as `LockTimeout` or an `OSError`, leaves new columns with old heights on disk. The TUI then sets `done=[]` and skips `_settings_reload`. It says "not written" while the screen shows the old layout.
  - Fix: stop at the first refusal. Better, add a multi-key `set_app` that chains `_plan_app` texts and does one `write_atomic`. On an exception, still reload. — medium
- Cleared: a move can't empty a column (2249-2252 guard). Columns and heights stay non-empty and the right shape, so `_layout_error` accepts them. `widths` is unchanged.

## lens: maintainer
- LOW — plugin/tests/test_code_tui.py:408-428 — The refusal test covers no navigation key (Enter, arrows, Tab) and no failure between the two layout writes. Add both.
- LOW — plugin/lib/fmcli.py:5917 — The `key` help text still doesn't mention that `list` takes a group.

## Acceptance criteria
- A captured key binds and persists: met (test at 392-406).
- A panel moved by keys changes layout: met (430-454).
- A runner test reports its result: met (466-486).
- I did not run the command.

## Implicit decisions
- `--version` on `argv[0]` stands in for a runner test.
- An overwritten binding is replaced silently, with a note.
- A move writes explicit heights.
- Arrows and Enter are bindable.

## Not checked
Screenshots, the narrow layout view, and running the tests.

**Noticed:** a layout move has no visible effect below `narrow_below` (80 columns), because the screen behind uses the narrow layout. `set_note` also stays stale after leaving the layout editor.
