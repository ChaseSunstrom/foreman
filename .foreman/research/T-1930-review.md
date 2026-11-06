## Verdict
Approve. I could not break either claim. I read the code only and ran nothing, because this session has no Bash tool.

## Findings

## lens: adversary
No findings. This is how each attack came out.

- **Claim 1 (relative x implies `isdir(w/x)` ⇒ `isdir(w)`):**
  - For a relative x, `os.path.join(w, x)` is `w + "/" + x`, or `w + x` if w ends in "/". The kernel resolves w first, so any component under w needs w to be a directory.
  - **w is a file or a dangling symlink:** `isdir(w/x)` fails with ENOTDIR or ENOENT. The old check is False, so dropping w loses nothing.
  - **w is a symlink to a directory:** both `os.path.isdir` calls follow it and agree.
  - **x is "":** `join(w, "")` is `w/`, and `stat("w/")` succeeds only if w is a directory (a symlink to one counts). This is the same test as `isdir(w)`.
  - **x starts with ".." or contains it:** `w/..` still has to traverse w. If w is a file, `stat("w/..")` returns ENOTDIR.
  - **Trailing slash on w:** `words` comes from `_resolve`, and its `os.path.normpath` strips the trailing slash. This does not matter anyway, because `stat("w/")` on a directory behaves the same as `stat("w")`.
  - **Permissions:** the filter can only keep more words than before, never fewer, because the original per-x `isdir(w/x)` check still runs on every survivor. Where `isdir(w)` is False, `isdir(w/x)` is also False, because the path needs w to be a searchable directory.
  - **NUL bytes and over-long paths:** `isdir` returns False when the path has a NUL byte or is too long. For an over-long `w/x`, `isdir(w)` can still be True, so the filter is a superset again. `guesses` is unchanged.
  - **Rewriting:** `words` is not changed beyond filtering. `w` goes into the same `os.path.join(w, x, _expand(t, ctx))`, so the guess strings are identical.
- **Claim 2 (every entry of `lost` is relative):** `lost` has only these sources.
  - `fmguard.py:3352` seeds it with `[""]` or `[]`.
  - `fmguard.py:2804` adds `""` for an unresolvable cd target.
  - `fmguard.py:2811` adds `os.path.join(x, t)` only in the branch where `t` is not absolute (the `os.path.isabs(t)` test is at 2807), and `[t]` when cdpath is set. Both are relative when x is relative.
  - `fmguard.py:3369`, `3411`, `3414` and `3423` only merge `lost` lists that came from those sources.
  - `fmguard.py:2812` and `3420` come back through `_moved`, so they add nothing new.
  - `~user` and `~` targets are expanded to absolute paths by `_expand` before `isabs` runs, so they take the absolute branch and never reach `lost`.
  - If an absolute x ever did appear, `any(map(os.path.isabs, lost))` turns the filter off and the old behaviour returns. The guard fails safe.
- **Normalisation by `_resolve` (`fmguard.py:306`):** it runs before the filter, and `w` is the same normalised string in the old and new code. `normpath` can collapse `a/../b` through a symlink differently from the kernel, but that happens in both versions, so it changes no verdict.
- **TOCTOU:** `isdir` runs once on each of `w` and `w/x`, as before, so there is no new race.

## lens: intent / maintainer
- LOW — `plugin/tests/test_guard.py:44` — the time bound is 4 s for both lines, while the acceptance criterion says under 2 s. A wall-clock bound this loose could let a regression of about 2x through. — Assert `< 2` per line, or measure each line separately. — medium confidence

## Acceptance criteria
- **Lines of 4 `(true); cd dN; cd xN;` blocks with 2 or 10 `$(ls j)` bodies, judged in under 2 s with the same verdicts:**
  - **Same verdicts:** met by reasoning. The filter drops only words w for which every `isdir(w/x)` is False, so the guess set is identical.
  - **Timing:** not verifiable from the code. The test (lines 34-49) asserts only a combined 4 s, and I did not run `python3 plugin/tests/run.py test_guard`.
- **The CHANGELOG claim of "under half a second":** not verifiable here.

## Implicit decisions
- The filter is switched off entirely if any `lost` entry is absolute. This is a conservative fallback, and no code path makes one today.
- The fast filter reuses `os.path.isdir` and does not cache results.
- The test bound is wall-clock, which is machine-dependent.

## Not checked
- I did not run the test suite or time the guard.
- I did not check the CHANGELOG wording beyond reading the diff.
- I did not check Windows or macOS, where `isabs` and `isdir` semantics differ. The code only runs here on Linux.

**Noticed:** none
