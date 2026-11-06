## Verdict
Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a `cd DIR &&` line. I found these by reading the code. I could not run anything, so none of the inputs below were executed.

## Findings

**1. HIGH (confidence medium-high). `fmguard.py:707-708` and `:712`: a line continuation on the starter line shifts the body.**
- The regex `(python[0-9.]*\s+-\s*<<.*)$` accepts a trailing `\`. Bash joins the next line onto the starter line, and the heredoc body only starts after that joined line. The guard still treats the next line as the first body line.
- Input:
  ```
  cd ~/.claude && python3 - <<'X' \
  1>settings.json
  settings=1
  open('/tmp/a','w').write('1')
  X
  ```
- Bash runs `python3 - 1>settings.json` and truncates `settings.json`.
- The guard's unit is `1>settings.json` plus the lines after it. That parses as a Python comparison.
- `settings` is bound once, so `_open_targets` accepts it and `_proved_writes` returns only `/tmp/a`.
- The shell redirect sits inside the "body", so no later check sees it.
- `_proved_writes` can't catch this either. It only scans `rest` for `\\\s*$` at `:827`, and the starter lines are kept out of `rest`.
- Fix: in `_python_units`, refuse `fed` when the line ends in `\`. Also refuse it when `run.group(1)` contains any `\`.

**2. HIGH (confidence medium). `fmguard.py:710-713`: a second heredoc form on the same line.**
- `_HEREDOC_START` doesn't match `<<\E`. The comment at `:886` already says `_heredocs` doesn't know that form.
- Input:
  ```
  cd /d && python3 - <<'X' <<\E
  print(1)
  X
  open('~/.claude/settings.json','w').write('{}')
  E
  ```
- The last stdin redirect wins in bash, so python runs the `E` body.
- `starts` has length 1 and `fed` is true. The unit is `print(1)`, so `_proved_writes` reports no writes.
- The `E` body lands in `rest`. `_interpreter_writes` only falls back to `_WRITE_API` when `proved is None` (`:916`), so the write is never flagged.
- Fix: in `_python_units`, compare `len(re.findall(r"(?<!<)<<(?!<)", line))` with `len(starts)`, as `_interp_code` does at `:885`. Refuse `fed` on a mismatch.

**3. MEDIUM-HIGH (confidence medium-high). `fmguard.py:712`: `.strip()` on the delimiter line.**
- Bash ends a non-`<<-` heredoc only on an exact `X`. The guard also accepts `X ` and ` X`.
- Input: a body of `X=1`, then the line `X ` (trailing space), then `open('/…/settings.json','w')…`, then the real `X`.
- The guard's unit is `X=1`, which proves no writes.
- Python really runs all three lines. `X ` is a valid expression, because `X` was bound on the line before it.
- The later `open` text is only in `rest`, where it is not analysed.
- Fix: end the body on `lines[i] == delim` exactly, or on `lines[i].lstrip("\t") == delim` when the marker is `<<-`.

**4. LOW-MEDIUM (confidence medium). `fmguard.py:707` and `:841`: the cd target decides which module `python -` imports.**
- `python -` puts the current directory first on `sys.path`.
- `_proved_writes` handles this with `bases` plus `os.path.exists`, but it only looks at directories that exist at check time.
- `_drives_fm` does not do this check at all. A `json.py` or `re.py` in the `cd` target is still counted as a `_PLAIN_IMPORTS` module. An earlier command could have created it with a split-string script.
- This is the same for a bare `python -` in the current directory. The `cd` prefix just lets the directory be any path.
- Fix: in `_drives_fm`, apply the shadow-module test for every `cd` target, or refuse `fed` when a `cd` is present and the body imports anything. Alternatively, run the units with `python -I`.

## Cleared
- A `;`, `&`, `|`, backtick or `$(` in `group(1)` is refused.
- A `cd` target with spaces, quotes or `$` fails the character class, so there is no match. The character class excludes `$`, quotes and spaces, so no expansion is possible. `cd -` and `cd ~` are harmless.
- `<<<` produces a second start match, so `len(starts)` is 2 and the line is not a unit.
- A quoted `<<` inside the cd chain is excluded by the `_top_level` check.

## Acceptance criteria
- **T-0282:** partly met. The `cd` forms, the `;`, pipe and `$(` fallbacks, and the substitution fallbacks match the criterion on the cases in the test diff at lines 266-271. The shared parse mismatches above are not covered by any test.
- **T-0283, T-0284, T-0285, T-0279:** not reviewed, because they are outside the adversary focus you set.

## Not checked
- The rest of the diff and the other lenses.
- `check_bash` call sites beyond `_interpreter_writes`.
- Whether bash version quirks change heredoc termination.

Files:
- `~/.claude/foreman/plugin/lib/fmguard.py`
- `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0286.diff`
