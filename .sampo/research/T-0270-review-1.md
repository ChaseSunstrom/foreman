**Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every finding below comes from reading the diff and `fmguard.py`.

## Findings

**HIGH — `plugin/lib/fmguard.py:1403-1415` (`_assignments`): regression, exec and file variables are missed behind any wrapper or keyword.**
- The old `_git_code` scanned every word of `c.argv`. The new `_assignments` stops at the first word that is not an assignment, `env` or a `-flag`.
- These lines now pass `_env_channels` and `_env_files`. `_strip_wrappers` (line 470) still resolves each of them to `git`, so only the new checks lose sight of them:
  - `timeout 5 env GIT_SSH_COMMAND='rm -rf ~/Documents' git fetch` (stops at `timeout`)
  - `env -u HOME GIT_SSH_COMMAND='…' git fetch` (`HOME` is not an assignment and has no leading dash, so it stops there)
  - `for i in 1; do GIT_SSH_COMMAND='…' git fetch; done` (stops at `do`; the same goes for `then`, `{` and `!`)
  - `nice env GIT_TRACE={protected}/f git status` and `command env …`
- `GIT_TRACE`, `GIT_INDEX_FILE`, `GIT_CONFIG_GLOBAL` and `HOME` are missed the same way.
- The old line-1283 `git_env` handling still scans all of `c.argv`, so it did not have this hole.
- Fix: skip anything `_strip_wrappers` would skip. Either reuse its loop to find where the real command starts, or scan all of `c.argv` as before, since a non-leading `NAME=` is harmless to check. Add test cases for `timeout`, `env -u`, `do`, and `nice` or `command` followed by `env`.

**MEDIUM — `fmguard.py:1304-1305`, `1496-1520`: `git clone -c` and `--config` exec keys are unchecked.**
- Only global options before the subcommand go through `_git_config_code`.
- `git clone -c core.sshCommand='rm -rf ~/Documents' ssh://h/r`, and `--config core.sshCommand=…`, write the key into the new repo's config and git uses it during the clone.
- `_GIT_EXEC_FLAGS["clone"]` has only `-u` and `--upload-pack`.
- Fix: in `_git_code`, for `clone`, run `_opt_values(tail, "-c", "--config")` through `_git_config_code`.

**MEDIUM — `fmguard.py:1457-1462` (`_git_config_code`): `init.templateDir` is missed.**
- `--template` and `GIT_TEMPLATE_DIR` are refused, but `git config init.templateDir /tmp/t` and `git -c init.templateDir=/tmp/t clone URL` are not.
- A later `clone` or `init` copies hooks from that folder, and a `post-checkout` hook runs at clone.
- Fix: refuse `init.templatedir` next to `core.hookspath`.

**MEDIUM — `fmguard.py:1403-1415`, `1455` (`_ASSIGN`): `NAME+=value` is not recognised.**
- `GIT_SSH_COMMAND+='rm -rf ~/Documents' git fetch` is valid bash, and it exports the appended value to git.
- `_ASSIGN` requires `=` straight after the name, so `_env_channels` never sees it.
- `_ASSIGNISH` (line 961) already handles `+=`, but this code does not use it.
- Fix: match `\+?=` in `_assignments`.

**MEDIUM — `fmguard.py:1319-1320` (`_git_writes`, `init`): the target is wrong when `--separate-git-dir` is given as two words.**
- `--separate-git-dir` is missing from the valued-option list passed to `_git_pos`.
- For `git init --separate-git-dir /tmp/g {protected}/r`, the first positional is `/tmp/g`, so `{protected}/r` is never checked.
- Only the `--separate-git-dir` value itself is added, from line 1573.
- Fix: add `--separate-git-dir` to the valued tuple.

**LOW — `fmguard.py:1371-1376` (`_GIT_EXEC_FLAGS`): abbreviated long options and missing exec keys.**
- git's parse-options accepts unambiguous prefixes. `git rebase --exe='…'` or `git difftool --extc=…` avoids the exact `--exec=` and `--extcmd=` matches.
- The exec-key regex `_GIT_EXEC_KEYS` omits `mergetool.<tool>.path`, `difftool.<tool>.path`, `sendemail.sendmailcmd`, `browser.<tool>.path` and `man.<tool>.path`.
- Fix: match flag prefixes of at least 3 characters per subcommand, and add the keys above.

**LOW — unlisted write targets.** `fast-export --export-marks=FILE`, `index-pack -o FILE`, `bugreport -o DIR` and `pack-objects BASE` are not in `_git_writes`. The content written is mostly not attacker-chosen, so the risk is limited to overwriting a file.

## False positives and crashes

- I found no new false positive from reading the code. The following were previously caught or are intentional:
  - `git config core.hooksPath .githooks` was already refused at line 1826.
  - `git config alias.X` is a deliberate `system` refusal and is covered in the tests.
  - `GIT_EXEC_PATH=$(git --exec-path)` is blocked and is rare.
- I traced the odd inputs and none of them crash:
  - `git config` with no arguments: the positional list is empty and every `pos[:1]` guard holds.
  - `export` with no `=`: the match returns `None` and is filtered out.
  - Empty `GIT_TRACE=` is skipped by the `\d*` pattern.
  - A unicode value only reaches `.lower()` and `fullmatch`.
  - `-O` with an empty attached value is dropped by `.strip()`.
- `_assignments` does not read ordinary arguments as assignments. It breaks at the first plain word. The cost is the HIGH finding above.
- Not verified: whether `EDITOR=$VISUAL` or `PAGER=$(command -v less)` goes through `check_bash("$VISUAL")` as an unresolvable command. That could be a false positive.

## Acceptance criteria

- Channels blocked and everyday git still passing: partly met. The listed spellings pass the tests, but the gaps above remain. I did not run the tests.
- `fm replay` and the guard suite: not verifiable from the code. Replaying 5,000 real commands would not exercise the `timeout`, `env -u` or `do` forms.

## Not checked

- I ran no tests and no replay.
- I did not read `test_guard.py`, `_target_cats` or the parser's `Cmd.argv` construction. I assumed wrappers and keywords stay in `c.argv`, which line 1235 and `_strip_wrappers` support.
