**Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is 0 lines, so I reviewed the working-tree code directly. I did not run anything.

**Key question: can the snapshot let a genuinely sensitive change by the task escape the adversary lens?**
- **When the snapshot works:** no. A task's own `+` lines are always measured against the focus-time tree. An already-dirty file's earlier changes are excluded. The task's own edit to that file still shows up, and so does a mid-task commit, because the diff is snapshot to worktree, not HEAD.
- **Path trigger:** `files` still includes ledger touches (`fmcli.py:218`), so a sensitive file name still triggers even when the content diff is empty.
- **Settable fields:** `base_tree` and `base` are not settable through `fm task set`, since `EDITABLE` gates the keys (`fmcli.py:464`). The agent can't move the base.
- **Where it leaks:** only when the snapshot or diff fails (findings below).

**Findings**

1. **MEDIUM — `fmcore.py:208-209` and `:232-235`, used at `fmcli.py:229` — the content trigger fails open silently.**
   - `worktree_tree` returns `None` on any `SubprocessError`, because `git add -A` runs with `check=True`. `task_diff` then returns `""`, and so does `_git` on non-zero exit or timeout.
   - **Scenario:** a task adds `os.system(...)` or `eval(x)` to `util.py`, and the tree also holds one unreadable file, such as a root-owned file from a docker volume or a `chmod 000` file.
     - `git add -A` exits 128 with "Permission denied".
     - `worktree_tree` returns `None` and `task_diff` returns `""`.
     - `sensitive(files, "")` then checks file names only, because `fmcli.py:229` passes `""` as the diff. The `util.py` change escapes the adversary lens, and `fm task done` raises no error.
   - **Second route:** `task_diff` uses a 60s timeout (`fmcore.py:235`) while `audit prep` allows 300s. A large diff, such as a vendored add, times out the same way.
   - **Third route:** when `base` is `None` (snapshot pruned and no start commit), `fmcli.py:219-229` skips both the scope check and the content scan.
   - **Fix:** in `done`, if `git_root(p.root)` is true and `task_diff` can't produce a diff (tree `None`, git failure, or no base), treat the task as risky. Add the adversary requirement with the reason "diff unavailable". Have `task_diff` return `None` on failure so callers can tell "empty" from "failed", and raise the timeout to match `audit prep`.
   - **Confidence:** high on the code path; the unreadable-file trigger is from my knowledge of git behaviour, not run here.

2. **LOW — `fmcli.py:573-574` — a failed snapshot at focus is silent.** When `worktree_tree` returns `None` (same failure modes), `base_tree` is never set and focus doesn't retry. The task falls back to the start commit. That is safe, because it over-includes earlier dirty work, but the user gets no hint why audits are noisy again. Fix: log "snapshot failed; diffing from the start commit". The 120s `git add` also runs while holding `c.lock(p.dir)`, which blocks other `fm` calls.

**Acceptance criteria**
- **Criterion 1** (earlier work isn't the task's change; the task's own sensitive edit to a dirty file still is; works with no commit): met by the code. `task_base` prefers `base_tree`, then `base`, and diffs tree to tree. I did not run `test_diff_gates.py`. Whether it covers the snapshot-failure path (finding 1) is not verified.
- **Criterion 2** (`fm check` passes): not verifiable from the code.

**Not checked**
- Whether the tests assert the failure path in finding 1.
- The T-0119 standing-yes code, which is out of scope.
- The `fm sync` `.foreman/**/*.md` exclusion glob semantics. It looks right, and `scope_drift` also exempts `.foreman/`.
- Rename or binary-diff edge cases.
- Concurrent sessions. Over-inclusion is the safe direction.
