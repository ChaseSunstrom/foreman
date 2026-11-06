## Verdict
Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I read the code but did not run any of it.

## Findings

1. **HIGH — `plugin/lib/fmcli.py:594-598`, `:589-593`: passing evidence without proof.** The evidence is written as `"exit 0 · …"` with `inconclusive=bool(unproven)`. That flag only looks at `unproven`. Three cases give `exit 0` and `ran=True` with no hunk actually shown to matter:
   - Every hunk is skipped, because `git apply -R` fails at `:576`. Then `tested == 0`, the summary is `0/0 hunks proven`, and the line still reads `exit 0`.
   - `--max` truncates the run. The summary says "N more not run", but the evidence is still a pass.
   - Some hunks are skipped. These are never listed as unproven.

   Fix: mark the evidence inconclusive when `skipped` is non-empty, when `len(hunks) > len(shown)`, or when `tested == 0`. Return 1 in those cases too.

2. **HIGH — `fmcli.py:580-583`: no baseline run, so a broken check proves everything.** `args.run` is never run on the unmodified worktree. The scratch worktree comes from `commit-tree`, so it holds only tracked and untracked-non-ignored files. Ignored dependencies (`.venv`, `node_modules`, a built artifact) are missing from it. If CMD fails there for that reason, or fails always, every hunk gets a non-zero code and counts as "proven" (`:583`). A timeout (`run_command` returns 124) is also counted as a kill. The result is passing evidence from a check that never passed.
   - Fix: run `args.run` once in the clean `wt` before the loop. If the exit code is non-zero, raise `UsageError`.

3. **MEDIUM — `fmcli.py:532`: trailing tab for paths with spaces.** Git ends the `+++`/`---` line with `\t` when the name contains a space. `(.+)$` captures it, so `f` becomes `"a b.py\t"`. Then:
   - `c._git(wt, "checkout", "-q", "--", f)` at `:581` fails silently, because `_git` returns `""` on error.
   - The hunk stays reverted, so later hunks of the same file are applied on top of it. They either fail and are skipped, or run against a mutated file.
   - Fix: use `(.+?)\t?$` and strip the tab. Also check the `checkout` result and abort or skip when it fails.

4. **MEDIUM — `fmcli.py:581`: deleted files are never restored.** For a deleted file, `-R` recreates it. The scratch tree does not track it, so `git checkout -- f` fails silently. The file then stays for every later hunk and can change their results. Fix: for files that are absent in `commit`, remove the file instead of checking it out. Alternatively, run `git -C wt reset --hard -q` or `git -C wt checkout -f commit -- .` after each hunk, plus `clean -fdq`.

5. **LOW — `fmcli.py:569-571`: a failed `commit-tree` is not reported clearly.**
   - An empty `commit` makes `worktree add` fail, so `isdir(wt)` is false and a `UsageError` is raised. That is safe. But the `not commit` test sits after the call, and the message blames `worktree add`.
   - `commit.gpgsign=true` makes `commit-tree` sign, which can fail and give an empty string. Fix: check `commit` right after `:559` and pass `--no-gpg-sign`.

6. **LOW — `fmcli.py:553`: file names are passed as globs.** `-- *files` is not literal, so a name like `[x].py` can match the wrong paths or none. Use `--literal-pathspecs`, as `:503` does.

## Checked and fine
- **Non-ASCII names:** `c._git` passes `core.quotePath=false` (`fmcore.py:2098`), so `+++ b/é.py` matches at `:532`.
- **Deleted file with `+++ /dev/null`:** the `--- a/` fallback at `:532` handles it.
- **Binary and mode-only changes:** there is no `@@`, so `body` is empty and the block is dropped silently at `:533`. They are never counted, but also never reported.
- **`\ No newline` lines:** they stay inside their hunk, and `:585` ignores them.
- **Wrong-file application:** `git apply` reads the `---`/`+++` lines, so a hunk cannot land on another file.
- **User's index and tree:**
  - `worktree_tree` works on a copy of the index (`fmcore.py:206-211`).
  - All mutation happens in `wt`.
  - `worktree add` only touches `.git/worktrees`.
- **Cleanup:** the `finally` covers the loop and timeouts. A `KeyboardInterrupt` landing between `:569` and `:572` could leave worktree metadata behind, but `prune` fixes that on the next run.
- **Unbounded `git apply` call:** `:574` has no timeout. This is minor.

## Acceptance criteria
- **Criterion 1 (revert each hunk alone, name those that still pass CMD):** partly met. The mechanism is present. It is unreliable for paths with spaces, for deleted files, and without a baseline run (findings 2-4).
- **Criterion 2 (all proven records passing evidence; unproven is inconclusive and never passing):** not met for the skipped, `--max` and zero-tested cases (finding 1).
- I did not run the tests in `plugin/tests/test_hunks.py`.

## Not checked
- `plugin/tests/test_hunks.py`.
- The CLI argument wiring for `--hunks`, `--max` and `--timeout`.
- The docs and CHANGELOG changes.
