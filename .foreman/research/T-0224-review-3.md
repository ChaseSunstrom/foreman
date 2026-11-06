## maintainer: changes needed

**MEDIUM — `plugin/lib/fmevolve.py:96,109-111`.** The two arms are not built from the same tree.
- The live arm runs `os.path.join(repo, plugin_dir)`, which is the working tree. The candidate worktree is cut from `HEAD`.
- The repo currently has uncommitted edits (`fmbench.py`, `fmcli.py`, and others). The candidate therefore lacks them, and the gate compares "HEAD plus mutation" against "working tree".
- `old` is read from the working tree (line 86) and written over the `HEAD` copy (line 101). Any uncommitted edit to the target is silently dropped from the candidate.
- Fix: refuse when `_git(repo, "status", "--porcelain", "--", plugin_dir)` is non-empty. Alternatively, run the live arm from a `HEAD` worktree via `fmbench._worktree`.
- Confidence: high on the code path. I did not check whether the tests cover a dirty repo.

**MEDIUM — `plugin/lib/fmevolve.py:103`.** The commit result is never checked.
- If the commit fails (git identity or hook problem), the branch stays at `HEAD` with the change only in the worktree's working tree.
- The candidate arm still runs on that worktree, so it benches the mutated file. But `kept` can come back true with a branch that carries no commit, so the "review with git diff HEAD...branch" instruction shows nothing.
- Fix: check `returncode` and raise `ValueError`. The `finally` block already cleans up.
- Confidence: medium-high.

**LOW — `plugin/lib/fmevolve.py:74-75`.** `_git` is a pure pass-through to `fmbench._git`, so it is dead indirection. Call `fmbench._git` directly, or drop the wrapper.

**LOW — `plugin/lib/fmevolve.py:106`.** `--live` is joined into a path without validation, so `../x` escapes `bench/results`. The caller is the user's own CLI, so the risk is small. Fix: `os.path.basename`, or reject a name containing a separator.

**LOW — `plugin/lib/fmevolve.py:116-117`.** `_git(repo, "worktree", "remove"/"branch -D")` ignores failures. A failed removal leaves a stale worktree and branch, and the stamp has one-second resolution. Fix: surface a warning on a non-zero return code.

## Not checked
- I did not run the tests.
- I only grepped `plugin/tests/test_evolve.py` and did not review it in full. Coverage of the dirty-repo and commit-failure cases is unverified.
- I did not review the `fmcli.py` and `fmbench.py` hunks.
