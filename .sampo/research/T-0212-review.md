**Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the code and did not run it.

**Findings**

- **MEDIUM** — `plugin/lib/fmbench.py:76`. The return code of `git checkout <commit> -- <tests>` is ignored.
  - `git show --name-only` (line 102) also lists tests the commit deleted or renamed away. For such a file, `checkout` fails with "pathspec did not match" and restores nothing.
  - In `validate`, the base-side check can then run without the hidden tests. A case can be kept, or dropped, for the wrong reason.
  - In `run_case`, grading runs against whatever the agent left in the tree.
  - Fix: use `git show --name-only --diff-filter=AM -z` and split on `\0`. This also fixes quoted non-ASCII names, which `core.quotepath` turns into `"caf\303..."` and which break `TEST_FILE` and `checkout`. Then check `returncode` and fail the grade if the restore fails.

- **MEDIUM** — `plugin/lib/fmbench.py:145-167` and `plugin/lib/fmbench.py:228-233`. Results are written only after every case has run.
  - `_worktree` raises `OSError` on a failed `worktree add`. `subprocess.run([fm, ...])` (line 150) raises `FileNotFoundError` if `bin/fm` is missing. It also raises `TimeoutExpired` after 60 s. `run_case` catches none of these, and `cmd_bench` doesn't either.
  - Ctrl-C or one crash at case N throws away the results, and the money, of cases 1 to N-1.
  - Fix: wrap `run_case` in `cmd_bench` and record an `error` result, and write the results file after each case.

- **LOW** — `plugin/lib/fmbench.py:200-201`. `build --ids X` overwrites `cases.json` with only X's cases and silently drops the rest. Merge by id, or document it.

- **LOW** — `plugin/lib/fmbench.py:158`. On timeout, `subprocess.run` kills only the `claude` process, not its tool subprocesses. Orphans can keep writing into a worktree that is then removed. A SIGKILL also leaves a `fm-bench-*` temp directory and a stale worktree entry. Fix: use `start_new_session=True` plus `killpg`, as `c.run_command` does, and run `git worktree prune` at the start of `run`.

- **LOW** — `plugin/lib/fmbench.py:210-212`. `list` sorts result files by name, so "last 8" is not the latest 8. It also reads every entry, and a stray `.tmp` file or a corrupt JSON file crashes the command. Sort by mtime and filter on `.json` with a try/except.

- **LOW** — `plugin/lib/fmbench.py:153`. The prompt is passed positionally. A raw request that begins with `-` would be parsed by `claude` as a flag. Fix: prefix the prompt with a fixed word, or pass it after `--`.

- **LOW** — `plugin/lib/fmbench.py:49-50`. The credential filter is a denylist. `*_KEY`, `DATABASE_URL` and similar variables pass through. This is acknowledged by the `ponytail` comment at line 221, and the bypass-mode risk is bounded by the guard. Accept it, or switch to an allowlist.

- **LOW** — `plugin/lib/fmbench.py:249-254`. `compare` shows pass flips only. Cost and turns appear only in the per-label summary lines, so cost and turn regressions are not shown per case. This is acceptable, but note it for `/foreman:improve`.

**Checked and fine**
- **Repo untouched:** the worktree is detached and every checkout, grade and replay runs inside it. The `finally` removes it, and it also runs on Ctrl-C.
- **Shell injection:** none beyond verify commands, which run through `bash -c` and come from the user's own briefs. Test paths are passed as argv after `--`.
- **Environment:** `FOREMAN_*`, `CLAUDECODE*` and credentials are stripped, `FOREMAN_STATE` is a temp directory, and the plugin's `bin` comes first on `PATH`.
- **Per-case bounds:** `--max-budget-usd` and a timeout apply to each case. There is no total-cost cap across cases, but `--max` bounds the case count.
- **Fail-to-pass logic:** correct, apart from the checkout-failure gap above. `build` also skips tasks with zero or more than one commit naming them.
- **Test file:** the pre-audit "secret-looking value" is a dummy `ghp_x` and `y` in `plugin/tests/test_bench.py:103`. It is a false positive.

**Acceptance criteria**
1. `build` turns finished tasks into cases, and `run` on a stubbed `claude` restores the hidden tests and grades by the verify commands. This is met in the code, but I didn't run `python3 plugin/tests/run.py -k test_bench`. The checkout-failure gap above is not covered by the tests.
2. One live case runs end to end and reports pass/fail, cost and turns. This is not verifiable from the code. The 1/1 at $0.16 you reported is consistent with the code.

**Not checked:** `fmcli.py` argument wiring, `MASTER.md` and the CHANGELOG, and whether `--setting-sources project,local` stops `~/.claude/CLAUDE.md` from loading.

**Lens results**
- intent: ok. The `build --ids` overwrite is a LOW surprise.
- adversary: ok. There is no injection path. The denylist and the guard-only protection are acknowledged.
- edge: changes needed. Deleted or quoted test paths, a mid-run crash losing results, and orphaned processes after a timeout.
- operator: ok. Results are in the state directory and nothing is installed. The `list` crash on a stray file is LOW.
- maintainer: ok with nits. Results dir handling in `list`, and the checkout restore needs a test.
