**Verdict: approve with nits.** The three-part acceptance criterion is met. I could not run the tests, because I had no shell in this audit. The task as the user worded it is only about half built, so the leftover items need to be captured.

## lens: adversary
- MEDIUM — plugin/lib/fmsettings.py:~1005 (`reread`, `_read_app`), plugin/lib/fmcodetui.py (`_watch_tui`) — The watcher reads the whole file in text mode every second on the UI thread. It has no `S_ISREG` check, no size cap and no stat gate. Take `tui.toml` as a symlink to `/dev/zero` or a very large file: it reads without bound. Replace `tui.toml` with a FIFO while the app runs (`rm tui.toml; mkfifo tui.toml`): `open()` blocks and the screen freezes. Boot's `load_config` already reads without a cap, so this is not new at boot, but the loop is new. Fix: in `reread`, `os.stat` first, skip unless it is a regular file, and compare `(st_size, st_mtime_ns)` to the last seen before reading. Refuse anything over the 1 MB cap that `_plan_app` already uses. — confidence 0.6
- No finding: the last-good copy cannot smuggle a refused setting. `_keep_good` stores raw text, but `boot` loads it again through `_try` → `_load` → `T.load_config`, which applies the same schema checks. A refused key is refused again. Add a test for this, because none covers it: a `tui.toml` with `border = "nope"`, boot, then break the render, and the fallback must show the default border.
- No finding: bisect only reads `tui.toml` and loads each try from a `mkstemp` copy. Nothing in `bisect`, `_try` or `_build` writes `tui.toml`. `_keep_good` writes only the good copy, under a lock.

## lens: edge
- LOW — plugin/lib/fmsettings.py:~1012 — An unreadable `tui.toml` (permissions, bad UTF-8) makes `reread` return `None` forever, so the user is never told. Fix: say it once, as `_watch_tui` does for invalid TOML. — 0.6
- LOW — plugin/lib/fmcodetui.py:1721-1726 (the `z` motion cycle) — After its own write, `_own_write()` makes the file the "seen" text. An outside edit to another key in the last second is merged into the file but never applied to `self.cfg`, and the watcher then sees no change. It applies only after a restart. Fix: have `z` take the file through `_settings_reload`, as the other writes do. — 0.5
- LOW — plugin/lib/fmsettings.py:~1060 (`_conflict`) — When the outside edit left invalid TOML, `_flat(text)` is `{}`, so every key counts as changed. The user sees "changed in … (now unset)" instead of "isn't valid TOML". The `_conflict` refusal logic is otherwise sound: it is inside the lock, a conflict means "the same key changed", other keys merge, and the refusal triggers a re-read so the next try goes through. — 0.6

## lens: maintainer
- LOW — plugin/lib/fmsettings.py:~1092 (`_build`) — Bisect rebuilds the file from flattened values, so it does not test the file's exact text, and it renames `keys.X` aliases through `_norm`. Fine for bisecting, but the code should say so. — 0.4
- LOW — plugin/tests/test_settings_safety.py:198 — The monkey test types only a few characters and never reaches a `:set`, so it exercises the write path rarely. — 0.4

## Acceptance criteria
- Boots the last good config and says so: met (`LastKnownGood` tests, `T.main` screen test).
- An external edit merges: met (`ExternalEdit`, including conflict refusal and preview).
- `fm settings bisect` names the bad key: met (`Bisect`, the `fm` verb, `settings.md`).
- Unbuilt items: the literal criterion does not name them, but the request and title do. These are missing:
  - the scope picker (run, project, everywhere)
  - repo policy pins
  - the headless check
  - pane parity for last-good and merge
  
  Parity for bisect is met through the verb and the command. The task should not close as the whole of "Round 3". Narrow the title or capture each item as its own task.

## Implicit decisions
- The last good copy lives at `state/settings/tui.good.toml` and is saved on every drawn start, even when some settings were refused.
- The watcher polls once a second and compares text, not mtime.
- With no good copy, boot falls back to `DEFAULTS`.
- Bisect assumes a failure is monotonic along the key prefix, and its output says when a key breaks only together with the others before it.
- `--print-config` bypasses `boot`.

## Not checked
Test runs; the screen visuals (the design lens had no screenshots); deep-nesting exceptions in `changed`; whether `T._toml` handles inline tables in `_build`.

Noticed: the other Round 3 items (scope picker, repo policy pins, headless check, pane parity for last-good and merge) need their own tasks.
