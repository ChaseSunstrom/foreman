**Verdict: approve with nits.** `note_flakes` can't change the exit code or hide a failure. The findings are a regex false-name problem, one missed flake path, and a few low-severity gaps. I read the code only; no Bash was available, so nothing was executed.

**Findings**

1. MEDIUM — `~/.claude/foreman/plugin/lib/fmcore.py:104`. `^ERROR: \S+ \(([\w.]+)\)` matches ordinary log lines.
   - **Trigger:** `ERROR: timeout (30)` records test "30". `ERROR: failed (retrying)` records "retrying".
   - **Effect:** if the gate later passes on the same tree, fm check reports "flaky: 30". The count then grows in `flakes.json`.
   - **Fix:** require a dotted or `test`-looking name inside the parens, for example `\(([A-Za-z_][\w]*(?:\.[\w]+)+)\)`. Also require `test_`/`Test` for the `FAIL:` form, or only trust the ERROR/FAIL forms when the output contains unittest's `Ran N tests`.
   - **Confidence:** high.

2. MEDIUM — `~/.claude/foreman/plugin/lib/fmcli.py:1465-1470` with `fmcore.py:135`. The common flake path is not recorded.
   - The in-run rerun overwrites `code` and `output` with the passing rerun (`code, output = 0, output2`). `note_flakes` then sees a pass and has no pending entry, so the failing test names from the first run are lost.
   - A test that fails and passes within one `fm check` is never listed in the flake ledger. Only the pre-existing note "flaky: failed, then passed on a rerun" appears, with no test names.
   - **Fix:** keep the first run's output (for example `first_out`) and feed `failing_tests(first_out)` to the ledger as flaky immediately when the rerun passes.
   - **Confidence:** high. The acceptance criteria only cover the cross-run case, so this is an intent gap rather than a violation.

3. LOW — `fmcore.py:143`. A corrupt entry in `flaky` permanently disables the ledger.
   - `kv[1].get` raises `AttributeError` on a non-dict value once the ledger holds more than 500 entries.
   - Line 138 tolerates non-dicts, but the sort does not.
   - `cmd_check` swallows the exception, so no flake line is ever written again, silently.
   - **Fix:** use `str((kv[1] or {}).get("last", "")) if isinstance(kv[1], dict) else ""`.
   - **Confidence:** medium. It needs a hand-edited or damaged file.

4. LOW — `fmcore.py:133`. `pending` is never pruned.
   - It is keyed by command, so growth is bounded by the number of distinct commands ever configured, with at most 200 names each.
   - Removed checks leave stale entries forever. `flaky` is capped at 500.
   - **Fix:** drop `pending` keys that are not in the current `checks`.

5. LOW — `fmcli.py:1898` and `:1903`. The flag suggestion can name a flag that is invalid for the failing command.
   - Unrecognized-argument errors are raised by the top-level parser, because subparsers use `parse_known_args`. The candidate set is therefore every flag of every command.
   - Example: `fm check --evidance` can resolve to another command's flag if that flag scores higher.
   - Subparser errors (for example a missing argument) use only that subparser's flags. A parent-level flag such as `-p` in `fm -p x task new …` counts as "unknown" and can yield a spurious "did you mean".
   - `difflib` ties over a `set` are nondeterministic, because string hashing is randomized per process (`PYTHONHASHSEED`).
   - **Fix:** use `sorted(flags)`.
   - **Confidence:** medium. I did not run the ratio cases.

6. LOW — `fmcli.py:1884` and `:1898`. `_ARGV` is module state.
   - It is stale or empty when `parse_args` runs outside `main()`. The test at `plugin/tests/test_gate_friction.py:194` covers only the subcommand-choice path.
   - A stale `_ARGV` from an earlier in-process `main()` call can add a wrong flag suggestion.

**Checked and found sound**
- **Exit code and lock timeouts:** `return 1 if failed else 0` is untouched, so `note_flakes` cannot change the exit code or hide a failure. `LockTimeout` subclasses `Exception` (`fmcore.py:35`), so the `except Exception` at `fmcli.py:1492` catches it. The worst case is a 5-second wait and no ledger update.
- **Cached and skipped gates:** they are excluded from `note_flakes`. `tree=None` cannot match, because of the `tree and` guard at line 136.
- **Regex on real outputs:**
  - unittest `FAIL: test (mod.Class.test)`, including trailing `(i=1)` subtest suffixes: matches.
  - pytest `FAILED t.py::t - msg`: matches.
  - Go `--- FAIL: TestX`: matches. Indented subtests are skipped, but the parent is captured.
  - cargo `test a::b ... FAILED`: matches.
  - pytest ids containing spaces are truncated at the first space, but consistently.
- **`_Parser.error` inputs:**
  - empty argv: `main()` substitutes `["help"]`, so there is no error.
  - `-` and `--`: skipped by the `--?[A-Za-z]` regex.
  - unicode: no crash.
  - exit status: it ends in `super().error`, which exits 2. I found no path where the new code raises first.

**Acceptance criteria**
- T-0272 cross-run fail then pass on the same tree, with the failing run still failing: **met.** Evidence is `fmcore.py:133-141` and test `test_gate_friction.py:172`. The "known flaky later failure says so" part is met at `fmcore.py:131`. I did not run the tests.
- T-0273 nearest subcommand or flag: **met** by code reading (`fmcli.py:1894-1903`, test at line 202). Not run.

**Not checked:** running the tests, the CHANGELOG and MASTER wording, and the ratio scores of specific typos.
