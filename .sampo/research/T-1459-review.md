**Verdict:** changes needed (no HIGH findings; the first four MEDIUMs are real gaps).

I had no shell, so I read the worktree files directly instead of running the diff. I did not run any tests.

## lens: adversary
- MEDIUM — plugin/lib/fmplugins.py:211 (feeds fmdoctor.py:1270-1272) — `_ROOT_PATH` is `[\w./-]+`, which stops at `@`. A hook naming `${CLAUDE_PLUGIN_ROOT}/node_modules/@scope/pkg/dist/index.js` yields the script `node_modules`. `_stand_named` finds no file there and returns, so scoped packages are never content-hashed and only the stat stand-in covers them. The test only uses `.bin/run`. — Widen the class to include `@+~` and handle the one-time "adds script" this causes for existing baselines. Add a scoped-package test. — high
- MEDIUM — fmdoctor.py:1270-1272 — The number of named scripts hashed has no bound. A hostile `hooks.json` (up to 8 MB) can name 50k paths, each a symlink in `node_modules/.bin` to one 4 MB file. That is about 200 GB of reads, and `fm doctor` hangs. `bin/` is capped at 500 and the tree walk at 4000 files. — Dedupe by realpath, cap the count (say 500) and total bytes, and past the cap stand in `!too-many-named`. — high
- MEDIUM — fmdoctor.py:1166-1172 — Entries past 20,000 are unseen. A real `node_modules` often exceeds that. Walk order is sorted, so `node_modules/zzz-evil/x.js` or an edit deep in a late package is invisible, and the `!too-many` marker is constant. — Past the cap, keep walking directories only and stand in each directory's `st_mtime_ns` under its own budget. — medium
- MEDIUM — fmdoctor.py:1179 — The stand-in has no `st_ctime_ns`. Rewriting a file with the same size and then `os.utime` back to the old mtime is invisible for every unnamed file, and for the named script's imports. `_tree_hash` already records ctime for unreadable and unlisted entries (lines 1214 and 1248). — Add `st_ctime_ns`. The cost is noise on chmod or hardlink-count changes. — medium
- LOW — fmdoctor.py:1166 — The `onerror` handler records only `!unlisted`. `_tree_hash` (line 1214) also records mode and times. A `chmod 000` subfolder in `node_modules` hides replaced files behind a constant name. — Reuse the `unlisted` stat stand-in. — high
- LOW — fmdoctor.py:1196-1197 — A named script over 4 MB gets only `!not-read mode size`, with no mtime. The normal walk (line 1240) records size and mtime. Bundled MCP servers over 4 MB are plausible. — Add `st.st_mtime_ns`. — high
- LOW — fmdoctor.py:1190 — For a symlinked `node_modules` pointing outside the plugin, the link target is recorded but the target file's content is never hashed. The comment "capabilities names it" overstates this: capabilities names only the path. — Hash it anyway (a regular file, ≤4 MB, no leak), or reword the comment. — medium
- LOW — fmdoctor.py:1224 — Each skipped folder gets its own 20k budget, so work is unbounded in the number of folders. The attacker pays inodes roughly in proportion, so this is not an amplification. — Add a per-plugin total (for example 100k). — low

## lens: edge
- LOW — fmdoctor.py:1319 — Old baselines already hold a `skipped` hash, so `skip(was) in (None, …)` does not match once the stand-ins change it. Every plugin with a skipped folder shows a one-time "changed" WARN. In the live cache that is security-guidance (hooks/`__pycache__`), foreman-ui, claude-hud and ecc (`node_modules`). After that, a false "changed" needs a new python minor version, or an npm install or prune. No test covers an old baseline that has a skipped folder. — Record the new stand-ins in a new field (None means unrecorded), as T-1434 did. — medium

## lens: intent / maintainer
- Nothing to add. The `sha` of old baselines is unchanged, and `.git` stays out as the brief asks.

## Acceptance criteria
- A change under `node_modules` or `.venv` shows as a supply change: met (test lines 464-468; WARN).
- A hook-named script in `node_modules` is hashed by content: met for `.bin/x` (line 472); not met for `@scope/` paths (first finding).
- `.git` changes don't show: met (line 475).

## Implicit decisions
- The stand-in format is mode, size and mtime_ns, with no ctime and no inode.
- 20k entries per folder, and 4 MB per named script.
- Ignoring the `.git` folder wholesale, so `.git/config` fsmonitor and `.git/hooks` are never watched unless a spec names them.
- A change in a skipped folder is a WARN, never a FAIL.

## Not checked
Test execution, timing measurements, and Windows paths.

**Noticed:** `fmplugins._ROOT_PATH` also truncates paths containing `+`, `@` or spaces for every `scripts` entry, not only in skipped folders.
