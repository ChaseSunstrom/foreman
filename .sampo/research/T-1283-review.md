**Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code, not from a reproduction.

## lens: adversary
- HIGH — plugin/lib/fmcodetui.py:1245 — `d` runs bare `git diff HEAD` / `git show` in the repo. `fmcode._git` (fmcode.py:749-752) exists to switch off `core.fsmonitor` and hooks because a worker can plant config in `.git/config`. Here a planted `core.fsmonitor=<cmd>`, or `diff.external` plus a `.gitattributes` entry, runs as the user the moment they press `d`. Fix: reuse `fmcode._git(root, "diff", "HEAD")`. — confidence: medium. A worker's ability to write `.git/config` is plausible but not shown.
  - category: guard-bypass; scenario: a worker writes `[core] fsmonitor=touch /tmp/x`, then the user presses `d`, and the command runs outside the guard.
- MEDIUM — plugin/lib/fmcodetui.py:1570 — `--plain` prints `entry_text()` of model words (`say`), action targets, revert file names and child stderr with no control-character filter. The curses path filters through `isprintable` (line 520), so only `--plain` is exposed. A repo file named `a\x1b]52;c;…` or a prompt-injected `say` text lands as raw escape sequences in the terminal. Fix: strip `\x00-\x1f\x7f-\x9f` from each entry in `entry_text` or `run_plain`. — confidence: high.

## lens: edge
- MEDIUM — plugin/lib/fmcodetui.py:389 — `_on_start` calls `self.__init__()`. `fm code --resume` emits `start` (fmcode.py:989) but never re-emits `plan` (it is only emitted at :991-995). After `r`, the track, checks and steps are blank. Replaying a history file that contains a resumed run shows the same. Fix: when `e.get("resume")` is true, keep the state, or emit `plan` after `resume`. — confidence: high.
- MEDIUM — plugin/lib/fmcodetui.py:1633 — `get_wch()` returns a `str` for control keys (`'\x12'`), so the `keyname()` mapping is never reached. Bindings from `parse_key("ctrl+r")` (`"^R"`, line 1408) therefore never fire. Fix: map one-character control strings other than `\t`, `\n`, `\r`, `\x1b` and `\b` to `"^"+chr(ord(k)+64)`. — confidence: high.
- MEDIUM — plugin/lib/fmcodetui.py:1686 — there is no `try/finally` around `curses.wrapper`. Ctrl-C, a traceback or SIGHUP kills the TUI while the child runs on in its own session (`start_new_session=True`, line 1268). The child then hits a closed stdout and dies mid-edit. Fix: call `app.stop()` in a `finally`, and handle SIGHUP. — confidence: high.
- MEDIUM — plugin/lib/fmcode.py:213 — `_numstat` reads every dirty or untracked file whole after every step, for every `fm code` run, not just the TUI. `-uall` includes the user's own large untracked files, and there is no size cap and no `try`. Fix: stream the line count with a size cap and wrap it in `try/except`. — confidence: high.
- LOW — fmcode.py:206 — `git diff --numstat` quotes non-ASCII paths, while `_dirty` uses `-z`, so a file like `café.py` appears twice in the Changed panel. Fix: pass `-z`.
- LOW — fmcodetui.py:1313 — `history()` parses every `.events.jsonl` in full on the UI thread when `h` is pressed. Fix: read only the first line and the tail.

## lens: intent
- MEDIUM — fmcodetui.py:1245 — the diff view is not per step, though the request asks for one. `State.files` is kept per step but unused by `show_diff`. `git diff HEAD` also omits untracked files, so a run that only adds files shows "no changes". Fix: build the diff per step from `state.files`, and use `git diff --no-index /dev/null F` for untracked files. — confidence: high.
- MEDIUM — fmcodetui.py:393 — `--plain` does not print the same stations. `_on_plan`, `task` and the baseline `before` verify runs never reach `state.log`, and a guard refusal's reason (`detail`) is dropped. The criterion says "prints the same stations". Fix: add log entries for `plan` and `task`, and print the refusal reason.
- LOW — fmcodetui.py:1659 — any one bad `tui.toml` line returns exit 2 and refuses to launch, even with `--plain`. The `load_config` docstring says "the rest apply". An extension that fails to load while the layout names its panel does the same. Fix: warn and continue, and keep exit 2 for `--print-config` only.
- LOW — fmcodetui.py:1671 — `main` ignores global `-p`, `--resume` and `--dry-plan`, and the child always runs in the current directory.

## lens: maintainer
- MEDIUM — fmcodetui.py:526 — `_draw` (line 861) catches only exceptions raised by an extension panel. A panel that returns strings, which is an easy mistake, makes `Canvas.line` raise inside `_panel` and crash the whole screen. Fix: validate the returned lines inside `_draw`'s `try`. — confidence: high.
- MEDIUM — plugin/tests/test_code_tui.py:1871 — no test presses `s` or `r`, and none covers resume. The criterion says "stop and resume work from keys", and that is where the resume bug sits.

## Acceptance criteria
- Criterion 1 (stations live): met on the state and render side.
- Criterion 2 (one TOML file): met, except that `ctrl+` keys do not work in a real terminal.
- Criterion 3 (extensions): met. It loads from `$FOREMAN_HOME/tui`, not the project.
- Criterion 4: not met. The diff view is not per step, and resume loses the state.
- Criterion 5: partly met. `--plain` lacks the plan, and the other two parts are fine.

## Implicit decisions
- The config folder is `$FOREMAN_HOME`, not `XDG_CONFIG_HOME`.
- Event schema 1.
- A TOML parse error stops the launch.

## Not checked
The CHANGELOG and MASTER wording, whether `test_docs` needs an edit, and the SVG look.

Noticed: `fm code tui` can't send a request that is literally "tui". A worker that writes `.git/config` is a gap in `fm code`'s own guard, separate from the TUI.
