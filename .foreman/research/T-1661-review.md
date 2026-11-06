**Verdict: changes needed.** The three acceptance criteria are implemented. Pressing Enter in a served number field writes the wrong value, and `--real` has two defects: it escapes the budget, and a failed model call crashes the run. I read the code only and did not run the tests or the page.

## lens: intent
- MEDIUM — plugin/lib/fmsettingsserve.py:120-121 (button order from :354-355) — the turn buttons come before the `set` button in each form, so the default button is "−". Pressing Enter in a number field posts `turn=-1`. Repro: type 120 into `layout.narrow_below` and press Enter. It writes 100 and reports success, not 120. Fix: put the `set` button first in the DOM (or take the turn buttons out of the form and use `formaction`), and add a test that submits without naming a button — high confidence
- LOW — plugin/lib/fmsettingsserve.py:353 — `step="1"` whenever the current value is whole, even for `number` type. An ext setting with range 0..1 and value 1 gets a slider that only reaches 0 or 1, and the browser rejects typed 0.5. Fix: `step = "1" if type == "int" else "any"` — high confidence

## lens: adversary
- MEDIUM — plugin/lib/fmsettings.py:239 (call at :271) — the sandbox patches `FOREMAN_STATE` for the whole loop. In `--real`, `fmideas.run_child` runs `fmbudget.check` and `fmbudget.record` against the temp state. The real daily cap never sees this spend, and `fm cost` never shows it. Fix: restore the real `FOREMAN_STATE` and `FOREMAN_HOME` around the `run_child` call — high confidence

## lens: edge
- MEDIUM — plugin/lib/fmsettings.py:271 and :1440 — `run_child` raises `ValueError` on timeout, no output, a logged-out `claude` or a budget refusal. That is not a `SettingError`, and the `newcomer` branch has no `except ValueError` (unlike `words` at :1454). Result: a traceback, and the goals already played are lost. Fix: catch `ValueError` in the turn loop and set `step=n, missing=f"model failed: {_safe(str(e))}"` — high confidence
- LOW (PLAUSIBLE) — plugin/lib/fmsettings.py:146-147 — float rounding stalls `]`. For `number` range 0..1 at 0.3 the step is 0.05, and `0.3/0.05` should come out as 5.999999999999999. `floor` gives 5, and `6*0.05` rounds back to 0.3, so the value doesn't move. No float test exists. Fix: take `k = round(v / step, 9)` before `floor` and `ceil`, and add a float test — medium confidence
- LOW — plugin/lib/fmsettingsserve.py:128-140 and :380-389 — the move form carries only `c` and `i`, and `move()` re-reads the layout with no base check. A stale tab, or a move made in the app's editor, makes the click move a different panel. Fix: post the panel name and compare it — high confidence

## lens: operator
- Cost of `--real`: at most 3 goals × 6 turns = 18 haiku calls per run, roughly 70k input tokens. It is manual and cheap, but the budget finding above means the cap doesn't bound it.

## lens: maintainer
- LOW — plugin/tests/test_settings_room.py — no test covers Enter submission, float detents, a `run_child` failure in `--real`, or `_goals` rejecting a bad file. Fix: add one test for each.

## lens: design
- LOW (accessibility) — plugin/lib/fmsettingsserve.py:354-365 — the page has no script, so the dial shows no number as you drag it. Every turn button is labelled "down one detent" or "up one detent" without the setting name. Fix: include the key in the `aria-label` and show the value as text beside the dial.
- LOW — plugin/lib/fmsettingsserve.py:362 — `ticks-{key}` ids repeat if a key exists on both surfaces. Fix: include the surface in the id.

## Acceptance criteria
- Layout grid with ← ↑ ↓ → moves, columns and heights in one write: met. `layout_moved`, `move()` and `_grid` do it, and the tests cover it.
- Range dial with ticks, stepped number, `[` and `]` in the app: met, apart from the defects above.
- `fm settings newcomer`: met. Scripted is the default, it writes only through `write_atomic` inside the sandbox, it names the step and the missing hint, and it exits 1 when stuck. `--real` is not met on error paths.

## Implicit decisions
- Detent grid is anchored at 0, not at the range's low end.
- Detent steps are about a twentieth of the span, on a 1-2-5 ladder.
- The newcomer plays at a fixed 120×40 screen.
- Pressing any key that leaves the settings or layout screen counts as stuck.
- The default goals file lives in `plugin/evals/settings/`.

## Not checked
- I ran no tests and loaded no page in a browser.
- Whether the settings hint row clips at 80 to 120 columns. It is now about 119 cells wide.
- Whether the plugin's evals folder ships in installs.

Pre-audit: the "secret-looking value" at `test_settings_room.py:48` is `fmsettingsserve.make()` and not a secret. The large-file flags are append-only edits. `test_code_tui.py` needs no edit, because nothing references `_SET_HINTS`. The diff has no step for `fmsettingsserve.py` or `fmcodetui.py`, which the first two criteria need.

**Noticed:** the hint row in plugin/lib/fmcodetui.py:1868 grew to about 119 cells and may clip "l layout" and "Esc close" below 120 columns, which is worth a width check.
