**Verdict:** changes needed. This is a narrow MEDIUM fix in the hook's fallback. The shim and rename work looks sound. I read the code but did not run the tests.

## lens: correctness / fail-closed

- MEDIUM — plugin/hooks/hook:57 — `committed_library()` sets `pkg.__path__ = [os.path.join(LIB, "sampo")]`, which is the working tree. Any module not yet loaded, or absent from HEAD, resolves from the working tree. Modules load in alphabetical order, and cross-imports are top-level, so `doctor.py:16-19` imports `py`, `serve` and `setup` before they load. A broken or edited working-tree sibling defeats the fallback, or runs uncommitted code under a guard that is meant to run HEAD only. Fix: set `pkg.__path__ = []`, register every HEAD module in `sys.modules` before any `exec`, and refuse (return False) if an import falls through. Also purge stale `sampo*` entries first. Confidence: high on the code path, not run. Reproducer: copy the repo, add a syntax error to `plugin/lib/sampo/setup.py` without committing it, then run `hook PreToolUse` with a committed `core` that fails. The fallback imports the broken file.
  - Summary: Fallback library imports working-tree siblings.
  - Failure scenario: an uncommitted or broken sibling module is imported or executed, so the guard runs working-tree code or errors out.
  - Category: security / fail-closed. Verdict: confirmed by reading.
- LOW — plugin/hooks/hook:92-99 — `from sampo import agents` falls back to the working-tree `agents.py` when HEAD lacks it. Fix: treat a module missing from HEAD as a refusal.
- LOW — plugin/tests/test_hooks.py:2029-2084 — only happy paths are covered. Add tests for a module missing from HEAD, a failed `git show`, and a broken working-tree sibling.
- LOW — plugin/tests/test_rename_aliases.py:48-68 — the scanner checks only the first string argument of `lazy`, `import_module`, `__import__`, `find_spec` and `patch`. It misses f-strings, later arguments and code embedded in strings. Fix: also walk f-string parts and all arguments.
- LOW — plugin/lib/sampo/doctor.py:1470 — `missing_modules` still scans `plugin/lib/fm*.py`, which are now shims. New modules in `lib/sampo/` are never checked against MASTER.md. Fix: scan `lib/sampo/*.py`. `test_planning.py:122` expects `fmnew`, so update it too.

## lens: stale docstrings (item c)

- LOW — about 351 `fm[a-z]{3,}` mentions in 72 files, many of them legitimate `fmguard`. Stale ones include smithtui.py:2,30,3519 (`fmcode.*`), home.py:8,62 (`fmcore.*`), cli.py:1909 (`fmcli.py`), cli.py:5308 (`fmrelease.py`), doctor.py:1056 (`fmhooks._cc_version`), mcp.py:36 and recall.py:272. Fix: a sweep task (T-2768 may already cover it). They are comments only, with no runtime effect.

## Shims and string lookups (item b)

No miss found. `cli.lazy` uses `__import__` plus `sys.modules[module]`. `run.module` and rune's `reach`/`_imports` use the sampo names. `core.PLUGIN_ROOT` is correct. `hooks._committed` is correct for `fmguard` and `sampo.core`. I found no pickle use. `design.py:27` and `release.py:16` guard the `secrets` shadow.

## Acceptance criteria

- Full suite passes: not verifiable (not run).
- Old paths resolve to the same module object and `mock.patch('fmforesight.x')` works: not verifiable by running. The two-line shims and the alias test point to met.
- No fm* import or string name outside the shims: not verifiable by running. The grep is clean for imports, `lazy` and `importlib`, but the scanner gaps above remain.

## Implicit decisions

- The synthetic package keeps the working-tree `__path__`.
- The shims are kept for two releases.
- `__init__.py` is empty.
- `fmguard` is excluded from the shim set.
- `SampoTestCase` keeps `ForemanTestCase` as an alias.

## Not checked

- Most of the 224k-line diff.
- Test execution.
- The design lens and logo images.
- `install.sh`, `MASTER.md` and the bench scripts.

**Noticed:**
- test_guard_cases.py:246-253 target lists still name shimmed fm paths.
- `GUARD_FILES` names the not-yet-existing sampo/ward.py (T-2745).
- The old pre-rename hook had the same working-tree sibling exposure, because `LIB` was on `sys.path`.
