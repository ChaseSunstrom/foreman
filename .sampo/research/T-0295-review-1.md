## maintainer: changes needed (no HIGH findings)

**MEDIUM — `~/.claude/foreman/MASTER.md:10`.** It says "the bench judge and soak ... run through `fmideas.run_child`". Nothing in `plugin/lib` calls `run_child` for them. The only callers are `fmevolve.py:82`, `fmsecond.py:42` and `fmideas.py:313`. `fmbench.py` doesn't import `fmideas` for running children. It uses it only for `taste` (`fmbench.py:276` and `:425`), and its replay runs through its own `Popen` at `fmbench.py:250`. This is wrong docs, or a runner the request named that was never converted. Fix: reword the sentence to the real callers, or convert the judge and soak.

**MEDIUM — `~/.claude/foreman/plugin/lib/fmideas.py:92` and `:120`.** Error text changed in two ways.
- Before, the ideas lens error was the tail: `(err or out).strip()[-200:]`. Now it is `c.fit(...)`, which keeps the head (`fmcore.py:1578-1580`). Claude's real error is usually at the end of stderr, so a failed lens now shows the first 200 characters of a long stderr.
- `c.fit` does not join lines, so the multi-line text goes into the `FAILED:` line of the lens file. Fix: keep the tail for these errors, or use `c.plain(...)` and take the tail.

**LOW — `fmideas.py:311-314`.** Error messages now repeat themselves and no longer match what they did.
- The oracle's budget refusal used to read `budget: ...`. It now reads `the oracle: budget: ...`.
- Its start failure reads `the oracle: the oracle child didn't run: ...`.
- The ideas start failure was `can't start the brainstorm children: X`. It is now `the brainstorm children: can't start claude: X`.

No test or caller matches these strings (I grepped the tests, `fmcli.py` and `fmnight.py`). Fix: pass `str(e)` straight through, or drop the prefix.

**LOW — `fmideas.py:119` and `:124`.** The research timeout ledger detail changed from `timed out: cost unknown` to `(timed out: cost unknown)`, because the empty detail is stripped. Research rows also lose any detail. It is harmless, but `fm budget` or digest readers that match the old string would break. I found none.

**LOW — `~/.claude/foreman/plugin/lib/fmevolve.py:82`.** Behaviour changes with no test.
- The mutation child now runs in a scratch folder with `--setting-sources project,local`. It no longer loads the caller's project or local settings. This is probably intended, since the child has no tools.
- A non-zero exit used to include stderr in the message. Now the exit is reported by `run_child`, and the "no revised file" message shows only the text.
- A budget error is now `ValueError` through `run_child`. It was `BudgetError`, which is a subclass, so the caller at `fmevolve.py:176` still catches it.

Fix: add one evolve case to `test_clean_helpers.py` with the stub child. It should check the exit and no-`<file>` paths and that `FOREMAN_NO_BACKGROUND` is `1`.

**LOW — `~/.claude/foreman/plugin/tests/test_clean_helpers.py:57`.** The test counts stub calls and checks the environment. It never covers timeouts, the failure paths, the ledger `detail` or the feature name. Those are the behaviours this refactor could change.

## Intent, for the record
- `c.TESTISH` (`fmcore.py:1738`) is broader than the old `fmbench` pattern. `test_*` now matches any extension, so `test_data.json` in `fmbench` counts as a test. That follows from "one pattern".
- `fmmap` gains `spec/` and `__tests__/`.
- The two criteria are otherwise met for ideas, research, oracle, second and evolve.

## Not checked
I did not run the test suites. I did not review the four word-overlap rules, because MASTER.md says they were left separate on purpose. The mechanical pre-audit item that MASTER.md needs no edit is partly moot, since it was edited and only the bench claim is wrong. I did not check whether CHANGELOG.md needs an edit.
