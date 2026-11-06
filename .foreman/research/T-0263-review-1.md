## Review of T-0263 (tour, pr proof, export agents)

Findings come from reading the diff plus `fmcore.py`, `fmmap.py` and `fmrecall.py`. I did not run any tests. Line numbers for new code are diff lines, because the working-tree line numbers weren't checked.

### Lens: adversary — changes needed
- **MEDIUM — export leaks absolute paths.** `fmcost.py` `agents_md` playbook loop (diff L214) writes `f"- {title}: {path}"`. `path` is built from `fmrecall.PLAYBOOKS`, which is `c.PLUGIN_ROOT/skills/...` (`fmrecall.py:34`), an absolute path under the user's home. A committed AGENTS.md would carry `~/.claude/foreman/plugin/...`, which exposes the username and means nothing on another machine or harness. Fix: omit the path, or give it relative to the plugin root. Confidence high.
- **MEDIUM — export does not clean free text.** Corrections (L183), lessons (L196) and decisions (L201) go through `c.plain` and `c.redact`. `redact` only matches secret patterns (`fmcore.py:554`). The user's own words, internal hostnames, customer names and pasted text go into a file meant to be committed. Corrections are the user's own words, copied verbatim. Lessons and decisions are agent-written text and are not `defang`ed. Add a one-line "review before committing" note to the command output. I did not check whether `fm sensitive on` should make export refuse. Confidence medium.
- **LOW — overwrite guard and symlinks (L226-233).** `open(path)` follows symlinks and `write_atomic` then replaces the link itself. If AGENTS.md is a symlink to a file that carries our mark, the link is silently turned into a regular file. A dangling link counts as `FileNotFoundError`, so it is also overwritten. A symlink to CLAUDE.md is refused without `--force`, so the common case is safe. With `--force`, `--out` accepts any path, for example `--out ~/.bashrc`. That is user-typed, so I count it as intended. Without `--force`, only nonexistent or marked files are written. Fix: if `os.path.islink(path)` and not `--force`, refuse. Confidence medium.
- **LOW — hostile bench JSON (L119-128).** `json.load(f).get("cases") or []` sits inside the `try`, but the `for x in cases` loop does not. `{"cases": 5}` raises an uncaught `TypeError` and `fm pr` crashes. Deeply nested JSON raises `RecursionError`, which is not a `ValueError`, with the same result. Fix: move the loop inside the `try`, add `isinstance(cases, list)`, and catch `(OSError, ValueError, RecursionError, TypeError)`. Confidence high.
- **Audit lines:** `add_audit` defangs and flattens results (`fmcore.py:945-951`), and the pr regex is anchored to one line. I found no injection there.

### Lens: edge — changes needed
- **MEDIUM — `fm tour` and renames.** `fmmap.py` `tour` (diff L266-269) uses `git show --numstat` and `task_diff(..., "--numstat")` with renames on by default. A rename comes out as `src/{a => b}.py` or `a => b`, and `parts[2]` becomes that string. The file read fails, so the text is empty and nothing in it counts as "used". `os.path.exists` is false, so the row is marked "(deleted)" and sorted wrongly. Fix: add `--no-renames` to both calls. A binary file (`-`) is handled and shows +0 −0. Confidence high.
- **LOW — `fm export` on an OS error.** `open(path)` for the mark check only catches `FileNotFoundError`. If `--out` points at a directory or an unreadable file, `IsADirectoryError` or `PermissionError` produces a traceback instead of a `UsageError`. Confidence high.
- **LOW — tour on a batch member.** For a done task, `--grep=(T-0248` will not match a batch commit titled `(T-0263: T-0248…`. The tour then falls back to `task_base`, which is the whole diff since focus. This is probably fine but undocumented.

### Lens: intent — ok with gaps
- T-0248: imported-first order, sizes, step and test all present.
- T-0249: the red→green command, each lens verdict, assumptions and bench replays are in `fm pr`, as the criterion says.
- T-0246: all six sections are present and the overwrite guard works.
- Truncation at 32 KiB cuts the playbooks last. It can cut mid-line and drops the section silently.

### Lens: operator — ok
- MASTER.md, CHANGELOG and help tiers are updated.
- Always-on context is not touched.
- Nothing is installed.

### Lens: maintainer — ok with nits
- **LOW — test gaps.** `test_handoff.py` never asserts the corrections section, redaction, the 32 KiB truncation, a rename in `tour` or hostile bench JSON. Add a test for each fix above.
- **LOW — `fmmap.py` (diff L312).** `_DEF =re.compile` lost its space after `=`. It is valid Python but looks like a typo.

### Not checked
I did not run the tests. I did not check `fm sensitive` interaction, `fm pr` JSON output, or the size and unboundedness of `fmmap.render`.
