**Verdict:** approve with nits. All four acceptance criteria are met in the code, and I found nothing HIGH. I read the diff and the surrounding code but did not run the tests.

## lens: intent
- LOW — `plugin/lib/fmeco.py:232` — `input().strip().lower()[:1]` accepts the first letter of any word. "don't know", "dunno" and "do later" all drop the item, and "k"/"r" typed as words do the same. A mistyped answer silently drops a deferred item. — Accept a verdict only when the answer is exactly one letter or the full word (`r`/`revive`, `k`/`keep`, `d`/`drop`), and re-prompt otherwise. — confidence 85%.

## lens: adversary
- No findings. A title or why from a brief goes through `c.plain` in the terminal loop (`fmeco.py:229`) and `fmcore.plain` plus `_one_line` in the app row (`fmcodetui.py:114`). The `--epsilon` error text is plain and fitted (`fmeco.py:317`). `prefer --reset` takes no path and only removes `prefer.json` inside the project directory (`fmeco.py:274`).

## lens: edge
- MEDIUM — `plugin/lib/fmeco.py:238` and `plugin/lib/fmcodetui.py:3002-3006` — Both loops work from a list read once, so another session can change an item mid-sweep.
  - Terminal: `swipe_apply` raises `UsageError` ("is not deferred") for that item. It propagates out of `swipe_loop`, which ends the sweep. The final "Swept: …" summary is lost and `said` is discarded. The loop also prints nothing after each verdict, so the user never sees what was applied.
  - App: the error is caught and shown, but the stale row stays at `item_index`, so every later press on it fails the same way.
  - Repro: defer two items, start `fm inbox swipe` in a terminal, run `fm task drop T-0001` elsewhere, then press `k` on T-0001.
  - Fix: in the loop, catch `fmcli.UsageError`, print it and continue. Echo each `swipe_apply` result as it lands. In the app, `del self.items[self.item_index]` in the `except` branch as well. — confidence 80%.
- LOW — `plugin/lib/fmeco.py:445-452` — If `prefer.json` is corrupt, `learned_weights` returns `{}`, so `n` is 0. The file is removed but the output says "There was nothing learned to forget" and no event is logged. — Count the file's presence, or say "cleared an unreadable file". — confidence 60%.

## lens: operator
- No findings. Cost is negligible: `inbox_pick` makes one extra `load_briefs` pass and one random draw per pair. Docs (CHANGELOG, MASTER, `backlog.md`) match the code. In Claude Code the Bash tool is not a TTY, so `fm inbox swipe` there still lists rather than prompting.

## lens: maintainer
- LOW — `plugin/lib/fmeco.py:216-217` — `_tty` is a new private helper. Check whether `fmcli` or `fmcore` already has an isatty helper to reuse. — confidence 40%.
- LOW — `plugin/tests/test_inbox_more.py:410-418` — No test covers a verdict that fails mid-loop (see the edge finding), and nothing asserts that the loop echoes each applied verdict. — Add a test where one item is dropped between list and apply. — confidence 70%.

## lens: design
- LOW — `plugin/lib/fmcodetui.py:2998-2999` and the `backlog` view note in `VIEWS` — The app keeps with space and moves with k. The terminal loop keeps with k (`fmeco.py:220`). The same verb has two keys in two surfaces. This follows the app's j/k list convention, so it is a trade-off, not a bug. — Say "space keep" prominently in the hint, or also accept `K`. — confidence 50%.
- Not verified: the status-bar message that shows each verdict is drawn at `fmcodetui.py:1261`. I did not confirm it is visible while the overlay is open.

## Acceptance criteria
- App backlog view and `PLUGIN_ROUTES["backlog"]`: met. `I` is bound to `backlog` (`fmcodetui.py:106`), `_backlog_key` applies each verdict at once, and the parity entry is added.
- Terminal `swipe`: met. `_tty()` and not `--json` runs `swipe_loop` (`fmeco.py:300`). `--apply` and pipes behave as before.
- `pick` skips blocked items and uses `--epsilon` (default 0.1): met (`fmeco.py:248-259`, validation at `:312-317`).
- `prefer --reset` and `/foreman:backlog reset`: met. The flag is restricted to `prefer`, and `backlog.md` has step 5.

## Implicit decisions
- Any item that depends on a not-closed item, including a deferred one, is hidden from `pick`.
- `pick` uses the global `random` module by default, so its output is nondeterministic unless `--epsilon 0`.
- `prefer --reset` asks for no confirmation and logs a `prefer_reset` event only when something was forgotten.
- The app key `I` is uppercase, and Esc or `q` closes the backlog view.
- `epsilon` is validated as a string-to-float with `nan` and `inf` rejected.

## Not checked
Rendered appearance (no screenshots). Whether other modes rebind `d`, `r` or space ahead of `_backlog_key`. I did not run the test suite.

**Noticed:** `swipe_apply` raises `UsageError` for stale items. A `--apply` batch aborts all-or-nothing, which is fine. Interactive callers now need per-item handling (see the edge finding).
