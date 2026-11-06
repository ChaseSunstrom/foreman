**Verdict:** approve with nits. I read the worktree files directly, because I had no way to run `git diff`. The code behaves as the brief intends. No finding is above MEDIUM.

## lens: intent
- No findings. `_TOP_NAME` at fmhooks.py:3250 matches a column-0 `def`, `async def`, `class` or `NAME =` while excluding `==`. `redefinitions` skips `X = f(X)`, so an in-place rebinding stays silent. An edit with no column-0 name returns at fmhooks.py:3262. The three tests at test_redefinitions.py:54-57 cover these cases.

## lens: edge
- MEDIUM — plugin/lib/fmcore.py:5482 — `redefinitions` has no decorator exemption, but the note fires on any `.py` in any project the hook finds. Module-level `@overload` stubs and `@singledispatch` `@f.register def _(...)` repeat a name on purpose, so each gets one false note per session — exempt a def or class that has `decorator_list` entries, or at least `overload` and `register`. This would change the test helper's behaviour for plugin/lib too, so the exemption could instead go in `_redefinition_note`. Confidence: medium. The false positive is clear from the code; I didn't run it.
- LOW — plugin/lib/fmhooks.py:3271-3277 — `_first_time` is called inside the list comprehension for every added name. When more than five names trigger, the ones cut by `notes[:5]` are marked as told and never shown, and the cap itself says nothing — append "and N more", or mark only the first five. Confidence: high.
- LOW — plugin/lib/fmhooks.py:3259-3261 — a Write puts the whole file into `added`. Every shadow already in the file is then reported as if this edit introduced it, once per session. This is arguably fine, but the note text ("now defines") overstates it — leave it, or say "defines". Confidence: medium.
- LOW — plugin/lib/fmhooks.py:3257 — the note also runs on `.py` files outside the project, where `_onwrite` deliberately skips the syntax check (fmhooks.py:1646, T-2035) — skip when `os.path.relpath(path, p.root)` starts with `..`. Confidence: medium.
- Handled correctly:
  - **MultiEdit:** the `edits` list is read, and non-dict entries are filtered out.
  - **Unparsable files:** `SyntaxError` returns None, and `_syntax_note` has already blocked.
  - **Large files:** the 2 MB cap matches `_syntax_note`.
  - **Async and decorated defs:** both are caught.
  - **`.ipynb` and other non-`.py` files:** skipped.
  - **Missing session id:** `_first_time` returns False, so there is no note and no crash.

## lens: operator
- LOW — plugin/lib/fmhooks.py:3265-3268 — a file the edit touches is read and parsed once more, after `_syntax_note` has already compiled it. The prefilter makes this rare; on a large file with a new top-level name it adds roughly one parse (tens of ms, estimated, not measured) to a sync hook. The brief's second acceptance criterion names `test_perf_hooks`, which does not exist in the worktree. The existing `test_perf_cost.py` has no `PostToolUseValidate` timing. So the cost claim rests on reading the code, not a measurement. Confidence: high.
- `import ast` is inside `redefinitions` (fmcore.py:5478), so it only loads after the prefilter passes. fmcore.py adds no top-level import, and `_TOP_NAME` uses `c.lazy`, so it compiles on first use and the LazyPatterns rule holds. The earlier LazyPatterns failure at 19:18 was fixed by the 19:19 evidence run, which passed.

## lens: maintainer
- fmcore.py:5475-5491 matches the old helper body line for line. The only differences are the docstring and the local `import ast`.
- LOW — step 3 is ticked "docs: CHANGELOG, MASTER", but neither file mentions T-2630 in the worktree, and the plan's scope lists both. Either the docs weren't written or they live outside this lane — confirm before close.
- test_redefinitions.py:8 imports `HookCase` from `test_hooks`. Importing one test module from another is an existing pattern, but it makes this module run with `test_hooks`' setup.

## Acceptance criteria
- AC1 (shadowing edit gets a note naming both lines; rebinding and no-name edits get none): met, by the code and the tests at test_redefinitions.py:45-60. The 19:17 `test_hooks test_redefinitions test_onwrite` run (264 tests) passed. That run is the builder's logged evidence; I did not rerun it.
- AC2 (hook suites pass; cost stays inside the hook budget): partly met. `test_hooks`, `test_redefinitions` and `test_core` passed. The named `test_perf_hooks` module does not exist, and no timing was taken.

## Implicit decisions
- Annotated assignments, tuple targets and augmented assignments are ignored.
- Redefinitions inside `if` or `try` blocks at module level are ignored.
- One note per path and name per session, keyed by a sha1 prefix.
- The note is skipped when a validator-timeout note already exists.
- The note cap is 5 names.

## Not checked
I did not run any tests or measure latency. I did not look at the guard or other callers of `fmcore.redefinitions`.

**Noticed:** the verify command in T-2630's acceptance criteria names a nonexistent `test_perf_hooks` module — fix the brief or add a `PostToolUseValidate` timing test.
