[instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
Changes needed. The guard change widens what the old rule blocked, and the outgrowth hint has a per-call cost.

## Findings

**HIGH (guard) — `plugin/lib/fmguard.py:1397-1398`.** `stash list/show` is exempted without looking at the remaining args. Before this change every `stash` form returned the checkout base (`.` or `-C` dir), so any command in a protected tree was blocked. Nothing else in the guard covers these three cases:
- **`--output=FILE`.** `git stash show -p --output=plugin/lib/fmguard.py` and `git stash list --output=X` pass. `--output` is a git diff option that `stash show` and `stash list` accept, and it writes the file. I did not run git. This is from git's documented behavior, so confidence is medium-high.
  - `_write_targets` has no `--output` handling for git. Its only `--output` handling is for curl, at line 1409.
  - The redirect check only sees `>`, via `c.redirs`. So `stash show -p > file` is still caught, but `--output` is not.
- **Code through config or env.** `git --paginate -c core.pager='sh -c "..."' stash list` runs the pager command. So does `git -c diff.external=CMD stash show -p --ext-diff`. Likewise `GIT_EXTERNAL_DIFF=CMD git stash show -p` and `GIT_PAGER=CMD git -p stash list`. A grep for `core.pager`, `ext-diff`, `GIT_PAGER` and `GIT_EXTERNAL_DIFF` in `fmguard.py` finds nothing. The only config check is `core.hookspath` in the env, at line 1284.
- **Where `-c` is skipped.** Line 1393 skips the `-c` value without inspecting it. `_check_git` at line 1497 does the same.

Fix: treat the exemption as true only when every arg after `list`/`show` is a plain ref or a short whitelist of flags (`-p`, `--stat`, `--name-only`, `-u`, `stash@{N}`). Return the base target if any arg starts with `--output` or `--ext-diff`, or if any `-c`/`--paginate`/`-p` global option or a `GIT_PAGER`/`GIT_EXTERNAL_DIFF` env assignment is present. Add table rows to `test_pass1.Stash` for `--output=` and `-c core.pager=`.

**MEDIUM (cost) — `plugin/lib/fmcore.py:1868-1869`, `2120-2127`.** The hint calls `task_touches` on every `next_for` call for any executing S task. That function reads and JSON-parses up to `TASK_WINDOW = 50000` ledger events.
- The comment at line 2120 says this window is meant for "a fm command, not a hook: it can afford it".
- The code (unchanged by this diff) sends `next_for` to `session_context`, and the Next line is injected every UserPromptSubmit.
- Result: a large ledger gets a multi-MB tail read and parse on every prompt.

Fix: pass a small window (for example 2000 events), or cache the touched count in the brief.

**MEDIUM (false positives) — `plugin/lib/fmcore.py:1869`.** `TESTISH` only excludes tests. Docs and data count as source, so an S task that edits one source file plus `CHANGELOG.md`, `MASTER.md` and a README gets the "outgrown S" nudge. This task's own diff touches both docs files. Nothing caps the repetition, and the "Next hint ignored" counter can only quiet a hint that is in `HINT_MARKS`. Fix: also exclude docs (`\.md$`, `docs/`), or count only `_CODE` files. `fmmap` already has `_CODE`.

**LOW — `plugin/lib/fmcore.py:1869`.** `task_touches` is not wrapped in try/except. A corrupt ledger line, or an unexpected `at` value, would raise inside `next_for` and blank SessionStart context. This is the same class as the earlier operator finding.

## fmideas.child_prompt
Fine. The closing instruction ("Return 8-12 ideas … wild") is unchanged and still last, so the output format holds. Only the order of the pack and the lens changed. The format spec lives in the system prompt (`child_cmd`), not in this string.
- The `test_ideas` mocks parse `Lens:` as a line prefix (lines 13-15, 156). They would pick up a stray `Lens:` line in the pack first. The pack has none today, so this is not a failure.
- `later_round_pack` keeps the original pack as a prefix, and the Prefix test asserts it.

## Acceptance criteria
- **T-0265 (stash list/show pass, other stash forms block):** met for plain forms, per the table in `test_pass1.py`. It is not met for the threat model: `--output=`, pager and external-diff variants now pass.
- **T-0266 (outgrown hint at 3 or more non-test files):** met per the Outgrown test, with the false-positive and cost caveats above.
- **T-0267 (shared pack prefix):** met per the Prefix test.

## Not checked
I did not run the tests or git. I did not verify whether `stash show` honors `core.fsmonitor`. I did not review the `fmmap` TESTISH move beyond the diff.
