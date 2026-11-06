## intent: changes needed (edge/adversary findings below)

**Verdict: changes needed.** I found no guard bypass. I could not run anything, because this audit is read-only, so everything below is from reading the code.

**What holds for the guard**
- `fmedit._check` builds the same `Ctx` as `fmhooks._guard_ctx` (`standing`, `trusted`, `allow`, `state_*`). It leaves out `scratch`, `confine` and `unbriefed`, which makes it stricter or equal, and standing/trust logic is unchanged.
- Paths are `realpath`ed before both the scope check and `fmguard.check("Write")`. A symlink into core or state is classified as core or state. A symlink out of the project, `..`, and an absolute path all fail the `../` test at `fmedit.py:63`.
- The edit can only touch files that already exist, so "files created by the edit" doesn't arise.

**Findings**

1. **MEDIUM, `plugin/lib/fmedit.py:81-86`: the write is not all-or-nothing.**
   - `_write` replaces files one at a time with no rollback.
   - If file 2 fails (read-only directory so `mkstemp` fails, ENOSPC, EACCES), file 1 is already changed and the user gets a traceback.
   - Repro: edit `a.py` and `ro/b.py` with `ro` at mode 555.
   - Fix: stage every temp file first, then `os.replace` them all. Or restore the originals from `texts` on exception.
   - Confidence: high.

2. **MEDIUM, `fmedit.py:77`: CRLF files are silently rewritten to LF.**
   - `open(..., encoding="utf-8")` uses universal newlines on read.
   - Any edit to a CRLF or lone-`\r` file rewrites every line ending.
   - An `old` text containing `\r\n` reports "not found".
   - Fix: `open(path, encoding="utf-8", newline="")`. The same fix is needed for the re-read at line 120.
   - Confidence: high.

3. **MEDIUM, `fmedit.py:36`: a malformed block is silently dropped.**
   - `BLOCK.finditer` skips a block with a typo (missing `>>>`) and applies the rest.
   - Fix: refuse when the number of `@@ ` header lines differs from the number of matches.
   - Related: an `old` text containing a line that is exactly `===` splits wrongly.

4. **MEDIUM, `fmedit.py:66`: scope globs never match.**
   - Scope entries are globs (`c.glob_match`, `fmcore.py:2784`; `fmhooks.py:1721`). This code does a prefix compare only.
   - A task with `--scope 'plugin/lib/fm*.py'` or `'**/*.md'` refuses every file.
   - Fix: use `c.glob_match(rel, s)`.

5. **MEDIUM, `fmedit.py:70`: the user's own rules are bypassed.**
   - An Edit goes through `fmhooks._rule_hits` and `_path_hits` (`fmhooks.py:1611-1628`), so `fm rules` path rules with `action: block` apply to it.
   - `fm edit` and `fm sub` skip them, and the `bash` rule only sees the command text, not the stdin spec.
   - Claude Code `permissions.deny Edit(...)` is skipped as well.
   - Fix: call `c.rule_hits(p, "path", path)` per target and refuse on a `block` hit.

6. **LOW, `fmedit.py:120,143-158`: lost update.**
   - Text is read first, then written later from that stale read. For `fm sub` the gap is the whole repo scan.
   - A concurrent edit by another session is overwritten.
   - Fix: re-read each file just before the write and abort if it changed.

7. **LOW, `fm sub`.**
   - `:137` reads outside the project (an absolute glob or `..`), and the preview prints per-file counts. That is a regex oracle on files like `~/.ssh/*` (PLAUSIBLE). Restrict the preview to the project.
   - `:144` silently skips files that aren't valid UTF-8, so "No match" can be wrong. Report how many were skipped.
   - `:146` an invalid `repl` such as `\9` raises an uncaught `re.error`.
   - `:139` the `.git` exclusion runs before `realpath`, and `fm edit` has no `.git` exclusion at all. This matches what Edit allows.

8. **LOW, `plugin/lib/fmlanes.py:20`: `"²".isdigit()` is true but `int()` raises a traceback.** Use `isdecimal()` and `isascii()`.

9. **LOW, `plugin/tests/test_batch_edit.py:118-122`: the `Hint` class sits after the `__main__` block, so running the file as a script skips it.**
   - There are also no tests for symlinks, glob scope, CRLF, partial failure or `fm sub --apply` out of scope.

**Acceptance criteria**
- `fm edit` is atomic, refuses a non-unique or missing `old`, and refuses files out of scope: **partly met**. Plain-path scope works, but atomicity fails on a write error (1) and glob scopes are refused (4).
- `fm sub` previews and applies: **met**, with the caveats in item 7.
- `fm lane max` raises the cap: **met** (`fmlanes.py:18-24`).
- The test command wasn't run: **not verifiable**.

**Implicit decisions**
- Builder cap bounds are 1 to 6, and any session can change the cap with no ask.
- `fm sub` defaults to `--max 50` files and a `**/*` glob.
- Relative `fm edit` paths resolve against the project root, not the current directory.
- `fm sub` skips undecodable files without saying so.

**Not checked:** the docs, the UI files in the diff, and running the tests.

**Noticed:**
- The builder CONTRACT (`fmlanes.py:127`) still forbids heredocs, so builders can't use `fm edit` or `fm sub` and nothing says so.
- `fm edit` can write `.git/config` (a `core.hooksPath` hole). Edit can too, so this is a guard gap.
