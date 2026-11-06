**Verdict:** changes needed. I could only read the code (no Bash tool), so I ran nothing, including `run.py test_guard`. Each finding below is from reading the code.

## lens: intent
- MEDIUM — plugin/lib/fmguard.py:3433 — The acceptance criteria name `cd $(…)` staying put, but only `$NAME` forms are handled. `_only_unset` (2600) is false for `$(…)` and backticks, because `_PART` gives them no name. `cd "$(true)" && git reset --hard` run from Foreman therefore gets cwds=[] and lost=[""], with no stay-put folder added. Nothing else puts `ctx.cwd` back, and `_target_cats` (3157) guesses only from words in the line, so it probably passes. The only `$(…)` case in the test table is the negative `git rev-parse` one. — Treat a `$(…)`/backtick target as possibly empty and add `.`, with a positive test. — PLAUSIBLE

## lens: adversary
- MEDIUM — plugin/lib/fmguard.py:3441 — The CDPATH widening treats each whole `_WORD` as one folder, but `:` is a word character. `export CDPATH=.:~/.claude/foreman; cd plugin && sh -c 'rm -rf lib'` from `/tmp` yields the single word `.:/home/…/foreman`. The join with `plugin` is never a directory, so only `[None]` is added and the nested rm passes. The test uses a single-entry CDPATH only. — Split each word on `:` (`for w in … for s in w.split(":")`) and test a colon-list. — CONFIRMED by reading the code
- MEDIUM — plugin/lib/fmguard.py:3404 — For a computed command word that may be a cd, `maybe` holds only `args[0]`. `$C -P /home/…/foreman/plugin && rm -rf lib` (or `--`) records `-P` as the folder, so cwds gets `/tmp/-P` and the rm check never sees plugin. The real cd path strips `-P -L -e -@ --` at 3414, but this path does not. — Take the first word not in that flag list, or add every non-flag argument to `maybe`. — PLAUSIBLE
- MEDIUM — plugin/lib/fmguard.py:3667 — The changelog says "An rm is judged in every folder the shell may be in", but only `cwds` is looped. After a cd the guard can't name (`lost`), rm is still judged only from `cwd`: `cd "$(echo <foreman>/plugin)" && rm -rf lib` is not judged in the folder the cd names. `_target_cats` guesses from line words for writes; `_check_rm` has no equivalent. — Run `_check_rm` for line-word guesses under `lost`, or reword the claim. — PLAUSIBLE

## lens: edge
- LOW — plugin/lib/fmguard.py:3435 — `raw[idx]` is used without the `len(raw) == len(cmds)` check that line 3362 requires before `_track_vars(raw[idx])`. If the two lists misalign, `ws` comes from another command and the "." (stay-put) folder can be dropped. — Add the same length check. — PLAUSIBLE

## lens: operator
ok. `_check_rm` is plain string work, and the 1024 cap at 3461 runs before the new loop. The new loop is cheap per call, but no timing test covers it.

## lens: maintainer
- MEDIUM — plugin/lib/fmguard.py:3404-3408 — The `bare`-dependent branches are dead. `_outside` (2794) returns `({}, None)` whenever any command word is computed and isn't a path, so `bare` is None and `_only_unset(…, bare)` is always false. The `unsure` branch and the "alone and unset: not guessed" arm never run, and `$X cd /tmp` passes only because `maybe` is always `["$OLDPWD", …]`. The changelog's "`$X cd D` is `cd D`" is not what runs. — Delete the dead branches, or make `_outside` expose the bare set; assert `$X` alone and `$X cd` against the real result. — CONFIRMED by reading the code
- LOW — plugin/tests/test_guard.py:2647-2677 — Missing cases: `cd "$(true)"`, `$C -P <dir>`, a colon CDPATH, and `C=; $C cd <dir>`. In that last one, `w0.split() or [""]` (3400) leaves `""` as the command word, so the real command is lost. — Add them.

## Acceptance criteria
- `cd "$X"` / `cd $X` / `$X cd D` / `$C D` / nested sh after CDPATH: met for the cases in the table. The colon-list CDPATH and `$C -P` variants are not.
- `cd $(…)` staying put: not met. There is no code or test for it.
- Common safe lines pass: the table asserts this, but I did not run it.

## Implicit decisions
- A name the line neither sets nor inherits is taken as empty. Positional `$1` also counts as unset.
- CDPATH candidates are the line's own words resolved against `ctx.cwd`.
- An unknown computed command word makes the shell "possibly anywhere" for the rest of the line.

## Not checked
I ran no tests and measured no timing. I did not check the 411 KB CHANGELOG beyond the new entry.

**Noticed:** `_DCWD["seen"]` (3304) is cleared only at depth 0, which fmmcp already handles at 3301. Otherwise none.
