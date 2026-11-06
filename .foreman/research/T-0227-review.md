## intent: changes needed

- **HIGH, missing: the UI half of the request is not built.**
  - The request's second DONE-WHEN asks that `fm ui --json` carry the new sections, that the mod render them, and that a shot.py capture shows them.
  - `plugin/lib/fmwatch.py` has no budget or spend reference, and git status shows no `mods/` changes.
  - The task's two acceptance criteria cover only CLI and hook behaviour, so they don't capture this half.
  - Fix: add the sections to fmwatch, render them in `register.tsx`, and add a mod test and a shot. Or log explicitly that this is deferred and capture a task for it.
- **MEDIUM: "tied to economy mode" is a re-implementation, not a tie.**
  - `plugin/lib/fmbudget.py:75-92` has its own 80% weekly and 90% five-hour thresholds. No Python code references economy mode (grep for "economy" in `plugin/lib` finds only fmbudget's comments).
  - The thresholds can drift from the mod's economy rule (T-0198).
  - Fix: share one threshold, or state in the docs that they are deliberately separate.
- **MEDIUM: the per-command cap is not per command for `fm evolve`.**
  - `fmbench.py:301` checks inside `run_arm`, which `fmevolve.py:127-129` calls twice, and `fmevolve.py:64` checks the mutation separately.
  - One `fm evolve` can therefore spend about 3x the `run` cap. Each check passes on its own estimate.
  - Fix: do one combined check in `generation` before the mutation.

## adversary: changes needed

- **MEDIUM: `--day nan` disables the budget silently.**
  - argparse `type=float` accepts `nan` (`fmcli.py:1992-1993`).
  - At `fmbudget.py:162`, `nan > cur[k]` is False. So `up` is empty, no `--because` is required, and no costly decision is recorded.
  - `set_caps` then writes `NaN` to budget.json, and it loads back as a float. Every comparison in `check` (`est > nan`, `usd+est > nan`) is False, so nothing is ever refused.
  - This sidesteps the "raising a cap records a costly decision" requirement.
  - Fix: reject non-finite or negative values in `cmd_budget` with `math.isfinite`, and treat them as raises.
- **LOW: the subagent cap is checked only at launch.** Parallel Agent launches all pass the check. `fmbudget.py:117-123` and `fmhooks.py:686-695` check once with no reservation. This is acceptable given the intent, but worth documenting.

## edge: changes needed

- **MEDIUM: a corrupt `budget.json` crashes the CLI.**
  - `fmbudget.py:32` calls `type(v)(data.get(k, v))`.
  - `{"day": null}` raises TypeError, and a list as the file content raises AttributeError. Neither is caught by `except (OSError, ValueError)`, and the second only protects the file read.
  - Callers catch only `BudgetError`, so `fm ideas`, `fm bench` and `fm budget` die with a traceback. The hook path is safe because `fmhooks.py:693` catches `Exception`.
  - Fix: wrap the coercion in try/except and fall back to `DEFAULTS`.
- **LOW: paid runs that time out are not recorded.**
  - `fmideas.py:143` and `fmresearch.py:181` kill on `TimeoutExpired` without calling `record`.
  - `fmbench.py:230` records `None` USD on a timeout.
  - The day's spend is undercounted, which fails open.
  - Fix: record the run with a nominal estimate, or at least count it in `runs`.
- **LOW: unreadable cost output makes `check` fail open.**
  - `result()` returns `usd=None` for plain output, and `estimate` skips rows with no cost.
  - Fix: a note in `fm budget` that such runs have unknown cost.
- **LOW: `subagent_stop` has no local guard.**
  - `fmhooks.py:1476-1479` calls `record` (a file write) with no try/except. A write failure aborts the rest of the handler, including the `subagent` log event.
  - Fix: wrap the budget block in try/except.

## Not checked

- `plugin/tests/test_budget.py`.
- `plugin/tests/helpers.py`. The pre-audit item says it needs no edit alongside `fmcore.py`, and the diff does not appear to touch `fmcore.py`.
- Whether the dispatcher already catches exceptions from `subagent_stop`.
- Whether the guard protects `state/budget.json` and `state/spend.jsonl` from agent writes.
