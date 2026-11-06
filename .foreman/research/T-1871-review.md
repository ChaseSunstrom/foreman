**Verdict:** approve with nits. Nothing here blocks the acceptance criteria, but the undo paths have two small robustness gaps. I read the diff and the surrounding code and did not run `python3 plugin/tests/run.py test_inbox_more`, so none of this is confirmed by a test run.

## lens: intent
- No findings. u in the TTY loop and in the app, the Undo button on the served page, "N left" on cards and the one-line empty deck are all there. `BASE_STYLE` is now shared by both served pages.

## lens: edge
- MEDIUM — plugin/lib/fmcodetui.py:3004-3008 — After `u`, the app rereads the whole deferred pile. A card answered with space (keep) was deleted from the view at :3021 but is still deferred, so every kept card reappears. Reproducer: keep A, keep B, press `u`. The list shows A again, though the user passed on it. Fix: reinsert only the undone card at its old index, or filter out ids kept in this view. — confidence high
- LOW — plugin/lib/fmeco.py:397,456 and plugin/lib/fmcodetui.py:3004 — `swipe_undo` pops the entry first and catches only `UsageError`. `mutate` can raise `fmcore.LockTimeout` (fmcore.py:898), which is a plain `Exception`. In the TTY loop that gives a traceback mid-sweep and loses `said`. In the app, the apply branch catches `Exception` ("a busy lock", :3013) but the undo branch does not. The popped entry is lost either way. Fix: catch `Exception` in `swipe_undo` and push the entry back on a non-`UsageError` failure. — confidence medium
- LOW — plugin/lib/fmeco.py:523-525 — A reload that re-posts a skip pushes a second `(tid, "skip", None)`. The keep path at :519 guards against this ("kept once"), but skip does not. Undo then needs two presses for one skip, and the second is a no-op that still says "back in the deck". Fix: `if tid in seen: return True, f"{tid} skipped"` before the append. — confidence medium
- LOW — plugin/lib/fmeco.py:409-414, 459 — Undoing a keep does nothing to the brief, but it prints "back in the deck" and the TTY loop adds "T-… undone" to `said`. The earlier "swept: kept" log line stays, and a second keep logs another one. Fix: have the TTY branch skip the `said` entry for "keep" (`not in ("skip", "keep")`), and say "card shown again" rather than "back in the deck". — confidence medium

## lens: maintainer
- LOW — plugin/lib/fmeco.py:464-467 — The `swipe_loop` branch does too much in one place. A conditional expression chooses between `swipe_apply` and `undo.append(...)`. `print(got[0]) if got else None` is an expression used as a statement. Fix: split it into an `if k == "s":` branch and a normal branch. — confidence high
- LOW — plugin/lib/fmeco.py:456 and plugin/lib/fmcodetui.py:3004 — Both callers pass a throwaway `set()` as `seen` just to satisfy `swipe_undo`'s signature. Fix: make `seen=None` optional. — confidence high
- LOW — plugin/lib/fmeco.py:437 vs plugin/lib/fmcodetui.py:1974 — The key-help string is repeated in two places, which is the same class of duplication T-1858 already got a nit for. — confidence low

## Acceptance criteria
- u and the undo button take back the last answer: met. TTY at fmeco.py:454, app at fmcodetui.py:3002, page at fmeco.py:503 and :516. The tests cover each, including a changed item and a dropped batch.
- Cards-left is shown: met. TTY at :444, page at :498, and the app via its list view.
- An empty deck ends in one line: met for the TTY (`test_an_empty_deck_ends_with_one_line`). The served page keeps its existing "Nothing left to sort" paragraph.
- Served pages share `BASE_STYLE`: met. The settings page ends `STYLE` with it (fmsettingsserve.py:302) and the swipe page appends it (fmeco.py:491).

## Implicit decisions
- Undo history lives in memory per session, per page server and per app view. It is not a persisted journal.
- A skip counts as an answer that can be undone.
- Undoing a revive or drop goes back to `deferred` and restores `revisit`.
- Undo needs the status to be unchanged and refuses batches.
- The page's undo form names the id it takes back, so a stale re-post gets 422.
- `:root{color-scheme:light dark}` replaces the hard-coded body colours, so both pages follow the system dark mode.
- `swipe_loop` returns `None` for an empty deck, where it used to return a list.

## Not checked
- Rendering of the served page and the app in a browser or terminal (no screenshots were listed), including the dark-mode contrast of `.why` and `.bad`.
- Concurrency of the served handler. I assumed it is single-threaded.
- The pre-audit "large file" and "usually changes with fmcli.py or test_code_tui.py" items. I found nothing in `fmcli.py` that needs an edit. `test_inbox_more.py` covers the app change.

**Noticed:** none
