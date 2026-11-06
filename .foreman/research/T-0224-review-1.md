**Verdict: changes needed**

**Findings**

1. **HIGH, `plugin/lib/fmevolve.py:109-112` with `plugin/lib/fmbench.py:372-377`: the guard check is bypassed.**
   - Before this change, `cmd_bench run` checked `plugin.json` and `has_guard(plugin)` before the replay loop. The refactor moved only the loop into `run_arm`. `evolve` calls `run_arm` directly, so the candidate plugin is never checked.
   - Replays run in bypass mode and the guard is the only barrier. The brief's own comment at line 375 says candidates must be "Foreman's own reviewed code".
   - `--target` accepts any file under `plugin/` (`fmevolve.py:84`). Inputs that break it:
     - `--target plugin/hooks/hooks.json --drop` empties the hooks file, so the candidate runs with no guard.
     - `--target plugin/lib/fmguard.py`, with the child returning a no-op guard or `--drop`.
     - `--target plugin/bin/fm` or any hook script, where the child writes arbitrary code that then runs in bypass mode.
   - Only the candidate needs the check, because the live arm is the current plugin. Fix:
     - Call `fmbench.has_guard(os.path.join(wt, plugin_dir))` before the candidate `run_arm`, and fail if it returns false.
     - Better, limit targets to instruction text (`.md` files). Code revised by an LLM and then run unsandboxed breaks the "no untrusted content" rule even with the guard file present, because `has_guard` only checks that the file exists.
   - Confidence: high. I read `has_guard` and `cmd_bench`.

2. **MEDIUM, `fmevolve.py:103` and `:109`: the arms are not like for like.**
   - The candidate worktree is created from `HEAD`. The live arm runs `os.path.join(repo, plugin_dir)`, which is the working tree.
   - Git status shows uncommitted `plugin/` edits right now (`fmbench.py`, `fmcli.py`). Any such edit is counted as a difference between the arms. The gate can pass or fail because of uncommitted work, not the revision.
   - Fix: refuse a dirty `plugin_dir` with `git status --porcelain -- plugin`. Or run the live arm from a `HEAD` worktree.
   - Confidence: high.

3. **MEDIUM, `fmevolve.py:103`: the commit result is never checked.**
   - A failed `git commit` (gpgsign, a pre-commit hook, or the file being untracked so `-a` skips it) is ignored.
   - The worktree still holds the edit, so the bench runs on it. If the gate passes, `kept` is true but the branch points at `HEAD` with no revision.
   - Fix: check `returncode`, raise `ValueError` on failure, and add `-c commit.gpgsign=false --no-verify`.
   - Confidence: medium. I read the code and did not run it.

4. **LOW, `fmevolve.py:105-107`: `--live` handling.**
   - `live` is joined into a path without the label regex used in `cmd_bench`, so `--live ../x` reads files outside the results folder. It is a CLI argument from the user, so the impact is small.
   - A live result with a different model or plugin is accepted silently.
   - Fix: apply the same `re.fullmatch` label check.

5. **LOW, `fmevolve.py:67`: the output regex.**
   - `<file>(.*?)</file>` stops at the first `</file>`. An instruction file that mentions that tag is truncated, and the truncated version is then benched and committed.
   - There is also no check that the frontmatter survived.
   - Fix: take the last `</file>`, and require the `---` frontmatter whenever the original had it.

**Acceptance criteria**

The brief did not list explicit criteria, only the task title. Against the intended behaviour, "never touches the live plugin" is met because the edit happens in the worktree. "Gate-decides, leave no trace" is met for failed candidates (`finally` block). "Safe replay" is not met, per finding 1.

**Not checked**

I did not run the tests. I did not read `plugin/tests/test_evolve.py` beyond the diff. I did not review the `fmfriction` API usage, which is wrapped in a broad `except`. I did not check concurrent `evolve` runs in one second beyond noting that the `git worktree add` failure is raised cleanly.
