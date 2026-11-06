**Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.

**Checked and fine**
- `-c Core.Pager` is handled. The `(?i)` flag at fmguard.py:1357 and `.lower()` at :1384 cover it.
- `-ckey=value` is not a form git accepts, so nothing to block.
- `--git-dir=`, `--work-tree=` and `--config-env=` are handled (:1434-1441, :1390).
- `-c core.hooksPath` is blocked in the system check (:1690).
- Alias chains re-enter `check_bash` with the `-c` options kept (:1398).

**Not blocked, ranked**

1. **HIGH: `git config` is never inspected, except for hooksPath (:1692-1696).**
   - `git config alias.x '!cmd'; git x` is not blocked. The same goes for `git config core.fsmonitor 'cmd'` followed by `git status`. The first command only writes `.git/config`, and `_git_code` reads only global `-c` options.
   - `git config --file ~/.claude/foreman/plugin/lib/x k v` writes to a protected path. `_write_targets` has no config branch (:1431-1453).
   - Fix: for `sub == "config"`, treat `-f`, `--file` and `--file=` values as write targets. Also run any key that matches `_GIT_EXEC_KEYS` or `alias.` through the `-c` logic, using the value as code.

2. **HIGH: environment variables that write files are ignored.**
   - `GIT_TRACE=~/.claude/foreman/plugin/lib/fmguard.py git status` appends to that file. `GIT_TRACE2_EVENT`, `GIT_TRACE2`, `GIT_TRACE_PACKET` and `GIT_INDEX_FILE` behave the same way.
   - Only `GIT_DIR=` and `GIT_WORK_TREE=` become `git_env` targets (:1283).
   - Fix: change that prefix tuple at :1283 to include `GIT_TRACE`, `GIT_TRACE2`, `GIT_TRACE2_EVENT`, `GIT_TRACE_PACKET`, `GIT_TRACE_SETUP` and `GIT_INDEX_FILE`. Match them as `NAME=`, and use `_write_targets`' write classification for them, not the tree classification.

3. **HIGH: subcommand arguments that run commands.** None of these are in `_git_code`, which only scans global options (:1380-1394).
   - `git rebase -x 'CMD'` or `--exec=CMD`.
   - `git bisect run CMD`.
   - `git submodule foreach 'CMD'`.
   - `git difftool -x CMD` or `--extcmd=CMD`.
   - `git grep -O'CMD'` or `--open-files-in-pager=CMD`.
   - `git fetch`, `clone` or `ls-remote --upload-pack=CMD`, and `push --receive-pack=CMD` or `--exec=CMD`.
   - `git filter-branch --tree-filter`, `--index-filter` or `--msg-filter`.
   - Fix: after `sub` is resolved at :1395, add a table of `{sub: flags}` and send the flag's value to `check_bash`. For `bisect run`, `submodule foreach` and `--exec`, use `rest` as the code.

4. **HIGH: config read from a file.**
   - `-c include.path=/tmp/x` is not blocked. The config file is written first to an unprotected path, then git loads it. A config like `[core] fsmonitor=…` then runs unchecked.
   - `GIT_CONFIG_GLOBAL=`, `GIT_CONFIG_SYSTEM=`, `GIT_CONFIG=`, `HOME=`, `XDG_CONFIG_HOME=` and `GIT_TEMPLATE_DIR=` (or `--template=`) are not in `_GIT_EXEC_ENV`. The template route can plant hooks.
   - Fix: refuse them with `None` in `_git_code`, as `GIT_EXEC_PATH` is at :1374. Also refuse `-c include.path` and `-c includeIf.*.path`.

5. **MEDIUM: write targets missing from `_write_targets` (:1446-1453).**
   - `git archive -o FILE`. Only `-o` for `format-patch` is handled.
   - `git bundle create FILE`.
   - `git worktree add PATH`.
   - `git init DIR`.
   - `git format-patch -oDIR` and `--output-directory`.
   - `git clone --separate-git-dir`.
   - `git checkout-index --prefix=DIR`.
   - `git submodule add URL PATH`.
   - Fix: add `-o` for `archive`, plus `bundle create` (the first positional after `create`), `worktree add`, and `init`. Take the first positional after the subcommand in each case and join it to `base`.

6. **MEDIUM: exec variables set in an earlier command.** `export GIT_SSH_COMMAND='sh -c "…"'; git fetch` is not blocked. The inline check at :1372 sees only the git command's own argv, so the exported value is never checked. Fix: check `NAME=value` assignments for `_GIT_EXEC_ENV` names in any simple command, not only in a git argv.

7. **MEDIUM: gaps in `_GIT_EXEC_KEYS` (:1357).** These keys are not covered:
   - `core.gitProxy`, `core.alternateRefsCommand`, `remote.*.uploadpack`, `remote.*.receivepack`.
   - `mergetool.*.cmd`, `difftool.*.cmd`, `trailer.*.command`, `submodule.*.update`.
   - `credential.<url>.helper`. The pattern `credential\.helper` does not match it.
   - `protocol.ext.allow` with an `ext::CMD` URL.
   - Also missing from `_GIT_EXEC_ENV`: `GIT_PROXY_COMMAND`.
   - Fix: widen the regex to `credential\..*helper`, `remote\..+\.(upload|receive)pack`, `(mergetool|difftool)\..+\.cmd`, `trailer\..+\.command`, `submodule\..+\.update`, `core\.(gitproxy|alternaterefscommand)`, and `protocol\..*allow`.

8. **LOW: `GIT_CONFIG_PARAMETERS` with a non-alias key (:1376-1377).** `GIT_CONFIG_PARAMETERS="'core.sshCommand=CMD'"` is not blocked. `_GIT_EXEC_KEYS.search` is anchored with `$`, so it fails on `key=value`. The fallback regex only knows alias, `core.pager`, `diff.external` and fsmonitor. Fix: for `PARAMETERS`, take `val.strip("'\" ").partition("=")[0]` and test that against `_GIT_EXEC_KEYS`.

**Acceptance criteria:** I did not receive them in the brief. I could not check the Stash tests in `~/.claude/foreman/plugin/tests/test_pass1.py`.

**Not checked:** I did not run the guard or the tests. I did not review the other `check_bash` branches.
