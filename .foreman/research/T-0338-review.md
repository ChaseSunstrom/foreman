## Verdict
Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypasses I built by hand-tracing. Please run them as the first regression tests.

## Findings

**1. HIGH. `plugin/lib/fmguard.py:1070-1073` and `:1083` (`_a_path` skips the computed-command check on word splitting).**
- Command: `X=/tmp/ok; Y=-X=; S="eval ${Y#-}"; true && $S/etc; rm -rf $X`
- Guard: `$S/etc` has a literal `/`, so `_a_path` is true and `_outside` no longer returns `{}, None`. In `_prefix_vars`, `X` is counted once, because the new lookbehind hides the `X` in `Y=-X=`. `fixed={X:/tmp/ok}`, and `rm -rf $X` is judged as `/tmp/ok`.
- Bash: an unquoted `$S/etc` splits into `eval` and `X=/etc`. So `eval X=/etc` runs in the main shell and `rm -rf /etc` runs. Before this change the computed command word cleared everything.
- Fix: `_a_path` should hold only when a literal `/` comes before the first `$`, `` ` `` or glob character, e.g. `"/" in re.split(r"[$`*?\[]", word)[0]`. A `/` that follows an expansion can sit in a later field.
- Confidence: high.

**2. HIGH. `plugin/lib/fmguard.py:1169-1173` (the `&&` prefix is not truncated when it is "straight").**
- Command: `false && HOME=/tmp/ok; rm -rf $HOME/x`
- Guard: `ends=[&&, ;]`, and `_straight_line(shell)` is false because `&&` is mixed with `;`. So `prefix="false && HOME=/tmp/ok"`. That prefix is straight (only `&&`), so the `semis` fallback at line 1170 never runs. `_raw_cmds` reads `HOME=/tmp/ok` as executed. `HOME` is counted once, so `fixed={HOME:/tmp/ok}`, and `rm_vars` turns `$HOME/x` into `/tmp/ok/x`.
- Bash: `false` skips the assignment, so `HOME` stays real and `rm -rf ~/x` runs.
- The same trick works on any inherited variable and on write targets (`_target_cats` uses `known`). The old code reached this only with a branch character in the command; the new `not _straight_line(shell)` clause makes it reachable from a plain `;`/`&&` mix.
- Fix: always cut the prefix at the semicolons before the first `&&`: `semis = [e for e in ends if s[e] != "&" and e < (s.find("&&") % (len(s) + 1))]`. Drop the `if not _straight_line(prefix)` guard.
- Confidence: high.

**3. MEDIUM. `plugin/lib/fmguard.py:1301-1303` (tilde expands to `ctx.home` even after `HOME=` is assigned).**
- Command: `HOME=~/.claude; D=~/foreman/plugin/lib/fmguard.py; echo x > $D`
- Guard: `env["HOME"]` is tracked, but `D` is set to `ctx.home + /foreman/…`, which is not core, so it is allowed.
- Bash: `~` uses the current `$HOME`, so the write lands in Foreman core.
- Direct `echo > ~/x` after `HOME=` already behaves this way via `_expand` at line 152. T-0330 spreads it to variables.
- Fix: in `_track_vars`, use `env.get("HOME", home)`. Better, treat `~` as unknown once `HOME` is assigned anywhere in the command.
- Confidence: medium-high.

**4. LOW. `plugin/lib/fmcli.py:2674` (`_options_first`: a negative-number message word moves to the front).**
- Command: `fm claude send ID -5 minutes`
- `-5` starts with `-`, has no registered action, and is moved ahead of the positionals. That gives `claude -5 send ID minutes`, so `action` becomes `-5` and argparse rejects it.
- Before this change the same command worked.
- Fix: treat `re.fullmatch(r"-\d+(\.\d+)?", t)` as a positional.
- Confidence: medium.

**5. LOW. `plugin/lib/fmcli.py:2672-2676` (`_options_first`: an abbreviated flag takes the wrong value).**
- Command: `fm session send ID --mod opus -- MSG`
- `--mod` is not in `_option_string_actions`, so n=0. That gives `session --mod send ID opus`, and `--mod` swallows `send`. The result is a confusing "invalid choice" error. It does not fail silently.
- Fix: resolve abbreviations the way argparse does (a unique prefix of `_option_string_actions`), or only reorder when the flag matches exactly.

**6. LOW. `plugin/lib/fmcli.py:2672-2676` (`_options_first`: a message word that matches a real flag now silently becomes that flag).**
- Command: `fm session start please add --title to the list`
- Before, this was an "unrecognized arguments" error. Now it succeeds with `title="to"` and the message "please add the list".
- `--arg X` and `--cwd X` behave the same way. A message word is only protected after `--`.
- Fix: document that, or error when a known flag follows a positional without `--`.

## Checked, no bypass found
- Tilde forms: quoted `~`, `\~`, `~user`, `~+`, `~-`, `a:~/x` and globs all fall back to unknown.
- The count lookbehind: `-X`, `/X` and `.X` are not shell assignment positions. I found no indirect setter (`read`, `printf -v`, `mapfile`, `getopts`, `declare -n`, `export -n`, `for`, `${X:=}`, arithmetic) that is reachable. The builtin ones set `bare=None`.
- Aliases and functions cannot match a word containing `/`.
- `mkdir -p` in `made`: `"$" not in d` excludes unknown values. Its remaining risk is findings 1 and 2, which feed wrong `known` values into it.

## Acceptance criteria
- T-0330, T-0331: met for the tested cases, but findings 1-3 widen what the guard trusts.
- T-0332, T-0334: not verifiable (no run). `fmcli.py:118-121` and `:165-168` read correctly.

## Not checked
I did not run the tests or the guard. I did not review CHANGELOG or other lenses.
